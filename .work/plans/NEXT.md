# NEXT - planning backlog

**Updated:** 2025-07-17

---

## Done

| Item | Artifact |
|------|----------|
| Agent OS bootstrap | `.work/` skeleton, `.cursorrules` from template |
| Foundation P0 (initial scope) | `.work/plans/foundation/20250717-01-rfp-platform-initial-scope.md` |
| Foundation probe (2 iterations) | Coverage 80% — D1–D4, D6–D8 confirmed; D5, D9, D10 partial |

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
| **0** | `@plan-foundation continue` | Walk P1–P6 gates: create docs 02–04, ADRs, standards, SPECs |
| **1** | `@plan-foundation certify plan-master-ready` | After P0–P6 complete (probe at 80%, may pass with waivers) |
| **2** | `@plan-master greenfield` | Master plan after foundation ready |

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
