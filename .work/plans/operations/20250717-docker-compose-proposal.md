# Docker Compose proposal — RFP Platform

**Status:** Draft (pending approval)
**Updated:** 2025-07-17
**Cross-ref:** DOCS_TECH_STACK.md, ADR-006 (Docker Compose deployment)

---

## 1. Service architecture

```
┌─────────────────────────────────────────────────────────────┐
│  docker-compose.yml                                         │
│                                                             │
│  ┌──────────────┐    ┌──────────────┐    ┌───────────────┐  │
│  │   Traefik    │───→│    api       │───→│  postgres     │  │
│  │  (reverse    │    │  (FastAPI)   │    │  (:5432)      │  │
│  │   proxy)     │    └──────┬───────┘    └───────────────┘  │
│  │  (:80, :443) │           │                               │
│  └──────────────┘    ┌──────▼───────┐    ┌───────────────┐  │
│                      │    worker    │───→│   redis       │  │
│                      │  (Celery)    │    │  (:6379)      │  │
│                      └──────┬───────┘    └───────────────┘  │
│                             │                               │
│                      ┌──────▼───────┐    ┌───────────────┐  │
│                      │   minio      │    │  dashboard    │  │
│                      │  (:9000)     │    │  (Vite build) │  │
│                      └──────────────┘    │  (:80)        │  │
│                                          └───────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## 2. Service definitions

### api (FastAPI)
| Field | Value |
|-------|-------|
| **Image** | `rfp-api:latest` (built from `Dockerfile.api`) |
| **Port** | `8000` (internal; exposed via Traefik) |
| **Depends on** | postgres, redis, minio (healthy) |
| **Health check** | `GET /health/live` |
| **Scale** | 1 replica (V1); horizontal in post-V1 |
| **Env** | `DATABASE_URL`, `REDIS_URL`, `MINIO_ENDPOINT`, `JWT_SECRET`, `LITELLM_API_KEY` |

### worker (Celery)
| Field | Value |
|-------|-------|
| **Image** | `rfp-worker:latest` (built from `Dockerfile.api` — same base) |
| **Port** | None (internal) |
| **Command** | `celery -A app.core.celery_app worker --loglevel=info` |
| **Depends on** | postgres, redis, minio (healthy) |
| **Scale** | 1 replica (V1) |
| **Env** | Same as `api` |

### dashboard (React + Vite)
| Field | Value |
|-------|-------|
| **Image** | `rfp-dashboard:latest` (built from `Dockerfile.dashboard`) |
| **Port** | `80` (Nginx serving static build) |
| **Health check** | `GET /` (Nginx status) |
| **Scale** | 1 replica |

### postgres
| Field | Value |
|-------|-------|
| **Image** | `postgres:16-alpine` |
| **Port** | `5432` (internal only) |
| **Volume** | `pgdata:/var/lib/postgresql/data` |
| **Env** | `POSTGRES_DB=rfp`, `POSTGRES_USER=rfp`, `POSTGRES_PASSWORD=${POSTGRES_PASSWORD}` |
| **Health check** | `pg_isready -U rfp` |
| **Extensions** | pgvector enabled via init script |

### redis
| Field | Value |
|-------|-------|
| **Image** | `redis:7-alpine` |
| **Port** | `6379` (internal only) |
| **Volume** | `redisdata:/data` |
| **Health check** | `redis-cli ping` |

### minio
| Field | Value |
|-------|-------|
| **Image** | `minio/minio:latest` |
| **Port** | `9000` (API), `9001` (console) |
| **Command** | `server /data --console-address ":9001"` |
| **Volume** | `miniodata:/data` |
| **Env** | `MINIO_ROOT_USER`, `MINIO_ROOT_PASSWORD` |
| **Health check** | `curl -f http://localhost:9000/minio/health/live` |

### traefik (reverse proxy)
| Field | Value |
|-------|-------|
| **Image** | `traefik:v3.0` |
| **Port** | `80` (HTTP), `443` (HTTPS — optional) |
| **Config** | Static config via CLI args; dynamic config via Docker labels |
| **Purpose** | Route `/api/*` → api:8000, `/` → dashboard:80 |

## 3. Port map

| Host port | Target | Service |
|-----------|--------|---------|
| `80` | `80` | traefik (HTTP) |
| `443` | `443` | traefik (HTTPS — optional, cert via Let's Encrypt) |
| `9000` | `9000` | minio (S3 API — internal only in prod) |
| `9001` | `9001` | minio (console — dev only) |

All inter-service communication uses Docker internal networking (no host port exposure for postgres, redis, api, worker).

## 4. Volumes

| Volume | Services | Purpose |
|--------|----------|---------|
| `pgdata` | postgres | Persistent DB storage |
| `redisdata` | redis | Persistent cache |
| `miniodata` | minio | File storage (RFPs, KB files, exports) |

## 5. Environment variables

### `.env.example` (committed)

```bash
# Secrets (set in production)
POSTGRES_PASSWORD=change_me
JWT_SECRET=change_me
LITELLM_API_KEY=sk-...

# Configurable
LITELLM_PROVIDER=openai
LITELLM_MODEL=gpt-4o
RFP_MAX_UPLOAD_MB=50
CELERY_CONCURRENCY=4
RATE_LIMIT_PER_MIN=100

# Defaults (rarely changed)
POSTGRES_DB=rfp
POSTGRES_USER=rfp
REDIS_URL=redis://redis:6379/0
MINIO_ENDPOINT=minio:9000
MINIO_ACCESS_KEY=rfp_access
DATABASE_URL=postgresql+asyncpg://rfp:${POSTGRES_PASSWORD}@postgres:5432/rfp
```

## 6. Startup order

```
1. postgres, redis, minio         (data layer)
2. api, worker                    (app layer — wait for data layer healthy)
3. dashboard                      (frontend — served by Nginx)
4. traefik                        (reverse proxy — routes traffic)
```

## 7. Resource limits

| Service | CPU | Memory |
|---------|-----|--------|
| api | 0.5 cores | 512MB |
| worker | 1.0 cores | 1GB |
| postgres | 1.0 cores | 1GB |
| redis | 0.25 cores | 256MB |
| minio | 0.5 cores | 512MB |
| dashboard | 0.1 cores | 128MB |
| traefik | 0.1 cores | 128MB |
| **Total** | **~3.5 cores** | **~3.5GB** |

Fits within a $20–40/mo VPS (4 cores, 8GB RAM) at Hetzner/OVH/Linode.

## 8. Approval request

Review and approve to create:
- `docker-compose.yml`
- `Dockerfile.api`
- `Dockerfile.dashboard`
- `.env.example`
- Update HANDOFF + NEXT
