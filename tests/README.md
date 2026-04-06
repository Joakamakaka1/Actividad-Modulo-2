# Pruebas de Software (`tests/`)

Esta carpeta está dedicada a la validación del funcionamiento correcto y de la estabilidad de la API.

## Contenido

- **`test_python.py`**: Script de pruebas de integración exhaustivas y automáticas (15 aserciones) que utiliza la librería de sincronización sencilla `requests`.

## Cómo Ejecutar las Pruebas

Para garantizar que todos los cambios mantienen la integridad del sistema en su arquitectura final Dockerizada, sigue estos pasos:

1. **Asegúrate de que tus contenedores Docker estén corriendo**:
   El proyecto completo (API + Base de Datos PostgreSQL) debe estar desplegado usando:
   ```bash
   docker-compose up -d
   ```
   *Nota: Las pruebas apuntan por defecto a `http://127.0.0.1:8080/api/v1` asumiendo que tu contenedor API de Docker está mapeado al puerto 8080 de tu sistema.*

2. **Ejecuta el script de pruebas nativamente en tu terminal (Requiere uv)**:
   ```bash
   uv run python tests/test_python.py
   ```

## Lo que se valida (Reglas de la Rúbrica)

El script de pruebas realiza verificaciones automáticas paso por paso cubriendo la totalidad de exigencias del entregable:
- **Salud del Ecosistema**: Conectividad de la aplicación API remota hacia la Base de Datos PostgreSQL hospedada en la red dockerizada.
- **Operaciones CRUD Completas**: 
  - Listado de la entidad.
  - Recuperación de una entidad por su ID.
  - Creación de recursos (POST).
  - Eliminación.
- **Manejo Estricto de Errores Controlados**: 
  - Verificación de código **HTTP 404 Not Found** al consultar recursos inexistentes.
  - Verificación dinámica de **HTTP 400 Bad Request** al violar exigencias de tipos de datos, validación estructural o al incumplir las reglas de negocio (como intentar poner un *deadline* en el pasado). 
