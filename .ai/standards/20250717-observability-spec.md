# RFP Platform — Observability spec

**Status:** Draft · **Updated:** 2025-07-17
**Cross-ref:** Foundation doc 04 §7 (performance targets), RAG Engine SPEC §10

---

## 1. Logging

### Format
Structured JSON logs. Every log line includes:

```json
{
  "timestamp": "2025-07-17T12:00:00Z",
  "level": "info|warn|error",
  "logger": "app.rag.service",
  "request_id": "req_abc123",
  "tenant_id": "tenant_xyz",
  "user_id": "user_001",
  "message": "Generated draft for question Q-42",
  "extra": { ... }
}
```

### Log levels

| Level | When | Examples |
|-------|------|----------|
| `debug` | Development only | SQL queries, request payloads |
| `info` | Normal operations | RFP uploaded, draft generated, export completed |
| `warn` | Recoverable anomalies | Provider fallback triggered, slow query >1s, rate limit approaching |
| `error` | Operation failure, no data loss | Provider unreachable, Celery task failed, parse error |

### Mandatory fields
- `request_id` — correlation ID across FastAPI + Celery (propagated via header)
- `tenant_id` — always, even on error (tells which tenant was affected)
- `duration_ms` — for request-scoped operations
- `component` — which BC or service (ingestion, rag, export, auth)

### Anti-patterns
- No PII in log fields (use entity IDs, not names/emails)
- No secrets in logs (API keys, tokens, passwords)
- No unbounded payload logging (truncate to 1KB)

## 2. Metrics

### Application metrics (exposed via `/metrics` — Prometheus)

| Metric | Type | Labels | Source |
|--------|------|--------|--------|
| `http_requests_total` | Counter | method, path, status | FastAPI middleware |
| `http_request_duration_ms` | Histogram | method, path | FastAPI middleware |
| `celery_tasks_total` | Counter | task_name, status | Celery hooks |
| `celery_task_duration_ms` | Histogram | task_name | Celery hooks |
| `rag_generation_total` | Counter | provider, status | RAG service |
| `rag_generation_duration_ms` | Histogram | provider, model | RAG service |
| `rag_confidence_distribution` | Histogram | — | RAG service |
| `rag_tokens_per_request` | Histogram | provider, model | RAG service |
| `rag_kb_query_duration_ms` | Histogram | — | RAG service |
| `rag_zero_context_count` | Counter | — | RAG service |
| `ingestion_parse_duration_ms` | Histogram | file_type | Ingestion service |
| `ingestion_file_size_bytes` | Histogram | file_type | Ingestion service |
| `db_connection_pool_size` | Gauge | — | DB middleware |
| `redis_memory_usage_bytes` | Gauge | — | Redis monitor |

### Business metrics

| Metric | Source | Purpose |
|--------|--------|---------|
| RFPs uploaded per day | Ingestion counter | Volume tracking |
| Drafts generated per day | RAG counter | Usage tracking |
| Average confidence score | RAG histogram | Quality trend |
| Export count per day | Export counter | Output tracking |
| Provider token spend ($) | LiteLLM cost tracking | Budget monitoring |

## 3. Tracing

- **Recommended:** OpenTelemetry auto-instrumentation for FastAPI + Celery
- **Trace propagation:** `trace_id` header passed from FastAPI → Celery tasks
- **Key spans:** DB queries, LiteLLM calls, file parsing, embedding generation
- **V1:** Console-exported traces; OpenTelemetry collector + Jaeger deferred to post-V1

## 4. Health checks

| Endpoint | Checks | Response |
|----------|--------|----------|
| `/health/live` | App process alive | `{"status": "ok"}` |
| `/health/ready` | DB reachable, Redis reachable, MinIO reachable | `{"status": "ok"}` or `{"status": "degraded", "components": {...}}` |

Used by Docker Compose health checks + load balancer (post-V1).

## 5. Alerting (V1 — manual)

No automated alerting in V1. Operators monitor via:
- `docker compose logs` tail
- Prometheus metrics scraped ad-hoc
- LiteLLM daily cost report

Post-V1: Alertmanager + PagerDuty/webhook integration.
