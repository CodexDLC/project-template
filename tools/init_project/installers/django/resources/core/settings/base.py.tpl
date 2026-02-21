"""
{{PROJECT_NAME}} — Base Settings.

Common settings for all environments.
Secrets and env-specific values loaded from .env via os.environ.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

# ═══════════════════════════════════════════
# Paths
# ═══════════════════════════════════════════

# src/backend_django/
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Load .env from backend root
load_dotenv(BASE_DIR / ".env")

# ═══════════════════════════════════════════
# Security
# ═══════════════════════════════════════════

SECRET_KEY = os.environ.get("SECRET_KEY", "django-insecure-CHANGE-ME")

DEBUG = os.environ.get("DEBUG", "False").lower() in ("true", "1", "yes")

# --- Smart ALLOWED_HOSTS ---
ALLOWED_HOSTS = ["localhost", "127.0.0.1", "backend"]

env_hosts = os.environ.get("ALLOWED_HOSTS", "")
if env_hosts:
    ALLOWED_HOSTS.extend([h.strip() for h in env_hosts.split(",") if h.strip()])

# ═══════════════════════════════════════════
# Application definition
# ═══════════════════════════════════════════

INSTALLED_APPS = [
    # ── Unfold Admin (must be before django.contrib.admin) ──
    "unfold",
    "unfold.contrib.filters",
    "unfold.contrib.forms",
    "unfold.contrib.inlines",
    "unfold.contrib.import_export",

    # ── Monitoring ──
    "django_prometheus",

    # ── Translation ──
    "modeltranslation",

    # ── Django Core ──
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # ── Shared Features ──
    "core",
    "features.main",
    "features.system",

    # ── Third Party ──
    "ninja",
]

MIDDLEWARE = [
    "django_prometheus.middleware.PrometheusBeforeMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django_prometheus.middleware.PrometheusAfterMiddleware",
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"

# ═══════════════════════════════════════════
# Unfold Configuration
# ═══════════════════════════════════════════

UNFOLD = {
    "SITE_TITLE": "{{PROJECT_NAME}} Admin",
    "SITE_HEADER": "{{PROJECT_NAME}}",
    "SITE_SYMBOL": "speed",  # Google Material Symbol name
    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": True,
    },
}

# ═══════════════════════════════════════════
# Redis & Cache
# ═══════════════════════════════════════════

REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
REDIS_PORT = int(os.environ.get("REDIS_PORT", 6379))
REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD", None)

REDIS_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}/0"
if REDIS_PASSWORD:
    from urllib.parse import quote_plus
    encoded_pass = quote_plus(REDIS_PASSWORD.strip("'\""))
    REDIS_URL = f"redis://:{encoded_pass}@{REDIS_HOST}:{REDIS_PORT}/0"

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_URL,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}

SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"

# ═══════════════════════════════════════════
# Database
# ═══════════════════════════════════════════

# Default: SQLite (overridden in prod.py for Postgres)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# ═══════════════════════════════════════════
# Auth
# ═══════════════════════════════════════════

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ═══════════════════════════════════════════
# Internationalization
# ═══════════════════════════════════════════

LANGUAGE_CODE = os.environ.get("LANGUAGE_CODE", "en")
TIME_ZONE = os.environ.get("TIME_ZONE", "UTC")
USE_I18N = True
USE_TZ = True

# Model Translation (django-modeltranslation)
MODELTRANSLATION_DEFAULT_LANGUAGE = LANGUAGE_CODE.split("-")[0]
MODELTRANSLATION_LANGUAGES = ("en", "de", "ru", "uk")

# ═══════════════════════════════════════════
# Static files
# ═══════════════════════════════════════════

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

# ═══════════════════════════════════════════
# Default primary key
# ═══════════════════════════════════════════

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
