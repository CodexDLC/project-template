from .models.site_settings import SiteSettings

def site_settings(request):
    """
    Makes site settings globally available in templates.
    """
    return {
        "site_settings": SiteSettings.load()
    }
