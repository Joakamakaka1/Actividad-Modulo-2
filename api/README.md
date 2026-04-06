# Estructura del Código Fuente (`api/`)

Esta carpeta contiene el núcleo de la aplicación Backend. La organización sigue una arquitectura en capas para separar responsabilidades y facilitar el mantenimiento.

## Organización de Paquetes

- **`api/`**: Contiene la lógica relacionada con el transporte (HTTP).
  - **`v1/`**: Versionamiento de la API.
  - **`endpoints/`**: Definición de rutas (CRUD completo: listar, obtener, crear, eliminar) y controladores de FastAPI.
  - **`deps.py`**: Proveedores de dependencias (Inyección de Dependencias).
- **`core/`**: Configuraciones globales y manejo de excepciones personalizadas para devolver HTTP 400 y 404 de manera consistente.
- **`db/`**: Infraestructura de la base de datos (Motor SQLAlchemy, sesiones asíncronas con asyncpg).
- **`models/`**: Definición de entidades ORM (Tablas de base de datos en PostgreSQL).
- **`schemas/`**: Modelos de validación de datos (Pydantic) para entrada y salida.
- **`repositories/`**: Capa de persistencia. Encapsula todas las operaciones de la DB.
- **`services/`**: Capa de servicios. Contiene la lógica de negocio y validaciones.
- **`main.py`**: Punto de entrada de la aplicación. Configura middlewares, logging de trazabilidad y excepcion handlers.

## Despliegue con Docker (Cumpliendo la rúbrica)

El proyecto está diseñado para ejecutarse en contenedores siguiendo los requisitos académicos de infraestructura y aislamiento:
- Servicio `api`: Contenedor con la aplicación FastAPI (construida desde un `Dockerfile` optimizado).
- Servicio `db`: Contenedor estable con la base de datos **PostgreSQL 15**.
- Comunicación ágil a través de una red compartida definida explícitamente (`notas_postgres_network`).
- Volumen nombrado ("named volume") `notas_postgres_volume` para garantizar la persistencia infinita de los datos.

### Seguridad y Variables de Entorno

El proyecto implementa prácticas seguras y carece de contraseñas *hardcodeadas* en sus archivos de manifiesto:

1. Copia el archivo `.env.example` a `.env` en la raíz de este proyecto.
2. Personaliza tus credenciales seguras (como `POSTGRES_PASSWORD`).

### Cómo ejecutar toda la infraestructura

Para levantar de cero el entorno, compilar la API y la BD por primera vez:
```bash
docker-compose up -d --build
```

La API estará automáticamente disponible y mapeada desde el contenedor huésped al puerto **8080**, tal y como solicita la rúbrica.
Revisa la Documentación Interactiva (Swagger) entrando a:
`http://localhost:8080/docs`.

### Mantenimiento
Para detener y suspender temporalmente los contenedores (preservando los datos persistentes del volumen):
```bash
docker-compose down
```
*(Cuidado)* Para destruir completamente los datos de la base de datos y reiniciar sus tablas de cero:
```bash
docker-compose down -v
```
