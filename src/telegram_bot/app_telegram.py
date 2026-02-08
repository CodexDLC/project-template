# src/telegram_bot/app_telegram.py
"""
Entry point для Telegram Bot клиента.
Подключается к Backend через HTTP API.
"""

import asyncio

from loguru import logger as log
from redis.asyncio import Redis

from src.telegram_bot.core.config import BotSettings
from src.telegram_bot.core.container import BotContainer
# from src.telegram_bot.core.factory import build_bot # TODO: Реализовать factory
# from src.telegram_bot.core.routers import main_router # TODO: Реализовать routers
from src.shared.core.logger import setup_logging


async def startup(container: BotContainer, settings: BotSettings) -> None:
    """
    Инициализация при запуске бота.
    """
    setup_logging(settings, service_name="telegram_bot")
    log.info("🤖 Telegram Bot starting...")
    log.info(f"Backend API: {settings.backend_api_url}")


async def shutdown(container: BotContainer) -> None:
    """
    Очистка ресурсов при остановке бота.
    """
    log.info("🛑 Shutting down Telegram Bot...")
    await container.shutdown()
    log.info("👋 Bot stopped")


async def main() -> None:
    """
    Основная функция запуска Telegram Bot.
    """
    # 1. Загрузка настроек
    settings = BotSettings()  # type: ignore[call-arg]

    # 2. Инициализация Redis
    redis_client = Redis.from_url(
        settings.redis_url,
        encoding="utf-8",
        decode_responses=True,
    )
    log.debug("Redis client initialized")

    # 3. Создание контейнера
    container = BotContainer(settings, redis_client)
    log.debug("BotContainer initialized")

    # 4. Startup
    await startup(container, settings)

    # 5. Создание Bot + Dispatcher
    # TODO: Раскомментировать, когда будет реализована фабрика
    # bot, dp = await build_bot(settings.bot_token, redis_client)
    # log.info("Bot and Dispatcher created")

    # 6. Подключение middleware
    # from src.telegram_bot.middlewares import (
    #     ContainerMiddleware,
    #     SecurityMiddleware,
    #     ThrottlingMiddleware,
    #     UserValidationMiddleware,
    # )

    # dp.update.middleware(UserValidationMiddleware())
    # dp.update.middleware(ThrottlingMiddleware(redis=redis_client, rate_limit=1.0))
    # dp.update.middleware(SecurityMiddleware())
    # dp.update.middleware(ContainerMiddleware(container=container))
    # log.info("Middleware attached")

    # 7. Подключение роутеров
    # dp.include_router(main_router)
    # log.info("Routers attached")

    # 8. Запуск polling
    log.info("🚀 Bot polling started (MOCK)")
    try:
        # await dp.start_polling(bot)
        pass
    finally:
        # 9. Shutdown
        await shutdown(container)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        log.info("Bot stopped by user")
    except Exception as e:  # noqa: BLE001
        log.critical(f"Critical error: {e}", exc_info=True)
