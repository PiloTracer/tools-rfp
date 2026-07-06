# RFP Platform

A self-hosted platform that receives, parses, and analyzes RFP documents, then generates a first-draft response grounded in your company's knowledge base, with a human review/approve workflow before final export.

---

## Quick start

```bash
# 1. Clone and configure
cp .env.example .env
# Edit .env: set POSTGRES_PASSWORD, JWT_SECRET, LITELLM_API_KEY, MINIO_SECRET_KEY

# 2. Start the stack
docker compose up -d

# 3. Open the dashboard
open http://localhost

# 4. Create an account, upload past proposals → upload an RFP → generate drafts
```

**Prerequisites:** Docker + Docker Compose

---

## Architecture

```
┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐
│  Upload  │ → │  Parse   │ → │  RAG     │ → │  Review  │ → │  Export  │
│  (API)   │   │ (Celery) │   │ (Celery) │   │  (React) │   │  (API)   │
└──────────┘   └──────────┘   └──────────┘   └──────────┘   └──────────┘
     │              │              │
     ▼              ▼              ▼
   MinIO        PostgreSQL      LiteLLM
   (files)      + pgvector      (LLM API)
```

**Stack:** Python/FastAPI, React/Vite, PostgreSQL 16 + pgvector, Redis, MinIO, Celery, LiteLLM

---

## Documentation

| Resource | Location |
|----------|----------|
| Foundation docs | `.work/plans/foundation/` |
| ADRs | `.work/decisions/` |
| Feature SPECs | `.work/features/` |
| Standards | `.work/standards/` |
| Session handoff | `.work/context/HANDOFF.md` |
| Tech stack | `DOCS_TECH_STACK.md` |

---

## Development

```bash
# Start dev stack
docker compose up -d

# Run tests
docker compose exec api pytest tests/ -q

# Run lint
docker compose exec api ruff check .

# Run type checker
docker compose exec api pyright .

# View logs
docker compose logs -f api worker
```

---

## Deployment

Single-server self-hosted via Docker Compose. See [compose proposal](.work/plans/operations/20250717-docker-compose-proposal.md) for resource requirements (~4 cores, 8GB RAM).

```bash
# Production
docker compose up -d
# Health check
curl http://localhost/health/ready
```
