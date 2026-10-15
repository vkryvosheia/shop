# `src/api/`

Code that talks to the backend lives here: small typed functions that call
`/api/...` endpoints and return data, e.g. `getProducts(): Promise<Product[]>`.

Components import these functions instead of calling `fetch` themselves.
Use relative URLs (`/api/...`): in development, Vite forwards them to the
backend (see `server.proxy` in `vite.config.ts`).
