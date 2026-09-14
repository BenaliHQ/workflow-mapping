---
name: wa-primer
description: "Five-minute mental model for Work Architecture: the two views, the three levels, what a core activity is, how the map is written, and which skill to run for what. Read once before any other wa-* skill."
---

# Work Architecture in five minutes

Read this once. Then run `/wa-start`.

## Two views of one business

| View | Levels | Answers |
|---|---|---|
| Workflow Map | Phase, Process, Core Activity | How does work move, from a trigger to an end state? |
| Function Chart | Function, Sub-function, Core Activity | What does the business do, whoever does it today? |

Both are built from the same unit, the core activity. You map workflows first. The function chart is built from three or more of them.

## The three levels of a workflow map

**Phase.** A stage of work. Boundaries sit where work hands off between functions. Named by the stage, never by who does it. A workflow has as many phases as it has stages.

**Process.** An ordered run of core activities that produces the outputs the next process needs. Title ends in "Process". Has a role (one or more job titles), a trigger, and an end state. At least two activities. Never skip this level.

**Core Activity.** The atomic unit of work. One observable outcome. Could be a task on someone's list. Title is verb + object + context, ideally under 15 words. The same activity can belong to several workflows; in Ops Map it is one object.

## Is it a core activity?

Three tests, in order. The first no decides.

1. Does it produce a distinct result the next activity depends on? No: it is a checklist line inside the parent.
2. Would you write a separate SOP for it? No: fold it into the parent's SOP.
3. Could it be a standalone task on a to-do list? No: it is a step within the parent.

Then two placement checks: does it need distinct expertise (it may be its own sub-function), and does the same work appear in another workflow (reuse the exact title).

Size check: a 5 to 10 line checklist means the right size.

## How the map is written

The map is read by the client's team on a phone, in a PDF, and inside Ops Map. It is a reference, not an essay.

- Small words, short sentences, one idea each.
- Say what happens. Why, what was considered, and when it was decided go in Notes and Assumptions.
- No names, no dates, no software in descriptions. Software has its own field.
- Use the client's own words. Never coin a term.
- Every field has a length cap. Workflow description three sentences; phase two plus a handoff line; process a trigger line, one or two sentences, an end-state line; activity one or two SOP sentences.

## Handoffs

Where work changes hands. Three types: Functional (between functions), Role (same function, different person), External (leaves the organization). Four parts: sender, receiver, what transfers, accepted when. Written once, as one line, in the receiving phase's description.

## The fields you fill in

| Level | Fields |
|---|---|
| Workflow | Title, Description |
| Phase | Title, Description |
| Process | Title, Role, Description |
| Core activity | Title, Sub-function, Software, Description, Trigger, End state, Status |

Status is active (running today), draft (being built), or gap (recommended, not yet happening).

## The rules that never bend

- No personal names anywhere. Roles only.
- Nothing invented. What the source does not say is UNKNOWN and becomes a question.
- Same work, same title, everywhere.
- The Process level is never skipped.

## Which skill does what

```
/wa-start                        Not sure where to begin? Start here.
/wa-interview                    Nothing written down, or a thin sketch. Get asked questions.
/wa-workflow architect           Raw material to a first-draft map.
/wa-workflow condense            First draft to condensed map.
/wa-workflow gap-analysis        Condensed map to a gap report with paste-ready fixes.
/wa-function-chart architect     Three or more condensed maps to a function chart.
/wa-function-chart gap-analysis  A chart to a review: ownership, drift, coverage, tooling.
/wa-visualize                    A map to a branded PDF or web page.
/wa-decide                       Stuck on one call? Walk the test.
/wa-feedback                     Tell the maintainers what did not work.
```

The usual path for one workflow: architect, condense, gap-analysis, visualize. After three condensed maps: chart architect, then chart gap-analysis.
