# TODO: Demo Linux Server Monitoring

Incremental implementation plan aligned with [requirements.md](./requirements.md).  
Each step is small enough for one AI-assisted change set. Check items off as you complete them.

**Conventions for every step**

- **Security:** follow the step’s security bullets before marking done.
- **Docs:** update the listed doc file(s) in the same change.
- Prefer small PRs / commits: one step (or one sub-step) at a time.

---


### Step 0.1 — Scaffold the Python/Flask project
- [x] Create app package layout (`app/`, `app/__init__.py`, `app/routes/`, `app/templates/`, `app/static/`)
- [x] Add `requirements.txt` with Flask (pin versions)
- [x] Add minimal `app.py` or `wsgi` entry that starts Flask on `0.0.0.0:5888`
- [x] Add `.gitignore` entries for `.venv/`, `__pycache__/`, `.env`, `*.db`
- [x] **Security:** do not commit secrets; use `.env.example` only with placeholders
- [x] **Docs:** create root `README.md` with venv create, install,## Phase 0 — Project initialization and basic UI
 and run commands

### Step 0.2 — Basic light UI shell
- [x] Add base template (`base.html`) with light theme CSS
- [x] Add a simple home/placeholder page with app title and nav skeleton
- [x] Style with simple, readable layout (no dark theme; tables-ready styles)
- [x] **Security:** set `SESSION_COOKIE_HTTPONLY` and a placeholder `SECRET_KEY` from env (fail clearly if missing in non-demo notes)
- [x] **Docs:** document UI entry URL (`http://<host>:5888`, bind `0.0.0.0`) in `README.md`

### Step 0.3 — Empty dashboard table stub (read-only)
- [x] Add `/dashboard` route rendering a static empty HTML table (columns: Status, CPU, Memory, Disk, Load, Network, Ports)
- [x] Mark page as read-only in UI copy (no edit controls yet)
- [x] **Security:** no server-side execution of user content; escape template output (Jinja autoescape on)
- [x] **Docs:** short note in `docs/requirements.md` or `README.md` that dashboard is stubbed

---

## Phase 1 — Sign-in and unit tests

### Step 1.1 — Config and password hashing helpers
- [ ] Add config module reading `SECRET_KEY` and admin credentials from environment
- [ ] Implement password hash verify helper (Werkzeug `generate_password_hash` / `check_password_hash`)
- [ ] Store only a **hashed** default admin password (never plaintext in code)
- [ ] **Security:** document that default `admin` / `admin123` is demo-only; hash at startup or ship pre-hash
- [ ] **Docs:** document env vars in `README.md` and `.env.example`

### Step 1.2 — Login / logout routes and forms
- [ ] Add `/login` GET/POST with username + password form
- [ ] On success, create session; redirect to dashboard
- [ ] Add `/logout` that clears session
- [ ] **Security:** constant-time hash check; generic error (“Invalid credentials”); POST-only login; CSRF token on forms (Flask-WTF or equivalent)
- [ ] **Docs:** document default login in `README.md`

### Step 1.3 — Protect routes (auth required)
- [ ] Add `@login_required` (or before-request) so `/dashboard` redirects unauthenticated users to `/login`
- [ ] Ensure logout is reachable when authenticated
- [ ] **Security:** session cookie `SameSite=Lax`; secure flag documented for HTTPS later; no auth bypass on static-only mistake for HTML pages
- [ ] **Docs:** note protected routes in `README.md`

### Step 1.4 — Unit tests for auth
- [ ] Add `pytest` (+ Flask test client) to `requirements.txt` / `requirements-dev.txt`
- [ ] Tests: login success, login failure, logout, dashboard requires login
- [ ] Tests: password hash verify helper
- [ ] **Security:** tests must not print secrets; use test `SECRET_KEY`
- [ ] **Docs:** add “Run tests” section (`pytest`) to `README.md`

---

## Phase 2 — CI/CD (GitHub Actions)

### Step 2.1 — Lint/format workflow baseline
- [ ] Add `.github/workflows/ci.yml` triggered on push/PR to `main`
- [ ] Job: checkout, setup Python, install deps, run tests
- [ ] **Security:** use official `actions/checkout` and `actions/setup-python` with pinned versions/SHA where practical; no secrets in logs
- [ ] **Docs:** add “CI” subsection describing what the workflow runs

### Step 2.2 — Tighten CI (quality gates)
- [ ] Add lint step (e.g. `ruff` or `flake8`) in the same or a second job
- [ ] Fail the workflow on test or lint failure
- [ ] **Security:** disable unnecessary `pull_request_target` / untrusted checkout patterns; least-privilege `permissions:` (e.g. `contents: read`)
- [ ] **Docs:** document required status checks / how to read CI failures in `README.md`

---

## Phase 3 — Server inventory (add / list / remove)

### Step 3.1 — Data model for servers
- [ ] Define server fields: display name, IP/hostname, SSH port, SSH username, auth type, secret material reference
- [ ] Choose SQLite (recommended) and create schema/migration or init script
- [ ] **Security:** never store SSH passwords or private key **contents** in plaintext logs; prefer key path or encrypted-at-rest password field for demo with clear warning
- [ ] **Docs:** document DB file location and backup/reset in `README.md`

