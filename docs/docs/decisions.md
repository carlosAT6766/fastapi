# Decisiones técnicas

| Decisión | Elección | Por qué |
|----------|----------|---------|
| Framework | FastAPI | Async nativo, OpenAPI automático |
| Arquitectura | Hexagonal | Dominio testeable, adaptadores intercambiables |
| Base de datos | PostgreSQL + SQLAlchemy 2.0 async | Robusta, transaccional (idempotencia atómica) |
| Cola + worker | Redis + arq | Un servicio cubre cola **y** pub/sub del WebSocket |
| Tiempo real | WebSocket + Redis pub/sub | Escala horizontal sin estado en la app |
| IA | OpenAI `gpt-4o-mini` + fallback fake | La demo funciona sin API key |
| RPA | Playwright | Moderno, imagen oficial en Docker |
| Idempotencia | Header `Idempotency-Key` + UNIQUE en Postgres | Evita ventas duplicadas por doble click |
| Auth | JWT HS256 (bcrypt) | Stateless, no requiere sticky sessions |
| Balanceador | Nginx round-robin, 3 réplicas | Demuestra alta concurrencia |
| Frontend | React + MUI | Dos apps (Admin + Tienda) desde el diseño |

## Notas de implementación

- `bcrypt` fijado `<4.1` por incompatibilidad con passlib 1.7.
- Wikipedia REST API exige `User-Agent` (si no, 403).
- El `user_id` de una venta se toma del token, no del body (anti-suplantación).
