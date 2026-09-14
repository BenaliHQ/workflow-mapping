---
name: wa-interview
description: "Get a workflow out of someone's head by asking questions, one section at a time. Two modes: interview the user from nothing (solo), or fill the gaps in a thin transcript, document, or notes (sparse). Catches the steps experts skip. Output feeds /wa-workflow architect."
argument-hint: "[solo | sparse]"
---

# wa-interview

## What this skill does

When there is not enough written input to build a map, you get the workflow by asking. You work one section at a time, show what you have captured, and only then move on. The output is a confirmed outline that `/wa-workflow architect` turns into the map.

The rules for what the outline must contain live in `wa-workflow/SKILL.md`. Read it first.

Two modes. If none was given, ask which fits:

| Mode | When |
|---|---|
| solo | The user is describing their own workflow with nothing written down |
| sparse | The user has a transcript, a document, or some notes that leave gaps |

## The problem you are solving

People who run a workflow every day skip steps when they describe it. They say "then we send the proposal" and leave out that someone pulled the pricing, someone checked it, and someone got it approved. Those skipped steps are real work, often with their own owner and their own tool. Your job is to notice the jump and ask.

## The steps

### Step 1. Set the edges

Ask, one at a time: what the workflow is called (ending in "Workflow"), what event starts it, how they know it is finished, how often it runs, who mostly does it.

Do not go further without a trigger and an end state.

In sparse mode, first say what the input already gives you and what it does not, so the user knows why you are asking.

### Step 2. Walk the workflow one section at a time

A section is a stretch of work that belongs together, usually one phase or one process. Start at the trigger.

For each thing the user describes, get four facts: who does it (job title, not name), what has to be true before they can, what comes out when it is done, and what tool they use if one is central.

**Catch the skipped steps.** After each thing they describe, check for a jump before moving on:

- If the output of one step is not the input of the next, ask what happens in between.
- If something appears that nobody made ("the estimate", "the signed contract"), ask who produced it and when.
- If a step needs a decision or an approval, ask who gives it and what happens when they say no.
- If a person or role appears for the first time, ask how the work reached them.
- If they say "just", "obviously", "of course", or "we always", ask them to spell out that step anyway.

Ask about one gap at a time. Do not stack questions.

### Step 3. Recap the section before moving on

When a section feels complete, show what you have, as a plain list:

```
So far, [section name]:
1. [Verb] [object]. Role: [role]. Tool: [x].
2. ...
Next thing after this: [what the user said comes next]
```

Ask: *"Anything missing between these? Anything out of order?"* Fix it, then move to the next section. Never move on with an unconfirmed section.

### Step 4. After the last section, ask about handoffs and branches

With the whole path captured, go back over it once:

- Where does the work change hands between functions, roles, or out to a client or vendor? For each: who sends, who receives, what moves, how both sides know it landed.
- Where can the work go one way or another? What is the question, who decides, what happens on each side?
- What happens when a handoff is rejected, when work is redone, when an approval loops back, when the client delays or changes scope?

"I do not know" and "that does not happen" are answers. Record them; never fill them in.

### Step 5. Show the whole outline and confirm

Turn the sections into the outline shape from `/wa-workflow architect` Step 8: phases, processes with role and activity count, handoffs in, roles inferred, reusable processes referenced. Show it. Ask: *"Does this match how the work actually moves?"* Fix until they say yes.

### Step 6. Hand off

*"I will run this through `/wa-workflow architect` to write the map. Continue?"* Pass the confirmed outline in with a note that the structure is already confirmed, so the architect skips its own confirmation step.

## Mode notes

**Solo.** Everything comes from the conversation. Expect more skipped steps, not fewer; the user knows the work too well.

**Sparse.** Walk the input's own order. For each thing it mentions, get the four facts and check for jumps exactly as in Step 2. Where the input contradicts what the user now says, show both and ask which is current.

## Never

- Invent a step, owner, trigger, end state, branch, or handoff. Ask, then record what was said.
- Go past the edges without a trigger and an end state.
- Move to the next section before the user confirms the recap.
- Accept "then we send it" without asking what had to happen first.
- Convert a name to a role without showing the mapping.
- Produce a map without a confirmed outline.
