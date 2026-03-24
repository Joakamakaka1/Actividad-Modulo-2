from fastapi import APIRouter
from api.api.v1.endpoints import health, notes

# Enrutador principal v1
api_router = APIRouter()

# Registro de sub-enrutadores
api_router.include_router(health.router, prefix="/health", tags=["Salud (Health)"])
api_router.include_router(notes.router, prefix="/notes", tags=["Notas (Notes)"])
