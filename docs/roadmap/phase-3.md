# Phase 3 — Long term

**Goals:** Advanced automation & vendor evolution resilience.

| Task | Impact |
|------|--------|
| Evaluate vendor push/webhook channels (if exposed) | Reduce latency vs pure polling |
| Typed DTO end-to-end | Less dict drift |
| Optional multi-region endpoint configuration | Safer forks for non-ES regions |

**Expected outcome:** Future-proofing — contingent on vendor API availability.

**Assumption:** Securitas does not publicly guarantee stable undocumented GraphQL fields — maintain defensive parsing.
