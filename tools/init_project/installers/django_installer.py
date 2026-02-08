"""
Django Installer — ЗАГЛУШКА.

Будущая логика:
  pre_install  — poetry add django djangorestframework ...
  install      — удалить src/backend-fastapi/, создать Django-структуру,
                 применить шаблоны settings.py/urls.py, создать base features
  post_install — python manage.py check
"""

from __future__ import annotations

from tools.init_project.config import InstallContext
from tools.init_project.installers.base import BaseInstaller


class DjangoInstaller(BaseInstaller):

    name = "Django"

    def pre_install(self, ctx: InstallContext) -> None:
        # TODO: poetry add django djangorestframework psycopg2-binary ...
        print("    ⚠️  Django installer not yet implemented — will be configured later")

    def install(self, ctx: InstallContext) -> None:
        """
        TODO:
        1. Удалить src/backend-fastapi/ (FastAPI код)
        2. Создать src/backend-django/ структуру с features (не apps)
        3. Применить шаблоны из actions/scaffolder/resources/django/
        4. Переписать settings.py с auto-discovery features
        5. Настроить urls.py
        6. Создать базовые features
        """
        pass

    def post_install(self, ctx: InstallContext) -> None:
        # TODO: python manage.py check
        pass
