# P0 — RFP Platform: initial scope

**Product:** RFP Platform
**Status:** Draft (foundation doc 01)
**Updated:** 2025-07-17

---

## 1. Product intent (one sentence)

A self-hosted platform that receives, parses, and analyzes RFP documents, then generates a first-draft response grounded in the company's knowledge base, with a human review/approve workflow before final export.

## 2. Target users

| Role | Responsibility |
|------|---------------|
| **Bid Manager** | Uploads RFP, reviews AI draft, fills gaps, finalizes response |
| **Sales Supervisor** | Oversees responses, assigns reviewers, approves final output |
| **Reviewer / Approver** | Reviews sections, requests changes, signs off |
| **Admin** | Manages users, configures knowledge base, compliance rules, system settings |

## 3. Core workflow (V1)

```
1. Company uploads past proposals + case studies → Knowledge Base
2. Company receives RFP → uploads (PDF/DOCX/XLSX/TXT/ODT) or email import
3. AI parses document → extracts requirements/questions
4. AI runs RAG against Knowledge Base → generates first draft
5. Draft appears in review UI with per-question answers
6. AI flags missing / low-confidence items
7. Bid Manager edits answers, adds missing info
8. Reviewer/Approver reviews and approves
9. Final response exported as DOCX
```

## 4. V1 features (P0)

| # | Feature | Priority |
|---|---------|----------|
| 1 | Manual RFP upload (PDF, DOCX, XLSX, TXT, ODT) | P0 |
| 2 | Document parsing + structure extraction | P0 |
| 3 | Knowledge base CRUD (upload past proposals, case studies) | P0 |
| 4 | AI first-draft generation via RAG | P0 |
| 5 | Per-question review UI with source citations | P0 |
| 6 | Missing/uncertain answer flagging | P0 |
| 7 | User edit & override of AI answers | P0 |
| 8 | Reviewer/approver workflow | P1 |
| 9 | Admin panel (user mgmt, KB mgmt, config) | P0 |
| 10 | DOCX export of reviewed response | P0 |
| 11 | Email integration (auto-import RFP) | P1 |
| 12 | Compliance rulebook enforcement | P1 |
| 13 | Role-based access control (RBAC) | P0 |

## 5. Deferred (post-V1)

- Collaborative real-time editing
- RFP opportunity scoring / bid-no-bid AI
- Public REST API
- SSO / SAML
- Analytics dashboard
- Multi-tenant (for SaaS variant)

## 6. Key product assumptions

| # | Assumption | Label |
|---|------------|-------|
| A1 | B2B companies with RFP volume of 10+/year will pay for automation | Inference |
| A2 | RAG on past proposals produces useful first drafts | Inference |
| A3 | DOCX export is the primary output format customers expect | Inference |
| A4 | Self-hosted deployment is a purchase criterion for security-conscious buyers | Inference |
| A5 | AI accuracy + citation transparency builds the trust needed for adoption | Inference |

## 7. Open unknowns

| # | Unknown | Owner |
|---|---------|-------|
| U1 | What is the ceiling on RFP document page count for reasonable processing time? | eng |
| U2 | What embedding + chunking strategy works best for RFP-style structured docs? | eng |
| U3 | How much fine-tuning vs RAG is needed for domain-specific RFP terminology? | eng |
| U4 | What's an acceptable per-RFP processing cost at V1 scale? | product |
| U5 | What file size / page limits should the uploader enforce? | product |
