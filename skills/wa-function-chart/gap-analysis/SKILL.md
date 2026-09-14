---
name: wa-function-chart gap-analysis
description: "Read a Function Chart, usually pulled from Ops Map, for what it reveals: work nobody owns, roles built around one person, tools doing the same job twice, activity titles drifting across workflows, and functions the business probably needs but has not mapped. Short prioritized report."
---

# wa-function-chart gap-analysis

## What this skill does

You take a finished function chart and read it for problems. This is the pass you run when the chart exists in Ops Map and you want to know what it is telling you.

The rules live in `wa-function-chart/SKILL.md` and the wa-workflow parent. Read both first.

Two kinds of finding, kept apart:

- **Structural and ownership findings** are facts from the chart. State them plainly.
- **Coverage findings** are what businesses like this usually have. State each as a question: *Typical in [business type]: [function or sub-function]. Does this apply here?*

## The steps

### Step 1. Get the context

Ask for the industry, the size of the operation (solo, small team, larger org), the chart, and, if the user has them, the condensed workflow maps. The maps are needed for Step 5 only.

### Step 2. Structural check

Go through the parent's checklist item by item. Each failure is a structural gap; note where it is.

Then read the status counts on each sub-function:

- Only gap activities: nothing here is running. Ask whether it is planned work or should come off the chart until something happens.
- Fewer than three active activities, padded out by draft or gap: say so. It is thinner than it looks.
- More than about 30 percent of the whole chart is gap: say the chart is mostly aspirational and current coverage is low.

### Step 3. Ownership check

For every function and sub-function, look at the roles.

- **No primary role.** An orphaned sub-function. Work nobody is formally responsible for. Propose the role that fits and ask.
- **One role primary across unrelated functions.** A unicorn role: a job built around one person, hard to hire for. Name the role, the functions it spans, and which activities would move to which role if it were split. In a solo business, say only that the operator is the single point of failure for those functions; do not prescribe a split.

### Step 4. Tooling check

Read the Software on the activities. Flag:

- Two or more tools doing the same job inside one sub-function. Ask whether that is deliberate before recommending consolidation.
- One tool carrying jobs it was not built for across many sub-functions. Say so; it may be overloaded.
- Activities that clearly need a tool and name none. Ask whether the step is manual or the tool is unrecorded.

### Step 5. Canonical drift check

Only with the maps in hand. For every activity the chart marks as appearing in two or more workflows, read its title in each map. Any mismatch is drift: list the variants and the chart's title, and put the fix in a Workflow Update Patch. Compare active activities only.

Without the maps, say the check was skipped and why. Never guess drift from the chart alone.

### Step 6. Coverage check, from research

Do not recommend a function from general knowledge. Search, then judge the sources, the same way the workflow gap-analysis does:

1. Search for *[industry] business functions organizational structure* and *common missing functions [business type]*. Pull clean text from useful sources.
2. Rate sources: high (standards bodies, academic, major analyst firms), medium (trade publications, major consulting firms, associations, recognized practitioner books), low (vendor marketing, listicles).
3. One high or two medium sources support a hypothesis. Low sources alone do not. In fields with no standards bodies, three practitioner sources agreeing may be cited as a downgraded signal, labeled as such.
4. Disagreement between good sources is shown as both positions, never blended.
5. Cite every source: URL, tier, date accessed.

Scale to the business. A solo operator does not get told they lack an HR function.

If research is unavailable or thin, say so and limit the report to Steps 2 through 5.

### Step 7. Write the report

One screen.

```markdown
# Function Chart Gap Analysis: [Business]

Industry: [x]. Size: [x]. Chart: [N functions, M sub-functions, K activities; A active, D draft, G gap].
Sources: [URL, tier, date] ...

## Summary
One sentence: strong on X, weak on Y, N structural, M ownership, K drift, J coverage questions.

## Structural gaps
1. [What, where, fix.]

## Ownership
Orphaned: [sub-function]. Proposed primary role: [role]. Agree?
Unicorn: [role] is primary on [functions]. If split: [activities] to [role], [activities] to [role]. Agree?

## Tooling
[Sub-function]: [tools]. Deliberate, or consolidate?

## Canonical drift
[Chart title]: [map A title], [map B title]. Patch below.

## Coverage questions
1. Typical in [business type]: [function]. Sources: [...]. Does this apply here?

## Priority
P0 structural: [...]. P1 ownership and drift: [...]. P2 coverage: [...]. P3 tooling: [...].

## Workflow Update Patch
[Per workflow: title to change, phase and process numbers]
```

### Step 8. Hand off

With P0 items: *"Fix these by re-running `/wa-function-chart architect`, then return."* With a clean chart: *"The chart is ready to use as the governance view. Run `/wa-workflow gap-analysis` on any map that has not had it."*

## Never

- Recommend a function the business does not need at its size.
- Treat a unicorn role in a solo business as a problem to fix now.
- Leave a structural failure below P0.
- Flag tool redundancy without asking whether it is deliberate.
- Report drift without the maps.
