# RFP Platform — Data classification standard

**Status:** Draft · **Updated:** 2025-07-17
**Cross-ref:** Foundation doc 01 §7 (data model), Threat model (T6)

---

## 1. Classification levels

| Level | Label | Examples | Handling |
|-------|-------|----------|----------|
| **L1** | Public | Product name, docs, marketing copy | No restrictions |
| **L2** | Internal | Tenant configuration, feature flags, usage stats | In-cluster access only |
| **L3** | Confidential | KB entries, RFP content, draft responses, user emails | Encrypted at rest; RLS-enforced; no PII in logs |
| **L4** | Restricted | API keys, JWT secrets, DB credentials, encryption keys | Environment variables only; never logged; never in source |

## 2. Entity classification (from foundation doc 01 §7)

| Entity | Level | PII present | Notes |
|--------|-------|-------------|-------|
| RFP Document | L3 | Yes (employee + business financials) | PII is content, not structural |
| Question/Requirement | L3 | Possibly | Content-dependent |
| KB Entry | L3 | Possibly | Content of past proposals |
| Draft Response | L3 | Possibly | Generated content |
| User | L3 | Yes (name, email) | Email is PII under GDPR |
| Tenant | L2 | No | Org name, config |
| Compliance Rule | L2 | No | Policy text |
| Approval | L3 | Yes (reviewer identity) | Timestamp + user ID |
| Previous Response | L3 | Yes | Past RFP responses |
| Permission | L2 | No | Role-to-action mapping |

## 3. Handling rules by level

### L3 — Confidential (most application data)

| Concern | Rule |
|---------|------|
| Storage | Encrypted at rest (PostgreSQL TDE + app-level encryption for sensitive fields) |
| Access | RLS per tenant; authenticated JWT required |
| Transmission | TLS 1.2+ in transit |
| Logging | Never log raw field content; log entity ID + action only |
| Export | DOCX exports carry same classification — tenant responsibility after download |
| Retention | Indefinite in V1; auto-purge deferred to post-V1 (documented in UNKNOWNS) |
| Backup | Encrypted backups; same retention as primary |

### L4 — Restricted (secrets)

| Concern | Rule |
|---------|------|
| Storage | Environment variables only (`POSTGRES_PASSWORD`, `JWT_SECRET`, `LITELLM_API_KEY`) |
| Access | Never in code; never in logs; never in error messages |
| Rotation | Keys rotated on compromise; password rotation documented in ops runbook |
| CI/CD | GitHub Actions secrets for CI; never in build artifacts |

## 4. PII identification

The following PII types may appear in RFP Platform data:

| Type | Where | GDPR relevance |
|------|-------|----------------|
| Name | User accounts, RFP content | Direct identifier |
| Email | User accounts, email import | Direct identifier |
| Phone | RFP content (employee contact info) | Direct identifier |
| Financial data | RFP content (pricing, cost proposals) | Business-sensitive (not personal under GDPR) |
| Gov IDs | RFP content (certifications, compliance) | May contain personal identifiers |

**Application-level PII:** User name/email stored in `identity` context — encrypted at rest.

**Content-level PII:** RFP documents and KB entries — treated as L3; application does not scan or redact PII in V1 (deferred to compliance rulebook SPEC, P1).
