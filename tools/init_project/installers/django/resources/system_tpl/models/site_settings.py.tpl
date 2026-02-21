from datetime import time
from decimal import Decimal

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class SiteSettings(models.Model):
    """
    Singleton model for global site settings (Contacts, Socials, Legal info).
    Automatically synced to Redis for Bot integration.
    """

    # --- General ---
    company_name = models.CharField(_("Company Name"), max_length=255, default="{{PROJECT_NAME}}")
    site_base_url = models.URLField(
        _("Site Base URL"), blank=True, help_text=_("If empty, uses value from .env (SITE_BASE_URL)")
    )
    logo_url = models.CharField(
        _("Logo URL"),
        max_length=500,
        blank=True,
        default="/static/img/logo.webp",
    )

    # --- Contacts ---
    phone = models.CharField(_("Phone"), max_length=50, default="+1 234 567 890")
    email = models.EmailField(_("Email"), default="info@{{PROJECT_NAME}}.com")
    address = models.CharField(_("Address"), max_length=255, blank=True)
    working_hours = models.CharField(_("Working Hours"), max_length=100, default="Mo-Fr: 09:00 - 18:00")

    # --- Social Links & Messengers (Client Facing) ---
    instagram_url = models.URLField(_("Instagram URL"), blank=True)
    facebook_url = models.URLField(_("Facebook URL"), blank=True)
    telegram_channel_url = models.URLField(_("Telegram Channel URL"), blank=True)
    telegram_client_bot_url = models.URLField(_("Telegram Client Bot/Support URL"), blank=True)
    whatsapp_url = models.URLField(_("WhatsApp URL"), blank=True)

    # --- SEO & Metadata ---
    meta_title = models.CharField(_("Default Meta Title"), max_length=255, default="{{PROJECT_NAME}}")
    meta_description = models.TextField(_("Default Meta Description"), blank=True)
    favicon_url = models.CharField(_("Favicon URL"), max_length=500, default="/static/img/favicon.ico")

    # --- Technical & Admin Metadata ---
    # These are used for internal logic (notifications, worker routing)
    telegram_admin_channel_id = models.CharField(
        _("Admin Channel ID (Internal)"),
        max_length=100,
        blank=True,
        help_text=_("Telegram ID for internal notifications (e.g. -100...)")
    )
    telegram_technical_bot_username = models.CharField(
        _("Technical Bot Username"),
        max_length=100,
        blank=True,
        help_text=_("The bot that sends admin alerts")
    )
    telegram_notification_topic_id = models.IntegerField(
        _("Notification Topic ID"),
        null=True,
        blank=True,
        help_text=_("The topic ID in the admin channel for general notifications")
    )
    telegram_topics = models.JSONField(
        _("Telegram Topics Map"),
        default=dict,
        blank=True,
        help_text=_("Mapping of services to Telegram Topic IDs (e.g. {'hair': 2, 'nails': 4})")
    )

    class Meta:
        verbose_name = _("Site Settings")
        verbose_name_plural = _("Site Settings")

    def __str__(self):
        return "Global Settings"

    def save(self, *args, **kwargs):
        self.pk = 1  # Singleton
        if not self.site_base_url:
            self.site_base_url = settings.SITE_BASE_URL

        super().save(*args, **kwargs)

        # Sync to Redis
        try:
            from features.system.redis_managers.site_settings_manager import SiteSettingsManager
            SiteSettingsManager.save_to_redis(self)
        except ImportError:
            pass

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

    def to_dict(self) -> dict:
        data = {}
        for field in self._meta.get_fields():
            if field.concrete and not field.many_to_many and not field.one_to_many:
                value = getattr(self, field.name)
                if isinstance(value, time):
                    data[field.name] = value.strftime("%H:%M")
                elif isinstance(value, Decimal):
                    data[field.name] = str(value)
                else:
                    data[field.name] = value
        return data
