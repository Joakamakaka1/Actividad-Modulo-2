import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from api.core.config import settings
from api.api.v1.api_router import api_router
from api.db.base import Base
from api.db.session import engine
from api.core.exceptions import BaseAPIException

# Importar todos los modelos para que SQLAlchemy los descubra antes de create_all
import api.models.note  # noqa: F401

# Configuración básica de Logging para Trazabilidad
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("api")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gestiona el ciclo de vida de la aplicación.
    - Arranque con conexión y BD
    - Cierre liberando recursos
    """
    logger.info("Iniciando aplicación. Creando tablas si no existen...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    logger.info("Cerrando aplicación. Liberando pool de base de datos...")
    await engine.dispose()


def create_app() -> FastAPI:
    """
    Fábrica de la aplicación FastAPI.
    Configura middlewares, manejadores de error y rutas.
    """
    app = FastAPI(
        title=settings.PROJECT_NAME,
        description="API REST para la gestión de notas y tareas (Docker + PostgreSQL)",
        version=settings.VERSION,
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        lifespan=lifespan,
    )

    # Manejar excepciones de la API Base como errores y registrar
    @app.exception_handler(BaseAPIException)
    async def base_api_exception_handler(request: Request, exc: BaseAPIException):
        logger.error(f"Error en API (Estado: {exc.status_code}): {exc.detail}")
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
        )

    # Forzar que los errores de validación de Pydantic devuelvan un HTTP 400 (Bad Request)
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ):
        logger.warning(
            f"Error de validación (400) en request a {request.url}: {exc.errors()}"
        )
        return JSONResponse(
            status_code=400,
            content={
                "detail": "Los datos proporcionados no son válidos (Bad Request).",
                "errors": exc.errors(),
            },
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
