# RFP Platform — Directory map

**Status:** Final · **Updated:** 2025-07-17
**Cross-ref:** DOCS_TECH_STACK.md · [Foundation doc 04](../../.work/plans/foundation/20250717-04-rfp-platform-arch-foundation.md)

---

## 1. Repository root

```
.
├── .ai/                    # Agent OS (skills, standards, concepts)
│   ├── docs/
│   │   └── integration/    # Mirrored vendor artifacts
│   ├── skills/             # Agent skill playbooks
│   ├── standards/          # Binding engineering standards
│   ├── concepts/           # NFR concept prompts
│   └── templates/          # Boilerplate templates
├── .work/                  # Project-specific plans, SPECs, ADRs
│   ├── context/
│   │   └── HANDOFF.md      # Session handoff
│   ├── decisions/           # ADRs (ADR-001…)
│   ├── features/            # Feature SPECs by bounded context
│   ├── plans/
│   │   ├── foundation/      # Foundation docs 01–04
│   │   ├── full/            # Master implementation plan
│   │   ├── ASSUMPTIONS.md
│   │   ├── NEXT.md
│   │   ├── RISK_REGISTRY.md
│   │   └── UNKNOWNS.md
│   └── README.md
├── backend/                # FastAPI application
│   ├── app/
│   │   ├── common/          # Shared utilities, base classes
│   │   ├── core/            # App config, DB session, migration runner
│   │   ├── ingestion/       # BC1 - Document Ingestion
│   │   ├── knowledge_base/  # BC2 - Knowledge Base
│   │   ├── rag/             # BC3 - RAG Engine
│   │   ├── review/          # BC4 - Review Workflow
│   │   ├── export/          # BC5 - Export
│   │   ├── identity/        # BC6 - Identity & Access
│   │   └── admin/           # BC7 - Administration
│   ├── migrations/          # Idempotent SQL migrations
│   ├── scripts/             # One-off utility scripts
│   └── tests/               # Test suite (mirrors app/ structure)
├── worker/                  # Celery worker (parsing, embeddings, LLM)
├── frontend/                # React + Vite UI
│   └── src/
│       ├── components/      # Reusable UI components
│       ├── pages/           # Route-level page components
│       ├── hooks/           # Custom React hooks
│       ├── services/        # API client
│       ├── locales/         # i18n translation files
│       │   ├── en/
│       │   └── es/
│       └── types/           # TypeScript type definitions
├── docker-compose.yml       # Compose (dev + prod)
├── Dockerfile.api
├── Dockerfile.dashboard
├── DOCS_TECH_STACK.md       # Pinned tech stack
├── .env.example             # Env template (no secrets)
├── .gitignore
└── .cursorrules
```

---

## 2. Bounded context boundaries

| Directory | BC | Owns | Depends on |
|-----------|----|------|------------|
| `backend/app/ingestion/` | BC1 | Upload, parse, extract structure | MinIO, Celery, Unstructured.io |
| `backend/app/knowledge_base/` | BC2 | KB CRUD, chunking, embedding pipeline | PostgreSQL + pgvector, Celery |
| `backend/app/rag/` | BC3 | RAG queries, draft generation | LiteLLM, KB, PostgreSQL |
| `backend/app/review/` | BC4 | Per-question editing, approval workflow | PostgreSQL, Celery (notify) |
| `backend/app/export/` | BC5 | DOCX generation, formatting | Review data, python-docx |
| `backend/app/identity/` | BC6 | Users, roles, JWT auth, RBAC | PostgreSQL, FastAPI Users |
| `backend/app/admin/` | BC7 | System config, KB mgmt UI, compliance rules | All contexts |

## 3. Dependency rules

- BCs may only depend on BCs with lower numbers (acyclic)
- Shared cross-cutting: `backend/app/common/` (models, deps, utils)
- No circular imports between BCs
- `backend/app/core/` for framework wiring only (DB, config, migration runner)

## 4. File naming conventions

| Layer | Pattern | Example |
|-------|---------|---------|
| SQL migrations | `NNNN_description.sql` | `0001_create_tenants.sql` |
| Foundation docs | `YYYYMMDD-NN-<slug>.md` | `20250717-01-rfp-platform-initial-scope.md` |
| ADRs | `YYYYMMDD-NNN-title.md` | `20250717-001-backend-stack.md` |
| Feature SPECs | `YYYYMMDD-SPEC.md` | `20250717-SPEC.md` |
| SPEC amendments | `YYYYMMDD-SPEC-amendment-NN.md` | `20250717-SPEC-amendment-01.md` |
