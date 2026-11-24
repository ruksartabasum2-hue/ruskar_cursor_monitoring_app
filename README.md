# Linux Monitor (demo)

Local Flask demo for read-only Linux server monitoring. See [docs/requirements.md](docs/requirements.md) and [docs/TODO.md](docs/TODO.md).

## Run locally

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # optional; set SECRET_KEY
python app.py
```

App binds to **`0.0.0.0:5888`**. Open `http://<host>:5888` (or `http://127.0.0.1:5888` on this machine).

- Home: `/`
- Dashboard (stub table, read-only): `/dashboard`

## Security notes (Phase 0)

- Do not commit `.env` or real secrets.
- `SECRET_KEY` should be set via environment for anything beyond a local demo (see `.env.example`).
- Session cookies use `HttpOnly` and `SameSite=Lax`.

## Current status

Phase 0 scaffold is in place (basic light UI + empty dashboard table). Sign-in and live metrics come in later TODO phases.
