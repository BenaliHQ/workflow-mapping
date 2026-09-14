---
name: wa-start
description: "Start here when you are not sure which Work Architecture skill to run. Asks what you have, sends you to the right skill, and tells you what to have ready."
---

# wa-start

## What this skill does

You find out what the user has and send them to the right skill. You do not do the mapping here.

If this is their first time, point them at `/wa-primer` first; it is a five-minute read. Do not block on it.

## Ask what they have

```
What do you have?

  1. Raw material about a workflow: notes, a transcript, a document, a file,
     a task-tool export, or a draft from an earlier session
  2. Nothing written down, or only a thin sketch. Ask me questions.
  3. A first-draft map I want to tighten
  4. A condensed map I want checked for gaps
  5. Three or more condensed maps. Build the function chart.
  6. A function chart I want reviewed
  7. I am stuck on one call: activity, process, phase, sub-function, function, or role
```

## Send them on

| They have | Run | Have ready |
|---|---|---|
| 1 | `/wa-workflow architect` | The material in full. For a file, the path. For a task export, the tree with assignees and checklists. For a resume, the old draft plus the new input. |
| 2 | `/wa-interview` (solo, or sparse if there is a thin sketch) | Nothing. Trigger and end state help. |
| 3 | `/wa-workflow condense` | The first-draft map |
| 4 | `/wa-workflow gap-analysis` | The condensed map, the industry, the size of the operation |
| 5 | `/wa-function-chart architect` | All the condensed maps, the business name |
| 6 | `/wa-function-chart gap-analysis` | The chart; the condensed maps too if they want drift checked |
| 7 | `/wa-decide [activity, process, phase, subfunction, function, role]` | The thing in question and where it sits |

If none fit, ask one question: *"In a sentence, what do you have and what do you want out of it?"* Then pick the closest row.

## Before they go

Say three things: which skill they are about to run, what it will hand back, and what usually comes next (architect, then condense, then gap-analysis; chart after three condensed maps).

Output from every skill is markdown in the ops map source format. It stays in the conversation unless they ask to save it.

## Never

- Answer the mapping question here. Route.
- Run two skills in one turn.
- Write to their filesystem unless asked.
