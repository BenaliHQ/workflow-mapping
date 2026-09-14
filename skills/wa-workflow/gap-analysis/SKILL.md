---
name: wa-workflow gap-analysis
description: "Review a condensed Workflow Map for what is missing or weak: structural rule failures, claims the activities do not back up, industry practices the map does not cover, and handoffs likely to fail. Produces a short prioritized report plus paste-ready fixes and gap entities."
---

# wa-workflow gap-analysis

## What this skill does

You take a condensed map and find what is missing, weak, or inconsistent. You hand back a short report and paste-ready patches.

The rules live in `wa-workflow/SKILL.md`. Read that file first.

Two kinds of finding, kept apart:

- **Structural findings** are rule failures. State them as facts.
- **Coverage findings** are practices this kind of workflow usually has. State every one as a question: *Typical in [industry] [workflow type]: [practice]. Does this apply here?* Never as a requirement.

Run on a condensed map. If the input is a first draft, send it to `/wa-workflow condense` first.

## The steps

### Step 1. Get the context

Ask for four things: the industry, the workflow type, the size of the operation (solo, small team, larger org), and the condensed map. If industry is unclear, ask: *"What do they sell, and who buys it?"* In a run with no user, take these from the run brief and the map's frontmatter; if industry stays unknown, skip Step 4.

### Step 2. Structural check

Go through the checklist at the end of `wa-workflow/SKILL.md`, item by item. Each item the map fails is a structural gap. Write it down with where it is (phase, process, or activity number).

Two things are not structural gaps, so do not list them here:

- A handoff that has a type but says UNKNOWN for its acceptance criteria. That is missing information, not a broken rule. It goes to the handoff risk list in Step 5.
- The first phase having no handoff-in line, and the last phase having no handoff-out line. That is how the template works.

### Step 3. Internal consistency check

Read every phase and process description and check the claims against the activities beneath them:

- An end state that no activity produces.
- Something transferred at a handoff that no activity creates.
- A trigger that nothing upstream fires.

These are the highest-value gaps and need no research. Each one becomes a question: *Your map says [claim], but no activity produces it. Does that step exist unmapped, or is it missing?*

### Step 4. Coverage check, from research

Do not recommend practices from general knowledge. Search, then judge the sources.

1. Search for *[industry] [workflow type] best practices* and *common gaps in [industry] [workflow type]*. Read the top few results. Pull clean text with WebFetch or Defuddle when a source looks useful.
2. Rate each source. High: standards bodies (APQC, PMI, ISO, SCOR), peer-reviewed or academic work, major analyst firms. Medium: trade publications, major consulting firms, trade associations, recognized practitioner books. Low: vendor marketing, listicles, SEO content.
3. One high source, or two medium sources, supports a hypothesis. Low sources alone do not; skip the recommendation and say so. In fields with no standards bodies (trades, creator work), three independent practitioner sources agreeing may be cited as a downgraded signal, labeled as such.
4. When good sources disagree, show both positions and let the user choose. Do not blend them.
5. Cite every source used: URL, tier, date accessed.

Scale to the business. A solo operator does not get told they lack an HR function.

If search is unavailable or returns nothing useful, say so and limit the report to Steps 2, 3, and 5.

### Step 5. Handoff risk

Score each handoff. Functional handoffs start high. Any handoff with UNKNOWN or vague acceptance criteria goes up one level. External handoffs are high when criteria are vague. Role handoffs start low.

For every high-risk handoff, propose what the acceptance criteria should cover, as a question to the user.

### Step 6. Write the report

Keep it short. The reader should know in one screen what is broken and what is worth adding.

```markdown
# Gap Analysis: [Workflow Name]

Industry: [x]. Workflow type: [x]. Map: [N phases, M processes, K activities].
Sources: [URL, tier, date] ...

## Summary
One sentence: strong on X, weak on Y, N structural gaps, M coverage questions, K handoff risks.

## Structural gaps
1. [What is wrong, where.] See Fix 1.

## Consistency questions
1. [Claim vs. activities.] Does this step exist unmapped, or is it missing?

## Coverage questions
1. Typical in [industry] [workflow type]: [practice]. Sources: [...]. Does this apply here? If yes, see Gap Entity 1.

## Handoff risks
1. Phase [N] to [N+1], [type]. Risk: [level]. Acceptance criteria should cover: [...]. Agree?

## Priority
P0 structural: [list]. P1 consistency and handoff: [list]. P2 coverage: [list].
```

Then the patches, in the ops map source format:

**Fix blocks**, one per structural gap: the field to change, its current value, the replacement value, and one line on why. When the right value is exactly what the operator has to supply (a missing role, a missing end state), do not invent it. Emit the block with bracketed placeholders, headed *Blocked on operator question [N]*, marked not ready to paste.

**Gap entity blocks**, one per coverage question the user confirms: full process or activity blocks with Status set to gap, written within the parent's voice caps. In a run with no user, emit them for every hypothesis, each tagged with the question that gates it, under a banner saying do not paste before confirmation.

In a run with no user, the report carries a DRAFT banner and its operator questions continue the map's numbering.

### Step 7. Hand off

*"Fix the P0 items, then re-run this skill to confirm. With three or more gap-reviewed maps, run `/wa-function-chart architect`."*

## Never

- Recommend a practice without a source that meets the threshold.
- Write a coverage finding as a requirement.
- Fill a blocked fix with a plausible value.
- Flag a cosmetic issue as structural. A wrong name is cosmetic; a missing step is structural.
- Guess the industry.
