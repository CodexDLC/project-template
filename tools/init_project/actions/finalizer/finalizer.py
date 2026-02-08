"""
Finalizer Action — финализация установки с двумя git коммитами.

Flow:
  1. commit_install() — ПЕРЕД установкой: git init → "Install" commit (ВСЕ файлы)
  2. execute()        — ПОСЛЕ установки: чистка артефактов → "Activate" commit
                        + создание веток develop/release

Фишка: Первый коммит содержит ВСЕ модули шаблона.
Команда `add bot` может восстановить их из git истории:
  git checkout <install-hash> -- src/telegram_bot
"""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

from tools.init_project.config import InstallContext


class FinalizerAction:
    """Финализация: два коммита + ветки."""

    def __init__(self) -> None:
        self._install_hash: str | None = None

    # ─────────────────────────────────────────
    # Phase 0: ПЕРЕД установкой
    # ─────────────────────────────────────────

    def commit_install(self, ctx: InstallContext) -> None:
        """Создаёт git init + коммит 'Install' со ВСЕМИ файлами шаблона."""
        root = ctx.project_root

        # Удаляем .git от шаблона если есть
        git_dir = root / ".git"
        if git_dir.exists():
            shutil.rmtree(git_dir)

        # Init + первый коммит
        self._run(["git", "init", "-b", "main"], root)
        self._run(["git", "add", "-A"], root)
        self._run(
            ["git", "commit", "-m", "Install: template snapshot (all modules)"],
            root,
        )

        # Запоминаем hash первого коммита (для команды add)
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=root,
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            self._install_hash = result.stdout.strip()
            print(f"    ✅ Commit 'Install': {self._install_hash[:8]}")

    # ─────────────────────────────────────────
    # Phase 4: ПОСЛЕ установки
    # ─────────────────────────────────────────

    def execute(self, ctx: InstallContext) -> None:
        """Чистка артефактов + коммит 'Activate' + ветки."""

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

        # ── Сохранить hash первого коммита в файл (для команды add) ──
        if self._install_hash:
            hash_file = ctx.project_root / ".template_install_hash"
            hash_file.write_text(self._install_hash, encoding="utf-8")

        # ── Commit "Activate" ──
        if ctx.init_git:
            self._commit_activate(ctx)

    def _commit_activate(self, ctx: InstallContext) -> None:
        """Коммит 'Activate' + ветки develop/release."""
        root = ctx.project_root

        self._run(["git", "add", "-A"], root)
        self._run(
            ["git", "commit", "-m", f"Activate: {ctx.project_name} project initialized"],
            root,
        )
        print("    ✅ Commit 'Activate': project ready")

        # Создаём ветки
        self._run(["git", "branch", "develop"], root)
        self._run(["git", "branch", "release"], root)
        print("    🌿 Created branches: develop, release")

        # Переключаемся на develop
        self._run(["git", "checkout", "develop"], root)
        print("    📍 Switched to branch: develop")

    # ─────────────────────────────────────────
    # Helpers
    # ─────────────────────────────────────────

    @staticmethod
    def _run(cmd: list[str], cwd: Path) -> bool:
        """Выполняет git команду, возвращает success."""
        try:
            subprocess.run(cmd, cwd=cwd, check=True, capture_output=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False
