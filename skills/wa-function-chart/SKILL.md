---
name: wa-function-chart
description: "Work Architecture function chart skill family. Shared rules for building and reviewing Function Charts. The architect and gap-analysis sub-skills read this file first."
argument-hint: "architect | gap-analysis"
---

# wa-function-chart: shared rules

Read this, and the definitions and voice sections of `wa-workflow/SKILL.md`, before running any `wa-function-chart` sub-skill.

If no sub-skill was named, ask: *"Building a chart (`architect`) or reviewing one (`gap-analysis`)?"*

## 1. What a function chart is

The organizational view of a business: Function, then Sub-function, then Core Activity. It shows what the business does, whoever does it today. One chart per business, built from its condensed workflow maps.

**Function.** A major area of responsibility: Sales, Operations, Finance, Marketing. Exists whether or not anyone is assigned. Named by the area, never by a team or person.

**Sub-function.** A distinct specialization inside a function. Named by the specialization, two words where possible: "Lead Management", "Build Execution". Never by cadence ("Daily Tasks"), by source workflow, or by who does it.

**Core Activity.** The same unit as in the workflow maps, same title. Each activity has exactly one home sub-function on the chart. It may appear in many processes across many workflows.

The chart is the source of truth for activity titles. When workflows disagree on a title, the chart decides and the workflows are updated.

## 2. The specialization test

The one test for whether activities share a sub-function:

*If you hired one person to do all of these, would they need the same training and use the same expertise for every one?*

Yes: one sub-function. No: split.

What does not split a sub-function: cadence, which workflow the activity came from, who currently does it. What does: the nature of the work, the expertise it needs, the tools and judgment it uses.

## 3. Sizes are smells, not rules

Most businesses land at roughly 5 to 10 functions, and most sub-functions hold roughly 3 to 15 activities. Outside those ranges, look before acting:

- A function with only a handful of activities is either incomplete (the work exists but is not mapped yet) or belongs inside another function.
- A sub-function with one or two activities probably merges with a neighbor.
- A sub-function with twenty or more probably contains two specializations. Apply the test.

Never merge or split only to land inside a range. Note the natural count and why it holds.

## 4. Status on the chart

Every activity carries the status from its source map: active, draft, or gap. The chart treats them differently.

| Status | On the chart | Sets canonical titles? | Counts toward sub-function size? |
|---|---|---|---|
| active | Shown | Yes | Yes |
| draft | Shown, marked draft | No, provisional | Yes, flagged |
| gap | Shown, marked gap | No | No; it is not running |

Why: a sub-function with two active and ten gap activities looks like twelve but runs as two. Canonical drift is checked among active activities only, so aspirational titles never force a rename.

## 5. Reviewing a chart later

Once a chart exists in Ops Map, it can be pulled down and read for what it reveals: work nobody owns, roles built around one person, tools doing the same job twice. That is a review activity, not part of building the chart. It lives in `/wa-function-chart gap-analysis`.

## 6. Roles, people, software

The chart is built without people first. Then:

- **Roles** attach to functions and sub-functions. Each has one primary role and can have many contributing roles. One role can be primary on several.
- **People** never enter the chart. A separate "Current staffing" section may say who holds each role today, to show dependency risk.
- **Software** attaches to activities, by product name, only when the tool is core to the work.

## 7. Output format

```markdown
# [Business] Function Chart

## Function 1: [Name]

### Sub-function 1.1: [Name]
Specialization: [one sentence]
Primary role: [job title]. Other roles: [job titles]
Active [N] / Draft [N] / Gap [N]

- [Activity title] (active; workflows: A, B)
- [Activity title] (draft; workflows: C)
- [Activity title] (gap; from gap-analysis)

### Sub-function 1.2: ...

## Function 2: ...

## Canonical activities
[Activity title]: workflows A, B, C

## Reusable processes
[Process title]: defined in [workflow], referenced by [workflows]

## Size smells
[Functions or sub-functions outside the usual ranges, with the reason the count holds]

## Current staffing (optional)
[Role]: [person]

## Workflow Update Patch
[Per workflow: title changes and sub-function renames to apply in ops map]
```

## 8. Checklist

Report only failures.

- Every activity has exactly one sub-function and at least one source workflow (or a gap-analysis source, for gap status).
- Every sub-function passes the specialization test and is named by specialization.
- Canonical activities have identical titles across all active workflows.
- No personal names in any function or sub-function title.
- Size smells are listed with their reason.
- The Workflow Update Patch is present when any title or sub-function changed.

## Sub-skills

- `/wa-function-chart architect`: three or more condensed maps to a function chart
- `/wa-function-chart gap-analysis`: a chart to a review of orphans, drift, coverage, and tooling
