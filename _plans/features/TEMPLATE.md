# Feature Templates

Use these templates when starting work on a v1 feature. Create a folder `_plans/features/v1.N_short_name/` with a plan and tracker file. Small features (like v1.5 consent notice) can skip the folder and be tracked directly in the master tracker.

---

## Feature Plan Template (`plan_v1.N.md`)

```
# v1.N: Title — Plan & Context
> **Goal:** One sentence.
> **Outcome:** [filled after completion]
> **Priority:** 1 | 2 | 3
> **Depends on:** [other features, or "None"]
---
## Pre-Conditions
## [Design sections]
  - Describe rationale, not tasks
  - Reference actual files, don't embed code
## Files Changed
| File | Changes |
```

---

## Feature Tracker Template (`tracker_v1.N.md`)

```
# v1.N: Title — Tracker
> **Last Updated:** YYYY-MM-DD
> **Feature Status:** NOT STARTED | IN PROGRESS | DONE
---
## Implementation Order
| # | Task | Status | Depends On | Notes |
## Verification Checklist
- [ ] specific tests with expected results
## Issues
| # | Date | Issue | Resolution |
```
