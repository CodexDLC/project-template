from django.contrib import admin
from unfold.admin import ModelAdmin
from .models.site_settings import SiteSettings
from .models.static_translation import StaticTranslation

@admin.register(SiteSettings)
class SiteSettingsAdmin(ModelAdmin):
    list_display = ("company_name", "email", "phone")
    fieldsets = (
        (_("General"), {"fields": ("company_name", "logo_url", "site_base_url")}),
        (_("Contacts"), {"fields": ("phone", "email", "address", "working_hours")}),
        (_("Social Links & Messengers"), {
            "fields": (
                "instagram_url",
                "facebook_url",
                "telegram_channel_url",
                "telegram_client_bot_url",
                "whatsapp_url"
            ),
            "description": _("Links shown to clients on the website and in the bot.")
        }),
        (_("SEO & Metadata"), {"fields": ("meta_title", "meta_description", "favicon_url")}),
        (_("Technical Settings (Bot)"), {
            "fields": (
                "telegram_admin_channel_id",
                "telegram_technical_bot_username",
                "telegram_notification_topic_id",
                "telegram_topics"
            ),
            "description": _("Internal settings for notification routing and bot identification.")
        }),
    )

@admin.register(StaticTranslation)
class StaticTranslationAdmin(ModelAdmin):
    list_display = ("key", "description")
    search_fields = ("key", "text")
