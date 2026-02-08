"""
Cleaner Action — удаление невыбранных модулей.

На основе выбора пользователя удаляет директории src/, deploy/, docs/
тех модулей которые не были выбраны.
"""

from __future__ import annotations

import shutil
from pathlib import Path

from tools.init_project.config import InstallContext, MODULES


class CleanerAction:
    """Удаляет директории невыбранных модулей."""

    def execute(self, ctx: InstallContext) -> None:
        # Определяем какие модули НЕ выбраны
        modules_to_remove: list[str] = []

        # Backend: если выбран fastapi — удаляем django, и наоборот
        if ctx.backend != "fastapi":
            modules_to_remove.append("fastapi")
        if ctx.backend != "django":
            modules_to_remove.append("django")

        # Bot
        if not ctx.include_bot:
            modules_to_remove.append("telegram_bot")

        # Удаляем
        for module_key in modules_to_remove:
            module_config = MODULES.get(module_key)
            if not module_config:
                continue

            all_dirs = (
                module_config.src_dirs
                + module_config.deploy_dirs
                + module_config.doc_dirs
            )

            for rel_path in all_dirs:
                full_path = ctx.project_root / rel_path
                if full_path.exists():
                    shutil.rmtree(full_path)
                    print(f"    🗑️  Removed: {rel_path}")

        # Если нет бэкенда вообще — удалить nginx тоже
        if ctx.backend is None:
            nginx_path = ctx.project_root / "deploy" / "nginx"
            if nginx_path.exists():
                shutil.rmtree(nginx_path)
                print("    🗑️  Removed: deploy/nginx")

        # Очистка пустых deploy/ если всё удалено
        deploy_path = ctx.project_root / "deploy"
        if deploy_path.exists():
            remaining = [
                p for p in deploy_path.iterdir()
                if p.is_dir() and p.name != "__pycache__"
            ]
            # Если остался только README.md — оставляем как есть
