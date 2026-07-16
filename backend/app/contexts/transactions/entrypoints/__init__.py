"""Transactions core entrypoints. Teammate B implements the routes below.

Contract (do not rename paths):
  POST /transactions/create         -> idempotent create (used for SALES: user_id from
                                       token, monto, tipo="venta", libro_id). Header
                                       `Idempotency-Key`. Repeat -> 200 with original.
  POST /transactions/async-process  -> enqueue a BOOK generation (tipo="libro",
                                       titulo, precio, estilo) -> arq worker.
  GET  /transactions/stream         -> WebSocket, token via subprotocol, Redis pub/sub fan-out.
  GET  /books?estado=listo          -> PUBLIC list of published books (for the storefront).
  GET  /sales                       -> sales list + metrics (total, recaudado).
"""

from fastapi import APIRouter

router = APIRouter(tags=["transactions"])


@router.get("/transactions/health")
async def transactions_health() -> dict[str, str]:
    return {"context": "transactions", "status": "stub"}
