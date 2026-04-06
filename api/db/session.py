from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from api.core.config import settings

# Motor de base de datos asíncrono configurado para PostgreSQL
engine = create_async_engine(
    settings.SQLALCHEMY_DATABASE_URI, 
    echo=False,
    pool_pre_ping=True
)

# Fábrica de sesiones asíncronas
AsyncSessionLocal = async_sessionmaker(
    engine, 
    expire_on_commit=False, 
    class_=AsyncSession
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Generador de sesiones de base de datos para inyección de dependencias."""
    async with AsyncSessionLocal() as session:
        yield session
