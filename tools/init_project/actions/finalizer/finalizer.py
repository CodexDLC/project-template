"""
Finalizer Action — финальная стадия установки.

1. Удаляет tools/init_project/ (сам инсталлятор)
2. Удаляет project_structure.txt (артефакт шаблона)
3. Опционально: git init + первый коммит
"""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

from tools.init_project.config import InstallContext


class FinalizerAction:
    """Финализация: чистка + git init."""

    def execute(self, ctx: InstallContext) -> None:
        # ── Удаление артефактов шаблона ──
        artifacts = [
            "project_structure.txt",
            "CHANGELOG.md",
        ]
        for artifact in artifacts:
            path = ctx.project_root / artifact
            if path.exists():
                path.unlink()
                print(f"    🗑️  Removed: {artifact}")

        # ── Git init ──
        if ctx.init_git:
            self._git_init(ctx.project_root, ctx.project_name)

        # ── Самоудаление инсталлятора ──
        # Делаем последним — после этого код инсталлятора больше не доступен
        installer_dir = ctx.project_root / "tools" / "init_project"
        if installer_dir.exists():
            shutil.rmtree(installer_dir)
            print("    🗑️  Removed: tools/init_project/")

    @staticmethod
    def _git_init(project_root: Path, project_name: str) -> None:
        """Инициализирует git и делает первый коммит."""
        try:
            subprocess.run(
                ["git", "init"],
                cwd=project_root,
                check=True,
                capture_output=True,
            )
            subprocess.run(
                ["git", "add", "-A"],
                cwd=project_root,
                check=True,
                capture_output=True,
            )
            subprocess.run(
                ["git", "commit", "-m", f"Initial commit: {project_name}"],
                cwd=project_root,
                check=True,
                capture_output=True,
            )
            print("    ✅ Git initialized with first commit")
        except FileNotFoundError:
            print("    ⚠️  Git not found — skipping git init")
        except subprocess.CalledProcessError as e:
            print(f"    ⚠️  Git error: {e}")
