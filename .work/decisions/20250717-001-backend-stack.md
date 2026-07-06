# ADR-001: Python + FastAPI backend

**Status:** Decided · **Date:** 2025-07-17

## Context

RFP Platform needs a backend framework for its HTTP API, async task routing, and AI/LLM integration. The platform is self-hosted via Docker Compose, targeting a solo/small team with a 1–2 month V1 timeline. Key requirements: async-native, strong validation, AI/ML ecosystem, low ops overhead.

## Decision

Use **Python 3.12** with **FastAPI** as the backend framework.

## Consequences

- **Positive:** Async-native handling of concurrent RFP processing; Pydantic schemas for request/response validation; auto-generated OpenAPI docs; mature Celery integration for task queues; rich AI/LLM library ecosystem.
- **Negative:** Python GIL limits CPU-bound parallelism (mitigated by Celery worker scaling); async debugging can be more complex than synchronous frameworks.
- **Neutral:** FastAPI's auto-docs become the primary API reference; OpenAPI spec can be exported for SDK generation.

## Alternatives considered

| Alternative | Reason rejected |
|-------------|-----------------|
| TypeScript + Node.js | Weaker AI/LLM library ecosystem; fewer battle-tested async task queue options for solo team |
| Go | Excellent performance but steeper learning curve for solo dev; smaller AI/ML library ecosystem |
| Django | Heavy ORM coupling; sync-by-default requires async hoop-jumping for Celery integration |

## References

- DOCS_TECH_STACK.md
- Foundation doc 04 §3
