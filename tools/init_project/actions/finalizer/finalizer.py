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

import subprocess
from pathlib import Path

from tools.init_project.config import InstallContext, safe_rmtree


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
            safe_rmtree(git_dir)

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
            "README-RU.md",
        ]
        for artifact in artifacts:
            path = ctx.project_root / artifact
            if path.exists():
                path.unlink()
                print(f"    🗑️  Removed: {artifact}")

        # ── Генерация проектного README ──
        self._generate_project_readme(ctx)

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
    # README generation
    # ─────────────────────────────────────────

    @staticmethod
    def _generate_project_readme(ctx: InstallContext) -> None:
        """Заменяет шаблонный README на чистый проектный."""
        name = ctx.project_name

        # Определяем стек
        stack_parts: list[str] = []
        if ctx.backend == "django":
            stack_parts.append("Django")
        elif ctx.backend == "fastapi":
            stack_parts.append("FastAPI")
        if ctx.include_bot:
            stack_parts.append("Telegram Bot")
        stack = " + ".join(stack_parts) if stack_parts else "Python"

        # Команды запуска
        run_lines: list[str] = []
        if ctx.backend == "django":
            run_lines.append("# Django dev server")
            run_lines.append("cd src/backend_django")
            run_lines.append("python manage.py runserver")
        elif ctx.backend == "fastapi":
            run_lines.append("# FastAPI dev server")
            run_lines.append("cd src/backend_fastapi")
            run_lines.append("uvicorn main:app --reload")
        if ctx.include_bot:
            run_lines.append("")
            run_lines.append("# Telegram Bot")
            run_lines.append("cd src/telegram_bot")
            run_lines.append("python -m main")
        run_block = "\n".join(run_lines)

        # Структура src/
        structure_lines: list[str] = ["src/"]
        if ctx.backend == "django":
            structure_lines.append("├── backend_django/   # Django backend")
        elif ctx.backend == "fastapi":
            structure_lines.append("├── backend_fastapi/  # FastAPI backend")
        if ctx.include_bot:
            structure_lines.append("├── telegram_bot/     # Telegram Bot")
        structure_lines.append("└── shared/           # Shared utilities")
        structure_block = "\n".join(structure_lines)

        readme = f"""# {name}

> {stack} project.

## Quick Start

```bash
# Install dependencies
poetry install

# Run
{run_block}

# Docker
cd deploy
docker compose up -d --build
```

## Structure

```
{structure_block}
```

## Development

```bash
ruff check src/        # Linting
ruff format src/       # Formatting
mypy src/              # Type checking
pytest                 # Tests
```

## Deploy

Managed via Docker Compose + GitHub Actions CI/CD.

See `deploy/` for Docker configs and `.github/workflows/` for pipelines.
"""

        readme_path = ctx.project_root / "README.md"
        readme_path.write_text(readme.strip() + "\n", encoding="utf-8")
        print("    📄 Generated: README.md (project)")

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
