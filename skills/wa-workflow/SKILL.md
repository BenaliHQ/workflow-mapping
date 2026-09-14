---
name: wa-workflow
description: "Work Architecture workflow skill family. Shared rules for building, condensing, and reviewing Workflow Maps. The architect, condense, and gap-analysis sub-skills read this file first."
argument-hint: "architect | condense | gap-analysis"
---

# wa-workflow: shared rules

Read this before running any `wa-workflow` sub-skill. Sub-skills do not restate these rules.

If no sub-skill was named, ask: *"Building a new map (`architect`), tightening a draft (`condense`), or reviewing for gaps (`gap-analysis`)?"*

## 1. The three levels

A Workflow Map shows how work moves from a trigger to an end state: Phase, then Process, then Core Activity. Never skip the Process level. Keep the same depth in every phase.

**Phase.** A stage of work. Boundaries sit where work hands off between functions. Named by the stage ("Lead Qualification", "Kickoff"), never by who does it. A workflow has as many phases as it has stages; two is valid.

**Process.** An ordered run of core activities that produces the outputs the next process needs. Title ends in "Process" and names the type of work. Has a role (a job title, never a name), a trigger, and an end state. More than one role is fine when different roles do different activities inside it; that is a Role handoff, written in the process description. At least two activities, no upper cap. A single-activity process is a smell: merge it or confirm it stands alone. Processes with the same title in different workflows contain the same activities.

**Core Activity.** The atomic unit of work. One observable outcome. Could be a standalone task on someone's list. Title is verb + object + context; under 15 words is the ideal. The same core activity can belong to several workflows. In Ops Map it is one object linked to each; in the map source it carries the identical title everywhere.

**Handoff.** Where work changes hands. Three types: Functional (between functions), Role (same function, different person), External (leaves the organization). Four parts: sender, receiver, what transfers, acceptance criteria.

## 2. Tests

**Is it a core activity?** Run in order. The first "no" decides.

| Test | Question | No means |
|---|---|---|
| Outcome | Does it produce a distinct result the next activity depends on? | Checklist line in the parent activity |
| SOP | Would you write a separate SOP for it? | Fold into the parent's SOP |
| Assignment | Could it be a standalone task on a to-do list? | Step within the parent |

**Where does it live?** Two placement checks, applied after the activity passes.

- **Specialization.** Does it need distinct expertise from its neighbors? If yes, it may belong in its own sub-function. This decides placement on the function chart, not whether it is a core activity.
- **Canonical.** Does the same work appear in another workflow? If yes, reuse that exact title. The function chart is the source of truth for titles.

**Granularity.** If you could write a 5 to 10 line checklist for it, it is the right size. A 20-line checklist means split it. A 1-line checklist means fold it.

## 3. Voice and caps

The map is read by the client's team on a phone, in a PDF, and inside Ops Map. It is a reference, not an essay. A new hire must understand every field on first read.

- Small words. Short sentences. One idea per sentence.
- Say what happens. Rationale, alternatives considered, and decision dates go in Notes and Assumptions.
- No personal names, client names, or dates in any field. No software in descriptions; the Software field carries the tool.
- No em dashes. No parentheses. No "as needed", "if applicable", "typically".
- Use the words already in the source or in the client's own narration. Never coin a term.

**Caps.** Limits, not targets.

| Field | Cap |
|---|---|
| Workflow description | 3 sentences: trigger, what moves through, end state |
| Phase description | 2 sentences plus the handoff line (section 5) |
| Process description | Trigger sentence, 1 to 2 sentences of what happens, end-state sentence |
| Core activity description | 1 to 2 SOP sentences, plus an optional `SOP checklist:` list |
| Activity trigger and end state | Noun phrase, 8 words or fewer |
| Any title | 15 words |

Detail that does not fit is one of three things: an `SOP checklist:` line under the activity, a Notes and Assumptions entry, or client context outside the map. Never a longer description.

**Example.** Same activity, same meaning.

Before: *The baseline is not edited. A working copy becomes the live schedule, kept as tight as the superintendent believes achievable and treated as a personal challenge to hit. Preserving the baseline dates unedited is what makes the planned-versus-actual review at Core Activity 2.3.3 possible, and is the measurement basis the proposed schedule-performance bonus would need; no source confirms a preserved comparison artifact in current practice. Tool: Instagantt (replaced by JobTread, decided 2026-08-25). Editing in Instagantt is expensive because dependencies must be individually disconnected and reconnected.*

After: *The baseline is not edited. A working copy becomes the live schedule, kept as tight as the superintendent thinks he can hit.*

Software field: *JobTread.* The bonus question goes to Operator questions. The Instagantt editing cost goes to Structure notes.

## 4. Titles

- Verb first, active voice. "Collect client contact information", not "Client contact information" or "Information is collected".
- No names or roles in any title. The role lives on the process.
- No conditional language, no em-dash explanations.
- Keep the source's verb when it is specific and active, even if uncommon. "Negotiate contract terms" beats "Coordinate contract terms".
- If the source gave a noun phrase and you chose the verb, flag it. An inferred verb changes the meaning of the work.
- Tool names are fine as context ("Edit full episode in Descript"). Show codes and brand acronyms are not.
- Workflow titles end in "Workflow". Process titles end in "Process". Phase titles have no suffix.

## 5. Handoffs

Written once, in the receiving phase's description, as one line in this exact shape:

*Functional handoff from Estimator to Project Manager. Transfers: signed contract, estimate, site notes. Accepted when: PM confirms the estimate matches the contract.*

