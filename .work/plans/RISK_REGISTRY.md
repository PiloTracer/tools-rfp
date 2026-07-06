# RISK_REGISTRY - planning registry

**Updated:** 2025-07-17 · **Maintained by:** plan-foundation / plan-master

Status: **Open** | **Mitigated** | **Accepted** | **Closed**

| ID | Risk | Category | Likelihood | Impact | Mitigation | Status | Owner |
|----|------|----------|------------|--------|------------|--------|-------|
| R1 | AI hallucination in generated RFP responses | AI | M | H | Grounding in RAG sources; confidence thresholds; human review gate | Mitigated | eng |
| R2 | Scope creep before foundation complete | process | M | M | plan-foundation gates; no broad coding until implementation-ready | Open | eng |
| R3 | Agent marks gate pass without evidence | process / agent | M | M | `.cursorrules` Completion Gate; code-verify | Mitigated | eng |
| R4 | Secrets committed to git | security | L | H | `.cursorrules` secrets scan; pre-commit hooks | Open | eng |
| R5 | RFP parsing fails on complex/scanned documents | technical | M | H | Multi-parser fallback chain; OCR via Tesseract | Mitigated | eng |
| R6 | LLM API cost exceeds sustainable budget per RFP | operational | M | M | Per-operation model tiering (cheap models for parsing); user-configurable; fallback to local models | Mitigated | eng |
| R7 | RFP document exceeds LLM context limits | technical | M | M | Chunking + hierarchical summarization before generation | Mitigated | eng |
| R8 | Knowledge base too large for efficient retrieval | technical | M | M | Hierarchical retrieval (summary → relevant section → chunk) | Open | eng |
| R9 | Customer data leaves self-hosted deployment | compliance | L | H | Fully self-hosted; all data in PostgreSQL + MinIO; API calls opt-in with non-training headers | Mitigated | eng |
| R10 | Compliance rulebook contradicts AI-generated content | compliance | M | H | Compliance rulebook loaded as override facts in RAG; second-pass compliance check | Open | eng |
| R11 | Multi-tenant RLS misconfiguration leaks data across tenants | security | L | H | Strict RLS policies; automated tenant isolation tests; row-level audit logging | Open | eng |
| R12 | LiteLLM abstraction adds latency overhead per LLM call | performance | M | M | Connection pooling; async calls; per-provider timeout tuning | Open | eng |
| R13 | Email integration auth tokens expire / OAuth scopes too broad | security | M | M | Token refresh logic; minimal scope requests; rotate-on-error | Open | eng |
| R14 | 13-feature V1 scope too large for 1–2 month solo/small team timeline | process | H | H | Ruthlessly prioritize P0 features; cut P1; consider phased launch | Open | product |

| R15 | Prompt injection via RFP question text | AI | M | H | System prompt restricts instruction override; human review gate | Mitigated | eng |
| R16 | RAG produces plausible-sounding but incorrect answer | AI | M | H | Source citations required; confidence threshold flagging; human review gate | Mitigated | eng |
| R17 | Embedding model produces poor retrievals for domain-specific RFP terminology | AI | M | M | Chunking strategy iteration; U2/U3 investigation needed | Open | eng |
| R18 | LLM API cost exceeds $5k/mo budget at V1 scale | operational | M | H | Model tiering (cheap for parsing, capable for generation); LiteLLM cost tracking | Mitigated | eng |
| R19 | Single Celery worker becomes bottleneck during RFP burst | performance | L | M | Acceptable for V1; add worker replica documented as post-V1 scaling path | Open | eng |

| R20 | Frontend bundles grow too large for acceptable load time | technical | L | M | Route-based lazy loading; code-splitting at page level | Mitigated | eng |
| R21 | Observability gaps obscure production issues | operational | M | M | Per-context metrics defined (observability spec); logging + health checks in V1; alerting deferred | Open | eng |

| R22 | Single Docker host is SPOF for production | operations | L | M | Acceptable for V1 99% uptime; backup + restore documented; post-V1: multi-host orchestration | Accepted | eng |
| R23 | No zero-downtime deploys in V1 | operations | L | M | Accepted for V1; deploy window documented in ops runbook | Accepted | eng |

## Review log

| Date | Reviewer | Action |
|------|----------|--------|
| 2025-07-17 | plan-foundation | Initial populate from greenfield P0 |