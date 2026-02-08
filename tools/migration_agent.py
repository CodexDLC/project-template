"""
Migration Agent — внедрение шаблона в существующий проект.

Сценарий: у тебя есть рабочий проект без структуры (или со старой структурой).
Этот скрипт:
  1. Клонирует шаблон во временную папку .temp_template/
  2. Анализирует текущий проект — что есть, чего не хватает
  3. Переносит недостающее: src/ модули, tools/, scripts/, docs/
  4. Создаёт deploy/ и .github/ (Docker + CI/CD)
  5. Создаёт стандартные папки по шаблону (если нет)
  6. НЕ удаляет .temp_template/ — выводит отчёт что осталось перенести вручную

Использование:
  python tools/migration_agent.py
  python tools/migration_agent.py --repo https://github.com/you/project-template.git

Что переносится автоматически (если нет в проекте):
  - src/shared/             общий код
  - src/telegram_bot/       бот (если нет)
  - src/backend_fastapi/    бэкенд (если нет)
  - tools/                  утилиты + инсталлятор
  - scripts/                скрипты (lint_docs, generate_tree)
  - docs/                   структура документации
  - deploy/                 Docker конфиги
  - .github/                CI/CD workflows
  - Конфиги: .gitignore, .dockerignore, .pre-commit-config.yaml

Что НЕ переносится (вручную или AI-агент):
  - Адаптация импортов под вашу структуру
  - Мерж существующей документации
  - Настройка .env под ваши переменные
  - Рефакторинг существующего кода
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

DEFAULT_REPO = "https://github.com/CodexDLC/project-template.git"
TEMP_DIR_NAME = ".temp_template"

# ──────────────────────────────────────────────
# Стандартная структура проекта по шаблону
# ──────────────────────────────────────────────

# Папки которые ВСЕГДА должны быть (создаём пустые если нет)
STANDARD_DIRS: list[str] = [
    "src",
    "src/shared",
    "scripts",
    "tools",
    "docs",
    "deploy",
    ".github",
    ".github/workflows",
    "tests",
]

# Модули которые можно перенести из шаблона
TRANSFERABLE_MODULES: dict[str, str] = {
    "src/shared": "Shared utilities (config, logging, redis)",
    "src/telegram_bot": "Telegram Bot (aiogram)",
    "src/backend_fastapi": "FastAPI Backend",
    "src/backend_django": "Django Backend",
}

# Инфраструктурные папки — переносятся всегда если нет
INFRA_DIRS: dict[str, str] = {
    "tools": "Project tools (installer, add_module, dev utils)",
    "scripts": "Scripts (linting, tree generation)",
    "docs": "Documentation structure",
    "deploy": "Docker configs (Dockerfiles, compose, nginx)",
    ".github": "CI/CD workflows (GitHub Actions)",
}

# Конфигурационные файлы
CONFIG_FILES: list[str] = [
    ".pre-commit-config.yaml",
    ".dockerignore",
    ".gitignore",
    "pyproject.toml",
]


# ══════════════════════════════════════════════
# Clone
# ══════════════════════════════════════════════

def _clone_template(target_dir: Path, repo_url: str) -> Path:
    """Клонирует шаблон во временную папку."""
    temp_dir = target_dir / TEMP_DIR_NAME
    if temp_dir.exists():
        print(f"  ⚠️  {TEMP_DIR_NAME}/ уже существует — удаляю старый клон")
        shutil.rmtree(temp_dir)

    print(f"  📥 Cloning template from {repo_url}...")
    try:
        subprocess.run(
            ["git", "clone", "--depth", "1", repo_url, str(temp_dir)],
            check=True,
            capture_output=True,
        )
        # Удаляем .git из клона — не нужен
        git_dir = temp_dir / ".git"
        if git_dir.exists():
            shutil.rmtree(git_dir)
        print("  ✅ Template cloned\n")
        return temp_dir
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"  ❌ Failed to clone: {e}")
        sys.exit(1)


# ══════════════════════════════════════════════
# Analyze — что есть в проекте
# ══════════════════════════════════════════════

def _analyze_project(target_dir: Path) -> dict[str, bool]:
    """Сканирует проект и возвращает карту: путь → существует (и не пустой)."""
    result: dict[str, bool] = {}

    # Проверяем модули
    for rel_path in TRANSFERABLE_MODULES:
        full = target_dir / rel_path
        result[rel_path] = full.exists() and (
            full.is_file() or any(full.iterdir())
        )

    # Проверяем инфраструктуру
    for rel_path in INFRA_DIRS:
        full = target_dir / rel_path
        result[rel_path] = full.exists() and (
            full.is_file() or any(full.iterdir())
        )

    # Проверяем конфиги
    for rel_path in CONFIG_FILES:
        full = target_dir / rel_path
        result[rel_path] = full.exists()

    # Проверяем стандартные папки
    for rel_path in STANDARD_DIRS:
        if rel_path not in result:
            full = target_dir / rel_path
            result[rel_path] = full.exists()

    return result


def _print_analysis(analysis: dict[str, bool]) -> None:
    """Печатает результат анализа."""
    print("  📊 Project Analysis:")
    print("  " + "─" * 45)

    for path, exists in sorted(analysis.items()):
        icon = "✅" if exists else "❌"
        print(f"    {icon} {path}")

    print()


# ══════════════════════════════════════════════
# Safe copy — перенос с проверкой
# ══════════════════════════════════════════════

def _safe_copy(src: Path, dst: Path, label: str) -> bool:
    """Копирует только если dst не существует или пустая. Возвращает True если скопировал."""
    if dst.exists():
        if dst.is_dir() and not any(dst.iterdir()):
            # Папка пустая — можно перезаписать
            shutil.rmtree(dst)
        else:
            return False

    if not src.exists():
        return False

    if src.is_dir():
        shutil.copytree(src, dst)
    else:
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)

    print(f"    ✅ Transferred: {label}")
    return True


# ══════════════════════════════════════════════
# Transfer — перенос файлов
# ══════════════════════════════════════════════

def _transfer_modules(temp_dir: Path, target_dir: Path, analysis: dict[str, bool]) -> list[str]:
    """Переносит src/ модули которых нет в проекте. Возвращает список перенесённых."""
    transferred: list[str] = []

    print("  📦 Modules (src/):")
    for rel_path, desc in TRANSFERABLE_MODULES.items():
        if analysis.get(rel_path, False):
            print(f"    ⏭️  {rel_path} — already exists, skipping")
            continue

        src = temp_dir / rel_path
        dst = target_dir / rel_path
        if _safe_copy(src, dst, f"{rel_path} ({desc})"):
            transferred.append(rel_path)

    if not transferred:
        print("    ℹ️  All modules already present")
    print()
    return transferred


def _transfer_infra(temp_dir: Path, target_dir: Path, analysis: dict[str, bool]) -> list[str]:
    """Переносит инфраструктурные папки. Возвращает список перенесённых."""
    transferred: list[str] = []

    print("  🏗️  Infrastructure:")
    for rel_path, desc in INFRA_DIRS.items():
        if analysis.get(rel_path, False):
            print(f"    ⏭️  {rel_path} — already exists, skipping")
            continue

        src = temp_dir / rel_path
        dst = target_dir / rel_path
        if _safe_copy(src, dst, f"{rel_path} ({desc})"):
            transferred.append(rel_path)

    if not transferred:
        print("    ℹ️  All infrastructure already present")
    print()
    return transferred


def _transfer_configs(temp_dir: Path, target_dir: Path, analysis: dict[str, bool]) -> list[str]:
    """Переносит конфигурационные файлы. Возвращает список перенесённых."""
    transferred: list[str] = []

    print("  ⚙️  Config files:")
    for rel_path in CONFIG_FILES:
        if analysis.get(rel_path, False):
            print(f"    ⏭️  {rel_path} — already exists, skipping")
            continue

        src = temp_dir / rel_path
        dst = target_dir / rel_path
        if _safe_copy(src, dst, rel_path):
            transferred.append(rel_path)

    if not transferred:
        print("    ℹ️  All configs already present")
    print()
    return transferred


# ══════════════════════════════════════════════
# Ensure standard dirs — создание недостающих папок
# ══════════════════════════════════════════════

def _ensure_standard_dirs(target_dir: Path) -> list[str]:
    """Создаёт стандартные папки если их нет. Возвращает список созданных."""
    created: list[str] = []

    print("  📁 Standard directories:")
    for rel_path in STANDARD_DIRS:
        full = target_dir / rel_path
        if not full.exists():
            full.mkdir(parents=True, exist_ok=True)
            print(f"    ✅ Created: {rel_path}/")
            created.append(rel_path)

    if not created:
        print("    ℹ️  All standard directories exist")
    print()
    return created


# ══════════════════════════════════════════════
# Compare — что осталось в temp и отличается
# ══════════════════════════════════════════════

def _build_manual_report(
    temp_dir: Path,
    target_dir: Path,
    transferred_modules: list[str],
    transferred_infra: list[str],
    transferred_configs: list[str],
) -> list[str]:
    """Собирает список того что нужно сделать вручную."""
    manual_tasks: list[str] = []

    # Проверяем src/ модули которые УЖЕ были (не перенесены)
    for rel_path, desc in TRANSFERABLE_MODULES.items():
        if rel_path not in transferred_modules:
            src = temp_dir / rel_path
            dst = target_dir / rel_path
            if dst.exists() and src.exists():
                manual_tasks.append(
                    f"Compare {rel_path}/ with template version "
                    f"(.temp_template/{rel_path}/)"
                )

    # Проверяем инфраструктуру которая уже была
    for rel_path, desc in INFRA_DIRS.items():
        if rel_path not in transferred_infra:
            src = temp_dir / rel_path
            dst = target_dir / rel_path
            if dst.exists() and src.exists():
                manual_tasks.append(
                    f"Review {rel_path}/ — merge with template version if needed"
                )

    # Конфиги которые уже были
    for rel_path in CONFIG_FILES:
        if rel_path not in transferred_configs:
            src = temp_dir / rel_path
            dst = target_dir / rel_path
            if dst.exists() and src.exists():
                manual_tasks.append(
                    f"Compare {rel_path} with template version"
                )

    # Всегда добавляем общие задачи
    manual_tasks.extend([
        "Adapt imports in your existing code to match template structure",
        "Update pyproject.toml dependencies (add missing groups)",
        "Configure .env variables for your environment",
        "Review and merge documentation if docs/ existed before",
    ])

    return manual_tasks


# ══════════════════════════════════════════════
# Main
# ══════════════════════════════════════════════

def main() -> None:
    print()
    print("═" * 55)
    print("  🔄 Migration Agent — Template Integration")
    print("═" * 55)
    print()

    # Определяем целевой проект (текущая директория)
    target_dir = Path.cwd()
    print(f"  Target project: {target_dir}")
    print()

    # Repo URL
    repo_url = DEFAULT_REPO
    if len(sys.argv) > 1 and sys.argv[1] == "--repo":
        if len(sys.argv) < 3:
            print("  ❌ --repo requires a URL argument")
            sys.exit(1)
        repo_url = sys.argv[2]

    # ── Step 1: Analyze current project ──
    print("  🔍 Analyzing current project...")
    analysis = _analyze_project(target_dir)
    _print_analysis(analysis)

    # ── Step 2: Clone template ──
    temp_dir = _clone_template(target_dir, repo_url)

    # ── Step 3: Ensure standard directories ──
    created_dirs = _ensure_standard_dirs(target_dir)

    # ── Step 4: Transfer modules (src/) ──
    transferred_modules = _transfer_modules(temp_dir, target_dir, analysis)

    # ── Step 5: Transfer infrastructure ──
    transferred_infra = _transfer_infra(temp_dir, target_dir, analysis)

    # ── Step 6: Transfer config files ──
    transferred_configs = _transfer_configs(temp_dir, target_dir, analysis)

    # ── Step 7: Report ──
    print("═" * 55)

    total = len(created_dirs) + len(transferred_modules) + len(transferred_infra) + len(transferred_configs)
    if total > 0:
        print(f"  ✅ Transferred {total} items into your project")
    else:
        print("  ℹ️  Nothing to transfer — project already has everything")

    print()

    # ── Manual tasks report ──
    manual_tasks = _build_manual_report(
        temp_dir, target_dir,
        transferred_modules, transferred_infra, transferred_configs,
    )

    if manual_tasks:
        print("  📋 Manual TODO (do it yourself or use AI agent):")
        print("  " + "─" * 50)
        for i, task in enumerate(manual_tasks, 1):
            print(f"    {i}. {task}")
        print()

    # ── НЕ удаляем temp! ──
    print(f"  💡 Template files kept in: {TEMP_DIR_NAME}/")
    print("     Use them for manual comparison and merging.")
    print("     Delete when done: rm -rf .temp_template/")
    print()


if __name__ == "__main__":
    main()
