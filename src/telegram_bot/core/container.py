from redis.asyncio import Redis

from src.telegram_bot.core.config import BotSettings


class BotContainer:
    """
    DI Container for Telegram Bot.
    Содержит настройки, Redis и клиенты к бэкенду.
    """

    def __init__(self, settings: BotSettings, redis_client: Redis):
        self.settings = settings
        self.redis_client = redis_client

        # --- API Clients (Gateways to Backend) ---
        # Здесь будут инициализироваться клиенты для фич
        # self.users = UserClient(base_url=settings.backend_api_url, ...)
        pass

    async def shutdown(self):
        """Закрытие соединений при остановке бота."""
        if self.redis_client:
            await self.redis_client.close()
