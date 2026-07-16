# ResumeAI — Frontend Admin

App de administración (React 18 + Vite + MUI 5) del proyecto ResumeAI. Recrea el
handoff de diseño (Plus Jakarta Sans, primary `#4f46e5`, radius 10) y se conecta al
backend FastAPI real.

## Arranque

```bash
cp .env.example .env      # ajusta VITE_API_URL (default http://localhost:8080)
npm install
npm run dev               # http://localhost:5173
```

## Scripts

- `npm run dev` — servidor de desarrollo Vite.
- `npm run build` — bundle de producción en `dist/`.
- `npm run lint` — ESLint.
- `npm run format` — Prettier.

## Docker

```bash
docker build -t resumeai-admin --build-arg VITE_API_URL=http://localhost:8080 .
docker run -p 8081:80 resumeai-admin
```

Build multi-stage: compila con Node y sirve `dist/` con nginx alpine (SPA fallback).

## Estructura

```
src/
  api/         cliente fetch + endpoints (auth, books, sales, users, settings, websocket) + mappers
  components/  reutilizables (DataTable, StatCard, SelectField, RowActionsMenu, Toasts, PageHeader)
  context/     AuthContext (JWT)
  features/    auth, shell (sidebar + orquestador), books, sales, config, users, print
  hooks/       useToasts
  utils/       formatters
  theme.js     tema MUI + sx del contrato de diseño
  constants.js opciones de select + metadata de estados
```

## Wiring al backend

- **Login** → `POST /auth/login`, guarda el JWT (localStorage), se adjunta como `Authorization: Bearer`.
- **Crear libro** → `POST /transactions/async-process` (`tipo:"libro"`, `titulo`, `precio`, `estilo`).
- **Vender** → `POST /transactions/create` (`tipo:"venta"`, `monto`, `libro_id`) con header `Idempotency-Key` (UUID).
- **Estado en vivo** → WebSocket `/transactions/stream` (token por subprotocol) → actualiza tabla + toasts.
- **Listas** → `GET /books`, `GET /sales`, `GET/POST/PATCH/DELETE /users`, `GET/PUT /settings`.
- **PDF** → `window.print()` sobre `#printArea` oculto con `@media print`.

> Los endpoints que aún no existan degradan de forma silenciosa (se integran en Ola 2).
