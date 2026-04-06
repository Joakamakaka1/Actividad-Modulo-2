# Estructura del Código Fuente (`api/`)

Esta carpeta contiene el núcleo de la aplicación Backend. La organización sigue una arquitectura en capas para separar responsabilidades y facilitar el mantenimiento.

## Organización de Paquetes

- **`api/`**: Contiene la lógica relacionada con el transporte (HTTP).
  - **`v1/`**: Versionamiento de la API.
  - **`endpoints/`**: Definición de rutas y controladores de FastAPI.
  - **`deps.py`**: Proveedores de dependencias (Inyección de Dependencias).
- **`core/`**: Configuraciones globales y constantes del sistema.
- **`db/`**: Infraestructura de la base de datos (Motor SQLAlchemy, sesiones async).
- **`models/`**: Definición de entidades ORM (Tablas de base de datos).
- **`schemas/`**: Modelos de validación de datos (Pydantic) para entrada y salida.
- **`repositories/`**: Capa de persistencia. Encapsula todas las consultas a la base de datos.
- **`services/`**: Capa de servicios. Contiene la lógica de negocio y coordina el uso de los repositorios.
- **`main.py`**: Punto de entrada de la aplicación. Configura FastAPI y carga los endpoints.

## Patrones Utilizados

- **Repository Pattern**: Aísla la lógica de acceso a datos, permitiendo que el resto de la aplicación no dependa de los detalles del ORM.
- **Service Pattern**: Centraliza las reglas de negocio, validaciones y transformaciones de datos.
- **Dependency Injection**: Utilizado nativamente por FastAPI para proporcionar sesiones de DB y servicios a los endpoints.

## Despliegue con Docker

El proyecto está diseñado para ejecutarse en contenedores siguiendo los requisitos académicos:
- Un contenedor con la aplicación FastAPI (construido desde el `Dockerfile`).
- Un contenedor con la base de datos **PostgreSQL**.
- Comunicación a través de una red compartida internamente en Docker.
- Volumen configurado para persistencia de la base de datos PostgreSQL.

### Requisitos Previos

- Tener instalados **Docker** y **Docker Compose**.

### Variables de Entorno

Puedes configurar el proyecto creando un archivo `.env` o pasando variables de entorno. Las principales son:
- `DATABASE_URL`: URL completa de conexión a la base de datos (`postgresql+asyncpg://user:password@host:port/db_name`).
- `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`: Variables utilizadas por el contenedor de la BD para inicializarse.

### Cómo ejecutar

Para levantar toda la infraestructura:
```bash
docker-compose up -d --build
```

La API estará disponible en `http://localhost:8080`.

Para detener y eliminar los contenedores (preservando el volumen de datos):
```bash
docker-compose down
```
