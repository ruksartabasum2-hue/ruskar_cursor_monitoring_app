# PRD: Demo Linux Server Monitoring

## 1. Overview

Local demo web app for **read-only**, near real-time monitoring of Linux servers. Internal L1/L2/L3 and application teams can check host health **without logging into each server**.

**Audience:** Internal infrastructure and application development teams (demo).  
**Deploy:** Local machine (where Cursor is running).  
**Stack:** Python, Flask, light theme, simple tables.

---

## 2. Problem

Operators must SSH into each Linux host to inspect live CPU, memory, network, and port usage. That is slow and hard to share across teams for a quick health check.

---

## 3. Goals

- Sign in with a single admin account (hashed password).
- Add Linux servers to monitor.
- **Dashboard** showing live metrics for all servers in simple tables.
- Auto-refresh every **10 seconds**.
- Read-only monitoring UI (no changes on remote hosts).
- Light, user-friendly UI.

### Non-goals (explicitly out of scope)

- Alerts / notifications
- Historical metrics / long-term storage
- Windows hosts
- Agents installed on servers (app pulls metrics over SSH)
- Multi-user RBAC beyond the single admin
- Production hardening, HA, or cloud deploy

---

## 4. Users

| Role | Access |
|------|--------|
| Admin (default) | Sign in; view dashboard; add/remove servers |

One hardcoded admin user. No self-registration or extra roles.

---

## 5. Features

### F1 — Read-only UI

- Monitoring views are view-only.
- No remote actions (no reboot, installs, or file changes on hosts).
- Local app writes only: session + server inventory.

### F2 — Sign in

- Default username: `admin`
- Password stored as a **hash** (Werkzeug preferred; bcrypt acceptable).
- Default demo password (document in README): `admin123`
- Protect all pages behind login; support logout.

### F3 — Add Linux servers

Collect when adding a server:

| Field | Required | Notes |
|-------|----------|--------|
| Display name | Optional | Friendly label |
| IP / hostname | Yes | Target host |
| SSH port | Yes | Default `22` |
| SSH username | Yes | e.g. `ubuntu`, `monitor` |
| Auth | Yes | Password **or** private key path (needed for live SSH pull) |

- Persist inventory locally (SQLite or file).
- Allow remove from the list.
- Support **more than a handful of hosts** (demo target: **10+** servers).

### F4 — Dashboard (primary UI)

- Light theme; **simple tables** (not heavy charts).
- One row (or clear table section) per server with live metrics:

| Column / area | Content |
|---------------|---------|
| Status | **Online** / **Offline** badge |
| CPU | Usage % |
| Memory | Used / total (and %) |
| Disk | Used / total (and %) for `/` or main mount |
| Load average | 1 / 5 / 15 |
| Network | RX / TX (simple rates or bytes) |
| Ports | Listening ports (port ± process if easy) |

- Auto-refresh every **10 seconds**.
- Dashboard is the main screen after login (no requirement for a separate heavy detail app; optional simple expand/row detail is fine if useful).

### F5 — Unreachable hosts

When SSH fails or times out:

1. Show an **Offline** badge.
2. Keep showing **last-known values** (from the last successful poll), clearly labeled as stale if possible.
3. Show a short **error message** (e.g. “SSH unreachable” / timeout).

---

## 6. Live metrics

- Pull **live** data from **real Linux hosts** over **SSH** (no mock happy-path data).
- Use standard Linux sources (`/proc`, `df`, `ss`/`netstat`, etc.) via SSH.
- Short SSH timeout; on failure → Offline + last-known + error (see F5).

---

## 7. UX

- **Theme:** light  
- **Layout:** login → dashboard (tables)  
- Clear Online/Offline badges and readable error text  
- Attractive but minimal Flask templates + CSS  

---

## 8. Tech & local run

| Item | Choice |
|------|--------|
| Language | Python 3 |
| Web | Flask |
| Auth hash | Werkzeug (or bcrypt) |
| Data | SQLite or local file |
| SSH | Paramiko (or equivalent) |
| Bind | `0.0.0.0` |
| Port | `5888` |

**Minimal local steps:**

1. Create venv; `pip install -r requirements.txt`
2. Ensure this machine can SSH to target hosts with the credentials entered in the UI
3. `python app.py` → listen on `0.0.0.0:5888` → open `http://<host>:5888`
4. Login: `admin` / `admin123`
5. Add servers → confirm dashboard metrics and 10s refresh

---

## 9. Capacity

- Demo should handle **more hosts** comfortably (about **10+** Linux servers).
- Keep collection simple; no production-scale tuning required.

---

## 10. Success criteria

- [ ] Login with hashed password; pages require session.
- [ ] Can add Linux servers (IP/hostname, SSH user, port, password or key).
- [ ] Dashboard tables show CPU, memory, disk, load, network, ports; refresh ~10s.
- [ ] Offline hosts: Offline badge + last-known values + error message.
- [ ] UI is light, simple tables, read-only for monitoring.
- [ ] Alerts, history, Windows, and agents are not implemented.
- [ ] Runs locally with the steps above.

---

## 11. Assumptions

- Private key path is on the machine running Flask (unless a simple upload is added later).
- Disk focuses on `/` unless other mounts are trivial.
- Network metrics can be simple (boot counters or short-interval delta).
- No HTTPS required for local demo.
- App binds to `0.0.0.0:5888` (reachable on the network interface; restrict access in non-demo use).
