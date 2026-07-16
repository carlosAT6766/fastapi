# ResumeAI — Prueba Técnica Fullstack

Tienda de **libros generados por RPA + IA**, construida sobre un núcleo transaccional
que cumple literalmente la prueba técnica (transacciones idempotentes, procesamiento
asíncrono con cola + worker, WebSocket en tiempo real, resumen con OpenAI y RPA).

## Arquitectura

- **Backend:** FastAPI **hexagonal** (contextos `auth`, `transactions`, `assistant`, `settings`).
- **Base de datos:** PostgreSQL (SQLAlchemy 2.0 async, Alembic).
- **Cola + tiempo real:** Redis (arq como worker + pub/sub para el fan-out del WebSocket).
- **RPA:** Playwright (abre Wikipedia, extrae el primer párrafo, llama a `/assistant/summarize`).
- **IA:** OpenAI (`gpt-4o-mini`) con *fallback* a un resumidor fake determinista (sin API key).
- **Balanceador:** Nginx round-robin frente a 3 réplicas de la API (sin sticky sessions gracias al pub/sub).
- **Frontends:** dos apps React + MUI — **Admin** (gestión) y **Tienda** (storefront público).
- **Auth:** JWT (HS256), protege todo salvo `/auth/*`, `/health` y `GET /books`.

### El ciclo completo

```
Admin crea libro ──async──▶ worker: RPA Wikipedia → /assistant/summarize ──▶ libro "listo" + precio
                                                                                    │ publicado
Tienda muestra el libro ◀───────────────────────────────────────────────────────────┘
        │ cliente pulsa "Comprar"
        ▼
POST /transactions/create (venta, idempotente)
        │
        ▼  WebSocket /transactions/stream
Admin ve la venta en vivo (sección Ventas + toast)
```

### Mapeo con el PDF

| PDF | Implementación |
|-----|----------------|
| `POST /transactions/create` idempotente (`user_id, monto, tipo`) | Registrar una **venta** (la Tienda la envía) |
| `POST /transactions/async-process` + worker + estados | Generar un **libro** (RPA + OpenAI) |
| `GET /transactions/stream` (WebSocket) | Estado de libros en vivo + notificaciones |
| `POST /assistant/summarize` (OpenAI) | El worker resume el párrafo de Wikipedia |
| Frontend React | Admin + Tienda (MUI) |
| RPA (Playwright/Selenium) | `rpa/bot.py` con Playwright |

## Cómo correr

Requisitos: Docker + Docker Compose.

```bash
cd fastapi
docker compose up --build          # postgres, redis, api x3, worker, nginx, frontends
```

- API (vía Nginx): http://localhost:8080  ·  Swagger: http://localhost:8080/docs
- Admin: http://localhost:5173  ·  Tienda: http://localhost:5174

Credenciales demo: **admin / admin123**. La Tienda entra sola como `customer@resumeai.com`.

### RPA (bajo demanda)

```bash
docker compose run --rm rpa-bot "Inteligencia artificial"
```

### OpenAI real (opcional)

Exporta `OPENAI_API_KEY` en `backend/.env` (copia de `.env.example`). Sin key, se usa el resumidor fake.

## Colección Postman

Importa `postman/ResumeAI.postman_collection.json`. Ejecuta **Login** primero (puebla `{{token}}`),
luego Books → Sales → Assistant → Settings.

## Estructura

```
backend/          FastAPI hexagonal (app/contexts/*, app/shared/*)
frontend-admin/   React + MUI — panel de administración
frontend-tienda/  React + MUI — storefront público
rpa/              Bot Playwright (RPA)
nginx/            Config del balanceador
postman/          Colección de la API
docs/             Documentación MkDocs (arquitectura y decisiones)
```

## Convenciones

Código en inglés, Clean Code + DRY. Lint: **Ruff** (backend) y **ESLint + Prettier** (frontends).
