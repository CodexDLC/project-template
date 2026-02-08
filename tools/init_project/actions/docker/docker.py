"""
Docker Action — ЗАГЛУШКА.

Генерация Docker файлов на основе выбранных сервисов.

TODO (будет реализовано после обсуждения CI/CD):
  - Dockerfile для каждого выбранного сервиса (FastAPI, Django, Bot, ARQ Worker)
  - docker-compose.yml для dev режима
  - docker-compose.prod.yml для production
  - nginx конфиг (если есть бэкенд)
  - Redis контейнер (если бот или кэш)
  - ARQ worker контейнер (если включен worker)

Шаблоны будут лежать в resources/ рядом:
  actions/docker/resources/
    ├── Dockerfile.fastapi.tpl
    ├── Dockerfile.django.tpl
    ├── Dockerfile.bot.tpl
    ├── Dockerfile.worker.tpl
    ├── Dockerfile.nginx.tpl
    ├── docker-compose.dev.tpl
    ├── docker-compose.prod.tpl
    ├── nginx.conf.tpl
    └── ...
"""

from __future__ import annotations

from tools.init_project.config import InstallContext


class DockerAction:
    """Генерация Docker файлов. Пока заглушка."""

    def execute(self, ctx: InstallContext) -> None:
        print("    ⏭️  Docker action — skipped (not yet implemented)")
