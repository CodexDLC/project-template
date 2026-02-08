import os

import pytest

# -----------------------------------------------------------------------------
# Environment Setup
# Устанавливаем переменные окружения ДО импорта любых модулей приложения,
# чтобы Pydantic Settings не падали при валидации.
# -----------------------------------------------------------------------------
os.environ.setdefault("SECRET_KEY", "test_secret_key_for_unit_tests")
os.environ.setdefault("DATABASE_URL", "postgresql+asyncpg://test_user:test_pass@localhost:5432/test_db")
os.environ.setdefault("BOT_TOKEN", "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11")
os.environ.setdefault("REDIS_URL", "redis://localhost:6379/0")

# -----------------------------------------------------------------------------
# Global Fixtures
# -----------------------------------------------------------------------------

@pytest.fixture(scope="session")
def anyio_backend():
    """
    Настройка для anyio (используется в Starlette/FastAPI TestClient).
    """
    return "asyncio"
