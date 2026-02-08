# Project Template

[🇷🇺 Русский](./README-RU.md)

> **Modular Monorepo Template**: Django / FastAPI / Telegram Bot — with installer, Docker, CI/CD, and PostgreSQL schema isolation.

---

## Quick Start

### 1. Clone

```bash
# Into a new folder:
git clone https://github.com/codexdlc/project-template.git my-project
cd my-project

# Or into the current folder:
mkdir my-project && cd my-project
git clone https://github.com/codexdlc/project-template.git .
```

### 2. Install dependencies

```bash
pip install poetry
poetry config virtualenvs.in-project true
poetry install --extras "fastapi bot dev"   # or: --extras "django bot dev"
```

### 3. Run the installer

```bash
python -m tools.init_project
```

The interactive CLI will ask:
- **Project name** — renames configs, pyproject.toml, etc.
- **Backend** — FastAPI, Django, or none
- **Telegram Bot** — include or remove
- **Git init** — create initial commits

### 4. What the installer does

1. **Poetry** — installs dependencies, removes unused groups (e.g. `django` group if FastAPI was chosen)
2. **Scaffolder** — generates `deploy/`, `.github/workflows/`, `.env` from `.tpl` templates
3. **Backend installer** — sets up the chosen framework (FastAPI is ready; Django is built from templates)
4. **Bot installer** — configures the Telegram bot module
5. **Cleaner** — removes unused modules (src dirs, deploy dirs, docs)
6. **Renamer** — replaces `project-template` marker with your project name
7. **Finalizer** — creates two git commits: `Install` (full state) → `Activate` (clean project)

---

## Project Structure

```
project-template/
├── src/
│   ├── backend-fastapi/      # FastAPI backend (async, Clean Architecture)
│   ├── backend-django/       # Django backend (features-based structure)
│   ├── telegram_bot/         # Telegram Bot (aiogram 3.x)
│   └── shared/               # Shared code: config, logging, constants
├── tools/
│   ├── init_project/         # Modular installer (kept after install)
│   │   ├── actions/          # Poetry, Docker, Scaffolder, Cleaner, Renamer, Finalizer
│   │   └── installers/       # Per-framework installers + resources/
│   ├── dev/                  # Developer utilities
│   └── migration_agent.py    # Migrate existing projects to this template
├── scripts/
│   ├── init_db_schemas.sql   # PostgreSQL schema isolation setup
│   └── generate_project_tree.py
├── deploy/                   # Generated: docker-compose, nginx (from .tpl)
├── .github/workflows/        # Generated: CI/CD pipelines (from .tpl)
├── docs/                     # Documentation (en_EN / ru_RU)
├── data/                     # Volumes, local data (gitignored)
└── pyproject.toml            # Poetry, Ruff, Mypy, Pytest configs
```

---

## Backends

### FastAPI (async REST API)

- **Architecture**: Clean Architecture with layers (routers → services → repositories)
- **Database**: SQLAlchemy 2.0 (async) + Alembic migrations
- **Config**: Pydantic Settings v2, `.env` file
- **Key features**: JWT auth, async PostgreSQL (asyncpg), Pydantic v2 schemas

```
src/backend-fastapi/
├── api/                  # Routers (endpoints)
├── core/                 # Config, database, security
├── database/
│   ├── models/           # SQLAlchemy models
│   └── migrations/       # Alembic (env.py, versions/)
├── repositories/         # Data access layer
├── schemas/              # Pydantic request/response models
└── services/             # Business logic
```

### Django (full-stack)

- **Architecture**: Features-based (not flat apps)
- **Settings**: Split into `base.py` / `dev.py` / `prod.py`
- **Key features**: Django Admin, ORM, split settings, feature isolation

```
src/backend-django/
├── core/                 # Project core (urls, wsgi, asgi)
│   └── settings/         # base.py, dev.py, prod.py
├── features/
│   ├── main/             # Main feature (views/, selectors/, urls)
│   └── system/           # System models (mixins, base models)
├── static/               # CSS, JS, images (separate from features)
├── templates/            # Django templates (separate from features)
└── locale/               # i18n translations
```

### Telegram Bot (aiogram 3.x)

- **Framework**: aiogram 3 with Dispatcher + Router pattern
- **Data modes**: `BOT_DATA_MODE=api` (REST calls to backend) or `direct` (own database)
- **Database**: SQLAlchemy + Alembic (when `direct` mode)
- **Config**: Pydantic Settings, shared `.env` with FastAPI

