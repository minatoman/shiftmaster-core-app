# ============================================
# ShiftMaster - 開発用Docker構成
# Multi-stage build for production optimization
# ============================================

# === Stage 1: Base Python Environment ===
FROM python:3.11-slim-bullseye as base

# System dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    default-libmysqlclient-dev \
    pkg-config \
    gettext \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Create app user for security
RUN groupadd --gid 1000 django && \
    useradd --uid 1000 --gid django --shell /bin/bash --create-home django

# === Stage 2: Dependencies ===
FROM base as dependencies

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# === Stage 3: Development ===
FROM dependencies as development

# Install development dependencies
RUN pip install --no-cache-dir \
    django-debug-toolbar \
    pytest-django \
    black \
    flake8 \
    isort

# Copy application code
COPY . /app/

# Change ownership to django user
RUN chown -R django:django /app

# Switch to django user
USER django

# Expose port
EXPOSE 8000

# Development command
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# === Stage 4: Production ===
FROM dependencies as production

# Copy application code
COPY --chown=django:django . /app/

# Install production dependencies
RUN pip install --no-cache-dir gunicorn psycopg2-binary

# Change ownership to django user
USER django

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health/', timeout=10)" || exit 1

# Production command
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "shiftmaster.wsgi:application"]
