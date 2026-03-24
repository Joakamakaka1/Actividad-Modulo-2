# Pruebas de Software (`tests/`)

Esta carpeta está dedicada a la validación del funcionamiento correcto de la API.

## Contenido

- **`test_python.py`**: Script de pruebas de integración que utiliza la librería `requests`.

## Cómo Ejecutar las Pruebas

Para garantizar que todos los cambios mantienen la integridad del sistema, sigue estos pasos:

1. **Asegúrate de que el servidor esté activo**:
   ```bash
   uv run fastapi dev api/main.py
   ```

2. **Ejecuta el script de pruebas**:
   ```bash
   uv run python tests/test_python.py
   ```

## Lo que se valida

El script realiza 15 verificaciones automáticas que cubren:
- Conectividad de la API y la Base de Datos.
- Creación de notas con validación de fechas futuras.
- Saneamiento de texto (eliminación de spam/palabras ofensivas).
- Operaciones CRUD (Lectura, Actualización a completado).
- Manejo de errores (404 Nota no encontrada, 422 Datos inválidos).
