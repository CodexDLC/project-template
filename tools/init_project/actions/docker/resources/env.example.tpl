# ═══════════════════════════════════════════
# {{PROJECT_NAME}} — Root Environment (Example)
# ═══════════════════════════════════════════
# Copy to .env and fill in your values:
#   cp .env.example .env

# ── Bot ──
BOT_TOKEN=your-telegram-bot-token
BOT_DATA_MODE=api
# BACKEND_BASE_URL=http://backend:8000/api/v1

# ── Database (PostgreSQL) ──
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your-password
POSTGRES_DB={{PROJECT_NAME}}
POSTGRES_HOST=postgres
POSTGRES_PORT=5432

# ── Redis ──
REDIS_HOST=redis
REDIS_PORT=6379

# ── Security ──
SECRET_KEY=your-secret-key
