from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.core.config import settings
from api.api.v1.api_router import api_router
from api.db.base import Base
from api.db.session import engine

# Importar todos los modelos para que SQLAlchemy los descubra antes de create_all
import api.models.note  # noqa: F401


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gestiona el ciclo de vida de la aplicación.
    - Al arrancar: Crea las tablas de la base de datos si no existen.
    - Al cerrar: Libera los recursos del motor de base de datos.
    """
    # Arranque: crear todas las tablas definidas en Base.metadata
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Cierre: disponer el pool de conexiones del motor
    await engine.dispose()


def create_app() -> FastAPI:
    """
    Fábrica de la aplicación FastAPI.
    Configura middlewares, rutas y metadatos.
    """
    app = FastAPI(
        title=settings.PROJECT_NAME,
        description="API REST para la gestión de notas y tareas (SQLite Async)",
        version=settings.VERSION,
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        lifespan=lifespan,
    )

    # Configuración de CORS por si se quisiera conectar con el frontend
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Inclusión del enrutador principal con prefijo de versión
    app.include_router(api_router, prefix=settings.API_V1_STR)
    return app


# Instancia principal de la aplicación
app = create_app()
