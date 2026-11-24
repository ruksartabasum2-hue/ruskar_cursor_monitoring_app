# PRD: Demo Linux Server Monitoring

## 1. Overview

Local demo web app for **read-only**, near real-time monitoring of Linux servers (CPU, memory, disk, load, network, ports). Built so L1/L2/L3 and app teams can check host health **without SSH login**.

**Audience:** Internal infra and application teams (demo only).  
**Deploy:** Local machine where Cursor is running.  
**Stack:** Python, Flask, light-theme UI.

---

## 2. Problem

Today, operators must SSH into each Linux host to inspect live resource and port usage. That is slow, error-prone, and not shareable across teams for a quick health check.

---

## 3. Goals (demo)

- Sign in with a single admin account.
- Add Linux servers for monitoring.
- Show a **dashboard** of all servers and a **detail** view per server.
- Display **live** metrics, auto-refreshing every **10 seconds**.
- UI is **read-only** (no remote shell, no config changes on hosts).
- Light, simple, user-friendly UI.

### Non-goals

- Alerts / email / Slack
- Historical graphs or long-term storage
- Multi-user RBAC or roles beyond admin
- Windows / non-Linux hosts
- Production hardening, HA, or cloud deploy
- Agents permanently installed on servers (demo uses SSH pull)

---

## 4. Users

| Role | Access |
|------|--------|
| Admin (default) | Sign in; view dashboard & details; add/remove servers |

Single hardcoded user is enough for this demo. No self-registration.

---

## 5. Features

### F1 — Read-only UI

- All monitoring screens are view-only.
- No actions that change state on remote servers (no reboot, no package install, no file edits).
- Allowed writes: local app data only (login session, server list CRUD in the app).

### F2 — Sign in

- Default username: `admin`
- Password stored as a **hash** (Werkzeug or bcrypt).
- Default demo password (document in README): `admin123` (changeable later if needed).
- Unauthenticated users are redirected to login.
- Simple logout.

### F3 — Add Linux servers

When adding a server, collect:

| Field | Required | Notes |
|-------|----------|--------|
| Display name | Optional | Friendly label |
| IP / hostname | Yes | Target host |
| SSH port | Yes | Default `22` |
| SSH username | Yes | e.g. `ubuntu`, `monitor` |
| Auth | Yes | Password **or** path to private key |

- Persist the server list locally (SQLite or simple JSON/file is fine for demo).
- Ability to remove a server from the list.
- Credentials used only by the local app to fetch metrics over SSH.

### F4 — Dashboard

- List all configured servers.
- Per server (summary): status (**Online** / **Offline** badge), CPU %, memory %, disk %, load average (1-min or 1/5/15 if easy).
- Click a server → detail page.
- Auto-refresh every **10 seconds**.

### F5 — Server detail

Live metrics for one host:

| Metric | What to show |
|--------|----------------|
| CPU | Usage % |
| Memory | Used / total (and %) |
| Disk | Used / total (and %) for root or main mounts |
| Load average | 1, 5, 15 minute |
| Network | RX / TX rates or cumulative bytes (simple is fine) |
| Ports | Listening ports (port + process name if available) |

- **Offline:** show clear **Offline** badge; do not invent metrics; optional short error (e.g. “SSH unreachable”).
- Auto-refresh every **10 seconds**.

---

## 6. Live metrics (how)

- Pull **live** data over **SSH** from each Linux host (no mock data for happy path).
- Prefer standard Linux commands / readable files (`/proc`, `df`, `ss`/`netstat`, etc.) via SSH.
- If SSH fails or times out → mark server **Offline**.
- Keep collection simple and demo-friendly (short SSH timeout).

---

## 7. UX

- **Theme:** light
- **Layout:** login → dashboard → server detail
- Clean tables/cards; readable status badges (Online / Offline)
- Attractive but minimal Flask templates + CSS (no heavy SPA required)

---

## 8. Tech & local run

| Item | Choice |
|------|--------|
| Language | Python 3 |
| Web | Flask |
| Auth hash | Werkzeug (`generate_password_hash` / `check_password_hash`) or bcrypt |
| Data | SQLite or local file |
| SSH | Paramiko (or equivalent) |
| Port | `5000` (default) |

**Minimal local steps (for implementer / README):**

1. Create venv and install dependencies (`requirements.txt`).
2. Ensure this machine can SSH to the target Linux hosts with the credentials entered in the UI.
3. Run: `python app.py` (or `flask run`) → open `http://127.0.0.1:5000`
4. Login: `admin` / `admin123`
5. Add a server → open dashboard / detail and confirm 10s refresh.

---

## 9. Capacity (demo)

- Support a **small normal demo set** (about **1–5** Linux hosts).
- No performance tuning required beyond that.

---

## 10. Success criteria

- [ ] Login works with hashed password; session protects pages.
- [ ] Can add a Linux server (host + SSH user/port + password or key).
- [ ] Dashboard shows Online/Offline and summary metrics; refresh ~10s.
- [ ] Detail page shows CPU, memory, disk, load, network, listening ports.
- [ ] Unreachable host shows **Offline** badge.
- [ ] UI is light-themed, readable, and read-only for monitoring.
- [ ] App runs locally with minimal setup steps above.

---

## 11. Open assumptions

- SSH key path is a path on the **machine running Flask**, not uploaded in the browser (unless easy to add later).
- Disk metric focuses on `/` (and other mounts only if trivial).
- Network metrics can be simple (bytes since boot or short interval delta).
- No HTTPS required for local demo.
