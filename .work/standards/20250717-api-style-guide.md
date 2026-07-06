# RFP Platform — API style guide

**Status:** Draft · **Updated:** 2025-07-17
**Cross-ref:** ADR-001 (FastAPI), CONVENTIONS

---

## 1. URL conventions

```
Base URL: /v1

/v1/{resource}              # List
/v1/{resource}/{id}         # Get single
/v1/{resource}/{id}/actions/{action}  # Action (non-CRUD)
```

### Examples

| Purpose | Path |
|---------|------|
| List RFPs | `GET /v1/rfps` |
| Get RFP detail | `GET /v1/rfps/{rfp_id}` |
| Upload RFP | `POST /v1/rfps/actions/upload` |
| List questions | `GET /v1/rfps/{rfp_id}/questions` |
| Generate draft | `POST /v1/rag/generate` |
| Export approved | `POST /v1/rfps/{rfp_id}/actions/export` |
| List KB entries | `GET /v1/kb` |
| Login | `POST /v1/auth/login` |

### Naming rules

- Resources: **plural nouns** (`/rfps`, `/questions`, `/kb-entries`)
- Actions: **verbs** under `/actions/{action}` for non-CRUD operations
- Kebab-case for multi-word resources: `/kb-entries`, `/knowledge-base`
- No underscores in URL paths

## 2. Standard response format

### Success
```json
{
  "data": { ... },
  "meta": {
    "request_id": "req_abc123",
    "timestamp": "2025-07-17T12:00:00Z"
  }
}
```

### List with pagination
```json
{
  "data": [ ... ],
  "meta": {
    "request_id": "req_abc123",
    "timestamp": "2025-07-17T12:00:00Z",
    "page": 1,
    "per_page": 20,
    "total": 142,
    "total_pages": 8
  }
}
```

### Error
```json
{
  "error": {
    "code": "RAG_PROVIDER_UNAVAILABLE",
    "message": "All LLM providers in fallback chain failed",
    "details": {}
  },
  "meta": {
    "request_id": "req_abc123",
    "timestamp": "2025-07-17T12:00:00Z"
  }
}
```

## 3. Pagination

| Parameter | Default | Max | Notes |
|-----------|---------|-----|-------|
| `page` | 1 | — | 1-indexed |
| `per_page` | 20 | 100 | — |

Response includes `Link` header for prev/next:
```
Link: </v1/rfps?page=2&per_page=20>; rel="next", </v1/rfps?page=1&per_page=20>; rel="prev"
```

## 4. Error codes

| HTTP | Code | When |
|------|------|------|
| 400 | `VALIDATION_ERROR` | Request body validation failed |
| 401 | `UNAUTHORIZED` | Missing or expired JWT |
| 403 | `FORBIDDEN` | Authenticated but insufficient role |
| 404 | `NOT_FOUND` | Resource doesn't exist |
| 409 | `CONFLICT` | Idempotency key conflict, duplicate |
| 422 | `UNPROCESSABLE_ENTITY` | Business logic rejection (e.g., PII detected) |
| 429 | `RATE_LIMITED` | Per-tenant rate limit exceeded |
| 500 | `INTERNAL_ERROR` | Unhandled server error |
| 503 | `SERVICE_UNAVAILABLE` | Provider down, dependency unavailable |

## 5. Authentication

| Scheme | Where | Notes |
|--------|-------|-------|
| Bearer JWT | `Authorization: Bearer <token>` | Access token (15min expiry) |
| Refresh token | `POST /v1/auth/refresh` | HTTP-only cookie or body (7d expiry) |

All endpoints require JWT except:
- `POST /v1/auth/login`
- `POST /v1/auth/register`
- `GET /health/live`
- `GET /health/ready`

## 6. Content types

| Operation | Request | Response |
|-----------|---------|----------|
| CRUD | `application/json` | `application/json` |
| File upload | `multipart/form-data` | `application/json` |
| Export | — | `application/vnd.openxmlformats-officedocument.wordprocessingml.document` |

## 7. Idempotency

| Method | Idempotent | Notes |
|--------|------------|-------|
| GET | Yes | Safe |
| PUT | Yes | Full replace |
| PATCH | Yes | Partial update |
| DELETE | Yes | Idempotent (404 on second call is correct) |
| POST | No | Use `Idempotency-Key` header for retry-safe actions |

For `POST` actions that could be retried (e.g., generate draft), clients send:
```
Idempotency-Key: <uuid>
```
Server deduplicates within 24h.

## 8. Rate limiting

- **Scope:** Per-tenant
- **Default:** 100 req/min per tenant
- **Headers returned:**
  - `X-RateLimit-Limit`
  - `X-RateLimit-Remaining`
  - `X-RateLimit-Reset`
- **429 response:** Returns `Retry-After` header (seconds)
