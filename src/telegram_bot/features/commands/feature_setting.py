from aiogram.fsm.state import State, StatesGroup

from src.telegram_bot.features.commands.logic.orchestrator import StartOrchestrator
from src.telegram_bot.features.commands.ui.commands_ui import CommandsUI


# 1. Определение состояний (для команд обычно не нужно, но для стандарта оставим)
class CommandsStates(StatesGroup):
    main = State()

STATES = CommandsStates

# 2. Настройки Garbage Collector
# В командах мы обычно разрешаем текст (так как это команды), но можно включить
GARBAGE_COLLECT = False

# 3. Настройки Меню
MENU_CONFIG = {
    "key": "commands",
    "text": "🛠 Команды",
    "icon": "🛠",
    "description": "Управление настройками и помощь",
    "target_state": "commands", # Директор должен знать этот ключ
    "priority": 100
}

# 4. Фабрика (DI)
def create_orchestrator(container):
    """
    Создает оркестратор, выбирая провайдер данных в зависимости от настроек.
    Оркестратор — singleton, user передаётся через handle_entry(user_id, payload).
    """
    # Логика выбора режима (API vs DB)
    # if container.settings.MODE == "DB":
    #     from .repository import AuthRepository
    #     data_provider = AuthRepository(container.db_session)
    # else:

    # Пока используем API клиент из контейнера
    data_provider = container.auth_client

    ui = CommandsUI()

    return StartOrchestrator(auth_provider=data_provider, ui=ui)
