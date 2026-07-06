# P1 — RFP Platform: integration foundation

**Product:** RFP Platform
**Status:** Draft (foundation doc 02)
**Updated:** 2025-07-17
**Cross-references:** [doc 01](20250717-01-rfp-platform-initial-scope.md) §8 · [doc 03](20250717-03-rfp-platform-adjacency.md) · [doc 04](20250717-04-rfp-platform-arch-foundation.md)

---

## 1. External integrations (V1 scope)

| Integration | Scope | Priority | Auth model | Notes |
|-------------|-------|----------|------------|-------|
| LLM provider — LiteLLM | AI draft generation | P0 | API key per provider | Abstraction layer; supports OpenAI, Anthropic, local |
| Email — Microsoft 365 | Inbound RFP auto-import | P1 | OAuth 2.0 (MS Graph) | Deferred to post-V1 |
| Email — Google Workspace | Inbound RFP auto-import | P1 | OAuth 2.0 (Gmail API) | Deferred to post-V1 |
| Email — Generic IMAP/SMTP | Inbound RFP auto-import | P1 | Username + password / app password | Deferred to post-V1 |
| Document signing | E-signature on exports | Post-V1 | — | Out of scope for V1 |

## 2. Integration dependency map

```
┌─────────────────┐     LiteLLM API     ┌──────────────────┐
│  RFP Platform    │ ──────────────────→ │  LLM Providers    │
│  (self-hosted)   │                     │  (OpenAI, etc.)   │
│                  │                     │                   │
│  Docker Compose  │     (Email P1)      │                   │
│  stack           │ ──────────────────→ │  M365 / Gmail API │
│                  │                     │                   │
│  MinIO (S3)      │     (local)         │                   │
│  PostgreSQL      │     (local)         └──────────────────┘
└─────────────────┘
```

### V1 dependency profile (P0 only)
- **LiteLLM HTTP client** — the only outbound external call in V1
- MinIO, PostgreSQL, Redis — all co-located in Docker Compose

### P1 deferred
- Email OAuth import (M365 / Gmail / IMAP)

## 3. LiteLLM integration design

| Concern | Decision | Rationale |
|---------|----------|-----------|
| Client lib | LiteLLM Python SDK | Standard; handles retries, fallback, cost tracking |
| Provider config | Per-tenant via Admin UI | Multi-provider flexibility |
| Non-training header | `openai-organization:` (OpenAI) | Prevents customer data from being used for training |
| Fallback | Provider → configurable fallback chain | Graceful degradation |
| Timeout | Configurable per provider | Avoids stuck workers |

## 4. Integration manifest

See `.work/docs/integration/MANIFEST.txt` for mirrored vendor artifacts.

| Vendor | Resource | Version | Mirrored |
|--------|----------|---------|----------|
| LiteLLM | SDK docs | latest | No (live docs) |
| OpenAI | API reference | latest | No (live docs) |
| Anthropic | API reference | latest | No (live docs) |

## 5. Open questions

Referenced in [UNKNOWNS.md](../../UNKNOWNS.md):
- U4: Acceptable per-RFP processing cost (drives provider price tier selection)
