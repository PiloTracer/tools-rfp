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

## Review log

| Date | Reviewer | Action |
|------|----------|--------|
| 2025-07-17 | plan-foundation | Initial populate from greenfield P0 |