"""
Универсальные DTO для ответов от Backend API.
Используются оркестраторами бота для обработки ответов от Gateway.
"""

from typing import Any

from pydantic import BaseModel


class ResponseHeader(BaseModel):
    """Заголовок ответа с метаданными."""
    current_state: str
    success: bool = True
    message: str | None = None


class CoreResponseDTO(BaseModel):
    """
    Стандартный ответ от Backend API.
    """
    header: ResponseHeader
    payload: Any | None = None


class CoreCompositeResponseDTO(CoreResponseDTO):
    """
    Композитный ответ: основной payload + дополнительные данные для меню.
    """
    menu_payload: Any | None = None
