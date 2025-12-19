# Todo-App
Tracks assignments and organizes them based on user preferences. Supports multiple users.

**Testing**
- **Run unit tests (mocked DB, default):** the test discovery will find tests automatically from the project root because `server` is a package (`__init__.py`).

```powershell
python -m unittest -v
```

- **Run integration tests (requires real Postgres and credentials in `config/db.yml`):** set the env var `RUN_INTEGRATION=1` and run the same command; tests will use `config/db.yml` only when that var is set.

```powershell
#$env:RUN_INTEGRATION = '1'
python -m unittest -v
```

Place real DB credentials in [config/db.yml](config/db.yml#L1-L10) before running integration tests.

**IMPORTANT — your `config/db.yml` is live**
- If `config/db.yml` contains credentials for your production or personal Postgres server, running integration tests with `RUN_INTEGRATION=1` will attempt to connect to that server and may modify data. Only run integration tests against a dedicated test database.
- Recommendations:
	- Use a separate test database or user with limited privileges for integration tests.
	- Do not commit `config/db.yml` with secrets. Add `config/db.yml` to `.gitignore` and keep an example file like `config/db.yml.example` in the repo.
	- Prefer environment variables for secrets (e.g., `DB_USER`, `DB_PASSWORD`) and update `server/api/db_utils.py` to read env vars first.
	- Enable integration runs explicitly: set `RUN_INTEGRATION=1` only in controlled environments (local dev after confirming test DB, or in CI with proper isolation).

**Dependencies**
- Install dependencies into the project venv (created automatically by the workspace environment):

```powershell
C:/PersonalProjects/toDoApp/Todo-App/.venv/Scripts/python.exe -m pip install -r requirements.txt
```

If you encounter Windows DLL errors for psycopg2, use the binary wheel:

```powershell
C:/PersonalProjects/toDoApp/Todo-App/.venv/Scripts/python.exe -m pip install psycopg2-binary PyYAML
```

**Repository structure & cleanup suggestions**
- **Make `server` the main package:** keep application code under [server](server#L1) and treat top-level files as project metadata. Adding `__init__.py` (already added) makes imports explicit.
- **Group api code:** move API modules into [server/api](server/api#L1) (already present). Consider splitting into `db/`, `routes/`, `models/` subpackages if the API grows.
- **Separate tests and fixtures:** keep tests under [server/tests](server/tests#L1). Add a `tests/fixtures` or `tests/helpers` folder for mocks and shared fixtures.
- **Centralize config:** keep runtime config in [config](config#L1) and avoid building paths relative to `__file__` in multiple places; use a small helper (e.g., `server/config.py`) to resolve config path once.
- **Virtual environment & dependency files:** ensure `requirements.txt` lists user-facing deps; add `requirements-dev.txt` for testing/dev-only packages.
- **Consider flattening small modules:** if `server/api` has only a couple of small files, consider moving them up into `server/` to reduce nesting.
- **Add CI test workflow:** include a CI job that installs dependencies, sets `RUN_INTEGRATION=1` only for an `integration` stage, and runs unit tests in isolation.

**Quick next steps**
- Add a README snippet describing how to set real DB creds in [config/db.yml](config/db.yml#L1-L10).
- If you want, I can create `server/config.py` to centralize path resolution and provide a `get_db_config()` helper.

If you'd like, I can apply any of the cleanup options above and update the repo accordingly.
