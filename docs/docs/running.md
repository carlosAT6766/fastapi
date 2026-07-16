# Cómo correr

## Requisitos

Docker + Docker Compose.

## Levantar todo

```bash
cd fastapi
docker compose up --build
```

Servicios:

- API (vía Nginx): <http://localhost:8080> — Swagger en `/docs`
- Admin: <http://localhost:5173>
- Tienda: <http://localhost:5174>

Credenciales demo: **admin / admin123**. La Tienda entra sola como `customer@resumeai.com`.

## RPA (bajo demanda)

```bash
docker compose run --rm rpa-bot "Inteligencia artificial"
```

## OpenAI real

Copia `backend/.env.example` a `backend/.env` y define `OPENAI_API_KEY`.
Sin key, se usa el resumidor fake determinista.

## Documentación (este sitio)

```bash
cd docs
pip install mkdocs-material
mkdocs serve   # http://localhost:8000
```