```
src/telegram_bot/
├── core/                 # Config, bot instance
├── handlers/             # Message/callback handlers
├── keyboards/            # Inline/reply keyboards
├── middlewares/          # Aiogram middlewares
├── services/             # Business logic / API clients
└── database/             # Models + Alembic migrations (direct mode)
```

---

## Database & Schema Isolation

All backends can share **one PostgreSQL database** (e.g. Neon) using separate schemas:

| Backend  | Schema        | Config variable |
| :------- | :------------ | :-------------- |
| FastAPI  | `fastapi_app` | `DB_SCHEMA`     |
| Django   | `django_app`  | `DB_SCHEMA`     |
| Bot      | `bot_app`     | `DB_SCHEMA`     |

### Setup

```bash
# Create schemas (run once on new database)
psql $DATABASE_URL -f scripts/init_db_schemas.sql
```

Each backend uses `search_path` to isolate tables:
- **FastAPI**: `connect_args.server_settings.search_path`
- **Django**: `DATABASES.default.OPTIONS.options` (prod.py)
- **Bot**: same as FastAPI pattern

---

## Migrations

Migrations run in **CI/CD pipeline**, not at application startup (prevents race conditions).

### FastAPI (Alembic)

```bash
cd src/backend_fastapi

# Create migration
alembic revision --autogenerate -m "add_users_table"

# Apply
alembic upgrade head

# Docker
docker compose run --rm -T backend alembic upgrade head
```

### Django

```bash
cd src/backend_django

python manage.py makemigrations
python manage.py migrate

# Docker
docker compose run --rm -T backend python manage.py migrate --noinput
```

### Bot (Alembic, direct mode only)

```bash
cd src/telegram_bot

alembic revision --autogenerate -m "add_bot_users"
alembic upgrade head
```

---

## Configuration

### Environment Variables

- **FastAPI + Bot** — shared root `.env` (loaded via `pydantic-settings`)
- **Django** — own `src/backend-django/.env` (loaded via `python-dotenv`)

Key variables:

| Variable        | Description              | Default        |
| :-------------- | :----------------------- | :------------- |
| `DATABASE_URL`  | PostgreSQL connection    | (required)     |
| `DB_SCHEMA`     | Schema name              | per-backend    |
| `BOT_TOKEN`     | Telegram bot token       | (required)     |
| `BOT_DATA_MODE` | `api` or `direct`        | `api`          |
| `SECRET_KEY`    | Django/JWT secret        | (required)     |
| `DEBUG`         | Debug mode               | `True`         |

### Deploy & CI/CD

Docker and GitHub Actions configs are **generated** by the installer from `.tpl` templates:

```
tools/init_project/actions/docker/resources/    → deploy/
tools/init_project/actions/scaffolder/resources/ → .github/workflows/
```

The CD pipeline runs migrations **before** `docker compose up -d`.

---

## Tools

### Installer (`tools/init_project/`)

The installer is **kept after installation** — not deleted. You can re-use it or reference its templates.

### Add Module (`tools/init_project/add_module.py`)

Restore a previously removed module (e.g. add bot to a FastAPI-only project):

```bash
python -m tools.init_project.add_module telegram_bot
```

Uses `git checkout` from the Install commit to restore files.

### Migration Agent (`tools/migration_agent.py`)

Migrate an existing project to this template structure:

```bash
python tools/migration_agent.py /path/to/existing-project
```

Analyzes your project, creates standard directories, transfers modules, and generates a TODO report for manual steps.

---

## Development

```bash
# Linting
ruff check src/
ruff format src/

# Type checking
mypy src/

# Tests
pytest

# Pre-commit hooks
pre-commit install
pre-commit run --all-files
```

Tool configs are in `pyproject.toml` (Ruff, Mypy, Pytest).

---

## Tech Stack

| Component  | Technology                                     |
| :--------- | :--------------------------------------------- |
| Python     | 3.13+                                          |
| FastAPI    | FastAPI, SQLAlchemy 2.0, asyncpg, Alembic      |
| Django     | Django 5.1, psycopg2, gunicorn                 |
| Bot        | aiogram 3.x, arq                               |
| Database   | PostgreSQL (Neon-compatible), schema isolation  |
| Config     | Pydantic Settings v2, python-dotenv (Django)    |
| Build      | Poetry (PEP 621)                               |
| Linting    | Ruff, Mypy, pre-commit                         |
| CI/CD      | GitHub Actions, Docker Compose                  |

---

Copyright © 2026 CodexDLC. MIT License.
