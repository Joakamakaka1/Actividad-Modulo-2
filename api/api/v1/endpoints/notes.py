import logging
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.db.session import get_db
from api.repositories.note_repository import NoteRepository
from api.services.note_service import NoteService
from api.schemas.note import NoteCreate, NoteResponse


logger = logging.getLogger(__name__)
router = APIRouter()


def _get_service(db: AsyncSession = Depends(get_db)) -> NoteService:
    """Dependencia que proporciona una instancia de NoteService."""
    repository = NoteRepository(db)
    return NoteService(repository)


@router.post("/", response_model=NoteResponse, status_code=status.HTTP_201_CREATED)
async def create_note(
    payload: NoteCreate,
    service: NoteService = Depends(_get_service),
) -> NoteResponse:
    """Crea una nueva nota."""
    logger.info(f"Intentando crear nueva nota con título: {payload.title}")
    note = await service.create_note(payload)
    logger.info(f"Nota creada exitosamente con ID: {note.id}")
    return NoteResponse.model_validate(note)


@router.get("/", response_model=list[NoteResponse])
async def list_notes(
    service: NoteService = Depends(_get_service),
) -> list[NoteResponse]:
    """Lista todas las notas."""
    logger.info("Obteniendo la lista completa de notas.")
    notes = await service.get_all_notes()
    logger.info(f"Se obtuvieron {len(notes)} notas.")
    return [NoteResponse.model_validate(n) for n in notes]


@router.get("/expired", response_model=list[NoteResponse])
async def get_expired_notes(
    service: NoteService = Depends(_get_service),
) -> list[NoteResponse]:
    """Lista notas cuyo plazo ha expirado y no se han completado."""
    logger.info("Solicitando notas expiradas.")
    notes = await service.get_expired_notes()
    return [NoteResponse.model_validate(n) for n in notes]


@router.get("/{note_id}", response_model=NoteResponse)
async def get_note(
    note_id: int,
    service: NoteService = Depends(_get_service),
) -> NoteResponse:
    """Obtiene una nota específica por su ID."""
    logger.info(f"Buscando nota con ID {note_id}")
    note = await service.get_note(note_id)
    return NoteResponse.model_validate(note)


@router.put("/{note_id}/complete", response_model=NoteResponse)
async def complete_note(
    note_id: int,
    service: NoteService = Depends(_get_service),
) -> NoteResponse:
    """Marca una nota como completada."""
    logger.info(f"Intentando marcar nota {note_id} como completada.")
    note = await service.complete_note(note_id)
    logger.info(f"Nota {note_id} marcada como completada.")
    return NoteResponse.model_validate(note)


@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_note(
    note_id: int,
    service: NoteService = Depends(_get_service),
):
    """Elimina una nota por su ID."""
    logger.info(f"Intentando eliminar la nota {note_id}")
    await service.delete_note(note_id)
    logger.info(f"Nota {note_id} eliminada exitosamente.")
