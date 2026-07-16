# ResumeAI

Tienda de **libros generados por RPA + IA** construida sobre un núcleo transaccional
que cumple la prueba técnica (idempotencia, procesamiento asíncrono, WebSocket en tiempo
real, resumen con OpenAI y RPA con Playwright).

- **Backend:** FastAPI hexagonal · PostgreSQL · Redis (arq + pub/sub)
- **Frontends:** React + MUI — Admin y Tienda
- **Infra:** Nginx (balanceador, 3 réplicas) · Docker Compose

Ver [Arquitectura](architecture.md), [Decisiones](decisions.md) y [Cómo correr](running.md).
