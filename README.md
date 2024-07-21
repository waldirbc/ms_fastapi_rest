# Microservicio con FastAPI

## Ejecutar el proyecto

Para ejecutar el proyecto, es necesario tener instalado `docker`.

```bash
docker build -t ms_fastapi_rest .
docker run -p 8002:8000 ms_fastapi_rest
```

## Consultar la API

Para consultar la API, se puede acceder a `http://localhost:8002/docs`.

## Ejemplo de consulta

Se adjunta json insomnia de pruebas en la carpeta `insomnia`.
