# 🏗️ Codex Project Template

[🇬🇧 English](./README.md)

> **Universal Monorepo Boilerplate**: Django / FastAPI + React / Vue + DevOps.

Этот репозиторий — фундамент для старта новых проектов. Он содержит настроенную структуру папок, готовые конфигурации Docker/CI и строгие стандарты документации.

---

## ⚡ Быстрый старт (Schnellstart)

Не клонируйте этот репозиторий вручную для работы! Используйте скрипт инициализации, чтобы создать чистый проект.

### 1. Клонирование шаблона

```bash
git clone https://github.com/codexdlc/project-template.git my-new-project
cd my-new-project
```

### 2. Запуск инициализатора

Скрипт спросит, какой стек вам нужен (Django или FastAPI), нужны ли медиа-функции (S3-mode), и удалит всё лишнее.

```bash
python tools/init_project.py
```

**Что сделает скрипт:**
*   🗑️ Удалит неиспользуемый бэкенд (например, Django, если вы выбрали FastAPI).
*   ⚙️ Сгенерирует базовый `.env`.
*   🧹 Очистит историю git (опционально).
*   📦 Переименует проект в конфигах.

### 3. Запуск окружения

```bash
cd deploy
docker-compose up -d --build
```

---

## 🧱 Архитектура и Структура

Проект следует методологии Monorepo с четким разделением ответственности.

| Директория | Описание |
| :--- | :--- |
| **📂 src/** | Исходный код модулей (backend, bot, frontend). |
| **📂 deploy/** | Docker-compose, Nginx конфиги, переменные окружения. |
| **📂 docs/** | Документация (см. ниже). |
| **📂 tools/** | Утилиты разработчика и скрипты инициализации. |
| **📂 scripts/** | CI/CD скрипты, линтеры, генераторы отчетов. |

---

## 📚 Документация: The Twin Realms

Мы используем уникальный подход к документации.

### 🇷🇺 Russian (Architect's Mind)
Для понимания концепций, "почему это сделано так" и онбординга.

*   **[📂 Корень документации](./docs/ru_RU/README.md)**
*   **[🏗️ Инфраструктура и Деплой](./docs/ru_RU/infrastructure/README.md)**
*   **[🧠 Архитектура Бэкенда](./docs/ru_RU/architecture/backend-fastapi/README.md)**

---

## 🛠️ Варианты Бэкенда

Шаблон поддерживает два режима ядра (выбирается при инициализации):

### 1. 🐍 FastAPI (Modern & Async)
Основан на архитектуре Clean Architecture.

*   **Режимы:**
    *   *Universal:* Полноценный API с пользователями, лайками и соц. механикой.
    *   *Headless (SAS/S3):* Режим микросервиса для хранения файлов (User + Media only).
*   **Фичи:** JWT Auth, Media CAS Storage (De-duplication), Alembic, Pydantic v2.

### 2. 🦄 Django (Batteries Included)
Классический подход для быстрых MVP и админок.

*   **Структура:** Split Settings, Domains instead of Apps.
*   **Фичи:** Django Admin, ORM, DRF.

---

## ✅ Pre-flight Checklist

Перед первым коммитом убедитесь, что:

- [ ] Вы запустили `python tools/init_project.py`.
- [ ] Файл `.env` создан в папке `deploy/`.
- [ ] Документация прошла линтинг: `python scripts/lint_docs.py`.

---

Copyright © 2026 CodexDLC. MIT License.
