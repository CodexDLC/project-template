from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.telegram_bot.features.bot_menu.resources.callbacks import DashboardCallback
from src.telegram_bot.features.bot_menu.resources.texts import DASHBOARD_TITLE
from src.telegram_bot.services.base.view_dto import ViewResultDTO


class BotMenuUI:
    """
    Отвечает за рендеринг главного меню (Дашборда).
    """

    def render_dashboard(self, buttons: dict[str, dict]) -> ViewResultDTO:
        """
        Генерирует ViewResultDTO на основе зарегистрированных кнопок.
        buttons: {
            "account": {"text": "👤 Профиль", "callback_data": "..."}
        }
        """
        builder = InlineKeyboardBuilder()

        # Сортируем кнопки (опционально, можно добавить priority)
        for key, btn_data in buttons.items():
            text = btn_data.get("text", key)
            # Если callback_data передана явно - используем её, иначе генерируем навигацию
            callback = btn_data.get("callback_data") or DashboardCallback(action="nav", target=key).pack()

            builder.button(text=text, callback_data=callback)

        builder.adjust(2) # По 2 кнопки в ряд

        return ViewResultDTO(
            text=DASHBOARD_TITLE,
            kb=builder.as_markup()
        )
