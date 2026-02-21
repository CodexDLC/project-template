"""
Django Installer — создание структуры Django проекта.

Flow:
  pre_install  — ничего (зависимости через PoetryAction)
  install      — создаёт полную Django структуру из шаблонов:
                 core/ (settings split), features/ (main + system),
                 static/, templates/, locale/
  post_install — проверка что manage.py существует

Не использует django-admin startproject / startapp напрямую,
потому что наша структура сильно отличается от стандартной Django:
  - core/ вместо project_name/
  - settings/ папка (base/dev/prod) вместо settings.py
  - features/ вместо apps в корне
  - views/ и models/ как папки, не файлы
  - selectors/ слой для чтения данных
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from tools.init_project.installers.base import BaseInstaller

if TYPE_CHECKING:
    from tools.init_project.config import InstallContext

# Путь к ресурсам Django
RESOURCES_DIR = Path(__file__).parent / "django" / "resources"


class DjangoInstaller(BaseInstaller):
    name = "Django"

    def pre_install(self, ctx: InstallContext) -> None:
        print("    🐍 Django installer — preparing...")

    def install(self, ctx: InstallContext) -> None:
        """Создаёт полную Django структуру из шаблонов."""
        backend_dir = ctx.project_root / "src" / "backend_django"

        # ── 1. Core (settings, urls, wsgi, asgi) ──
        self._create_core(backend_dir, ctx.project_name)

        # ── 2. API (Django Ninja) ──
        self._create_api(backend_dir, ctx.project_name)

        # ── 3. Features: main + system ──
        self._create_feature_main(backend_dir, ctx.project_name)
        self._create_feature_system(backend_dir, ctx.project_name)

        # ── 4. Static / Templates / Locale ──
        self._create_static_dirs(backend_dir, ctx.project_name)
        self._create_templates(backend_dir, ctx.project_name)
        self._create_locale(backend_dir)

        # ── 5. Root files (manage.py, .env, README) ──
        self._create_root_files(backend_dir, ctx.project_name)

        print("    ✅ Django structure created")

    def post_install(self, ctx: InstallContext) -> None:
        manage = ctx.project_root / "src" / "backend_django" / "manage.py"
        if manage.exists():
            print("    ✅ manage.py verified")
        else:
            print("    ⚠️  manage.py not found — something went wrong")

    # ─────────────────────────────────────────
    # Core
    # ─────────────────────────────────────────

    def _create_core(self, backend_dir: Path, project_name: str) -> None:
        """Создаёт core/ с split settings."""
        core_dir = backend_dir / "core"
        settings_dir = core_dir / "settings"
        settings_dir.mkdir(parents=True, exist_ok=True)

        # Core files
        tpl_core = RESOURCES_DIR / "core"
        self._render(tpl_core / "__init__.py.tpl", core_dir / "__init__.py", project_name)
        self._render(tpl_core / "urls.py.tpl", core_dir / "urls.py", project_name)
        self._render(tpl_core / "asgi.py.tpl", core_dir / "asgi.py", project_name)
        self._render(tpl_core / "wsgi.py.tpl", core_dir / "wsgi.py", project_name)

        # Settings
        tpl_settings = tpl_core / "settings"
        self._render(tpl_settings / "__init__.py.tpl", settings_dir / "__init__.py", project_name)
        self._render(tpl_settings / "base.py.tpl", settings_dir / "base.py", project_name)
        self._render(tpl_settings / "dev.py.tpl", settings_dir / "dev.py", project_name)
        self._render(tpl_settings / "prod.py.tpl", settings_dir / "prod.py", project_name)

        print("    ✅ core/ (settings split: base/dev/prod)")

    # ─────────────────────────────────────────
    # API (Django Ninja)
    # ─────────────────────────────────────────

    def _create_api(self, backend_dir: Path, project_name: str) -> None:
        """Создаёт api/ с Django Ninja роутерами."""
        api_dir = backend_dir / "api"
        api_dir.mkdir(parents=True, exist_ok=True)

        tpl_api = RESOURCES_DIR / "api"
        self._render(tpl_api / "__init__.py.tpl", api_dir / "__init__.py", project_name)
        self._render(tpl_api / "urls.py.tpl", api_dir / "urls.py", project_name)

        print("    ✅ api/ (Django Ninja, versioned routes)")

    # ─────────────────────────────────────────
    # Features
    # ─────────────────────────────────────────

    def _create_feature_main(self, backend_dir: Path, project_name: str) -> None:
        """Создаёт features/main/ — стартовая feature с views/ и selectors/."""
        feat_dir = backend_dir / "features" / "main"
        views_dir = feat_dir / "views"
        selectors_dir = feat_dir / "selectors"
        migrations_dir = feat_dir / "migrations"

        for d in [views_dir, selectors_dir, migrations_dir]:
            d.mkdir(parents=True, exist_ok=True)

        tpl = RESOURCES_DIR / "feature_tpl"

        # __init__.py
        self._render(tpl / "__init__.py.tpl", feat_dir / "__init__.py", project_name)

        # apps.py
        self._render_feature_apps(
            tpl / "apps.py.tpl",
            feat_dir / "apps.py",
            app_name="main",
            app_class="Main",
            app_verbose="Main",
        )

        # admin.py, tests.py, translation.py
        self._render(tpl / "admin.py.tpl", feat_dir / "admin.py", project_name)
        self._render(tpl / "tests.py.tpl", feat_dir / "tests.py", project_name)
        self._render(tpl / "translation.py.tpl", feat_dir / "translation.py", project_name)

        # urls.py
        self._render(tpl / "urls.py.tpl", feat_dir / "urls.py", project_name, extra={"{{APP_NAME}}": "main"})

        # models.py (пустой, можно потом сделать папку)
        (feat_dir / "models.py").write_text("# from django.db import models\n", encoding="utf-8")

        # views/__init__.py + views/home.py
        (views_dir / "__init__.py").write_text("", encoding="utf-8")
        self._render(tpl / "home_view.py.tpl", views_dir / "home.py", project_name)

        # selectors/__init__.py
        (selectors_dir / "__init__.py").write_text("", encoding="utf-8")

        # migrations/__init__.py
        (migrations_dir / "__init__.py").write_text("", encoding="utf-8")

        print("    ✅ features/main/ (views/, selectors/, urls)")

    def _create_feature_system(self, backend_dir: Path, project_name: str) -> None:
        """Создаёт features/system/ — полноценное ядро проекта (SiteSettings, RedisSync, Commands, etc.)."""
        feat_dir = backend_dir / "features" / "system"
        models_dir = feat_dir / "models"
        redis_dir = feat_dir / "redis_managers"
        migrations_dir = feat_dir / "migrations"

        # New: Management & Fixtures
        mgmt_dir = feat_dir / "management" / "commands"
        fixtures_dir = feat_dir / "fixtures"

        for d in [models_dir, redis_dir, migrations_dir, mgmt_dir, fixtures_dir]:
            d.mkdir(parents=True, exist_ok=True)

        tpl_system = RESOURCES_DIR / "system_tpl"
        tpl_base = RESOURCES_DIR / "feature_tpl"

        # 1. Base files
        self._render(tpl_base / "__init__.py.tpl", feat_dir / "__init__.py", project_name)
        self._render_feature_apps(
            tpl_base / "apps.py.tpl",
            feat_dir / "apps.py",
            app_name="system",
            app_class="System",
            app_verbose="System Core",
        )
        self._render(tpl_system / "admin.py.tpl", feat_dir / "admin.py", project_name)
        self._render(tpl_system / "translation.py.tpl", feat_dir / "translation.py", project_name)
        self._render(tpl_system / "context_processors.py.tpl", feat_dir / "context_processors.py", project_name)

        # 2. Models
        self._render(tpl_system / "models" / "__init__.py.tpl", models_dir / "__init__.py", project_name)
        self._render(tpl_system / "models" / "site_settings.py.tpl", models_dir / "site_settings.py", project_name)
        self._render(
            tpl_system / "models" / "static_translation.py.tpl", models_dir / "static_translation.py", project_name
        )
        self._render(tpl_system / "models" / "mixins.py.tpl", models_dir / "mixins.py", project_name)

        # 3. Redis Managers
        self._render(
            tpl_system / "redis_managers" / "site_settings_manager.py.tpl",
            redis_dir / "site_settings_manager.py",
            project_name,
        )

        # 4. Management & Fixtures
        (feat_dir / "management" / "__init__.py").write_text("", encoding="utf-8")
        (feat_dir / "management" / "commands" / "__init__.py").write_text("", encoding="utf-8")

        self._render(
            tpl_system / "management" / "commands" / "update_site_settings.py.tpl",
            mgmt_dir / "update_site_settings.py",
            project_name,
        )
        self._render(
            tpl_system / "management" / "commands" / "update_static_translations.py.tpl",
            mgmt_dir / "update_static_translations.py",
            project_name,
        )
        self._render(
            tpl_system / "management" / "commands" / "update_all_content.py.tpl",
            mgmt_dir / "update_all_content.py",
            project_name,
        )
        self._render(
            tpl_system / "fixtures" / "site_settings.json.tpl", fixtures_dir / "site_settings.json", project_name
        )

        # 5. Cleanup/Init
        (migrations_dir / "__init__.py").write_text("", encoding="utf-8")

        # features/__init__.py
        features_init = backend_dir / "features" / "__init__.py"
        if not features_init.exists():
            features_init.write_text("", encoding="utf-8")

        print("    ✅ features/system/ (SiteSettings + RedisSync + Commands + Fixtures)")

    # ─────────────────────────────────────────
    # Static / Templates / Locale
    # ─────────────────────────────────────────

    def _create_static_dirs(self, backend_dir: Path, project_name: str) -> None:
        """Создаёт static/ структуру с поддержкой CSS компилятора."""
        static_dir = backend_dir / "static"
        css_dir = static_dir / "css"

        for sub in ["css", "js", "img"]:
            (static_dir / sub).mkdir(parents=True, exist_ok=True)

        tpl_css = RESOURCES_DIR / "static" / "css"
        if tpl_css.exists():
            # CSS инфраструктура
            self._render(tpl_css / "base.css.tpl", css_dir / "base.css", project_name)
            self._render(tpl_css / "tokens.css.tpl", css_dir / "tokens.css", project_name)
            self._render(tpl_css / "layout.css.tpl", css_dir / "layout.css", project_name)
            self._render(tpl_css / "components.css.tpl", css_dir / "components.css", project_name)
            self._render(tpl_css / "compiler_config.json.tpl", css_dir / "compiler_config.json", project_name)

            # Создаём пустой app.css чтобы Django не ругался при первом запуске
            (css_dir / "app.css").write_text("/* Compiled CSS will appear here */\n", encoding="utf-8")
        else:
            # Fallback если шаблонов нет
            (css_dir / "base.css").write_text("/* Base styles */\n", encoding="utf-8")

        print("    ✅ static/ (css/ with compiler config, js/, img/)")

    def _create_templates(self, backend_dir: Path, project_name: str) -> None:
        """Создаёт templates/base.html и templates/home/home.html."""
        templates_dir = backend_dir / "templates"
        home_dir = templates_dir / "home"
        home_dir.mkdir(parents=True, exist_ok=True)

        self._render(RESOURCES_DIR / "base.html.tpl", templates_dir / "base.html", project_name)
        self._render(RESOURCES_DIR / "home.html.tpl", home_dir / "home.html", project_name)

        print("    ✅ templates/ (base.html, home/home.html)")

    def _create_locale(self, backend_dir: Path) -> None:
        """Создаёт пустую locale/ структуру для i18n."""
        locale_dir = backend_dir / "locale"
        locale_dir.mkdir(parents=True, exist_ok=True)
        print("    ✅ locale/ (ready for i18n)")

    # ─────────────────────────────────────────
    # Root files
    # ─────────────────────────────────────────

    def _create_root_files(self, backend_dir: Path, project_name: str) -> None:
        """Создаёт manage.py, .env, .env.example, __init__.py, README.md."""
        # __init__.py
        init_file = backend_dir / "__init__.py"
        if not init_file.exists():
            init_file.write_text("", encoding="utf-8")

        # manage.py
        self._render(RESOURCES_DIR / "manage.py.tpl", backend_dir / "manage.py", project_name)

        # .env + .env.example + .env.production
        self._render(RESOURCES_DIR / "env.tpl", backend_dir / ".env", project_name)
        self._render(RESOURCES_DIR / "env.example.tpl", backend_dir / ".env.example", project_name)
        self._render(RESOURCES_DIR / "env.production.tpl", backend_dir / ".env.production", project_name)

        # README.md
        self._render(RESOURCES_DIR / "README.md.tpl", backend_dir / "README.md", project_name)

        print("    ✅ manage.py, .env, .env.example, .env.production, README.md")

    # ─────────────────────────────────────────
    # Template rendering helpers
    # ─────────────────────────────────────────

    @staticmethod
    def _render(
        tpl_path: Path,
        output_path: Path,
        project_name: str,
        *,
        extra: dict[str, str] | None = None,
    ) -> None:
        """Читает .tpl, заменяет маркеры, пишет результат."""
        if not tpl_path.exists():
            return

        content = tpl_path.read_text(encoding="utf-8")
        content = content.replace("{{PROJECT_NAME}}", project_name)

        if extra:
            for marker, value in extra.items():
                content = content.replace(marker, value)

        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(content, encoding="utf-8")

    @staticmethod
    def _render_feature_apps(
        tpl_path: Path,
        output_path: Path,
        *,
        app_name: str,
        app_class: str,
        app_verbose: str,
    ) -> None:
        """Рендерит apps.py для feature с заменой APP маркеров."""
        if not tpl_path.exists():
            return

        content = tpl_path.read_text(encoding="utf-8")
        content = content.replace("{{APP_NAME}}", app_name)
        content = content.replace("{{APP_CLASS}}", app_class)
        content = content.replace("{{APP_VERBOSE}}", app_verbose)

        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(content, encoding="utf-8")
