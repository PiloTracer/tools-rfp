# P1 — RFP Platform: adjacency foundation

**Product:** RFP Platform
**Status:** Draft (foundation doc 03)
**Updated:** 2025-07-17
**Cross-references:** [doc 01](20250717-01-rfp-platform-initial-scope.md) · [doc 02](20250717-02-rfp-platform-integration.md) · [doc 04](20250717-04-rfp-platform-arch-foundation.md)

---

## 1. Adjacent modules — V1 scope

**None confirmed.** The RFP Platform is a self-contained vertical application with no upstream/downstream dependencies on adjacent enterprise systems (CRM, accounting, inventory, BI) in V1.

### Explicitly out of scope for V1

| Module | Reason for exclusion | Future trigger |
|--------|---------------------|----------------|
| CRM sync | No pipeline integration needed at launch | Customer request for opportunity import |
| Accounting/ERP | No financial posting from RFP responses | Post-award workflow integration |
| BI/Reporting | In-app dashboards deferred | Customer demand for cross-RFP analytics |
| E-signature | Manual export sufficient for V1 | Volume increase |

## 2. Data flow boundaries

```
┌─────────────────────────────────────┐
│         RFP Platform (V1)           │
│                                     │
│  ┌──────────┐  ┌───────────────┐   │
│  │ Ingestion│→│    RAG + KB   │   │
│  └──────────┘  └───────┬───────┘   │
│                        ↓           │
│  ┌──────────┐  ┌───────────────┐   │
│  │  Export  │←│ Review/Approve │   │
│  └──────────┘  └───────────────┘   │
│                                     │
│  ┌──────────┐  ┌───────────────┐   │
│  │ Identity │  │   Admin       │   │
│  └──────────┘  └───────────────┘   │
└─────────────────────────────────────┘

External touchpoints (V1):
- LiteLLM API (outbound only)
```

## 3. Integration points (future)

When adjacencies are added, they connect via:

| Adjacent system | Integration point | Protocol |
|-----------------|------------------|----------|
| CRM | RFP import from CRM pipeline | REST webhook |
| BI | Export RFP response data | REST API / data export |
| E-signature | Trigger signing on approved export | Webhook callback |
