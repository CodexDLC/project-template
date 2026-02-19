name: Deploy Production (Tag-based)

on:
  push:
    tags:
      - 'v*'
  workflow_dispatch:

jobs:
  build-and-push:
    name: Build & Push Docker Images
    runs-on: ubuntu-latest

    permissions:
      contents: read
      packages: write

    steps:
      - uses: actions/checkout@v4

      - name: Extract version from tag
        run: |
          echo "VERSION=${GITHUB_REF#refs/tags/}" >> $GITHUB_ENV

      - name: Lowercase repo name
        run: |
          echo "REPO_LOWER=${GITHUB_REPOSITORY,,}" >> $GITHUB_ENV

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Log in to GHCR
        uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

{{BUILD_PUSH_STEPS}}

  # ── Deploy ────────────────────────────────────────────────────────────────
  # TODO: Add your deploy job here.
  #
  # Examples:
  #   - SSH + docker compose pull && up -d
  #   - Kubernetes: kubectl rollout restart
  #   - Render / Railway / Fly.io: deploy hook
  #
  # Uncomment and configure the block below for SSH deploy to VPS:
  #
  # deploy:
  #   name: Deploy to VPS
  #   needs: build-and-push
  #   runs-on: ubuntu-latest
  #   steps:
  #     - name: SSH Deploy
  #       uses: appleboy/ssh-action@v1.0.3
  #       env:
  #         VERSION: ${{ env.VERSION }}
  #         ENV_FILE_CONTENT: ${{ secrets.ENV_FILE }}
  #       with:
  #         host: ${{ secrets.HOST }}
  #         username: ${{ secrets.USERNAME }}
  #         key: ${{ secrets.SSH_KEY }}
  #         envs: VERSION,ENV_FILE_CONTENT
  #         script: |
  #           set -e
  #           cd /opt/{{PROJECT_NAME}}/deploy
  #           printf '%s\n' "$ENV_FILE_CONTENT" > .env
  #           docker compose -f docker-compose.prod.yml pull
{{MIGRATION_STEPS_COMMENT}}
  #           docker compose -f docker-compose.prod.yml up -d --remove-orphans --wait --wait-timeout 120
  #           docker image prune -f
  #           echo "Deployed $VERSION successfully!"
