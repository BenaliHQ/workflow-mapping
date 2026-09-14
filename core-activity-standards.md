---
date: 2026-03-25
type: reference
status: active
project: workflow-mapping
---

# Core Activity Standards

Rules, principles, and guidelines for defining, naming, condensing, and maintaining core activities across all workflow maps. These standards apply to all current and future mapping work.

Established during the workflow review and condensation session on 2026-03-25. First applied to the Daily Operating Workflow (153 → 61 activities, 60% reduction).

---

## Core Activity Rules

### 1. One outcome, one activity
If multiple listed activities all contribute to the same observable outcome, they are one core activity. The sub-steps become the SOP checklist. This is the primary filter for condensation.

### 2. Canonical activities are untouchable
Activities that appear across multiple workflows with the same title must keep that exact title everywhere. Before condensing or renaming anything, check if it's referenced in other workflows. The function chart is the single source of truth for canonical titles.

### 3. The SOP test prevents over-condensation
If you'd write different SOPs for two activities, they stay separate. Different instructions = different activities.

### 4. The assignment test prevents under-condensation
If an activity would never appear as a standalone task on someone's to-do list, it's a step within a larger activity. Fold it into the parent.

### 5. Verification steps fold into the activity they verify
Quality checks and verification steps are not separate activities. They become part of the parent activity's SOP checklist or the process audit.

### 6. Two-pass review is one or two activities depending on assignment
When the same person does critical and refinement passes in one sitting, it's one activity with two passes in the SOP. When a separate reviewer does each pass, they're separate activities because they're separate assignments.

---

## Naming Rules

### 7. Verb first, always
Every core activity title starts with an action verb: Review, Process, Log, Route, Extract, Identify, Present, Commit, Prepare, Build, Send, Update, Capture, Reconcile, Audit.

### 8. No em-dash explanations in titles
The title is the title. Explanatory detail goes in the SOP. The workflow table shows what happens; the SOP shows how.

### 9. Context distinguishes, not decorates
Include context only when needed to make the activity unique on the function chart. Don't add context that's obvious from the process it lives in.

### 10. Under 15 words
Long enough to be specific, short enough to scan on a function chart.

### 11. No conditional language in titles
No "if applicable," "if needed," "when available." If an activity is conditional, the process notes when it applies. The title describes the work.

### 12. Vault paths stay for now, use readable names
"Update project status" not "Update project `_status.md`." Paths will be stripped when SOPs are built and the SOP handles the implementation detail.

---

## Process Rules

### 13. Single-activity processes are a smell
If a process has only one activity, either merge it with a related process or confirm it genuinely stands alone. Not always wrong, but should be a conscious decision.

### 14. Processes merge when they serve the same purpose
The test: "Would you explain these as one unit of work to someone?" If yes, merge. If they serve different purposes that happen to be small, keep separate.

### 15. Processes should have 2-6 activities
Below 2, the process is probably too granular. Above 6, it's probably doing two different things and should split. Guideline, not hard rule — autonomous Claude processing can run larger.

---

## Cross-Workflow Rules

### 16. Same work, same title, everywhere
If the same work appears in multiple workflows, the title must be identical. During condensation, check every activity against all other workflows before renaming.

### 17. Routing activities stay separate when destinations are canonical
Don't merge routing activities that go to different canonical destinations (e.g., vault locations vs someday-maybe).

### 18. Logging and updating activities condense when the target is the same type
"Create Slack log" and "Create email log" can become one processing activity. But "Update company notes" and "Update project status" stay separate — different targets, different SOPs.

---

## What to Preserve

### 19. Detail moves to SOP, not to the trash
When condensing, granular steps become the checklist in the core activity's future SOP document. They're relocated to the right level, not deleted. The workflow shows what happens; the SOP shows how.

### 20. Audits stay inline
Process audits are the enforcement mechanism. They stay in the workflow as callouts, not condensed away. They validate that the condensed activity was done completely.

---

## Application

These standards apply to:
- All workflow maps produced by this methodology
- All future Work Architecture mapping engagements
- The function chart extraction process
- Skill folder and SOP development

When in doubt, apply the tests in order: outcome test → SOP test → assignment test → naming rules.
