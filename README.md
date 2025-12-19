# Todo-App
Tracks assignments and organizes them based on user preferences. Supports multiple users.

**Testing**
- **Run unit tests (mocked DB, default):** the test discovery will find tests automatically from the project root because `server` is a package (`__init__.py`).

```powershell
python -m unittest -v
# Todo-App

A lightweight Flask-based TODO assignments API used for tracking and organizing assignments.

Features
- Small RESTful API for managing assignments
- Example SQL seed file loaded on startup
- Unit and optional integration tests (Postgres)

Prerequisites
- Python 3.8+
- (Optional) Postgres for integration tests

Quickstart (Windows - PowerShell)

1) Create a virtual environment and install deps

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2) Run the application

```powershell
# From project root
python -m server.server
```

The server entrypoint will load the provided SQL seed file (used for a simple demo DB) and start Flask in debug mode.

Configuration
- Runtime DB configuration is stored in `config/db.yml`. Do not commit secrets to the repository; prefer environment variables for production credentials.
- To run integration tests against a real Postgres instance, populate `config/db.yml` with a test database and set `RUN_INTEGRATION=1` before running tests.

Testing
- Unit tests (default, mocked or local-only) — discovery uses Python's unittest:

```powershell
python -m unittest -v
```

- Integration tests (use caution):

```powershell
# Set this only when you have a dedicated test Postgres configured in config/db.yml
$env:RUN_INTEGRATION = '1'
python -m unittest -v
```

Notes & Security
- If `config/db.yml` contains production credentials, running integration tests may modify live data. Use a dedicated test database and limited-privilege user.
- Consider adding `config/db.yml` to `.gitignore` and keeping `config/db.yml.example` with placeholders instead.

Project layout

- `server/` — application package containing `server.py` and `api/` modules
- `server/api/` — API endpoints and DB utilities (seed SQL in `data.sql`)
- `config/` — runtime configuration (e.g., `db.yml`)
- `tests/` — unit and integration tests

Next steps (optional)
- I can centralize config loading (e.g., add `server/config.py`) and/or add a `config/db.yml.example` and `.gitignore` entry for `config/db.yml`.

License
- MIT / Unspecified — add a LICENSE file if desired.

If you'd like a different README structure or more details (API docs, example requests, CI), tell me what to include and I'll update it.
