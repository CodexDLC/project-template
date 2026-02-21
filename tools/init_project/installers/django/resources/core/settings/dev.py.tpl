"""
{{PROJECT_NAME}} — Development Settings.

Inherits from base.py. Smart DB: tries Postgres (container/local), falls back to SQLite.
"""

import os
import socket
import dj_database_url
from .base import *  # noqa: F401,F403

# ═══════════════════════════════════════════
# Debug
# ═══════════════════════════════════════════

DEBUG = True

# ═══════════════════════════════════════════
# Database — Smart Fallback
# ═══════════════════════════════════════════

def get_db_availability(url):
    """Check if the database in the URL is reachable."""
    if not url or not url.startswith("postgres"):
        return False
    try:
        from urllib.parse import urlparse
        p = urlparse(url)
        host = p.hostname or "localhost"
        port = p.port or 5432
        with socket.create_connection((host, int(port)), timeout=0.1):
            return True
    except (socket.timeout, ConnectionRefusedError, OSError, ValueError):
        return False

db_url = os.environ.get("DATABASE_URL")

if db_url and get_db_availability(db_url):
    DATABASES["default"] = dj_database_url.config(default=db_url)
    # print(f"    🗄️  Using PostgreSQL via DATABASE_URL")
else:
    # Use SQLite (already configured in base.py)
    # print("    🗄️  Using SQLite (PostgreSQL not reachable or not configured)")
    pass

# ═══════════════════════════════════════════
# Debug tools (django-debug-toolbar)
# ═══════════════════════════════════════════

INSTALLED_APPS.append("debug_toolbar")
MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")
INTERNAL_IPS = ["127.0.0.1"]

# ═══════════════════════════════════════════
# Security Overrides
# ═══════════════════════════════════════════

CSRF_TRUSTED_ORIGINS = ["http://localhost:8000", "http://127.0.0.1:8000"]
