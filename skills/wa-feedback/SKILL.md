---
name: wa-feedback
description: "Tell the maintainers what a wa-* skill got wrong, what it got right, and what you worked around. Files a GitHub issue on BenaliHQ/workflow-mapping."
---

# wa-feedback

## What this skill does

You capture one piece of feedback about a wa-* skill and file it where the maintainers will see it. Capture only. Do not try to fix the skill here.

## Ask three things

1. Which skill, and what were you mapping?
2. What went wrong or felt off? Be specific: what you asked, what it did, what you expected.
3. What did you do instead, or what would you change?

If they also want to say what worked, take it. Do not press.

## File it

```bash
gh issue create --repo BenaliHQ/workflow-mapping \
  --title "wa-feedback: [skill] — [one line]" \
  --label "wa-feedback" \
  --body "[the three answers, in the user's words]"
```

If the label does not exist, file without it. If `gh` is unavailable or has no access, save the entry as `wa-feedback-[date].md` in the current directory and say to send it to the maintainer.

Tell the user where it went.

## Never

- Reword the user's feedback. File what they said.
- Write inside the installed plugin folder. It is a sync cache and gets wiped.
- Fix the skill in this session. That happens in the bundle.