### Step 3.2 — Add-server form (UI + POST)
- [ ] Authenticated form: name, host, port (default 22), username, password **or** key path
- [ ] Validate host/port/username (port range, non-empty host)
- [ ] Persist and redirect to dashboard
- [ ] **Security:** CSRF on form; validate/sanitize inputs; reject path traversal on key paths where feasible; do not echo secrets back in HTML
- [ ] **Docs:** document “Add server” fields in `README.md`

### Step 3.3 — List servers on dashboard (inventory only)
- [ ] Show configured servers in the dashboard table (host + status placeholder “Unknown”)
- [ ] Support **10+** rows without breaking layout
- [ ] **Security:** authorize all inventory mutations to logged-in admin only
- [ ] **Docs:** screenshot or short usage note for inventory list

### Step 3.4 — Remove server
- [ ] Add remove action (POST + confirm) for a server id
- [ ] **Security:** CSRF; POST-only delete; no GET delete links
- [ ] **Docs:** document remove flow
- [ ] Unit tests: add server, list, remove, auth required for mutations

---

## Phase 4 — Live metrics over SSH

### Step 4.1 — SSH client wrapper
- [ ] Add Paramiko (or equivalent) helper: connect with password or key path, short timeout
- [ ] Return structured success/failure (no raw exception leak to UI)
- [ ] **Security:** disable unknown-host auto-add blindly or document `known_hosts` policy; timeout connections; never log passwords/keys
- [ ] **Docs:** document SSH prerequisites and known_hosts expectation

### Step 4.2 — Collect CPU, memory, disk, load
- [ ] Remote commands/files for CPU %, memory used/total, disk `/`, load 1/5/15
- [ ] Parse into a typed dict/model
- [ ] **Security:** use fixed command allowlist (no user-controlled shell strings)
- [ ] **Docs:** document which metrics are collected
- [ ] Unit tests: parsers with sample `/proc` / command fixtures (no real SSH required)

### Step 4.3 — Collect network and listening ports
- [ ] Parse RX/TX (simple) and listening ports (+ process name if easy)
- [ ] **Security:** fixed commands only; cap output size parsed
- [ ] **Docs:** note port column format
- [ ] Unit tests: parser fixtures for `ss`/`netstat`-like output

### Step 4.4 — Wire metrics into dashboard
- [ ] On dashboard load (or background helper), fetch metrics per server
- [ ] Fill table columns with live values
- [ ] **Security:** read-only remote usage; no write commands on hosts
- [ ] **Docs:** update usage: “open dashboard → see live metrics”

---

## Phase 5 — Offline handling, cache, and refresh

### Step 5.1 — Offline badge + error message
- [ ] On SSH failure/timeout, mark server **Offline**
- [ ] Show short error message (e.g. SSH unreachable)
- [ ] **Security:** sanitize error strings (no credential leakage)
- [ ] **Docs:** document offline behavior per PRD
- [ ] Unit tests: failure path sets offline + error

### Step 5.2 — Last-known values
- [ ] Cache last successful metrics per server (memory or SQLite)
- [ ] When offline, display last-known values labeled as stale
- [ ] **Security:** cache must not include SSH secrets
- [ ] **Docs:** explain stale/last-known labeling
- [ ] Unit tests: offline uses cache when present

### Step 5.3 — 10-second auto-refresh
- [ ] Add dashboard auto-refresh every **10 seconds** (meta refresh or lightweight JS fetch)
- [ ] Prefer partial update if already easy; full page refresh is OK for demo
- [ ] **Security:** refresh endpoint requires auth; no open JSON API without session
- [ ] **Docs:** document refresh interval

---

## Phase 6 — Polish, hardening, and final docs

### Step 6.1 — UX polish (light tables)
- [ ] Improve table readability (spacing, badge colors for Online/Offline)
- [ ] Empty states: no servers yet; all offline
- [ ] **Security:** confirm monitoring UI has no remote mutation controls
- [ ] **Docs:** final screenshots or GIF optional in `README.md`

### Step 6.2 — Security pass
- [ ] Review: hashed passwords, CSRF, session cookies, no secrets in repo, SSH command allowlist
- [ ] Ensure `.env` is gitignored; CI uses dummy env vars
- [ ] **Docs:** add `docs/SECURITY.md` with demo threat model and limitations

### Step 6.3 — Final documentation and CI green
- [ ] Align `README.md` with full local run path (install → run → login → add server → dashboard)
- [ ] Confirm `docs/requirements.md` and this TODO reflect shipped scope
- [ ] Ensure GitHub Actions CI is green on `main`
- [ ] **Security:** remind operators to change demo password if exposed beyond local demo
- [ ] **Docs:** mark completed phases in this file

---

## Suggested implementation order (summary)

1. [ ] Phase 0 — Init + basic UI  
2. [ ] Phase 1 — Sign-in + unit tests  
3. [ ] Phase 2 — GitHub Actions CI  
4. [ ] Phase 3 — Server inventory  
5. [ ] Phase 4 — Live SSH metrics  
6. [ ] Phase 5 — Offline / last-known / 10s refresh  
7. [ ] Phase 6 — Polish, security pass, final docs  

---

## Out of scope (do not implement)

- [ ] ~~Alerts / notifications~~ (skip)
- [ ] ~~Historical graphs / long-term storage~~ (skip)
- [ ] ~~Windows hosts~~ (skip)
- [ ] ~~Monitoring agents on servers~~ (skip)
- [ ] ~~Multi-user RBAC~~ (skip)
