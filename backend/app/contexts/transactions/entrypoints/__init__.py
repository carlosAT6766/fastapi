"""Transactions core entrypoints (HTTP + WebSocket).

Contract (paths are fixed):
  POST /transactions/create         -> idempotent sale create (Idempotency-Key header)
  POST /transactions/async-process  -> enqueue a BOOK generation job (arq)
  GET  /transactions/stream         -> WebSocket, token via subprotocol, Redis fan-out
  GET  /books?estado=               -> PUBLIC list of published books
  GET  /sales                       -> user sales list + metrics
"""

from contextlib import suppress
from datetime import datetime

from fastapi import (
    APIRouter,
    Depends,
    Header,
    HTTPException,
    Request,
    Response,
    status,
)
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.websockets import WebSocket, WebSocketDisconnect

from app.shared.db import get_session
from app.shared.models import KIND_SALE, Transaction
from app.shared.security import decode_token, get_current_user

from ..application.use_cases import (
    GetTransactionsSnapshot,
    ListPublishedBooks,
    ListUserSales,
    PublishBook,
    RegisterSale,
    RequestBookGeneration,
    UpdateBook,
)
from ..domain.errors import BookNotFoundError, BookNotSellableError
from ..domain.events import EVENT_SNAPSHOT, transaction_event
from ..infrastructure.event_publisher import RedisEventPublisher
from ..infrastructure.repository import SqlAlchemyTransactionRepository
from ..infrastructure.ws_stream import (
    extract_token,
    forward_events,
    forward_storefront_events,
)

router = APIRouter(tags=["transactions"])

WS_JOB_NAME = "generate_book"
WS_POLICY_VIOLATION = status.WS_1008_POLICY_VIOLATION


class SaleCreate(BaseModel):
    monto: float = Field(gt=0)
    tipo: str = KIND_SALE
    libro_id: int


class BookCreate(BaseModel):
    titulo: str = Field(min_length=1)
    precio: float = Field(gt=0)
    estilo: str = Field(min_length=1)


class TransactionOut(BaseModel):
    id: int
    user_id: int
    tipo: str
    estado: str
    sub_estado: str | None = None
    titulo: str | None = None
    precio: float | None = None
    estilo: str | None = None
    resumen: str | None = None
    monto: float | None = None
    libro_id: int | None = None
    libro_titulo: str | None = None
    created_at: datetime | None = None

    model_config = {"from_attributes": True}


class BookUpdate(BaseModel):
    titulo: str = Field(min_length=1)
    precio: float = Field(gt=0)
    estilo: str = Field(min_length=1)
    resumen: str | None = None


class BookOut(BaseModel):
    id: int
    titulo: str | None = None
    precio: float | None = None
    estilo: str | None = None
    resumen: str | None = None
    publicado: bool = False
    created_at: datetime | None = None

    model_config = {"from_attributes": True}


class SalesResponse(BaseModel):
    sales: list[TransactionOut]
    metrics: dict[str, float]


def get_repository(
    session: AsyncSession = Depends(get_session),
) -> SqlAlchemyTransactionRepository:
    return SqlAlchemyTransactionRepository(session)


@router.post("/transactions/create", response_model=TransactionOut)
async def create_transaction(
    payload: SaleCreate,
    response: Response,
    idempotency_key: str | None = Header(default=None, alias="Idempotency-Key"),
    user=Depends(get_current_user),
    repository: SqlAlchemyTransactionRepository = Depends(get_repository),
) -> Transaction:
    """Idempotently register a sale. Repeats return the original transaction (200)."""
    if not idempotency_key:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Idempotency-Key header is required")

    use_case = RegisterSale(repository, RedisEventPublisher())
    try:
        sale, created = await use_case.execute(
            user_id=user.id,
            monto=payload.monto,
            libro_id=payload.libro_id,
            idempotency_key=idempotency_key,
        )
    except BookNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
    except BookNotSellableError as exc:
        raise HTTPException(status.HTTP_409_CONFLICT, str(exc)) from exc

    response.status_code = status.HTTP_201_CREATED if created else status.HTTP_200_OK
    return sale


