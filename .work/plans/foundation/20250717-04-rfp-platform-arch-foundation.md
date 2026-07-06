# P1 — RFP Platform: architecture foundation

> **⚠️ This document is the architecture foundation — not a full implementation plan.**
> The master plan lives in `.work/plans/full/` (created by `@plan-master`).

**Product:** RFP Platform
**Status:** Draft (foundation doc 04)
**Updated:** 2025-07-17
**Cross-references:** [doc 01](20250717-01-rfp-platform-initial-scope.md) · [doc 02](20250717-02-rfp-platform-integration.md) · [doc 03](20250717-03-rfp-platform-adjacency.md)

---

## 1. High-level architecture

```
                          ┌───────────────┐
       User               │   Frontend    │
     (Browser) ──────────→│  React + Vite │
                          └───────┬───────┘
                                  │ HTTP (JSON)
                          ┌───────▼───────┐
                          │   FastAPI     │
                          │  (backend/)   │
                          └───┬───┬───┬───┘
                              │   │   │
              ┌───────────────┤   │   ├───────────────┐
              │                   │                   │
       ┌──────▼──────┐     ┌─────▼──────┐     ┌──────▼──────┐
       │ PostgreSQL  │     │   Redis    │     │   MinIO     │
       │ + pgvector  │     │  (cache/   │     │   (file     │
       │ (relational │     │   queue)   │     │   storage)  │
       │ + embeddings)│    └────────────┘     └─────────────┘
       └─────────────┘
              │
       ┌──────▼──────┐
       │   Celery    │
       │  (worker/)  │
       └──────┬──────┘
              │ HTTP
       ┌──────▼──────┐
       │  LiteLLM   │──→ OpenAI / Anthropic / local
       └─────────────┘
```

## 2. Bounded contexts (from doc 01 §3a)

| # | Context | Responsibility | Primary store | Key dependencies |
|---|---------|---------------|---------------|------------------|
| BC1 | Document Ingestion | Upload, parse, extract RFP structure | MinIO (files) → PostgreSQL (structure) | Celery (async parse), Unstructured.io |
| BC2 | Knowledge Base | Store/retrieve past proposals, case studies | PostgreSQL + pgvector | Embedding pipeline |
| BC3 | RAG Engine | Embeddings, retrieval, draft generation | PostgreSQL + pgvector (embeddings) | LiteLLM, KB |
| BC4 | Review Workflow | Per-question editing, approval, sign-off | PostgreSQL | Frontend (React) |
| BC5 | Export | DOCX generation, formatting | — (generated on demand) | Review data |
| BC6 | Identity & Access | Users, roles, RBAC | PostgreSQL | JWT tokens |
| BC7 | Administration | System config, KB mgmt, compliance rules | PostgreSQL | All contexts |

### Dependency direction

```
BC1 (Ingestion) ──→ BC2 (KB) ──→ BC3 (RAG) ──→ BC4 (Review) ──→ BC5 (Export)
                    ↑                                    ↑
                    └─── BC7 (Admin) ──────────────────────┘

BC6 (Identity) ←── All contexts (authn/z)
```

## 3. Technology decisions (see also DOCS_TECH_STACK.md)

| Layer | Choice | Rationale |
|-------|--------|-----------|
| Backend language | Python 3.12 | AI/LLM ecosystem maturity; solo-dev-friendly |
| HTTP framework | FastAPI | Async-native, Pydantic validation, auto-docs |
| Database | PostgreSQL 16 + pgvector | Single DB for relational data + vector embeddings; reduced ops surface |
| Cache/queue | Redis 7 | Celery broker + caching + rate limiting |
| Frontend | React + Vite + TypeScript | Rich document review UI; component ecosystem |
| Auth | FastAPI Users + JWT | Self-contained; no external IdP dependency for V1 |
| File storage | MinIO | S3-compatible, self-hosted, no cloud dependency |
| Task queue | Celery | Document parsing, embedding, LLM calls; async offloading |
| LLM adapter | LiteLLM | Multi-provider abstraction; avoids vendor lock-in |
| Dev environment | Docker Compose | Single `docker compose up`; no per-dev tooling |

## 4. Tenant architecture

- **Model:** Multi-tenant SaaS with Row-Level Security (RLS)
- **Isolation:** Every table has `tenant_id`; RLS policies enforce per-tenant visibility
- **Connection pooling:** Single database, connection pool per app instance
- **Backup:** PostgreSQL dump per schedule (V1); no per-tenant backup

