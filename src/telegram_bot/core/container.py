from redis.asyncio import Redis

from src.telegram_bot.core.config import BotSettings
from src.telegram_bot.features.commands.client import AuthClient


class BotContainer:
    """
    DI Container for Telegram Bot.
    Содержит настройки, Redis и клиенты к бэкенду.
    Контракты фич получают реализации отсюда.
    """

    def __init__(self, settings: BotSettings, redis_client: Redis):
        self.settings = settings
        self.redis_client = redis_client

        # --- API Clients (Gateways to Backend) ---
        self.auth_client = AuthClient(
            base_url=settings.backend_api_url,
            api_key=settings.backend_api_key,
            timeout=settings.backend_api_timeout,
        )

    async def shutdown(self):
        """Закрытие соединений при остановке бота."""
        if self.redis_client:
            await self.redis_client.close()
