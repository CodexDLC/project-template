name: Deploy Production (Tag-based)

on:
  push:
    tags:
      - 'v*'  # Triggered on any tag starting with 'v' (e.g. v1.2.3)
  workflow_dispatch:  # Manual trigger

jobs:
  pre-deploy-check:
    name: Check Server Availability
    runs-on: ubuntu-latest
    steps:
      - name: Test SSH Connection
        uses: appleboy/ssh-action@v1.0.3
        with:
          host: ${{ secrets.HOST }}
          username: ${{ secrets.USERNAME }}
          key: ${{ secrets.SSH_KEY }}
          script: echo "SSH Connection Successful!"

  deploy:
    name: Build & Deploy to VPS
    needs: pre-deploy-check
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

      - name: Copy configs to VPS
        uses: appleboy/scp-action@v0.1.7
        with:
          host: ${{ secrets.HOST }}
          username: ${{ secrets.USERNAME }}
          key: ${{ secrets.SSH_KEY }}
          source: "deploy/"
          target: "/opt/{{PROJECT_NAME}}/"
          strip_components: 0
          rm: false
          overwrite: true

      - name: SSH Deploy
        uses: appleboy/ssh-action@v1.0.3
        env:
{{DOCKER_IMAGE_ENVS}}
          DOMAIN_NAME: ${{ secrets.DOMAIN_NAME }}
          REDIS_PASSWORD: ${{ secrets.REDIS_PASSWORD }}
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          GITHUB_ACTOR: ${{ github.actor }}
          VERSION: ${{ env.VERSION }}
          ENV_FILE_CONTENT: ${{ secrets.ENV_FILE }}
        with:
          host: ${{ secrets.HOST }}
          username: ${{ secrets.USERNAME }}
          key: ${{ secrets.SSH_KEY }}
          envs: {{DOCKER_IMAGE_ENV_NAMES}},DOMAIN_NAME,REDIS_PASSWORD,GITHUB_TOKEN,GITHUB_ACTOR,VERSION,ENV_FILE_CONTENT
          script: |
            set -e

            cd /opt/{{PROJECT_NAME}}/deploy

            echo "Deploying version: $VERSION"

            # Write .env into deploy folder (where docker-compose.prod.yml lives)
            printf '%s\n' "$ENV_FILE_CONTENT" > .env

            update_var() {
              grep -q "^$1=" .env && sed -i "s|^$1=.*|$1=$2|g" .env || echo "$1=$2" >> .env
            }

{{UPDATE_VAR_CALLS}}

            [ ! -z "$DOMAIN_NAME" ] && update_var "DOMAIN_NAME" "$DOMAIN_NAME"
            [ ! -z "$REDIS_PASSWORD" ] && update_var "REDIS_PASSWORD" "$REDIS_PASSWORD"

            if ! grep -q "DOMAIN_NAME" .env; then
              DOMAIN=$(grep "SITE_BASE_URL" .env 2>/dev/null | cut -d'/' -f3 | cut -d':' -f1 || echo "")
              [ ! -z "$DOMAIN" ] && update_var "DOMAIN_NAME" "$DOMAIN"
            fi

            # Login to GHCR
            echo "$GITHUB_TOKEN" | docker login ghcr.io -u "$GITHUB_ACTOR" --password-stdin

            # Pull images
            docker compose -f docker-compose.prod.yml pull

            # Run migrations before cutover
            echo "Running migrations..."
            if ! docker compose -f docker-compose.prod.yml run --rm -T backend python manage.py migrate --noinput; then
              echo "Migration failed! Aborting deployment."
              exit 1
            fi

            echo "Collecting static files..."
            docker compose -f docker-compose.prod.yml run --rm -T backend python manage.py collectstatic --noinput

            # Start services
            echo "Starting services..."
            docker compose -f docker-compose.prod.yml up -d --remove-orphans --wait --wait-timeout 120

            # Verify containers are healthy
            echo "Checking container health..."
            docker compose -f docker-compose.prod.yml ps

            # Cleanup old images
            docker image prune -f

            echo "Deployment $VERSION completed successfully!"
