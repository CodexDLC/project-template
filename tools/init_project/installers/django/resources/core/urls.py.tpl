"""
{{PROJECT_NAME}} — URL Configuration.

Features auto-included via include().
API via Django Ninja at /api/.
"""

from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import include, path

from api.urls import api

# Technical and non-localized patterns
urlpatterns = [
    path("i18n/", include("django.conf.urls.i18n")),
    path("api/", api.urls),
    path("", include("django_prometheus.urls")),
]

# Localized patterns
urlpatterns += i18n_patterns(
    path("admin/", admin.site.urls),
    path("", include("features.main.urls")),
)

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
