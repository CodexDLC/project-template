"""
Runner — оркестратор установки.

Порядок:
1. installers.pre_install()
2. installers.install()
3. cleaner — удаление невыбранных модулей
4. renamer — замена имени проекта
5. docker — генерация Docker файлов (заглушка)
6. poetry — управление зависимостями (заглушка)
7. scaffolder — создание структур (заглушка)
8. installers.post_install()
9. finalizer — git init, коммит, самоудаление
"""

from __future__ import annotations

from tools.init_project.config import InstallContext
from tools.init_project.installers.base import BaseInstaller
from tools.init_project.installers.fastapi_installer import FastAPIInstaller
from tools.init_project.installers.django_installer import DjangoInstaller
from tools.init_project.installers.bot_installer import BotInstaller
from tools.init_project.installers.shared_installer import SharedInstaller

from tools.init_project.actions.cleaner.cleaner import CleanerAction
from tools.init_project.actions.renamer.renamer import RenamerAction
from tools.init_project.actions.docker.docker import DockerAction
from tools.init_project.actions.poetry.poetry import PoetryAction
from tools.init_project.actions.scaffolder.scaffolder import ScaffolderAction
from tools.init_project.actions.finalizer.finalizer import FinalizerAction


def _get_installers(ctx: InstallContext) -> list[BaseInstaller]:
    """Собирает список активных installers на основе выбора."""
    installers: list[BaseInstaller] = []

    # Shared — всегда
    installers.append(SharedInstaller())

    # Backend
    if ctx.backend == "fastapi":
        installers.append(FastAPIInstaller())
    elif ctx.backend == "django":
        installers.append(DjangoInstaller())

    # Bot
    if ctx.include_bot:
        installers.append(BotInstaller())

    return installers


def run(ctx: InstallContext) -> None:
    """Запускает полный flow установки."""

    installers = _get_installers(ctx)

    # ── Phase 1: Installers pre_install + install ──
    for installer in installers:
        print(f"  📦 {installer.name} — pre_install...")
        installer.pre_install(ctx)

    for installer in installers:
        print(f"  📦 {installer.name} — install...")
        installer.install(ctx)

    # ── Phase 2: Actions ──
    print("  🧹 Cleaning unused modules...")
    CleanerAction().execute(ctx)

    print("  ✏️  Renaming project...")
    RenamerAction().execute(ctx)

    print("  🐳 Docker setup...")
    DockerAction().execute(ctx)

    print("  📦 Poetry dependencies...")
    PoetryAction().execute(ctx)

    print("  🏗️  Scaffolding...")
    ScaffolderAction().execute(ctx)

    # ── Phase 3: Installers post_install ──
    for installer in installers:
        print(f"  📦 {installer.name} — post_install...")
        installer.post_install(ctx)

    # ── Phase 4: Finalize ──
    print("  🎯 Finalizing...")
    FinalizerAction().execute(ctx)
