"""
test_python.py — Pruebas de integración para la API de Notas.

Instrucciones:
    1. Arrancar el servidor: uv run fastapi dev api/main.py
    2. Ejecutar este script: uv run python tests/test_python.py
"""

import sys
from datetime import datetime, timedelta, timezone

import requests

# Configuración de URLs para las pruebas
BASE_URL = "http://127.0.0.1:8000/api/v1"
NOTES_URL = f"{BASE_URL}/notes"

# Colores para salida en terminal
PASS = "\033[92m[PASS]\033[0m"
FAIL = "\033[91m[FAIL]\033[0m"

failures = 0


def check(condition: bool, description: str) -> None:
    """Verifica una condición e imprime el resultado."""
    global failures
    if condition:
        print(f"{PASS} {description}")
    else:
        print(f"{FAIL} {description}")
        failures += 1


# ---------------------------------------------------------------------------
# 1. Pruebas de Salud (Health)
# ---------------------------------------------------------------------------
print("\n--- Salud (Health) ---")
r = requests.get(f"{BASE_URL}/health/")
check(r.status_code == 200, "GET /health/ devuelve 200")
check(r.json().get("status") == "ok", "El estado de salud es 'ok'")

r = requests.get(f"{BASE_URL}/health/db")
check(r.status_code == 200, "GET /health/db devuelve 200")
check(r.json().get("database") == "conectada", "La base de datos está conectada")

# ---------------------------------------------------------------------------
# 2. Creación de una nota válida
# ---------------------------------------------------------------------------
print("\n--- Crear nota ---")
future = (datetime.now(timezone.utc) + timedelta(days=7)).isoformat()
payload = {
    "title": "Mi primera tarea",
    "content": "Estudiar FastAPI",
    "deadline": future,
}
r = requests.post(NOTES_URL + "/", json=payload)
check(r.status_code == 201, "POST /notes/ devuelve 201")
note_id = r.json().get("id")
check(isinstance(note_id, int), f"Nota creada con id={note_id}")
check(r.json().get("is_completed") is False, "La nueva nota no está completada")

# ---------------------------------------------------------------------------
# 3. Obtención de la nota creada
# ---------------------------------------------------------------------------
print("\n--- Obtener nota ---")
r = requests.get(f"{NOTES_URL}/{note_id}")
check(r.status_code == 200, f"GET /notes/{note_id} devuelve 200")
check(r.json().get("title") == "Mi primera tarea", "El título de la nota coincide")

# ---------------------------------------------------------------------------
# 4. Marcar nota como completada
# ---------------------------------------------------------------------------
print("\n--- Completar nota ---")
r = requests.put(f"{NOTES_URL}/{note_id}/complete")
check(r.status_code == 200, f"PUT /notes/{note_id}/complete devuelve 200")
check(r.json().get("is_completed") is True, "La nota ahora está completada")

# ---------------------------------------------------------------------------
# 5. Obtener una nota inexistente → 404
# ---------------------------------------------------------------------------
print("\n--- Obtener nota inexistente ---")
r = requests.get(f"{NOTES_URL}/99999")
check(r.status_code == 404, "GET /notes/99999 devuelve 404")

# ---------------------------------------------------------------------------
# 6. Crear nota con fecha PASADA → 422 error de validación
# ---------------------------------------------------------------------------
print("\n--- Validación: deadline pasado ---")
past = (datetime.now(timezone.utc) - timedelta(days=1)).isoformat()
r = requests.post(
    NOTES_URL + "/", json={"title": "Expirada", "content": "YA", "deadline": past}
)
check(r.status_code == 422, "POST /notes/ con deadline pasado devuelve 422")

# ---------------------------------------------------------------------------
# 7. Crear nota con campos faltantes → 422
# ---------------------------------------------------------------------------
print("\n--- Validación: campos faltantes ---")
r = requests.post(NOTES_URL + "/", json={"title": "Sin deadline"})
check(r.status_code == 422, "POST /notes/ con campos faltantes devuelve 422")

# ---------------------------------------------------------------------------
# 8. Listado de notas expiradas
# ---------------------------------------------------------------------------
print("\n--- Notas expiradas ---")
r = requests.get(f"{NOTES_URL}/expired")
check(r.status_code == 200, "GET /notes/expired devuelve 200")
check(isinstance(r.json(), list), "La respuesta es una lista")

# ---------------------------------------------------------------------------
# Resumen Final
# ---------------------------------------------------------------------------
print(f"\n{'=' * 40}")
total = 15  # Total de aserciones realizadas
passed = total - failures
print(f"Resultado: {passed}/{total} pasadas, {failures} fallidas.")
if failures:
    sys.exit(1)
