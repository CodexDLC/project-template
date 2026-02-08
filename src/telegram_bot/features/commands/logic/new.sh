git commit --amend -m "refactor: migrate code to new project template structure

- **Telegram Bot:**
  - Ported code from legacy src.frontend to src.telegram_bot.
  - Removed specific game logic (Arena, Combat) to keep the template clean.
  - Updated imports to match the new monorepo structure.

- **Backend:**
  - Standardized imports to src.backend_fastapi.
  - Integrated shared logging and configuration.

- **Infrastructure:**
  - Added initial Docker and CI/CD configurations.
  - Reorganized documentation into the Twin Realms structure."