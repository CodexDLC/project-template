# frontend/telegram_bot/core/routers.py
"""
Централизованный реестр роутеров для Telegram Bot.
Аналог Django urls.py - все роутеры регистрируются здесь.
"""

from aiogram import Router

# --- System Commands ---
from src.telegram_bot.features.commands import handlers as commands_handlers
# --- Common Services ---
from src.telegram_bot.services.fsm.common_fsm_handlers import router as common_fsm_router

# Главный роутер приложения
main_router = Router(name="main_router")

# --- Регистрация роутеров ---
# Порядок важен: сначала системные, потом игровые фичи, последним - garbage collector
main_router.include_routers(
    # System
    commands_handlers.router,


    # last
    common_fsm_router,
)