"""
Оркестратор фичи commands.
Координирует работу между контрактом (данные) и UI (отображение).
"""

from aiogram.types import User
from src.shared.schemas.user import UserUpsertDTO

from src.telegram_bot.services.base.base_orchestrator import BaseBotOrchestrator
from src.telegram_bot.services.base.view_dto import UnifiedViewDTO
from src.telegram_bot.features.commands.contracts.commands_contract import AuthDataProvider
from src.telegram_bot.features.commands.ui.commands_ui import CommandsUI


class StartOrchestrator(BaseBotOrchestrator):
    """
    Оркестратор стартового экрана.
    handler вызывает handle_start() → получает UnifiedViewDTO → отдаёт sender.
    """

    def __init__(self, auth_provider: AuthDataProvider, ui: CommandsUI, user: User):
        super().__init__(expected_state=None)
        self.auth = auth_provider
        self.ui = ui
        self.user = user

    async def render(self, user_name: str) -> UnifiedViewDTO:
        """Превращает имя пользователя в готовый UI."""
        menu_view = self.ui.render_start_screen(user_name)
        return UnifiedViewDTO(menu=menu_view, content=None, clean_history=True)

    async def handle_start(self) -> UnifiedViewDTO:
        """
        Основной метод: синхронизация юзера + рендер стартового экрана.
        """
        # 1. Sync user через контракт (API или Repository)
        user_dto = UserUpsertDTO(
            telegram_id=self.user.id,
            first_name=self.user.first_name,
            username=self.user.username,
            last_name=self.user.last_name,
            language_code=self.user.language_code,
            is_premium=bool(self.user.is_premium),
        )
        await self.auth.upsert_user(user_dto)

        # 2. Render
        user_name = self.user.first_name or "User"
        return await self.render(user_name)
