# Change Log — AI Session Work (2026-09-09 / 2026-09-10)

Every change made in this session, in order. Verified with
`manage.py check` (both services), auth-service `pytest` (4 passed),
and a live register → login → `auth/me` → `game/account` flow.

> Note: `services/game-service/` is still **untracked** (`??` in git status).
> Nothing was committed — all changes are working-tree only.

---

## Phase 0 — Revert of earlier AI changes (per request)

The workspace contained uncommitted work from a previous AI session.
At the user's request ("revert all of your changes cause i dont want to change anything")
it was fully reverted:

1. `docker-compose.yml` — restored to HEAD with `git restore docker-compose.yml`
   (discarded ~67 added lines that defined `game-service` / `game-postgres`).
2. `services/game-service/` — deleted entirely (`Remove-Item -Recurse -Force`),
   including its `.venv`. It was fully untracked, so this just removed new files.
3. Result: `git status` → `nothing to commit, working tree clean`.

(Later the user asked to fix the `game-service` error, so the service was
reconstructed — see Phase 1.)

---

## Phase 1 — Fixed `game-service` circular-import crash

**Symptom:** `docker compose exec game-service python manage.py check` failed with
`ImportError: cannot import name 'APIView' from partially initialized module
'rest_framework.views' (most likely due to a circular import)`.

**Root cause:** `config/settings.py` pointed `DEFAULT_AUTHENTICATION_CLASSES` at
`src.presentation.dota.views.JWTAuthentication` — a class that didn't even exist,
inside a `views.py` that imports `APIView` at module top. DRF imports the auth
class *while* `rest_framework.views` is still initializing
(`views → schemas → api_settings → views…`), hence the deadlock.
Auth backends must not live in a views module (auth-service correctly keeps its
one in `src/infrastructure/security/`).

**Changes:**

1. `services/game-service/` — **restored from the `geme-sense-game-service`
   Docker image** (the local copy had been deleted in Phase 0, which left the
   bind-mount masking `/app` with an empty dir). Recovered via
   `docker create` + `docker cp /app` into a temp dir, then copied back
   (excluding `__pycache__`). All files below were part of this restore;
   the *edits* on top of it are items 2–6.
2. `services/game-service/src/infrastructure/authentication/jwt.py` — was an
   **empty file**; implemented `JWTAuthentication` (DRF `BaseAuthentication`,
   imports only `rest_framework.authentication`, never `views`) plus a lightweight
   `AuthenticatedUser` (game-service has no users table, so no DB lookup —
   it only validates the auth-service token).
3. `services/game-service/config/settings.py` — `DEFAULT_AUTHENTICATION_CLASSES`:
   `src.presentation.dota.views.JWTAuthentication`
   → `src.infrastructure.authentication.jwt.JWTAuthentication`.
4. `services/game-service/src/presentation/health/views.py` — added
   `authentication_classes = []` / `permission_classes = []` (mirrors auth-service).
   Without this, the global `IsAuthenticated` default made `/api/v1/health/`
   return 403 and the container stayed `unhealthy`.
5. `services/game-service/requirements.txt` — added `PyJWT>=2.8,<3.0`.
   The image had no `jwt` module at all (`import jwt` → `ModuleNotFoundError`).
6. `docker-compose.yml` — re-added `game-postgres` (postgres:17-alpine,
   `POSTGRES_DB=game_db`, `game_postgres_data` volume, `pg_isready` healthcheck)
   and `game-service` (build `./services/game-service`, `gamesense-game`,
   `8002:8000`, `env_file: .env.docker`, `POSTGRES_HOST=game-postgres`,
   bind-mount `./services/game-service:/app`, healthcheck on `/api/v1/health/`),
   plus the `game_postgres_data` volume. Reconstructed from `docker inspect`
   of the orphaned containers.

**Verify:** `manage.py check` → `System check identified no issues`,
health endpoint `{"status":"ok","service":"game-service"}`, container `healthy`.

---

## Phase 2 — Aligned JWT to one shared secret

**Problem:** auth-service signed/verified tokens with Django's `SECRET_KEY`
(hardcoded `django-insecure-…`), game-service verified with `JWT_SECRET`
(`tax0u…` from `.env.docker`). A token from login could never validate in
game-service → permanent 401 there.

**Changes (single shared `JWT_SECRET` from env, `HS256`):**

1. `services/auth-service/config/settings.py`
   - Added `JWT_SECRET = os.getenv("JWT_SECRET", "gamesense-jwt-dev")`,
     `JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")`,
     `JWT_ACCESS_TOKEN_LIFETIME_MINUTES = int(os.getenv(..., "30"))`.
   - Removed the duplicated `JWT_ACCESS_TOKEN_LIFETIME_MINUTES`/`JWT_ALGORITHM`
     block (it was defined twice, lines ~137 and ~147).
2. `services/auth-service/src/infrastructure/security/jwt_token_generator.py` —
   `jwt.encode(..., settings.SECRET_KEY, ...)` → `settings.JWT_SECRET`.
3. `services/auth-service/src/infrastructure/security/jwt_authentication.py` —
   `jwt.decode(..., settings.SECRET_KEY, ...)` → `settings.JWT_SECRET`.