@router.post(
    "/transactions/async-process",
    response_model=TransactionOut,
    status_code=status.HTTP_202_ACCEPTED,
)
async def async_process(
    payload: BookCreate,
    request: Request,
    user=Depends(get_current_user),
    repository: SqlAlchemyTransactionRepository = Depends(get_repository),
) -> Transaction:
    """Create a pending book and enqueue its generation on the arq worker."""
    use_case = RequestBookGeneration(repository, RedisEventPublisher())
    book = await use_case.execute(
        user_id=user.id, titulo=payload.titulo, precio=payload.precio, estilo=payload.estilo
    )
    await request.app.state.arq.enqueue_job(WS_JOB_NAME, book.id)
    return book


@router.get("/books", response_model=list[BookOut])
async def list_books(
    estado: str | None = None,
    repository: SqlAlchemyTransactionRepository = Depends(get_repository),
) -> list[Transaction]:
    """Public storefront listing of published books (no auth)."""
    return await ListPublishedBooks(repository).execute(estado=estado)


@router.patch("/books/{book_id}", response_model=BookOut)
async def update_book(
    book_id: int,
    payload: BookUpdate,
    user=Depends(get_current_user),
    repository: SqlAlchemyTransactionRepository = Depends(get_repository),
) -> Transaction:
    """Edit an existing book's title/price/style/summary."""
    use_case = UpdateBook(repository, RedisEventPublisher())
    try:
        return await use_case.execute(
            book_id=book_id,
            titulo=payload.titulo,
            precio=payload.precio,
            estilo=payload.estilo,
            resumen=payload.resumen,
        )
    except BookNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc


@router.post("/books/{book_id}/publish", response_model=BookOut)
async def publish_book(
    book_id: int,
    user=Depends(get_current_user),
    repository: SqlAlchemyTransactionRepository = Depends(get_repository),
) -> Transaction:
    """Make a ready book visible in the storefront."""
    use_case = PublishBook(repository, RedisEventPublisher())
    try:
        return await use_case.execute(book_id=book_id)
    except BookNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
    except BookNotSellableError as exc:
        raise HTTPException(status.HTTP_409_CONFLICT, str(exc)) from exc


@router.get("/sales", response_model=SalesResponse)
async def list_sales(
    user=Depends(get_current_user),
    repository: SqlAlchemyTransactionRepository = Depends(get_repository),
) -> SalesResponse:
    """List the user's sales plus aggregate metrics."""
    sales, metrics = await ListUserSales(repository).execute(user_id=user.id)
    return SalesResponse(
        sales=[TransactionOut.model_validate(sale) for sale in sales], metrics=metrics
    )


@router.websocket("/transactions/stream")
async def stream(
    websocket: WebSocket,
    session: AsyncSession = Depends(get_session),
) -> None:
    """Real-time transaction stream, authenticated via subprotocol JWT."""
    token = extract_token(websocket)
    if not token:
        await websocket.close(code=WS_POLICY_VIOLATION)
        return
    try:
        user_id = decode_token(token)
    except HTTPException:
        await websocket.close(code=WS_POLICY_VIOLATION)
        return

    await websocket.accept(subprotocol=token)

    repository = SqlAlchemyTransactionRepository(session)
    snapshot = await GetTransactionsSnapshot(repository).execute(user_id=user_id)
    for transaction in snapshot:
        await websocket.send_json(transaction_event(transaction, EVENT_SNAPSHOT))

    with suppress(WebSocketDisconnect):
        await forward_events(websocket, user_id)


@router.websocket("/storefront/stream")
async def storefront_stream(websocket: WebSocket) -> None:
    """Public real-time catalog stream (no auth): pushes catalog changes such as
    a newly published book so the storefront updates without a reload."""
    await websocket.accept()
    with suppress(WebSocketDisconnect):
        await forward_storefront_events(websocket)