## 5. Security architecture

| Concern | Approach |
|---------|----------|
| Authn | JWT tokens via FastAPI Users; password hashing (bcrypt) |
| Authz | RBAC (roles: bid_manager, reviewer, supervisor, admin); RLS for tenant isolation |
| PII protection | Encryption at rest (PostgreSQL TDE + app-level for sensitive fields); no PII in logs |
| LLM data privacy | Non-training headers on provider API calls |
| Secrets | `.env` file (not committed); documented in `.env.example` |
| Rate limiting | Redis-backed per-tenant rate limits |

## 6. Data flow — key paths

### Upload → Draft (happy path)

```
1. User uploads PDF/DOCX to FastAPI endpoint
2. File stored in MinIO; metadata row created in PostgreSQL
3. Celery task triggered: parse with Unstructured.io + LibreOffice
4. Parsed questions/requirements written to PostgreSQL
5. RAG task triggered: for each question, query KB embeddings via pgvector
6. Draft generated via LiteLLM (prompt = question + context + instructions)
7. Draft stored per-question in PostgreSQL
8. Frontend polls/receives update → review UI renders
```

### Review → Export

```
1. User edits/approves per-question answers in React UI
2. Approver signs off → status changes to 'approved'
3. Export task generates DOCX via python-docx
4. File served as download
```

## 7. Performance targets (from doc 01 §5)

| Operation | Target | Bottleneck | Mitigation |
|-----------|--------|------------|------------|
| Upload + parse | <5 min | Document complexity, page count | Celery async; progress updates via WebSocket/SSE |
| AI draft per question | <60s | LLM latency, context size | LiteLLM streaming; model tiering per question |
| Full RFP draft | <30 min | RFP size (50–200 questions) | Parallel per-question generation |
| Availability | 99% uptime | Single-node Docker Compose | Health checks; restart policy; backup strategy |

## 8. Component responsibility matrix

| Component | BC1 | BC2 | BC3 | BC4 | BC5 | BC6 | BC7 |
|-----------|-----|-----|-----|-----|-----|-----|-----|
| FastAPI (routes) | Upload endpoint | KB CRUD APIs | Trigger RAG | Review APIs | Export trigger | Auth endpoints | Admin APIs |
| Celery (workers) | Parse | Embed | Generate draft | — | Build DOCX | — | — |
| PostgreSQL | Metadata | Entries + vectors | Vectors | Drafts | — | Users + roles | Config |
| MinIO | Files | Source files | — | — | Output files | — | — |
| Redis | — | — | — | — | — | — | Rate limits |
| React | Upload form | KB browser | — | Review UI | Download btn | Login/register | Admin panel |

## 9. Open architecture decisions

Referenced in [UNKNOWNS.md](../../UNKNOWNS.md):

| ID | Question | Blocked by | Required for |
|----|----------|------------|--------------|
| U1 | Max RFP page count for processing | — | Ingestion pipeline design |
| U2 | Embedding + chunking strategy | — | RAG quality |
| U3 | Fine-tuning vs RAG | U2 | LLM strategy |
| U7 | Concurrent user count for V1 | Owner decision | Scaling architecture |
| U8 | SOC2/GDPR compliance timeline | Owner decision | Compliance ADR |

## 10. Decisions register

| # | Decision | Status | Reference |
|---|----------|--------|-----------|
| 001 | Python + FastAPI | Proposed | DOCS_TECH_STACK.md |
| 002 | PostgreSQL + pgvector | Proposed | DOCS_TECH_STACK.md |
| 003 | React + Vite frontend | Proposed | DOCS_TECH_STACK.md |
| 004 | Multi-tenant RLS | Proposed | Doc 01 §9 |
| 005 | LiteLLM multi-provider | Proposed | Doc 01 §8 |
| 006 | Docker Compose deployment | Proposed | DOCS_TECH_STACK.md |

**Note:** These become formal ADRs in Phase 2.

## 11. Foundation gate readiness

### P1 GATE checklist

- [x] Scope doc (01) exists; uses **architecture foundation** wording
- [x] Architecture foundation doc (04) exists with bounded contexts + dependency direction
- [ ] 01↔02↔03↔04 cross-linked
- [ ] Integration manifest + mirror (if applicable)
- [x] Open questions explicit in `UNKNOWNS.md`
- [x] Initial risks in `RISK_REGISTRY.md`
