# Work Architecture — Workflow Mapping

Benali's methodology for mapping how a business works. Produces two complementary views:

- **Workflow Map** — sequential view. Phase → Process → Core Activity. Shows *how* work moves from trigger to end state.
- **Function Chart** — organizational view. Function → Subfunction → Core Activity. Shows *what* the business does, independent of who currently does it.

Both share one atomic unit: the **Core Activity** (action verb + object + context — under 15 words, passes the 5 tests).

This repo is the public mirror of Benali's workflow-mapping plugin. It contains the methodology reference and a Claude Code plugin that teaches Claude how to produce ops-map-ready workflow output.

## Install (one line)

In Claude Code, tell Claude:

```
claude plugin marketplace add BenaliHQ/workflow-mapping
claude plugin install workflow-mapping@workflow-mapping
```

Or tell Claude Code: *"Install the workflow-mapping plugin from BenaliHQ/workflow-mapping"*. The repo is public; no GitHub login is needed. Update later with `claude plugin update workflow-mapping@workflow-mapping`.

Verify the install by running `/wa-primer` — it should load a 5-minute orientation on Work Architecture.

## What ships in the plugin

### Skills (13)

| Skill | Purpose |
|---|---|
| `/wa-primer` | Five-minute mental model. Read once. |
| `/wa-start` | Router: what do you have, which skill to run. |
| `/wa-interview` | No input or thin input: get the workflow by asking, one section at a time (solo or sparse). |
| `/wa-decide` | Stuck on one call: activity, process, phase, sub-function, function, or role. |
| `/wa-workflow` | Parent rules: definitions, tests, voice and length caps, handoff line, output template. |
| `/wa-workflow architect` | Raw input to first-draft map. |
| `/wa-workflow condense` | First draft to condensed map. |
| `/wa-workflow gap-analysis` | Condensed map to gap report with paste-ready fixes. |
| `/wa-function-chart` | Parent rules for the chart. |
| `/wa-function-chart architect` | Three or more condensed maps to a function chart with a Workflow Update Patch. |
| `/wa-function-chart gap-analysis` | Chart review: ownership, drift, coverage, tooling. |
| `/wa-visualize` | Map to print PDF, web page, or session questions document. |
| `/wa-feedback` | File feedback on the skills as a GitHub issue. |

### Reference docs (alongside the plugin)

- `methodology.md` — the full Work Architecture methodology (deep read)
- `core-activity-standards.md` — governance rules for core activities
- `industry-discovery-questions.md` — starter question banks by industry

The skills inline the rules they enforce; these docs are for human understanding, not skill runtime.

## Ops map schema

The plugin produces output that matches ops map fields exactly, using fenced code blocks per field so you can one-click copy each value:

| Entity | Ops map fields |
|---|---|
| Workflow | Title, Description |
| Phase | Title, Description (end state + handoff prose embedded) |
| Process | Title, Role, Description (trigger + end state embedded) |
| Core Activity | Title, Sub-function, Software, Description, Trigger, End state, Status (active / draft / gap) |

## First-run flow

1. `/wa-primer` — once, for the mental model
2. `/wa-start` — tells Claude what you have (ops map entry / transcript / notes / file / task-management export / nothing) and routes you
3. Typical chain: `/wa-workflow architect` → `/wa-workflow condense` → `/wa-workflow gap-analysis` for one workflow
4. After 3+ condensed workflows: `/wa-function-chart architect` → `/wa-function-chart gap-analysis`
5. Stuck on a decision: `/wa-decide [type]`
6. Feedback on the skills themselves: `/wa-feedback`

## Key rules the skills enforce

- **No people's names, ever.** Roles only.
- **Nothing invented.** What the source does not say is UNKNOWN and becomes an operator question.
- **Core activity title:** verb + object + context, ideally under 15 words. Three tests decide whether something is a core activity: outcome, SOP, assignment.
- **Never skip the Process level.** A process has a role or roles, a trigger, an end state, and at least two activities.
- **No count rules.** A workflow has as many phases as it has stages. Sizes on the function chart are smells to check, not rules.
- **Voice and length caps on every field.** Small words, short sentences, what happens only. Rationale, dates, client names, and software stay out of descriptions; software has its own field.
- **Handoffs are one line** in the receiving phase: type, sender, receiver, what transfers, accepted when.
- **Same work, same title, everywhere.** The function chart is the source of truth.
- **Apply, then log.** Naming fixes are applied and recorded in a change table, not approved one at a time.

## Version

1.5.0 (2026-09-14). Full rewrite of every skill for Fable 5.1 and Astra after the operator's line-by-line review: voice caps, no count rules, three core-activity tests, Software field, apply-then-log, interview in solo and sparse modes only. wa-visualize scripts unchanged; Business-system retheme and diagram output are tracked separately.