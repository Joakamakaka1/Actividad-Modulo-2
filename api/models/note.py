from datetime import datetime
from sqlalchemy import Boolean, DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from api.db.base import Base


class Note(Base):
    """Modelo ORM que representa una nota o tarea en la base de datos."""

    __tablename__ = "notes"

    # Identificador único de la nota
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    
    # Título corto de la nota
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    
    # Contenido detallado de la nota
    content: Mapped[str] = mapped_column(Text, nullable=False)
    
    # Fecha límite de cumplimiento (con zona horaria)
    deadline: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    
    # Estado de cumplimiento de la nota
    is_completed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
