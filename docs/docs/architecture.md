# Arquitectura

## Modelo unificado (libro = job async, venta = transacción)

Un único núcleo `Transaction` con `tipo` discrimina:

- `tipo="libro"`: se genera con RPA + IA (estados `buscando → resumiendo → listo/fallido`).
- `tipo="venta"`: operación financiera idempotente (`monto`, `libro_id`).

Esto da semántica real al payload del PDF (`user_id, monto, tipo`).

## El ciclo completo

```
Admin crea libro ─async─▶ worker: RPA Wikipedia → /assistant/summarize ─▶ libro "listo" + precio
Tienda muestra el libro ◀────────────────────────────────────────────────────┘
      │ Comprar
      ▼
POST /transactions/create (venta idempotente)
      │  WebSocket /transactions/stream (Redis pub/sub)
      ▼
Admin ve la venta en vivo
```

## Hexagonal

Cada contexto (`auth`, `transactions`, `assistant`, `settings`) se organiza en
`domain / application (puertos) / infrastructure (adaptadores) / entrypoints`.
Las dependencias apuntan hacia adentro; las entidades de dominio no conocen el ORM.

## Balanceador + tiempo real

Nginx round-robin frente a 3 réplicas. El WebSocket funciona **sin sticky sessions**:
el worker publica el cambio en un canal Redis pub/sub y cualquier réplica reenvía a sus
sockets. Un snapshot desde Postgres al conectar cubre la carrera del pub/sub.
