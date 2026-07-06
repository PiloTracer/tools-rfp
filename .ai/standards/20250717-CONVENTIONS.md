# RFP Platform — Code conventions

**Status:** Final · **Updated:** 2025-07-17
**Cross-ref:** DOCS_TECH_STACK.md · [Foundation doc 04](../../.work/plans/foundation/20250717-04-rfp-platform-arch-foundation.md)

---

## 1. Python (backend/)

### Formatting & linting
- **Formatter:** Ruff — run `ruff format .` before commit
- **Linter:** Ruff — run `ruff check .`; all rules from `RUF` + `F` (pyflakes) + `E/W` (pycodestyle)
- **Type checker:** Pyright in strict mode

### Imports
```python
# stdlib
import json
from pathlib import Path

# third-party
from fastapi import APIRouter, Depends
from pydantic import BaseModel

# app-local
from app.ingestion.models import RfpDocument
from app.common.deps import get_current_user
```

### Naming
| Element | Convention | Example |
|---------|------------|---------|
| Modules | snake_case | `document_parser.py` |
| Classes | PascalCase | `RfpParser` |
| Functions | snake_case | `extract_questions()` |
| Variables | snake_case | `parsed_doc` |
| Constants | UPPER_SNAKE | `MAX_UPLOAD_SIZE_MB` |
| Private helpers | `_` prefix | `_normalize_text()` |

### Project structure per module
```
backend/app/<bounded_context>/
├── __init__.py
├── models.py        # SQLAlchemy ORM models
├── schemas.py       # Pydantic request/response schemas
├── service.py       # Business logic (no HTTP)
├── router.py        # FastAPI route definitions
├── deps.py          # Dependency injection
├── exceptions.py    # Domain-specific errors
└── tasks.py         # Celery tasks (if async processing)
```

### Error handling
- Domain-specific exceptions in `exceptions.py`, inheriting from `AppError`
- HTTP errors raised as `HTTPException` in routers only — not in services
- Services return `Result[T, AppError]` pattern or raise domain exceptions

### Testing
- Tests mirror app structure: `backend/tests/<bounded_context>/test_*.py`
- 1 test file per module
- Use pytest fixtures for DB, client, auth
- Prefer `async def test_*` with `httpx.AsyncClient`

---

## 2. TypeScript/React (frontend/)

### Formatting & linting
- **Formatter:** Prettier
- **Linter:** ESLint with TypeScript plugin
- **Type checking:** `tsc --noEmit`

### Naming
| Element | Convention | Example |
|---------|------------|---------|
| Components | PascalCase | `RfpReviewPanel.tsx` |
| Hooks | `use` prefix | `useRfpDocument()` |
| Utilities | camelCase | `formatDate()` |
| Types/Interfaces | PascalCase | `RfpDocument` |
| Files (components) | PascalCase | `QuestionCard.tsx` |
| Files (utilities) | camelCase | `dateUtils.ts` |
| CSS modules | `*.module.css` | `reviewPanel.module.css` |

### i18n
- All user-facing strings wrapped in `t()` from react-i18next
- Locale files in `frontend/src/locales/{en,es}/translation.json`

### State management
- React Context + `useReducer` for per-page state
- No global state library (Redux, Zustand) in V1

---

## 3. SQL / Migrations

- One file per migration: `backend/migrations/NNNN_description.sql`
- Must be idempotent (`IF NOT EXISTS`, `OR REPLACE`)
- Ran by migration runner on every app start (before serving traffic)

---

## 4. Git

- **Commit messages:** `type: description` (no ref) or `REF: description` when ref known
- **No `Co-authored-by:`** — stripped by hook
- **No attribution markers** in source files
- **Scope:** per `.cursorrules` — `touch-scope-verify` + `blast-radius-check` enforce it
