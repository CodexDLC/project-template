from modeltranslation.translator import TranslationOptions, register
from .models.site_settings import SiteSettings
from .models.static_translation import StaticTranslation

@register(SiteSettings)
class SiteSettingsTranslationOptions(TranslationOptions):
    fields = ("company_name", "address", "working_hours", "meta_title", "meta_description")

@register(StaticTranslation)
class StaticTranslationTranslationOptions(TranslationOptions):
    fields = ("text",)
