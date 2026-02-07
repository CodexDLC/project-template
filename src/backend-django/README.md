# Django Project Setup

## Quick Start

1. Create Django project:
```bash
   cd src
   django-admin startproject backend .
```

2. Recommended structure (Codex way):
   - Split settings: `backend/settings/` (base.py, dev.py, prod.py)
   - Features structure: `features/` instead of `apps/`
   - Use Pydantic Settings for configuration

3. See docs: `docs/en_EN/architecture/backend/` for detailed setup

## Or use vanilla Django and adapt later