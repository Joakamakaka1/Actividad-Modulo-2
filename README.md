# Modulo 2 — Gestión de Notas con FastAPI

API REST construida con **FastAPI**, **SQLAlchemy 2.0 (Async)** y **PostgreSQL**, desplegada con **Docker Compose**. Gestiona una lista de notas/tareas con fechas de entrega (deadlines).

## Arquitectura del Proyecto

Se ha implementado una arquitectura en capas siguiendo los principios **SOLID**, garantizando un código mantenible, testeable y escalable.

```
├── Dockerfile                 # Imagen de la aplicación FastAPI
├── docker-compose.yml         # Orquestación de servicios (API + PostgreSQL)
├── .env.example               # Plantilla de variables de entorno
├── .dockerignore              # Archivos excluidos de la imagen Docker
├── pyproject.toml             # Dependencias del proyecto (gestionadas con uv)
├── api/
│   ├── main.py                # Punto de entrada, logging y exception handlers
│   ├── api/                   # Rutas HTTP (endpoints CRUD)
│   ├── core/                  # Configuración global y excepciones personalizadas
│   ├── db/                    # Motor async de SQLAlchemy (asyncpg)
│   ├── models/                # Entidades ORM (tablas PostgreSQL)
│   ├── repositories/          # Capa de acceso a datos (Patrón Repository)
│   ├── services/              # Lógica de negocio (Patrón Service)
│   └── schemas/               # Modelos de validación (Pydantic)
└── tests/
    └── test_python.py         # 15 pruebas de integración automáticas
```

Para más detalles sobre la organización interna, consulta el [README de api/](api/README.md) y el [README de tests/](tests/README.md).

## Tecnologías

| Tecnología | Justificación |
|---|---|
| **FastAPI** | Alto rendimiento, soporte nativo `async/await` y validación automática |
| **PostgreSQL 15** | Base de datos relacional robusta, desplegada en contenedor |
| **SQLAlchemy 2.0 + asyncpg** | ORM asíncrono de principio a fin, sin bloqueos en el event loop |
| **Docker + Docker Compose** | Orquestación reproducible de servicios con red y volúmenes dedicados |
| **uv** | Gestor de paquetes ultrarrápido (Rust), instalaciones deterministas con `uv.lock` |

## Requisitos Previos

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) instalado.
- (Opcional) [uv](https://docs.astral.sh/uv/) si deseas ejecutar los tests desde tu máquina local.

## Configuración

### 1. Clonar el repositorio

```bash
git clone https://github.com/Joakamakaka1/Actividad-Modulo-2.git
cd Actividad-Modulo-2
```

### 2. Configurar variables de entorno

Copia la plantilla y personaliza las credenciales:

```bash
cp .env.example .env
```

Contenido del `.env`:

```env
DB_ENGINE=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=notes_db
DATABASE_URL=postgresql+asyncpg://${POSTGRES_USER}:${POSTGRES_PASSWORD}@localhost:5432/${POSTGRES_DB}
```

> **Nota:** La variable `DATABASE_URL` del `.env` se usa solo para desarrollo local nativo. Dentro de Docker Compose, la URL se inyecta automáticamente apuntando al contenedor `db`.

## Despliegue con Docker Compose

### Levantar el proyecto completo

Este único comando construye la imagen de la API y levanta ambos contenedores:

```bash
docker-compose up -d --build
```

### Verificar que los contenedores están corriendo

```bash
docker-compose ps
```

Deberías ver dos contenedores activos:

| Contenedor | Imagen | Puerto expuesto |
|---|---|---|
| `notas_api` | Construida desde `Dockerfile` | `8080` → `8000` |
| `notas_postgres` | `postgres:15-alpine` | `5432` → `5432` |

### Acceder a la API

- **Swagger UI (Documentación interactiva):** [http://localhost:8080/docs](http://localhost:8080/docs)
- **ReDoc (Documentación alternativa):** [http://localhost:8080/redoc](http://localhost:8080/redoc)

### Ver logs en tiempo real

```bash
docker-compose logs -f api
```

### Detener los contenedores

Preservando los datos de la base de datos:

```bash
docker-compose down
```

Eliminando también el volumen de datos (reinicio completo):

```bash
docker-compose down -v
```

## Infraestructura Docker

El archivo `docker-compose.yml` define la siguiente arquitectura:

```
┌─────────────────────────────────────────────────┐
│              notas_postgres_network              │
│                                                  │
│   ┌──────────────┐       ┌───────────────────┐   │
│   │  notas_api   │──────▶│  notas_postgres   │   │
│   │  (FastAPI)   │       │  (PostgreSQL 15)  │   │
│   │  :8000       │       │  :5432            │   │
│   └──────┬───────┘       └────────┬──────────┘   │
│          │                        │              │
└──────────┼────────────────────────┼──────────────┘
           │                        │
      host:8080                volumen:
                          notas_postgres_volume
```

- **Red personalizada** (`notas_postgres_network`): Los contenedores se comunican internamente por nombre (`db`).
- **Volumen nombrado** (`notas_postgres_volume`): Persiste los datos de PostgreSQL entre reinicios.
- **Healthcheck**: El servicio `api` espera a que PostgreSQL esté listo antes de arrancar (`depends_on` + `service_healthy`).

## Endpoints de la API

| Método | Ruta | Descripción | Errores |
|---|---|---|---|
| `GET` | `/api/v1/notes/` | Lista todas las notas | — |
| `GET` | `/api/v1/notes/{id}` | Obtiene una nota por ID | `404` |
| `POST` | `/api/v1/notes/` | Crea una nueva nota | `400` |
| `DELETE` | `/api/v1/notes/{id}` | Elimina una nota | `404` |
| `PUT` | `/api/v1/notes/{id}/complete` | Marca una nota como completada | `404` |
| `GET` | `/api/v1/notes/expired` | Lista notas con deadline vencido | — |
| `GET` | `/api/v1/health/` | Estado de la API | — |
| `GET` | `/api/v1/health/db` | Estado de la conexión a la BD | — |

## Pruebas de Integración

Con los contenedores Docker levantados, ejecuta las 15 pruebas automáticas:

```bash
uv run python tests/test_python.py
```

Las pruebas validan:
- Conectividad API ↔ Base de Datos
- Operaciones CRUD completas (crear, leer, listar, eliminar)
- Control de errores **HTTP 404** (recurso inexistente)
- Control de errores **HTTP 400** (validación de campos y reglas de negocio)

---
*Desarrollado como parte del Módulo 2 - Programación Avanzada.*
