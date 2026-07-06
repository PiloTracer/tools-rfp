# P0 — RFP Platform: initial scope

**Product:** RFP Platform
**Status:** Draft (foundation doc 01)
**Updated:** 2025-07-17

---

## 1. Product intent (one sentence)

A self-hosted platform that receives, parses, and analyzes RFP documents, then generates a first-draft response grounded in the company's knowledge base, with a human review/approve workflow before final export.

### Founder intent (verbatim — P0 capture)

A self-hosted platform that receives, parses, and analyzes RFP documents, then generates a first-draft response grounded in the company's knowledge base, with a human review/approve workflow before final export.

### Measurable success criteria

| Criterion | Target | Label |
|-----------|--------|-------|
| Win rate improvement | Increase RFP win rate (baseline TBD) | Inference |
| Cost reduction | Lower cost per RFP response vs manual process | Inference |
| Volume throughput | Handle 10+ RFPs/month vs current ~3 | Inference |

## 2. Target users

| Role | Responsibility |
|------|---------------|
| **Bid Manager** | Uploads RFP, reviews AI draft, fills gaps, finalizes response |
| **Sales Supervisor** | Oversees responses, assigns reviewers, approves final output |
| **Reviewer / Approver** | Reviews sections, requests changes, signs off |
| **Admin** | Manages users, configures knowledge base, compliance rules, system settings |

### Primary user journeys

| # | Journey | Actors | Steps |
|---|---------|--------|-------|
| J1 | Upload & parse RFP | Bid Manager | Upload file → system parses → questions extracted → review queue |
| J2 | Generate AI draft | Bid Manager | Select RFP → AI generates per-question drafts → review flagged items |
| J3 | Review & approve | Reviewer → Supervisor | Review answers → request changes → approve → export |
| J4 | Manage knowledge base | Admin | Upload past proposals → chunk & embed → verify retrieval quality |
| J5 | Email import | Bid Manager | RFP arrives via email → auto-import → parse → draft |

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

## 3a. Bounded contexts (V1)

| # | Context | Responsibility |
|---|---------|---------------|
| BC1 | Document Ingestion | Upload, parse, extract RFP structure |
| BC2 | Knowledge Base | Store/retrieve past proposals, case studies |
| BC3 | RAG Engine | Embeddings, retrieval, draft generation |
| BC4 | Review Workflow | Per-question editing, approval, sign-off |
| BC5 | Export | DOCX generation, formatting |
| BC6 | Identity & Access | Users, roles, RBAC |
| BC7 | Administration | System config, KB mgmt, compliance rules |

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

## 5. Non-functional requirements (V1 targets)

| Category | Target | Source |
|----------|--------|--------|
| Upload + parse time | < 5 min per RFP | Probe iter-1 |
| AI draft per question | < 60s | Probe iter-1 |
| Full RFP draft generation | < 30 min | Probe iter-1 |
| Concurrent users | TBD (probe deferred) | — |
| Availability | 99% uptime | Probe iter-1 |
| Compliance | TBD (probe deferred) | — |

## 6. Deferred (post-V1)

- Collaborative real-time editing
- RFP opportunity scoring / bid-no-bid AI
- Public REST API
- SSO / SAML
- Analytics dashboard
- Multi-tenant (for SaaS variant)

## 7. Data model & sensitivity

### Core entities (V1)

| # | Entity | Key fields | Relationships |
|---|--------|------------|---------------|
| E1 | RFP Document | file, parsed structure, status, tenant_id | has many Questions |
| E2 | Question/Requirement | text, section, answer_draft_id, confidence | belongs to RFP; has one Draft Response |
| E3 | Knowledge Base Entry | content, embeddings, source_file, tenant_id | belongs to Tenant |
| E4 | Draft Response | answer_text, sources[], confidence_score | belongs to Question; references KB Entries |
| E5 | User | name, email, role, tenant_id | belongs to Tenant |
| E6 | Tenant | name, config, kb_scope | has many Users, KB Entries, RFPs |
| E7 | Compliance Rule | rule_text, scope, override_flag | belongs to Tenant |
| E8 | Approval | status, reviewer_id, timestamp, comments | belongs to RFP or Question |
| E9 | Previous Response | content, rfp_source, win_status | belongs to Tenant; feeds KB |
| E10 | Permission | resource, action, role/grantee | belongs to Tenant |

### PII & data sensitivity

| Category | PII present | Notes |
|----------|-------------|-------|
| Employee PII (names, emails, phone numbers) | Yes | Reviewers, approvers, bid managers |
| Business-sensitive financials | Yes | Pricing, cost proposals, margins in RFPs |
| Gov/regulatory identifiers | Yes | Certifications, compliance docs in RFPs |

**Encryption at rest:** PostgreSQL default + application-level for sensitive fields (TBD in ADR).
**Retention:** Indefinite at V1; defer auto-purge to post-V1.

## 8. External integrations (V1)

| Integration | Scope | Priority |
|-------------|-------|----------|
| Email import — Microsoft 365 | Inbound RFP via email | P1 |
| Email import — Google Workspace | Inbound RFP via email | P1 |
| Email import — Generic IMAP/SMTP | Inbound RFP via email | P1 |
| LLM provider | Multi-provider via LiteLLM (OpenAI, Anthropic, local) | P0 |
| Document signing | Deferred (post-V1) | — |

## 9. Constraints

| Category | Value | Source |
|----------|-------|--------|
| Team size | Solo/small (1–2 devs) | Probe iter-2 |
| Budget | Tight (<$5k/mo infra) | Probe iter-2 |
| Timeline | 1–2 months to V1 launch | Probe iter-2 |
| Deployment | Multi-tenant SaaS (RLS), Docker Compose | Probe iter-1 |
| LLM provider | Multi-provider via LiteLLM | Probe iter-1 |

**Implication:** 1–2 month timeline with solo/small team is aggressive for the 13-feature V1 scope. Recommend prioritizing P0 features only (features 1–7, 9, 10, 13) and deferring P1 items (8, 11, 12) or cutting further.

## 10. Key product assumptions

| # | Assumption | Label |
|---|------------|-------|
| A1 | B2B companies with RFP volume of 10+/year will pay for automation | Inference |
| A2 | RAG on past proposals produces useful first drafts | Inference |
| A3 | DOCX export is the primary output format customers expect | Inference |
| A4 | Self-hosted deployment is a purchase criterion for security-conscious buyers | Inference |
| A5 | AI accuracy + citation transparency builds the trust needed for adoption | Inference |

## 10. Open unknowns

| # | Unknown | Owner |
|---|---------|-------|
| U1 | What is the ceiling on RFP document page count for reasonable processing time? | eng |
| U2 | What embedding + chunking strategy works best for RFP-style structured docs? | eng |
| U3 | How much fine-tuning vs RAG is needed for domain-specific RFP terminology? | eng |
| U4 | What's an acceptable per-RFP processing cost at V1 scale? | product |
| U5 | What file size / page limits should the uploader enforce? | product |
