---
name: wa-function-chart architect
description: "Build a Function Chart from three or more condensed Workflow Maps. Pulls every activity, groups by shared expertise into functions and sub-functions, settles canonical titles, and hands back a Workflow Update Patch so the maps match the chart."
---

# wa-function-chart architect

## What this skill does

You take three or more condensed workflow maps and reorganize their activities from "in what order" to "under what kind of work." The result is the business's function chart plus a patch that brings the maps in line with it.

The rules live in `wa-function-chart/SKILL.md` and the wa-workflow parent. Read both first.

## The steps

### Step 1. Check you have enough

Count the condensed maps. Fewer than three: stop. A chart from one or two maps makes functions look arbitrary and hides the cross-workflow patterns. Say how many more maps are needed and send the user back to `/wa-workflow architect` and `condense`.

Confirm each map is condensed, not a first draft. Get the business name.

If the maps together are very long (roughly 10,000 words or more), say you will work in two passes: first a flat list of every activity, then the grouping.

### Step 2. List every activity

From every map, pull every core activity into one flat list with: title, status, tentative sub-function, source workflow, source process, and whether it sits inside a reusable process (and which map holds the canonical definition).

Mark every activity that appears in two or more maps as a canonical candidate.

### Step 3. Settle reusable processes

Where a process appears in two or more maps with the same role and roughly the same work, ask the user once, with the full list: same process referenced from different places, or different processes with similar names? For each confirmed reusable process, note which map holds the canonical definition. The others become references, and that change goes in the patch.

### Step 4. Settle canonical titles

For each canonical candidate, compare its title across the maps. Identical: nothing to do. Different: show the user the variants once, as a list, and for each ask them to pick a title or confirm they are different work. Only active activities anchor a title; draft and gap titles follow.

Every rename goes in the Workflow Update Patch.

### Step 5. Propose the functions

Read the whole activity list before naming anything. Group by the nature of the work, not by who does it and not by industry defaults. Only after grouping, compare against the usual shapes as a sanity check:

| Business type | Functions usually seen |
|---|---|
| Service business | Sales, Operations, Finance, Marketing, People, Strategy |
| Construction | Sales, Estimating, Project Management, Field Operations, Finance, Safety |
| Recurring-revenue service | Sales, Onboarding, Client Success, Operations, Finance, Product |
| Solo consulting | Strategy, Sales, Production, Content, Administration, Knowledge Management |

Show the proposed functions with their activities and one sentence each on why they are one function. Ask: *"Does this match how you would describe the business? Is any function thin because its work is not mapped yet?"*

### Step 6. Consolidate the sub-functions

The activities arrive with tentative sub-functions from the maps. This step tidies them:

1. List every tentative name under each function.
2. Merge near-duplicates ("Proposal Creation", "Proposal Generation", "Proposal Prep" are one). The new name goes in the patch.
3. Apply the specialization test to anything that looks oversized; split where two kinds of expertise sit together.
4. Merge anything with one or two activities into a neighbor unless the work is genuinely distinct.

Show the sub-functions with their activities and specialization sentence. Ask: *"Any activity in the wrong place?"*

### Step 7. Attach roles and software

For each sub-function ask which roles do its work. Record one primary role and any others that take part; a function or sub-function can carry many roles. A person's name goes through the parent's name-to-role ladder. If nobody can name a primary role, record "unassigned" and move on; that finding belongs to gap-analysis, not here.

Software attaches to activities by product name, only where the tool is core to the work. If the user wants current staffing recorded, put it in the optional section, never in the chart itself.

### Step 8. Write the chart and hand off

Output per the parent's format, including the Canonical activities list, the Reusable processes list, any size smells with their reason, and the Workflow Update Patch.

The patch is per workflow: each activity title to change (with phase and process numbers), each sub-function rename with the count of activities affected, and each process to convert to a reusable reference.

Run the parent's checklist and report only failures. Then: *"Apply the patch in ops map so the maps match the chart. Then run `/wa-function-chart gap-analysis` to review the chart for ownership gaps, drift, and coverage."*

## If the user is stuck

Function or sub-function: `/wa-decide 5`. One sub-function or two: `/wa-decide 4`. Same process or different: `/wa-decide 2`.

## Never

- Build from fewer than three condensed maps.
- Name a function by who does the work.
- Propose functions from the sanity table instead of from the activities.
- Invent an activity to fill out a thin function.
- Leave a canonical conflict unresolved.
- Skip the Workflow Update Patch when anything was renamed.
