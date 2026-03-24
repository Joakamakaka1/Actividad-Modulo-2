import logging
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from api.db.session import get_db

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/")
async def health_check():
    """Prueba simple de salud de la API."""
    return {"status": "ok", "api": "saludable"}


@router.get("/db")
async def db_health_check(db: AsyncSession = Depends(get_db)):
    """Prueba de conexión a la base de datos SQLite."""
    try:
        # Ejecutamos una consulta simple para verificar la conectividad
        await db.execute(text("SELECT 1"))
        return {"status": "ok", "database": "conectada"}
    except Exception as e:
        logger.error("Fallo la prueba de salud de la DB: %s", e)
        return {"status": "error", "database": "desconectada"}