4. `services/game-service/config/settings.py` — added `JWT_ALGORITHM`
   from env (was hardcoded `"HS256"` in code).
5. `services/game-service/src/infrastructure/authentication/jwt.py` — decode uses
   `settings.JWT_ALGORITHM` instead of hardcoded `"HS256"`.
6. `.env.example` (gitignored, not visible in `git status`) — documented
   `POSTGRES_DB=game_db`, `JWT_SECRET=change-me-in-production`,
   `JWT_ALGORITHM=HS256`, `JWT_ACCESS_TOKEN_LIFETIME_MINUTES=30`.

Side effect: tokens issued before this change no longer validate (different
signing key) — users just log in again.

---

## Phase 3 — Fixed `user_id` type mismatch (int → UUID)

**Problem:** auth-service user IDs are UUIDs (`sub` claim), but
`GamingAccountModel.user_id` was `BigIntegerField` and the domain/repo/use-case
layers typed it `int` — any authenticated game write/query would crash.

**Changes (`user_id: UUID` everywhere):**

1. `services/game-service/src/infrastructure/persistence/models.py` —
   `user_id = models.BigIntegerField()` → `models.UUIDField(db_index=True)`.
2. `services/game-service/src/domain/entities/gaming_account.py` —
   `user_id: int` → `user_id: UUID` (+ import).
3. `services/game-service/src/domain/repositories/gaming_account_repository.py` —
   `get_by_user_and_game(user_id: int, …)` → `user_id: UUID` (+ import).
4. `services/game-service/src/infrastructure/persistence/repositories.py` —
   same signature change (+ import).
5. `services/game-service/src/application/use_cases/connect_dota_account.py` —
   `execute(user_id: int, …)` → `user_id: UUID` (+ import).
6. `services/game-service/src/application/use_cases/sync_dota_matches.py` —
   `execute(user_id: int, …)` → `user_id: UUID` (+ import).
7. `services/game-service/src/infrastructure/authentication/jwt.py` — `sub`
   claim is parsed into `UUID(...)` (invalid → `AuthenticationFailed`), so
   `request.user.id` downstream is a real UUID object.
8. **New migration** `services/game-service/src/infrastructure/persistence/migrations/`
   (`__init__.py` + `0001_initial.py`, created via
   `manage.py makemigrations persistence`) — creates `gaming_accounts`
   (with `user_id uuid` + `unique_user_game`) and `matches`. Applied with
   `manage.py migrate` against `game-postgres`; `\d gaming_accounts` confirms
   `user_id | uuid`. (Bare `makemigrations` detected nothing; the explicit app
   label `persistence` was required.)

---

## Phase 4 — Made auth-service `pytest` runnable

**Problem:** `pytest.ini` sets `DJANGO_SETTINGS_MODULE`, but `pytest-django`
was not installed (`requirements.txt` only had bare `pytest`), so
`python -m pytest` failed at collection
(`Unknown config option: DJANGO_SETTINGS_MODULE` → `ImproperlyConfigured`).
Pre-existing failure, unrelated to the JWT/user_id work.

**Changes:**

1. `services/auth-service/requirements.txt` — added `pytest-django`
   (unpinned, like the existing `pytest`/`PyJWT` entries).
   - The file is **UTF-16-LE with BOM** (that's why file readers reported it as
     "binary"). An early append mangled its encoding; it was rewritten cleanly
     in the same UTF-16-LE + CRLF format with all 10 lines.
2. Installed `pytest-django 4.14.0` in the running container for immediate use.

**Verify:** `python -m pytest -q` → `4 passed`.

---

## Verification summary (final state)

- `docker compose exec auth-service python manage.py check` → no issues
- `docker compose exec game-service python manage.py check` → no issues
- Auth `pytest` → 4 passed
- Live flow with a fresh user: register 201 → login 200 → `auth/me` 200 →
  `game/account` 404 `"Dota 2 account is not connected."`
  (authenticated — correct when no Steam account is linked) vs 403 with no token
- Token manually decodes with the shared `JWT_SECRET`; `sub` is a UUID
- UUID write round-trip on `gaming_accounts` (create → filter → delete) passed
- All containers `healthy` (`gamesense-auth :8000`, `gamesense-game :8002`)

## Known remaining items (not changed)

- `auth-service` `SECRET_KEY` is still the hardcoded dev value; `DEBUG=True`,
  `ALLOWED_HOSTS=[]`.
- `MAILERS` dict in auth `settings.py` is a typo (Django expects `EMAIL_BACKEND`).
- Redis/RabbitMQ are provisioned in compose but unused by the code.
- Real secrets live in local `.env` / `.env.docker` (gitignored) — rotate `JWT_SECRET`
  / `STRATZ_TOKEN` if they were ever committed anywhere.
- `docker compose up --build auth-service` currently fails on flaky PyPI
  connectivity (read timeouts on the Django wheel, ~30 kB/s) — code is verified
  live via bind mounts; just rerun the build when the network recovers.
- `services/game-service/` is untracked; nothing in this session was committed.
