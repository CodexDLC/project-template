"""
Director — координатор переходов между фичами.
Управляет FSM стейтами и делегирует рендеринг оркестраторам.
"""

from typing import TYPE_CHECKING, Any, Protocol, cast, runtime_checkable

from aiogram.fsm.context import FSMContext
from loguru import logger

from src.telegram_bot.services.director.registry import RENDER_ROUTES, SCENE_ROUTES

KEY_SESSION_DATA = "session_data"

if TYPE_CHECKING:
    from src.telegram_bot.core.container import BotContainer


@runtime_checkable
class OrchestratorProtocol(Protocol):
    async def render(self, payload: Any) -> Any: ...
    def set_director(self, director: Any): ...


class Director:
    """
    Координатор переходов между фичами.
    Два публичных метода:
    - set_scene: межфичевый переход (смена FSM State + entry logic)
    - render: внутрифичевый переход (без смены FSM State)
    """

    def __init__(self, container: "BotContainer", state: FSMContext, user_id: int):
        self.container = container
        self.state = state
        self.user_id = user_id

    async def set_scene(self, feature: str, payload: Any) -> Any:
        """
        Межфичевый переход: смена FSM State + вызов entry logic.

        Args:
            feature: Ключ фичи из SCENE_ROUTES
            payload: Данные для рендера
        """
        scene_config = SCENE_ROUTES.get(feature)
        if not scene_config:
            logger.error(f"Director | unknown_scene='{feature}' user_id={self.user_id}")
            return None

        # Смена FSM State
        current_fsm = await self.state.get_state()
        if current_fsm != scene_config.fsm_state.state:
            await self.state.set_state(scene_config.fsm_state)
            logger.debug(f"Director | fsm_changed='{scene_config.fsm_state}' user_id={self.user_id}")

        # Entry logic через render()
        return await self.render(feature, scene_config.entry_service, payload)

    async def render(self, feature: str, service: str, payload: Any) -> Any:
        """
        Внутрифичевый переход: вызов orchestrator БЕЗ смены FSM State.

        Args:
            feature: Ключ фичи из RENDER_ROUTES
            service: Ключ сервиса внутри фичи
            payload: Данные для рендера
        """
        feature_routes = RENDER_ROUTES.get(feature)
        if not feature_routes:
            logger.error(f"Director | unknown_feature='{feature}' user_id={self.user_id}")
            return None

        container_getter = feature_routes.get(service)
        if not container_getter:
            logger.error(f"Director | unknown_service='{service}' feature='{feature}' user_id={self.user_id}")
            return None

        # Получение orchestrator из container
        factory_or_instance = getattr(self.container, container_getter, None)
        if not factory_or_instance:
            logger.error(f"Director | container_missing='{container_getter}' user_id={self.user_id}")
            return None

        orchestrator = factory_or_instance() if callable(factory_or_instance) else factory_or_instance
        orchestrator = cast(OrchestratorProtocol, orchestrator)

        if hasattr(orchestrator, "set_director"):
            orchestrator.set_director(self)

        return await orchestrator.render(payload)
