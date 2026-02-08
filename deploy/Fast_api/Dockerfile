# === STAGE 1: Builder ===
FROM python:3.12-slim AS builder

WORKDIR /app

# System dependencies for build
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libpq-dev \
    libmagic1 \
    libmagic-dev \
    libjpeg-dev \
    zlib1g-dev \
    libpng-dev \
    && rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python -m venv /app/.venv

# Copy requirements
COPY backend/requirements.txt .

# Install dependencies
RUN /app/.venv/bin/pip install --no-cache-dir -r requirements.txt

# === STAGE 2: Runtime ===
FROM python:3.12-slim

WORKDIR /app

# System dependencies for runtime
RUN apt-get update && apt-get install -y \
    libpq5 \
    curl \
    libmagic1 \
    libjpeg62-turbo \
    zlib1g \
    libpng16-16 \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd -m -u 1000 appuser

# Copy venv from builder
COPY --from=builder /app/.venv /app/.venv

# Copy application code
COPY backend /app/backend

# Create data directories
RUN mkdir -p /app/data/uploads /app/data/logs && \
    chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Add venv to PATH
ENV PATH="/app/.venv/bin:$PATH"

# Health check
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Start command
# --proxy-headers: Trust X-Forwarded-For headers from Nginx
# --forwarded-allow-ips='*': Trust any proxy (Docker IP is dynamic)
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers", "--forwarded-allow-ips='*'"]
