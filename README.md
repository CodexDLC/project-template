# 🏗️ Codex Project Template

[🇷🇺 Русский](./README-RU.md)

> **Universal Monorepo Boilerplate**: Django / FastAPI + React / Vue + DevOps.

This repository is the foundation for starting new projects. It contains a configured folder structure, ready-made Docker/CI configurations, and strict documentation standards.

---

## ⚡ Quick Start

Do not clone this repository manually for work! Use the initialization script to create a clean project.

### 1. Clone the Template

```bash
git clone https://github.com/codexdlc/project-template.git my-new-project
cd my-new-project
```

### 2. Run Initializer

The script will ask which stack you need (Django or FastAPI), whether you need media functions (S3-mode), and will remove everything unnecessary.

```bash
python tools/init_project.py
```

**What the script does:**
*   🗑️ Removes unused backend (e.g., Django if you chose FastAPI).
*   ⚙️ Generates a base `.env`.
*   🧹 Cleans git history (optional).
*   📦 Renames the project in configs.

### 3. Start Environment

```bash
cd deploy
docker-compose up -d --build
```

---

## 🧱 Architecture & Structure

The project follows the Monorepo methodology with clear separation of concerns.

| Directory | Description |
| :--- | :--- |
| **📂 src/** | Source code modules (backend, bot, frontend). |
| **📂 deploy/** | Docker-compose, Nginx configs, environment variables. |
| **📂 docs/** | Documentation (see below). |
| **📂 tools/** | Developer utilities and init scripts. |
| **📂 scripts/** | CI/CD scripts, linters, report generators. |

---

## 📚 Documentation: The Twin Realms

We use a unique approach to documentation.

### 🇬🇧 English (Technical Truth)
For schemas, API contracts, and technical details. Mandatory for developers.

*   **[📂 Documentation Root](./docs/README.md)**
*   **[🏗️ Infrastructure & Deploy](./docs/en_EN/infrastructure/README.md)**
*   **[🧠 Backend Architecture](./docs/en_EN/architecture/backend-fastapi/README.md)**

---

## 🛠️ Backend Options

The template supports two core modes (selected during initialization):

### 1. 🐍 FastAPI (Modern & Async)
Based on Clean Architecture.

*   **Modes:**
    *   *Universal:* Full API with users, likes, and social mechanics.
    *   *Headless (SAS/S3):* Microservice mode for file storage (User + Media only).
*   **Features:** JWT Auth, Media CAS Storage (De-duplication), Alembic, Pydantic v2.

### 2. 🦄 Django (Batteries Included)
Classic approach for fast MVPs and admin panels.

*   **Structure:** Split Settings, Domains instead of Apps.
*   **Features:** Django Admin, ORM, DRF.

---

## ✅ Pre-flight Checklist

Before the first commit, ensure that:

- [ ] You ran `python tools/init_project.py`.
- [ ] The `.env` file is created in `deploy/` folder.
- [ ] Documentation passed linting: `python scripts/lint_docs.py`.

---

Copyright © 2026 CodexDLC. MIT License.
