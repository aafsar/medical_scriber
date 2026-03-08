# Feature Development Workflow

Step-by-step process for working on a v1 feature, from start to completion.

---

## 1. Pick a Feature

Check [`tracker_master.md`](tracker_master.md) for the next feature to work on. Prefer Priority 1 first, then Priority 2, then Priority 3. Verify the feature has no unresolved dependencies.

## 2. Decide: Folder or Inline?

- **Standard features** (multi-file changes, design decisions needed) — create a feature folder under `_plans/features/`.
- **Small features** (single-file change, no design ambiguity, e.g. v1.5 consent notice) — skip the folder and track directly in `tracker_master.md`. Jump to Step 5.

## 3. Create the Feature Folder

```
mkdir _plans/features/v1.N_short_name
```

**Naming convention:**
- Prefix: `v1.N_` where N is the feature number from the roadmap
- Suffix: lowercase, underscores, 2–4 words describing the feature
- Examples: `v1.1_deployment/`, `v1.7_pdf_export/`, `v1.8_persistence/`

## 4. Create Plan and Tracker Files

Copy the templates from [`features/TEMPLATE.md`](features/TEMPLATE.md) into two files:

```
_plans/features/v1.N_short_name/
├── plan_v1.N.md          # Design decisions, rationale, file change list
└── tracker_v1.N.md       # Task table, verification checklist, issues
```

**Naming convention:**
- Plan: `plan_v1.N.md` (e.g. `plan_v1.7.md`)
- Tracker: `tracker_v1.N.md` (e.g. `tracker_v1.7.md`)

Fill in the plan first (goal, priority, design sections, files changed). Then populate the tracker with the implementation task list.

## 5. Update the Master Tracker

In [`tracker_master.md`](tracker_master.md):

1. Set the feature's **Status** to `IN PROGRESS`
2. Add a link in the **Docs** column pointing to the feature folder: `[plan](features/v1.N_short_name/plan_v1.N.md)`
3. For small/inline features, add task rows directly under the feature's priority table instead

## 6. Implement

Work through the tasks in the feature tracker. Update task statuses as you go. Log any issues encountered in the tracker's Issues table.

## 7. Verify

Complete the verification checklist in the feature tracker. Every checkbox should pass before marking the feature done.

## 8. Close Out

1. **Feature tracker:** Set Feature Status to `DONE`, fill in the Last Updated date
2. **Feature plan:** Fill in the `Outcome` line at the top
3. **Master tracker:** Set the feature's Status to `DONE`
4. **Commit** the completed feature

---

## Quick Reference

| Item | Location | Convention |
|------|----------|------------|
| Feature folder | `_plans/features/v1.N_short_name/` | lowercase, underscores |
| Plan file | `plan_v1.N.md` | design rationale, no task lists |
| Tracker file | `tracker_v1.N.md` | tasks, verification, issues |
| Templates | [`features/TEMPLATE.md`](features/TEMPLATE.md) | copy from here |
| Master tracker | [`tracker_master.md`](tracker_master.md) | status + link to feature docs |
| Roadmap details | [`masterplan.md`](masterplan.md) Section 7 | feature descriptions |
