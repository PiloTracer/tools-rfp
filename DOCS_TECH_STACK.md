# Technology stack — RFP Platform

**Status:** Final — ready for implementation. Linked from `.cursorrules` as `DOCS_TECH_STACK.md`.

**Updated:** 2025-07-17

---

## 1. Summary

| Layer | Choice | Version (pin) | Notes |
|-------|--------|---------------|-------|
| Language (primary) | Python | 3.12 | AI/LLM ecosystem maturity |
| HTTP API | FastAPI | latest | Async-native, Pydantic validation |
| Database | PostgreSQL + pgvector | 16 | Single DB for relational + embeddings |
| Cache / queue | Redis | 7 | Celery broker + caching + rate-limiting |
| Frontend | React + Vite + TypeScript | latest | Rich document review UI |
| Auth | FastAPI Users + JWT | latest | Self-contained for self-hosted |
| Hosting | Docker Compose | N/A | Self-hosted, single `docker compose up` |
| Document parsing | Unstructured.io + LibreOffice | latest | PDF/DOCX/XLSX/ODT/TXT |
| File storage | MinIO | latest | S3-compatible, self-hosted |
| Task queue | Celery | latest | Document processing, LLM calls |
| LLM adapter | LiteLLM | latest | Multi-vendor abstraction layer |

---

## 2. Repository layout

| Path | Purpose |
|------|---------|
| `backend/` | Application source (FastAPI) |
| `backend/migrations/` | Idempotent SQL migrations (Alembic) |
| `backend/tests/` | Test suite |
| `worker/` | Celery worker: parsing, embeddings, LLM |
| `frontend/` | UI (React + Vite) |
| `.ai/` | Agent OS (skills, standards, guides) |
| `.work/` | Plans, SPECs, ADRs, HANDOFF |

See `.ai/standards/*-DIRECTORY_MAP.md` after customization.

---

## 3. Local development

| Item | Value |
|------|-------|
| Dev stack script | `./dev-stack.sh` |
| Compose file | `docker-compose.yml` |
| Test command | `pytest tests/ -q` |
| Lint | `ruff check .` |
| Scope check | `bash .ai/scripts/touch-scope-verify.sh` (when Agent OS scripts present) |
| Blast radius | `bash .ai/scripts/blast-radius-check.sh` (when Agent OS scripts present) |
| Type check | `pyright .` |

---

## 4. CI/CD

| Item | Status |
|------|--------|
| Platform | GitHub Actions |
| Deploy targets | Self-hosted (Docker Compose) |

---

## 5. Open decisions (track in `.work/plans/UNKNOWNS.md`)

| ID | Topic | Owner |
|----|-------|-------|
| U1 | Max RFP page count for processing | eng |
| U2 | Embedding + chunking strategy | eng |
| U3 | Fine-tuning vs RAG for domain terminology | eng |
| U4 | Acceptable per-RFP processing cost | product |
| U5 | File size/page limit for uploader | product |

---

## 6. ADR cross-reference

Decisions live in `.work/decisions/`. This file holds **pins** only; rationale belongs in ADRs.
