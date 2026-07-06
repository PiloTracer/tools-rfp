# HANDOFF - session boundary

## Session status

**Open:** -

**Updated:** YYYY-MM-DD

**Closed:** -

**Repository state:** Greenfield / planning / implementation - describe briefly.

**Recommended pick-up file:** `.work/plans/NEXT.md`

**Lost or new?** Read `.ai/START_HERE.md` (from repo root).

---

## Fresh start - what the next session should do first

1. Run **`@session-control start`** (or follow the manual list in `session-control` skill).
2. Read **`.cursorrules`**.
3. Read **P0 initial scope** when present: `.work/plans/foundation/*-01-*-initial-scope.md`.
4. Read **this file** through §Fresh start, then §Open owner actions.
5. Read `.work/plans/NEXT.md`.
6. Read `.work/plans/ASSUMPTIONS.md`, `RISK_REGISTRY.md`, `UNKNOWNS.md`.

End with **`@session-control close`** (add `commit` / `commit push` only when requested). For mid-session checkpoints use **`@session-control commit`** or **`@session-control commit push`** (no close).

### Conditional reads (customize per project)

| If the task touches… | Read first |
|----------------------|------------|
| Product scope / foundation | `.work/plans/foundation/*-01-*.md` … `*-04-*.md` |
| Any code or new feature | `.ai/standards/*CONVENTIONS*`, `*FEATURE_STANDARD*` |
| External integration | `*-02-*.md`, `.ai/docs/integration/MANIFEST.txt` (if any) |
| Security | `.ai/standards/*threat-model*` |
| Stack / topology | `REPLACE:TECH_STACK_DOC` |
| Master plan / milestones | `.work/plans/full/*-full-plan.md` |
| High-risk feature | Relevant `.work/features/<slug>/*-SPEC.md` |

---

## Open owner actions

| # | Action | Blocks | Owner |
|---|--------|--------|-------|
| - | (none) | | |

---

## What this cycle produced (audit history - skim last session only)

| Date | Session | Artifacts |
|------|---------|-----------|
| YYYY-MM-DD | | |
| 2025-07-17 | @session-control commit push | Initial bootstrap commit (`67de44d`) pushed to main |
| 2025-07-17 | @ai-director policy | Saved memory: `commit-push-only-on-explicit` (high priority) |

---

## Explicit unknowns (promoted from UNKNOWNS)

| ID | Summary | Blocks |
|----|---------|--------|
| - | | |

---

## Cross-LLM verification

- **Triggered:** no
- **Result:** -
- **Notes:** -

## Latest action (@ai-director)
**Date:** 2025-07-17
**Request:** "make sure commit and push are done only on operator's explicit request"
**Classified bucket:** policy reinforcement
**Routing confidence:** high
**Executed:**
1. `remember` feedback → saved high-priority project memory `commit-push-only-on-explicit`
2. Reviewed existing protections: `.cursorrules` (`NEVER git commit/push unless user requests it`) and `session-control/skill.md` hard rules already enforce this
**User correction:** none
**Blockers:** none
**Next recommended:** @session-control start when ready to begin work