- First phase: no handoff-in. Open with *Begins when [workflow trigger].*
- Last phase: no handoff-out. Close with *Ends the workflow when [end state].*
- A phase that continues under the same owner: *Begins when [prior phase] completes. Carries forward: [what]. Entry check: [what].*
- Missing acceptance criteria: write *Accepted when: UNKNOWN, source does not specify.* List every such handoff as one consolidated operator question. A typed handoff with UNKNOWN criteria is a data gap. An untyped handoff is a structural failure.

## 6. Reusable processes

The same work, same role, same general trigger and end state, called from more than one workflow.

- Keep `_process-registry.md` next to the maps: one line per process with title, role, canonical workflow. Create it when the first workflow is confirmed; append on every later map. Session memory is not the registry.
- Check the registry before defining a process. If a match is likely, confirm with the user or log the question.
- The canonical definition lives in one workflow. Elsewhere the process has its title, its role, and this description: *Reusable process. Defined in [canonical workflow], Process [N.M]. Here: triggered by [local trigger]; ends when [local end state].* No activities are listed under a reference.

## 7. Names, conflicts, pushback

**Names become roles.** Stop at the first step that answers.

1. Ask, if a user is present.
2. Use an explicit title anywhere in the source.
3. Use a consistent assignee pattern in task-tool data. Leaf-level assignments outweigh container-level.
4. Infer from responsibilities.
5. Use "Team member responsible for [function]".

Roles from step 3 or below go under Assumptions to verify with a confidence level (high, medium, low). Never map a name from memory of another engagement.

**Conflicting sources.** Show both positions with source labels and ask, or log the question. Use the more recent or more specific as the provisional working state. Keep both in Notes and Assumptions. Never delete the earlier one.

**Pushback on a rule.** One sentence on the failure the rule prevents, then the closest compliant alternative. If they still want the deviation, apply it and record *Rule deviation: [what], despite [rule]. Reason: [theirs].* under Structure notes.

## 8. Working method

Naming fixes, folds, and merges are applied directly, not approved one at a time. Every change lands once, in the change table at the end of the output. Rows with an inferred verb also become numbered operator questions.

Structural choices (phase boundaries, process groupings, inferred roles) are shown once for confirmation as a short outline before the full output is built. Do not print per-activity test results; summarize the pass basis per process.

**Non-interactive runs** (sub-agent, batch, overnight): every question becomes a numbered operator question, unsupplied required fields read `UNKNOWN: [what is missing]`, hard stops become flags, and the output carries a DRAFT banner. Never present it as paste-ready.

## 9. Output template

Ops Map imports the markdown source. Each field is a bold label followed by a fenced block. Sections separate with `---`. Keep the shape exactly.

| Level | Fields |
|---|---|
| Workflow | Title, Description |
| Phase | Title, Description |
| Process | Title, Role, Description |
| Core activity | Title, Sub-function, Software, Description, Trigger, End state, Status |

**Sub-function** is a tentative two-word specialization, confirmed later in `/wa-function-chart architect`. List the tentative set once, in a table under Structure notes.

**Software** names the tool when one is core to the activity. Explicit product names, never "CRM". Leave the block empty when no tool applies.

**Status** is active (running today), draft (being built), or gap (recommended, not yet happening). Default active.

**Chain.** Each activity's Trigger is the prior activity's End state. The last End state matches the process's "Ends when".

````markdown
# [Name] Workflow

## Workflow

**Title:**
```
[Name] Workflow
```

**Description:**
```
Triggered when [event]. [One clause per phase outcome, in order.] The workflow ends when [end state].
```

---

## Phase 1

**Title:**
```
[Stage of work]
```

**Description:**
```
Begins when [workflow trigger]. [What happens.] Ends when [phase end state].
```

---

### Process 1.1

**Title:**
```
[Type of work] Process
```

**Role:**
```
[Job title]
```

**Description:**
```
Triggered by [trigger]. [What happens.] Ends when [end state].
```

---

#### Core Activity 1.1.1

**Title:**
```
[Verb] [object] [context]
```

**Sub-function:**
```
[Two words]
```

**Software:**
```
[Product name, or empty]
```

**Description:**
```
[One or two SOP sentences.]

SOP checklist:
- [Folded step, verbatim]
```

**Trigger:**
```
[Noun phrase]
```

**End state:**
```
[Noun phrase]
```

**Status:**
```
active
```

---

## Phase 2

**Description:**
```
[Type] handoff from [role] to [role]. Transfers: [what]. Accepted when: [check]. [What happens.] Ends when [end state].
```

[Continue through the last phase, which closes with "Ends the workflow when [end state]."]

---

## Notes & Assumptions

### Sources and confidence
- [Each input, most recent first, with confidence]

### Structure notes
- [Reusable-process references, single-activity processes kept, rule deviations, tentative sub-function table]

### Assumptions to verify
- [Inferred roles with confidence, provisional working states from conflicts]

### Operator questions
1. [Closed question with a proposed answer]

### Change table
| Original | Applied | Rule | Verb inferred? |
|---|---|---|---|
````

The `SOP checklist:` heading is literal. Downstream tools parse it.

## 10. Checklist

Run before presenting. Report only failures.

- No personal names, client names, dates, or software in any description.
- Titles: verb first on activities; "Workflow" and "Process" suffixes present.
- Every field within its cap.
- Every process has at least one role, a trigger, an end state, and at least two activities.
- Every handoff typed; acceptance criteria present or UNKNOWN.
- Trigger and end-state chain holds in every process.
- Decision points show their branches.
- Change table complete; inferred verbs listed as operator questions.

## Sub-skills

- `/wa-workflow architect`: raw input to first-draft map
- `/wa-workflow condense`: first draft to condensed map
- `/wa-workflow gap-analysis`: condensed map to gap report
