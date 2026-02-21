from django.db import models
from django.utils.translation import gettext_lazy as _


class StaticTranslation(models.Model):
    """
    Model to store static text content editable via Admin.
    Avoids bloating .po files for dynamic content.
    """

    key = models.CharField(
        _("Key"),
        max_length=100,
        unique=True,
        help_text=_("Unique identifier used in templates (e.g., 'home_hero_title')"),
    )
    text = models.TextField(_("Text Content"))
    description = models.CharField(
        _("Description"), max_length=255, blank=True
    )

    class Meta:
        verbose_name = _("Static Translation")
        verbose_name_plural = _("Static Translations")
        ordering = ["key"]

    def __str__(self):
        return self.key
