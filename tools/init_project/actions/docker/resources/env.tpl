# ═══════════════════════════════════════════
# {{PROJECT_NAME}} — Root Environment
# ═══════════════════════════════════════════

# === ENVIRONMENT ===
# development - для локальной разработки (localhost)
# production - для Docker/продакшена (service names)
ENVIRONMENT=production

# === POSTGRESQL (База данных) ===
POSTGRES_DB={{PROJECT_NAME}}_db
POSTGRES_USER={{PROJECT_NAME}}_user
POSTGRES_PASSWORD={{POSTGRES_PASSWORD}}
POSTGRES_HOST=postgres
POSTGRES_PORT=5432

# === REDIS (Кэш и очереди) ===
REDIS_HOST=redis
REDIS_PORT=6379
# REDIS_PASSWORD=secret

# === TELEGRAM BOT ===
BOT_TOKEN={{BOT_TOKEN}}
# Режим работы бота: 'api' или 'direct'
BOT_DATA_MODE=api

# === TELEGRAM CHANNELS & ROLES ===
TELEGRAM_ADMIN_CHANNEL_ID=-1003363984639
TELEGRAM_TOPICS={"hair": 2, "nails": 4, "face": 6, "eyes": 8, "body": 10, "depilation": 12}
telegram_notification_topic_id=1
TELEGRAM_ADMIN_ID=123456789

# ID разработчиков (через запятую)
SUPERUSER_IDS=123456789
# ID владельцев (через запятую)
OWNER_IDS=123456789

# === BACKEND API (Связь Бота с Джанго) ===
BACKEND_API_URL=http://backend:8000
BACKEND_API_KEY={{BACKEND_API_KEY}}

# === DJANGO SETTINGS ===
SECRET_KEY={{DJANGO_SECRET_KEY}}
ALLOWED_HOSTS=localhost,127.0.0.1,backend

# === DOCKER IMAGES ===
DOCKER_IMAGE_BACKEND=my-registry/{{PROJECT_NAME}}-backend:1.0.0
DOCKER_IMAGE_BOT=my-registry/{{PROJECT_NAME}}-bot:1.0.0
DOCKER_IMAGE_WORKER=my-registry/{{PROJECT_NAME}}-worker:1.0.0
DOCKER_IMAGE_NGINX=my-registry/{{PROJECT_NAME}}-nginx:1.0.0
