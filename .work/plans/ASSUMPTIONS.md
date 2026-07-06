# ASSUMPTIONS - planning registry

**Updated:** 2025-07-17 · **Maintained by:** plan-foundation / plan-master

Label every entry: **Confirmed** | **Inference** | **Unverified** | **Rejected**

| ID | Assumption | Label | Source | Notes |
|----|------------|-------|--------|-------|
| A1 | RFP Platform targets B2B companies with RFP volume 10+/year | Inference | foundation doc 01 | |
| A2 | RAG on past proposals produces useful first drafts | Inference | foundation doc 01 | |
| A3 | DOCX export is the primary output format customers expect | Inference | foundation doc 01 | |
| A4 | Self-hosted deployment is a purchase criterion for security-conscious buyers | Inference | foundation doc 01 | |
| A5 | AI accuracy + citation transparency builds the trust needed for adoption | Inference | foundation doc 01 | |
| A6 | Dev workflow follows `.cursorrules` (Docker or documented local CI) | Confirmed | `.cursorrules` | |
| A7 | V1 targets relaxed NFRs: <5min parse, <60s/question, <30min full draft | Confirmed | Probe iter-1 user answer | |
| A8 | 99% uptime acceptable for V1 (not 99.9%) | Confirmed | Probe iter-1 user answer | |
| A9 | Multi-tenant SaaS with RLS from day one (not single-tenant) | Confirmed | Probe iter-1 user answer | |
| A10 | RFPs contain employee PII, business financials, and gov/regulatory identifiers | Confirmed | Probe iter-1 user answer | |
| A11 | LiteLLM multi-provider abstraction for LLM calls (not single vendor lock-in) | Confirmed | Probe iter-1 user answer | |
| A12 | Email import via Microsoft 365, Google Workspace, and generic IMAP/SMTP | Confirmed | Probe iter-1 user answer | |
| A13 | Success criteria: win rate improvement, cost reduction, volume throughput | Confirmed | Probe iter-2 user answer | Specific targets TBD (baseline measurement needed) |
| A14 | 7 bounded contexts: Ingestion, KB, RAG, Review, Export, Identity, Admin | Confirmed | Probe iter-2 user answer | |
| A15 | 10 core entities including Approval, Previous Response, Permission | Confirmed | Probe iter-2 user answer | |
| A16 | Solo/small team (1–2 devs), tight budget (<$5k/mo), 1–2 month timeline | Confirmed | Probe iter-2 user answer | Aggressive scope — may need cuts |
| A17 | Scope should prioritize P0 features only (1–7, 9, 10, 13); defer P1 (8, 11, 12) | Inference | Probe iter-2 agent analysis | Based on timeline constraint |

| A18 | English + Spanish i18n sufficient for V1 bilingual teams | Inference | ADR-007 | |
| A19 | pgvector ANN search is performant enough for <100K KB chunks at V1 | Inference | ADR-002 | |
| A20 | RAG with LiteLLM multi-provider is the right abstraction for draft generation | Confirmed | ADR-005 | |

## Rejected

| ID | Assumption | Reason |
|----|------------|--------|
| - | (none) | |

## Review log

| Date | Reviewer | Action |
|------|----------|--------|
| 2025-07-17 | plan-foundation | Initial populate from greenfield P0 |