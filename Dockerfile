FROM python:3.12-slim

# Evitar que Python escriba archivos .pyc y forzar el volcado de consola
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Instalar dependencias del sistema requeridas por asyncpg y psycopg2
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Instalar uv desde la imagen oficial
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copiar dependencias y ficheros propios
COPY pyproject.toml uv.lock ./
COPY api/ ./api/

# Sincronizar el entorno de servidor (sin dev dependencies) aprovechando el lock
RUN uv sync --frozen --no-dev --no-cache

EXPOSE 8000

# Ejecutar el servidor con uvicorn invocando directamente a uv run
CMD ["uv", "run", "uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
