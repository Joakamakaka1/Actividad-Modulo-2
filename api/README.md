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
