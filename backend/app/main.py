"""FastAPI application entrypoint.

Mounts one router per bounded context. This file is STABLE during parallel
development: teammates implement inside their own context package; they do not
edit main.py. The arq pool lives on app.state for enqueuing jobs.
"""

import os
from contextlib import asynccontextmanager

from arq import create_pool
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.contexts.assistant.entrypoints import router as assistant_router
from app.contexts.auth.entrypoints import router as auth_router
from app.contexts.settings.entrypoints import router as settings_router
from app.contexts.transactions.entrypoints import router as transactions_router
from app.shared.init_db import init_db
from app.shared.redis import REDIS_SETTINGS


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    app.state.arq = await create_pool(REDIS_SETTINGS)
    yield
    await app.state.arq.close()


app = FastAPI(title="ResumeAI API", version="0.1.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", tags=["meta"])
async def health() -> dict[str, str]:
    # Hostname lets Nginx round-robin be observed across replicas (X-Served-By demo).
    return {"status": "ok", "served_by": os.environ.get("HOSTNAME", "local")}


for _router in (auth_router, transactions_router, assistant_router, settings_router):
    app.include_router(_router)
