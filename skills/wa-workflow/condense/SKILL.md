---
name: wa-workflow condense
description: "Take a first-draft Workflow Map and fold everything that is not a core activity into SOP checklists. Merges duplicates, unifies canonical titles, keeps every detail by moving it down, never by deleting it."
---

# wa-workflow condense

## What this skill does

A first draft usually lists too many things as core activities. Many of them are steps inside a bigger activity, checks, or the same work written twice. This skill tests each one and folds what does not belong. Nothing is deleted; folded steps move into the parent activity's `SOP checklist:` list.

The rules live in `wa-workflow/SKILL.md`. Read that file first. This file only gives the order of work.

The tests decide how much gets folded. There is no target percentage. A granular draft may lose half its activities; a clean draft may lose almost none. Both are correct outcomes.

## The steps

### Step 1. Check the input

The input must already be a map: phases, processes, activities in the ops map source format. Raw notes go to `/wa-workflow architect` first.

Skip any process marked as a reusable reference. Its canonical definition lives in another workflow and is condensed there.

### Step 2. Test every activity

Run the parent's three tests on each activity in order: outcome, SOP, assignment. The first "no" decides.

- Passes all three: keep it.
- Fails: fold it into the activity it belongs to, as a line under `SOP checklist:`. Keep the folded title word for word.

Do not print the test results per activity. For each process, write one line in the change table saying what was kept and on what basis.

### Step 3. Merge what is the same work

After folding, look for activities that should be one:

| You see | Do this |
|---|---|
| Two activities producing the same deliverable | Merge. "Same deliverable" means the same output, not the same verb. Editing a teaser, a clip, and a full episode are three deliverables and stay three. |
| A "verify", "check", or "confirm" activity | Fold into the activity it checks. |
| Logging or updating activities with the same kind of target | Merge. "Create Slack log" and "Create email log" become "Create activity log". Different targets stay separate. |
| Routing activities to different destinations | Keep separate. |
| An audit activity | Keep. Audits are enforcement, not clutter. |
| Items the source tool tracked as separate tasks with their own completion or assignee | Keep separate. The tool already proved they are assignable on their own. |
| A process left with one activity | Merge it with a related process, or confirm it stands alone. |

### Step 4. Settle status when things merge

When activities merge, the result takes the most concrete status: active beats draft, draft beats gap. If a gap activity merges into an active one, note in Structure notes that the gap work already existed and was under-described.

### Step 5. Unify canonical titles

Check `_process-registry.md` and the other maps you have for the same work under a different title. Then ask the user once, with the full list: *"Do any of these activities appear in other workflows you have mapped? If you do not know, say so."*

Where the same work exists elsewhere, the title must match exactly. Pick the canonical title with the user and apply it. Where they do not know, mark the activity as a canonical candidate for the function chart pass.

### Step 6. Write the condensed map

Output the full map in the ops map source format, with the parent's voice caps applied to every field you touched.

Place the metadata so the map stays clean for copy-paste:

- Above the `## Workflow` block: activity count before, after, and the reduction, plus a short condensation log (what was folded, merged, renamed, and why in a few words each).
- The map itself, untouched by commentary.
- Below `## Notes & Assumptions`: the change table (before, after, decisive test, reason) and any canonical conflicts the user still needs to resolve.

If the reduction landed well outside 40 to 60 percent, say why in one line under Structure notes.

### Step 7. Hand off

*"Next, run `/wa-workflow gap-analysis` to check the condensed map for missing steps and weak handoffs. Once three or more maps are condensed, `/wa-function-chart architect` builds the function chart."*

## A short example

Before, nine activities under "Prepare Proposal Process": open template, fill client name, fill scope, fill pricing, review for typos, check pricing math, save as PDF, name the file, upload to Drive.

After, three activities:

- Draft proposal using client scope and pricing. SOP checklist: open template, fill client name, fill scope, fill pricing.
- Review proposal for accuracy and polish. SOP checklist: review for typos, check pricing math.
- Publish proposal PDF to shared Drive. SOP checklist: save as PDF, name the file, upload to Drive.

Each of the three passes all three tests. The other six are still there, one level down.

## If the user is stuck

- Not sure whether something is an activity or a checklist line: `/wa-decide 1`.
- Not sure whether two processes are the same work: `/wa-decide 2`.

## Never

- Delete a folded step. It moves to an SOP checklist.
- Rename a canonical activity without the user's confirmation.
- Fold to hit a percentage. If every activity passes, leave the map alone.
- Condense a reusable process reference. Its canonical definition owns that.
- Interleave counts, logs, or commentary with the map's fenced blocks.
