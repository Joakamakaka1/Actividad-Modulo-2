from datetime import datetime, timezone
from api.models.note import Note
from api.schemas.note import NoteCreate
from api.repositories.note_repository import NoteRepository

# Lista de palabras no permitidas (saneamiento simple)
_BAD_WORDS: frozenset[str] = frozenset({"spam", "ofensivo", "basura"})

class NoteService:
    """
    Gestiona la lógica de negocio y coordina las llamadas al Repositorio.
    Implementa reglas de validación y transformación de datos.
    """
    def __init__(self, repository: NoteRepository) -> None:
        self._repo = repository

    async def create_note(self, data: NoteCreate) -> Note:
        """
        Orquestra la creación de una nota personalziada.
        Valida el deadline y sanea el contenido.
        """
        self._validate_deadline(data.deadline)
        sanitized_title = self._sanitize_text(data.title)
        sanitized_content = self._sanitize_text(data.content)

        note = Note(
            title=sanitized_title,
            content=sanitized_content,
            deadline=data.deadline,
            is_completed=False,
        )
        return await self._repo.create(note)

    async def get_note(self, note_id: int) -> Note | None:
        """Obtiene una nota delegando la búsqueda al repositorio."""
        return await self._repo.get_by_id(note_id)

    async def complete_note(self, note_id: int) -> Note | None:
        """Lógica para marcar una nota como completada."""
        note = await self._repo.get_by_id(note_id)
        if not note:
            return None
        note.is_completed = True
        return await self._repo.update(note)

    async def get_expired_notes(self) -> list[Note]:
        """Obtiene notas expiradas utilizando la fecha/hora actual en UTC."""
        now = datetime.now(timezone.utc)
        return await self._repo.list_expired(now)

    @staticmethod
    def _validate_deadline(deadline: datetime) -> None:
        """Valida que la fecha límite no sea en el pasado."""
        now = datetime.now(timezone.utc)
        # Aseguramos que la fecha tenga información de zona horaria para comparar
        if deadline.tzinfo is None:
            deadline = deadline.replace(tzinfo=timezone.utc)
        if deadline <= now:
            raise ValueError("El deadline debe ser una fecha futura.")

    @staticmethod
    def _sanitize_text(text: str) -> str:
        """Elimina palabras prohibidas del texto (sin distinguir mayúsculas)."""
        words = text.split()
        cleaned = [w for w in words if w.lower() not in _BAD_WORDS]
        return " ".join(cleaned)
