from typing import NamedTuple

from aiogram.fsm.state import State

from src.frontend.bot.resources.fsm_states.states import BotState
from src.shared.enums.domain_enums import CoreDomain


# Config для режиссера: какой стейт включить и какой сервис вызвать при входе
class SceneConfig(NamedTuple):
    fsm_state: State
    entry_service: str  # Ключ в RENDER_ROUTES[feature] для entry point


# =============================================================================
# SCENE_ROUTES: Межфичевые переходы (смена FSM State)
# =============================================================================
SCENE_ROUTES: dict[str, SceneConfig] = {

}

# Alias для обратной совместимости
DIRECTOR_ROUTES = SCENE_ROUTES


# =============================================================================
# RENDER_ROUTES: Внутрифичевые переходы (без смены FSM State)
# feature -> logic -> container_getter
# =============================================================================
RENDER_ROUTES: dict[str, dict[str, str]] = {

}
