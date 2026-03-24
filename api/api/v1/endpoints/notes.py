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
    """
    Crea una nueva nota.
    El 'deadline' debe ser una fecha futura.
    Se aplican reglas de saneamiento de texto.
    """
    note = await service.create_note(payload)
    return NoteResponse.model_validate(note)


@router.get("/expired", response_model=list[NoteResponse])
async def get_expired_notes(
    service: NoteService = Depends(_get_service),
) -> list[NoteResponse]:
    """Lista todas las notas cuyo plazo ha expirado y no han sido completadas."""
    notes = await service.get_expired_notes()
    return [NoteResponse.model_validate(n) for n in notes]


@router.get("/{note_id}", response_model=NoteResponse)
async def get_note(
    note_id: int,
    service: NoteService = Depends(_get_service),
) -> NoteResponse:
    """Obtiene una nota específica por su ID."""
    note = await service.get_note(note_id)
    return NoteResponse.model_validate(note)


@router.put("/{note_id}/complete", response_model=NoteResponse)
async def complete_note(
    note_id: int,
    service: NoteService = Depends(_get_service),
) -> NoteResponse:
    """Marca una nota como completada."""
    note = await service.complete_note(note_id)
    return NoteResponse.model_validate(note)
