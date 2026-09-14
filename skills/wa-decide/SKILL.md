---
name: wa-decide
description: "Interactive help when you are stuck on one Work Architecture call: core activity or checklist item, one process or two, phase or process, one sub-function or two, function or sub-function, or what role a person maps to. Walks the test and hands back a short decision to paste into the skill you came from."
argument-hint: "[activity | process | phase | subfunction | function | role]"
---

# wa-decide

## What this skill does

You help the user make one call they are stuck on, by walking the test with them so they can make the same call themselves next time. You hand back a short decision block they paste into the skill they came from.

The tests live in `wa-workflow/SKILL.md` and `wa-function-chart/SKILL.md`. Read both first.

If the user gave an argument, go straight to that decision. If they pasted context from another skill, use it; ask only for what is missing. Otherwise ask which one:

```
1. Is this a core activity, or a step inside one?
2. Is this one process or two?
3. Is this its own phase, or part of one?
4. Is this one sub-function or two?
5. Is this a function, or a sub-function of one?
6. What role does this person map to?
```

Every decision ends with the same block:

```
Decision: [the call]
Because: [one line per test, pass or fail, with why]
Apply: [the rewrite, the split, the merge, or the role to use]
```

Then say: *"Paste this back into the skill you were running, or tell me to continue there with it."*

## 1. Core activity or step

Ask for the activity name and what it involves. Run the parent's three tests in order and stop at the first no:

- Outcome: does it produce a distinct result the next activity depends on?
- SOP: would you write a separate SOP for it?
- Assignment: could it be a standalone task on someone's list?

Three yeses: core activity. Any no: a step inside the parent activity, written as an SOP checklist line.

Then size it: could you write a 5 to 10 line checklist for it? Much longer means split it; one or two lines means fold it.

If a tool is involved, decide where it goes: the Software field always; the title only when using the tool is the work ("Log deal stage in HubSpot", not "Review proposal in Google Docs").

## 2. One process or two

Ask for the activities and their order. Three questions:

- Would you explain these as one unit of work, or two?
- Do they all lead to one set of outputs, or to two different results?
- Do the roles change partway through? If so, is that a role handoff inside one process, or the start of a different process?

One unit, one set of outputs: one process, even with several roles. Two results, or work someone would describe separately: two processes.

## 3. Phase or process

Ask for the candidate phase and its neighbors. Two questions:

- At its boundaries, does the work cross between functions?
- Does the work change character here: different expertise, different tools, different goal?

Yes to either: its own phase. No to both: a process inside the neighboring phase.

## 4. One sub-function or two

Ask for the activities. One question, the specialization test:

*If you hired one person to do all of these, would they need the same training and use the same expertise for every one?*

Yes: one sub-function. No: two.

Remind the user what does not split a sub-function: cadence, which workflow the activity came from, who does it today.

## 5. Function or sub-function

Ask what the work area is. One question: is this a major area of responsibility for the business on its own, or a kind of work inside a broader one?

Common calls:

| Candidate | Usually |
|---|---|
| Marketing, Finance, Sales | Function |
| Lead Generation | Sub-function of Sales or Marketing |
| Client Onboarding | Sub-function of Operations or Client Success |
| Client Success | Function in a recurring-revenue business |
| Content Production | Sub-function of Marketing, or a function when content is the product |
| Administration | Function, kept to generic admin work only |

## 6. What role a person maps to

Ask for the sentence with the name in it and what that person does. Walk the parent's ladder in order and stop at the first step that answers:

1. Ask the user for the title.
2. Find an explicit title in the source.
3. Use a consistent assignee pattern in task-tool data.
4. Infer from responsibilities.
5. Use "Team member responsible for [function]".

State the confidence (high for steps 1 and 2, medium or low below that). Anything below high gets a note in Assumptions to verify. Never map a name from another engagement.

## Never

- Skip the test because the answer looks obvious. The user is learning the test.
- Add a test that is not in the parents.
- Decide an ambiguous case alone. When the tests split, show the split and ask.
