from datetime import datetime
from pydantic import BaseModel, field_validator


class NoteCreate(BaseModel):
    """Esquema para la creación de una nueva nota."""

    title: str
    content: str
    deadline: datetime

    @field_validator("title", "content")
    @classmethod
    def strip_whitespace(cls, v: str) -> str:
        """Limpia espacios en blanco antes y después del texto."""
        return v.strip()


class NoteUpdate(BaseModel):
    """Esquema para la actualización parcial de una nota existente."""

    title: str | None = None
    content: str | None = None
    deadline: datetime | None = None
    is_completed: bool | None = None


class NoteResponse(BaseModel):
    """Esquema de respuesta devuelto al cliente."""

    id: int
    title: str
    content: str
    deadline: datetime
    is_completed: bool

    # Configuración para permitir la conversión desde modelos ORM
    model_config = {"from_attributes": True}


class NoteInDB(NoteResponse):
    """Esquema interno que incluye campos de base de datos (extiende NoteResponse)."""
    pass
