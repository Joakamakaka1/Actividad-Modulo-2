from typing import Any
from fastapi import HTTPException, status

class BaseAPIException(HTTPException):
    """Base class for API exceptions."""
    def __init__(self, status_code: int, detail: Any):
        super().__init__(status_code=status_code, detail=detail)

class NoteNotFoundException(BaseAPIException):
    """404 — La nota solicitada no existe."""
    def __init__(self, detail: Any = "Nota no encontrada."):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

class InvalidDeadlineException(BaseAPIException):
    """422 — El deadline proporcionado no es válido."""
    def __init__(self, detail: Any = "El deadline debe ser una fecha futura."):
        super().__init__(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=detail)

class BadRequestException(BaseAPIException):
    """400 — Petición errónea por lógica de negocio o datos incorrectos."""
    def __init__(self, detail: Any = "Petición incorrecta."):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)
