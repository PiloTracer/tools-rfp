# Foundation probe ledger

**Updated:** 2025-07-17 · **Iterations:** 2 · **Coverage:** 80% (target 85%)

| Dim | Topic | Status | Conf | Evidence / source | Iter |
|-----|-------|--------|------|-------------------|------|
| D1 ★ | Product intent & success | confirmed | high | doc 01 §1 — verbatim founder intent + 3 measurable success criteria (win rate, cost, volume) | 2 |
| D2 | Audience / personas | confirmed | high | doc 01 §2 — 4 roles named + 5 primary user journeys mapped | 2 |
| D3 ★ | Scope in / out | confirmed | high | doc 01 §4–5 — 13 V1 features with priority; deferred list explicit | 1 |
| D4 | Functional capabilities | confirmed | high | doc 01 §3a — 7 bounded contexts mapped (Ingestion, KB, RAG, Review, Export, Identity, Admin) | 2 |
| D5 ★ | NFRs | partial | med | doc 01 §5 — relaxed perf targets; 99% uptime; concurrency (U7) + compliance (U8) deferred | 1 |
| D6 | Integrations & ext deps | confirmed | high | doc 01 §8 + MANIFEST.txt — email (M365, Google, IMAP), LiteLLM multi-provider; manifest created | 2 |
| D7 | Data model & sensitivity | confirmed | high | doc 01 §7 — 10 entities with relationships and PII classification | 2 |
| D8 | Constraints | confirmed | high | doc 01 §9 — solo/small team, tight budget, 1–2 month timeline; scope prioritization flagged | 2 |
| D9 ★ | Deploy / hosting / tenancy | partial | med | Multi-tenant SaaS (RLS) confirmed; Docker Compose; no formal ADR yet → blocks P2 | 1 |
| D10 ★ | Risks & assumptions | partial | med | 17 assumptions (13 Confirmed); 14 risks (4 Open); 10 unknowns | 2 |

## Open probes (carried to next iteration)
- D9 ★: Formal hosting/tenancy ADR needed in P2 → blocks plan-master-ready
- D5 ★: Concurrent user count (U7) and compliance (U8) still open → owner decisions needed

## Deferred (→ UNKNOWNS)
- U7: Concurrent user count for V1 · owner=eng · blocks=scaling architecture
- U8: SOC2/GDPR compliance at launch or deferred · owner=legal/product · blocks=compliance ADR
- U9: V1 scope too large for timeline — which features to cut? · owner=product · blocks=feature prioritization
- U10: Baseline metrics for success measurement · owner=product · blocks=success criteria validation
