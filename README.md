# Modulo 2 — Gestión de Notas con FastAPI

Este proyecto es una API REST robusta construida con **FastAPI**, **SQLAlchemy (Async)** y **SQLite**, diseñada para gestionar una lista de notas o tareas con fechas de entrega (deadlines).

## Arquitectura del Proyecto

Se ha implementado una arquitectura en capas siguiendo los principios **SOLID**, garantizando un código mantenible, testeable y escalable.

```
api/
├── main.py                # Punto de entrada de la aplicación y configuración de FastAPI.
├── api/                   # Lógica de transporte (HTTP) y rutas.
├── core/                  # Configuraciones globales (Pydantic Settings).
├── db/                    # Infraestructura de la base de datos (Motor async).
├── models/                # Definición de entidades ORM (SQLAlchemy).
├── repositories/          # Capa de Acceso a Datos (Patrón Repository).
├── services/              # Capa de Lógica de Negocio (Patrón Service).
└── schemas/               # Modelos de validación (Pydantic).
tests/
└── test_python.py         # Script de pruebas de integración automáticas.
```

Para más detalles sobre la organización interna, consulta el [README de api/](api/README.md) y el [README de tests/](tests/README.md).

## Elección de Tecnologías y Justificación

1.  **FastAPI**: Seleccionado por su alto rendimiento, soporte nativo para `async/await` y validación automática.
2.  **SQLite (vía aiosqlite)**: Se eligió SQLite por su sencillez de despliegue y portabilidad perfecta. Al utilizar el driver `aiosqlite`, mantenemos toda la aplicación **asíncrona** de principio a fin, evitando bloqueos en el bucle de eventos.
3.  **SQLAlchemy 2.0**: El estándar de la industria para ORM en Python. Su nueva versión 2.0 ofrece una sintaxis más clara y un soporte asíncrono excepcional.
4.  **UV (Gestor de Paquetes)**: Se utiliza `uv` en lugar de `pip` o `poetry` por ser significativamente más rápido (escrito en Rust), gestionar versiones de Python automáticamente y garantizar instalaciones deterministas mediante `uv.lock`.

## Instalación y Configuración

El proyecto utiliza `uv` para una gestión de dependencias eficiente.

1.  **Clonar el repositorio e instalar dependencias:**
    ```bash
    uv sync --extra dev
    ```

2.  **Configurar variables de entorno:**
    Crea un archivo `.env` para personalizar la configuración si es necesario:
    ```env
    # El sistema utiliza SQLite por defecto
    DB_ENGINE=sqlite
    ```

## Ejecución del Programa

Para iniciar el servidor de desarrollo:

```bash
uv run fastapi dev api/main.py
```

- **Documentación Interactiva (Swagger)**: `http://127.0.0.1:8000/docs`
- **Documentación Alternativa (Redoc)**: `http://127.0.0.1:8000/redoc`

---

## Pruebas de Integración

Se incluye un script que valida 15 escenarios clave del sistema.

**Para ejecutar las pruebas:**
1. Inicia el servidor (puerto 8000).
2. Ejecuta:
   ```bash
   uv run python tests/test_python.py
   ```

---
*Desarrollado como parte del Módulo 2 - Programación Avanzada.*
