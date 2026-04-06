from typing import ClassVar
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Configuración global de la aplicación utilizando Pydantic Settings.
    Gestiona variables de entorno y valores por defecto.
    """

    PROJECT_NAME: str = "Modulo 2 - Gestión de Notas"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"

    # Configuración de CORS por si se quisiera conectar con el frontend (Cross-Origin Resource Sharing)
    BACKEND_CORS_ORIGINS: list[str] = ["http://localhost:3000", "http://localhost:5173"]

    # Configuración de base de datos
    # Este 'localhost' y las credenciales genéricas 'postgres' solo actúan como
    # VALOR POR DEFECTO EN DESARROLLO si la aplicación no encuentra un archivo .env
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/notes_db"

    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        """Devuelve la cadena de conexión para SQLAlchemy async con PostgreSQL."""
        return self.DATABASE_URL

    # Configuración del modelo de Pydantic para cargar desde .env
    model_config: ClassVar[SettingsConfigDict] = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=True, extra="ignore"
    )


# Instancia global de configuración
settings = Settings()
