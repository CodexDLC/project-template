"""
{{PROJECT_NAME}} — Production Settings.

Inherits from base.py. Postgres, DEBUG=False, security hardened.
"""

import os

from .base import *  # noqa: F401,F403

# ═══════════════════════════════════════════
# Security
# ═══════════════════════════════════════════

DEBUG = False

# Trust X-Forwarded-Proto header from Nginx
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Usually Nginx handles HTTPS redirect, so we keep this False
# to avoid issues with internal Docker communication or LB.
SECURE_SSL_REDIRECT = os.environ.get("SECURE_SSL_REDIRECT", "False").lower() == "true"

SECURE_HSTS_SECONDS = 31_536_000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
LANGUAGE_COOKIE_SECURE = True

# CSRF & Origins
env_origins = os.environ.get("CSRF_TRUSTED_ORIGINS", "")
if env_origins:
    CSRF_TRUSTED_ORIGINS = [o.strip() for o in env_origins.split(",") if o.strip()]
else:
    # Fallback to domain name if provided
    domain = os.environ.get("DOMAIN_NAME", "")
    if domain:
        CSRF_TRUSTED_ORIGINS = [f"https://{domain}", f"https://www.{domain}"]

# Cookie domains (for cross-subdomain sessions)
# cookie_domain = os.environ.get("COOKIE_DOMAIN", "")
# if cookie_domain:
#     CSRF_COOKIE_DOMAIN = cookie_domain
#     SESSION_COOKIE_DOMAIN = cookie_domain

# ═══════════════════════════════════════════
# Database — PostgreSQL
# ═══════════════════════════════════════════

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("DB_NAME", "{{PROJECT_NAME}}"),
        "USER": os.environ.get("DB_USER", "postgres"),
        "PASSWORD": os.environ.get("DB_PASSWORD", ""),
        "HOST": os.environ.get("DB_HOST", "postgres"),
        "PORT": os.environ.get("DB_PORT", "5432"),
        "OPTIONS": {
            # Schema isolation: Django only sees django_app + public schemas.
            # Migrations create tables in django_app schema.
            # This allows sharing one DB (e.g. Neon) with FastAPI/Bot
            # without table name conflicts.
            "options": f"-c search_path={os.environ.get('DB_SCHEMA', 'django_app')},public",
        },
    }
}

# ═══════════════════════════════════════════
# Static files — collected by collectstatic
# ═══════════════════════════════════════════

STATIC_ROOT = BASE_DIR / "staticfiles"

# ═══════════════════════════════════════════
# Logging
# ═══════════════════════════════════════════

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "WARNING",
    },
}
