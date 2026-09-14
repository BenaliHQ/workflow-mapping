---
name: wa-workflow architect
description: "Turn raw input (ops map entry, transcript, interview notes, files, task-management exports, or a verbal description) into a first-draft Workflow Map in the ops map source format. Flags what the source does not say. Never invents content."
---

# wa-workflow architect

## What this skill does

You are given raw material about how some work gets done. You turn it into a first-draft Workflow Map in the ops map source format.

The rules for what a good map looks like live in `wa-workflow/SKILL.md`. Read that file first. This file only tells you the order to work in.

Two things matter most:

- The map says only what the source says. Anything the source does not say is marked UNKNOWN and becomes a question for the operator.
- The client's own words are the vocabulary. You do not coin terms.

## The steps

### Step 1. Know what you have

Look at the input and name its type: ops map entry, transcript, interview notes, a file, a task-management export, a verbal description, or an old draft plus new material. If you cannot tell, ask once.

Three input types need extra handling before you start. See the appendix for each:

- A file (PDF, docx, image): Appendix A.
- A task-management export (ClickUp, Asana, Monday): Appendix B.
- An old draft plus new input: Appendix C.

Then check for thinness. If the input holds fewer than about 15 concrete steps or actions, it is not enough to build a map from. Say so and offer two choices: switch to `/wa-interview sparse` so the gaps get filled by questions (recommended), or build anyway with UNKNOWN in every field the source cannot fill and the output marked DRAFT.

### Step 2. Confirm the workflow's edges

Confirm three things with the user: the workflow's name, what triggers it, and what its end state is.

No trigger or no end state means there is no workflow yet. Keep asking until both are clear. In a run with no user present, log them as operator questions and continue.

### Step 3. Find the phases

Read the whole source. Mark each place where the work changes hands between functions, or where the character of the work shifts. Those are the phase boundaries.

A workflow has as many phases as the work has stages. Do not add or merge phases to hit a number.

### Step 4. Find the processes inside each phase

Within a phase, group the activities that run in order and produce what the next group needs. Each group is a process.

For every process, get three things from the source: the role or roles that do it, what triggers it, and its end state. A process can have more than one role when different roles do different activities inside it; note the Role handoff in the process description. "The team" is not a role. If any of the three is missing, it is UNKNOWN and an operator question.

Before naming a process, check `_process-registry.md`. If the same process already exists in another workflow, reference it instead of defining it again.

### Step 5. Find the core activities inside each process

List the candidate activities the source describes for each process. Run the parent's three tests on each one. What passes is a core activity. What fails becomes an `SOP checklist:` line under the activity it belongs to.

For each core activity, fill from the source: Software (if a tool is named), a tentative two-word Sub-function, Trigger, End state, and Status.

### Step 6. Type the handoffs and capture the branches

At every phase boundary, write the one-line handoff from the parent rules: type, sender, receiver, what transfers, accepted when. If the source does not say how the receiver accepts the work, write UNKNOWN. Do not guess acceptance criteria.

Wherever the source says work can go one way or another, capture the decision point: the question, who decides, and each branch.

### Step 7. Ask about the unhappy paths

Ask the user, once, in one short list:

- What happens when a key handoff is rejected?
- What happens when work has to be redone?
- Are there approvals that can loop back?
- What happens when the client delays, cancels, or changes scope?

Record what they say. Record "not captured" for what they do not know. Never invent a branch.

### Step 8. Show the outline and get one confirmation

Before writing any field text, show the skeleton:

```
Phase 1: [name]
  Process 1.1: [name]. Role: [role]. [N] activities.
  Process 1.2: ...
Phase 2: [name]. Handoff in: [type], [sender] to [receiver].
  ...
Roles I inferred (please confirm): [list, with confidence]
Reusable processes referenced: [list]
```

Ask: *"Does this match how the work moves? Anything missing, out of order, or wrong?"* Fix it until they say yes. This is the one confirmation step; there is no field-by-field approval later.

If the source came with its own labels ("Step 1", or a tool's "phase" or "list"), add a small table showing what each label became and why. This is required whenever the source uses methodology words for a different level.

### Step 9. Write the map

Fill every field per the parent's template and length caps. Use the client's words. Apply naming fixes directly and log each one in the change table. Flag any activity where you had to choose the verb yourself.

Fill Notes and Assumptions under its four headings: every gap, inferred role, contradiction, rule deviation, and unanswered probe goes there.

### Step 10. Check, present, hand off

Run the parent's checklist and report only what failed. Present the map. Ask: *"Does this match how work actually moves? Anything I guessed that you need to correct?"*

Then point to the next step: *"Run `/wa-workflow condense` to test every activity and fold what is not a core activity into SOP checklists."* If open operator questions still block the structure, say that instead.

## If the user is stuck on a judgment call

Send them to `/wa-decide` only for calls you cannot make from the source:

- Is this an activity or a checklist item? `/wa-decide 1`
- Is this one process or two? `/wa-decide 2`
- Is this a phase or a process? `/wa-decide 3`

Ask them to paste the Decision block back when they return.

## Never

- Fill a missing field by inference. UNKNOWN, then a question.
- Skip the Process level.
- Add or merge phases, processes, or activities to hit a count.
- Choose between two sources that disagree without saying so.
- Invent an unhappy path or an acceptance criterion.
- Present a map with unresolved UNKNOWNs as ready to paste.

---

## Appendix A. Files

Read the file. Rate how well you could extract it:

| Confidence | File types |
|---|---|
| High | Plain text, markdown, native Word or Google Docs exports |
| Medium | Searchable PDFs, screenshots of documents |
| Low | Scanned PDFs, photos of whiteboards or flipcharts |

High: go straight to Step 1's thinness check.

Medium or low: show the user what you extracted (the first section in full, then a summary of the rest), flag the parts you are unsure of, and wait for their corrections before structuring anything.

Diagrams and arrows: you can read the labels but not the flow. Ask the user what the connections mean.

## Appendix B. Task-management exports

Task-tool data is ground truth: real tasks, real assignees, real completion states. Treat it as high confidence. No echo step.

Three rules:

1. **The tool's levels are not the map's levels.** A ClickUp "phase" may be process-sized. Classify each container yourself: a container with its own owner and a handoff at its edges is a Phase; a run of tasks toward one set of outputs is a Process; a task or checklist item is a Core Activity or an SOP checklist line. Show the mapping in Step 8's label table.
2. **Assignees are role evidence.** A container where one person holds every task points to a role. This counts as step 3 of the parent's name-to-role ladder.
3. **Templates are not proof.** Before an activity from a template defaults to active, check it against at least one completed real instance. Where they differ, treat it as conflicting sources.

Task tools record happy paths only. Unhappy paths and acceptance criteria are always follow-up questions on this input.

## Appendix C. Resuming an old draft

Say in a few lines what the old draft already holds and what the new input adds, changes, or contradicts. For each contradiction, use the parent's conflicting-sources rule. Get the user to confirm the merged picture, then continue from Step 3.
