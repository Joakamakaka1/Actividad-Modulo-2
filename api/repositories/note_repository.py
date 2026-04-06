from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from api.models.note import Note

class NoteRepository:
    """
    Gestiona el acceso directo a la base de datos para la entidad Note.
    Aísla las consultas de SQLAlchemy del resto de la aplicación.
    """
    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def create(self, note: Note) -> Note:
        """Persiste una nueva nota en la base de datos."""
        self._db.add(note)
        await self._db.commit()
        await self._db.refresh(note)
        return note

    async def get_by_id(self, note_id: int) -> Note | None:
        """Busca una nota por su clave primaria."""
        result = await self._db.execute(select(Note).where(Note.id == note_id))
        return result.scalar_one_or_none()

    async def list_expired(self, now: datetime) -> list[Note]:
        """Obtiene las notas cuya fecha límite ha pasado y no están completadas."""
        result = await self._db.execute(
            select(Note).where(Note.deadline < now, Note.is_completed.is_(False))
        )
        return list(result.scalars().all())

    async def list(self) -> list[Note]:
        """Obtiene todas las notas de la base de datos."""
        result = await self._db.execute(select(Note))
        return list(result.scalars().all())

    async def delete(self, note: Note) -> None:
        """Elimina una nota de la base de datos."""
        await self._db.delete(note)
        await self._db.commit()

    async def update(self, note: Note) -> Note:
        """Confirma los cambios realizados en una instancia de Note."""
        await self._db.commit()
        await self._db.refresh(note)
        return note
