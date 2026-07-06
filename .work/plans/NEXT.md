# NEXT - planning backlog

**Updated:** 2026-07-06

---

## Done

| Item | Artifact |
|------|----------|
| Agent OS bootstrap | `.work/` skeleton, `.cursorrules` from template |
| Foundation P0 (initial scope) | `.work/plans/foundation/20250717-01-rfp-platform-initial-scope.md` |
| Foundation probe (2 iterations) | Coverage 80% — D1–D4, D6–D8 confirmed; D5, D9, D10 partial |
| Foundation P1 (exploration) | Docs 02 (integration), 03 (adjacency), 04 (architecture foundation) created; 01↔02↔03↔04 cross-linked |
| Foundation P2 (ADRs) | 7 ADRs created (stack, DB, frontend, tenancy, LiteLLM, deploy, locales) |
| Foundation P3 (SPECs) | CONVENTIONS, FEATURE_STANDARD, DIRECTORY_MAP in `.work/standards/`; RAG Engine SPEC (BC3 — highest risk) with R1–R8; architecture fitness review passed |
| Foundation P4 (Cross-cutting) | Threat model, data classification, observability spec, API style guide in `.work/standards/`; UX/UI validation: personas + journeys exist (doc 01); accessibility deferred (U16) |
| v0.5.2 layout consolidation (2026-07-06) | Standards restored to `.work/standards/`; integration manifest to `.work/docs/integration/`; path references updated; `@deploy-basic update` applied |
| Foundation P5 (Infrastructure) | Docker Compose proposal approved → `docker-compose.yml`, `Dockerfile.api`, `Dockerfile.dashboard`, `.env.example` created; sandbox onboarding runbook documented |
| Foundation P6 (Operations) | README, .gitignore created; P6 gate passed; **Plan-master-ready certified** (S4: 10/10 pass) |

---

## Blocked on owner

| # | Item | Notes |
|---|------|-------|
| 1 | Concurrent user count for V1 (U7) | Blocks scaling architecture decisions |
| 2 | SOC2/GDPR compliance timeline (U8) | Blocks compliance ADR |
| 3 | V1 feature prioritization — which features to cut for 1–2 month timeline (U9) | Blocks scope lock |

---

## Recommended next

| Priority | Item | Notes |
|----------|------|-------|
| **0** | `@plan-master greenfield` | Create master implementation plan now that plan-master-ready is certified |
| **1** | `@plan-master status` | Check implementation-ready status after master plan is Approved |

---

## Current iteration

*(No active iteration - run `@code-implementation plan - M1` after master plan is **Approved** and `implementation-ready: yes`.)*

```markdown
## Current iteration - M{N}: <milestone name>

**Milestone ref:** M{N} · `{MASTER_PLAN}` §<task section>
**Status:** planning | in-progress | complete
**Started:** YYYY-MM-DD

### In scope
- …

### Out of scope (explicit)
- …

### Tasks
| ID | Description | Files | Status | Notes |
|----|-------------|-------|--------|-------|
| M{N}-T1 | … | … | pending | |

### Acceptance criteria
- [ ] …

### Validation steps
- [ ] Tests: `pytest tests/ -q` (per `.cursorrules`)
- [ ] Lint: `ruff check .`
- [ ] Type: `pyright .`

### Owner blockers
- none

### Concept / NFR registry (this iteration)
| Concept id | Applies | Status | Evidence / trigger |
|------------|---------|--------|-------------------|
| MOD-06 | yes | pending | AI-assisted session |

### Cross-LLM verification
- Triggered: no

### Done this iteration
| Task | Completed | Notes |
|------|-----------|-------|
```
