---
name: wa-visualize
description: "Turn one or more finished Workflow Maps into something people can read. Default: a client review site with a page per workflow and a review page where the client answers open questions in place and copies the answers back by email. Also: a Benali-branded print PDF."
argument-hint: "<workflow.md ...> [site | print]"
---

# wa-visualize

## What this skill does

You take one or more maps in the ops map source format and render them. The maps stay the source of truth; every render is an export.

| Output | Script | Use it for |
|---|---|---|
| site (default) | `scripts/render_site.py` | The client walkthrough and review: an index, a read-only page per workflow, and a review page with open questions the client answers in place |
| print | `scripts/render.py` | A client-facing PDF, only when someone needs a file: cover, one page per phase, notes page |

Default to **site**, for one workflow or many. Use print only when a PDF is asked for.

`scripts/render_interactive.py` (web) and `scripts/render_questions.py` (questions PDF) are superseded by site as of 1.6.0. They still run, but do not reach for them for new work.

The scripts ship in this skill's folder. They are plain Python with no dependencies. Missing fields render as UNKNOWN; they are never filled in.

## Before rendering

A map full of unresolved UNKNOWNs renders with a DRAFT badge and UNKNOWN tags. That is deliberate. If the audience is the client, resolve the operator questions first, or tell the user the badge will show.

Use the directory the map lives in as the working directory unless the user names another.

## Site

What the client sees, per workflow: each phase as its own card with a navy header; processes with their role; core activities with role, software pills (one fixed colour per tool) and status (active green, draft blue, gap orange). Clicking an activity opens its description, a yellow Trigger pill and a green End state pill. No SOP checklists appear. The review page adds a question card beside each activity that has one, with a response box; the reviewer types answers, then presses Copy responses and pastes the text into an email. Answers stay in the reviewer's own browser until they copy them.

### 1. Write the inputs next to the maps

`site.json`, paths relative to it:

```json
{
  "client": "Apex Construction Co.",
  "title": "Apex workflow maps",
  "base": "/apex",
  "out": "../../../apex",
  "maps": [
    {"source": "sources/office-bidding-workflow.md", "slug": "office-bidding-workflow", "tab": "Office bidding", "title": "Office bidding and pre-construction"}
  ],
  "updates": "updates.json",
  "questions": "questions.json"
}
```

- `base` is the site path the pages are served from (`/apex` on a review site). Leave it empty to preview from disk.
- `tab` is the short name on the review page tab; `title` defaults to the map's workflow title.
- One map is fine. The tabs disappear and the review covers that workflow.

`questions.json` (optional; no file means no review page). Keyed by map slug. Each question is pinned to the activity it is about:

```json
{"office-bidding-workflow": [
  {"at": "5.3.2", "q": "When the principal approves a trade's bid request, is that the trade's signed scope?", "guess": "Yes"},
  {"at": "phase:4", "q": "Should RFIs stay part of this workflow instead of getting their own?"}
]}
```

- `at` is an activity number, `proc:N` for a process, or `phase:N` for a phase. Pin to the most specific thing the question is about.
- Write every question for the client to read cold: plain words, one question, answerable yes/no or with a short pick. Roles only, never names and never "you". Add `guess` when you have a likely answer.
- Do not paste the map's Operator questions as they are. Rewrite each one, drop any that point at notes the client cannot see, and drop any already answered.
- An activity with an open question renders as draft, even if the map says active.

`updates.json` (optional). Agreed changes on top of a map, keyed by map slug, then by activity number:

```json
{"office-bidding-workflow": {
  "proc:5.2":  {"role": "Principal, Superintendent"},
  "5.3.3":     {"doer": "Office Manager"},
  "3.1.3":     {"sw": "JobTread", "desc": "Sent through JobTread, like the construction agreement."},
  "2.1.2":     {"status": "active"},
  "6.3.1":     {"n": "6.3.2"},
  "add:5.3.3": {"n": "5.3.4", "title": "Request current insurance from trades with lapsed documents", "doer": "Office Manager", "sw": "JobTread", "status": "gap"},
  "before:6.3.1": {"n": "6.3.1", "title": "Build the list of open items before cleaning starts", "doer": "Superintendent", "status": "gap"}
}}
```

- Fields: `title`, `doer` (the activity's role; defaults to the process role), `sw`, `status`, `desc` (shown as the first paragraph of the description), `n` (renumber). `add:X` inserts after X, `before:X` inserts before X.
- Only record changes the operator agreed to, with the source in your notes. When the change is settled, fold it into the map itself through the mapping skills and remove it here.

### 2. Render

```bash
python3 <skill-dir>/scripts/render_site.py <path>/site.json
```

It refuses to render when an update or question points at an activity that is not on the map. Fix the pin; never delete the question to make it pass.

### 3. Check before sharing

- Open `review.html` and one workflow page. Check a phone-width window too.
- Expand an activity: description, Trigger and End state only.
- Type a test answer, press Copy responses, paste somewhere, then clear the box.
- Every software name has a colour in `assets/tool-colors.json`. Add a new tool there rather than letting it fall back to a borrowed colour.
- If it goes onto a review site, follow that repo's deploy pattern. Publishing puts it in front of the client, so the operator approves the push.

## Print

1. Render:

   ```bash
   python3 <skill-dir>/scripts/render.py <map.md> -o <workdir>/<slug>.html
   ```

   Read stderr. Parse warnings mean a field the renderer could not find. Pagination warnings mean content that will not fit a page. Zero pagination warnings before continuing.

2. Export:

   ```bash
   CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
   "$CHROME" --headless --disable-gpu --no-pdf-header-footer \
     --print-to-pdf="<workdir>/<slug>.pdf" "file://<abs-path>/<slug>.html"
   ```

3. Verify the PDF. The HTML render is not proof.
   - Page count matches what the renderer reported. A mismatch means silent overflow or clipping.
   - Thumbnail every page with `qlmanage -t -s 1200 -o <workdir> "<slug>.pdf"` and look at each: cover first (grid artifacts show on grounds), then every phase page (no clipped rows), then the notes page.
   - Brand check: clean hairline grid, Majorelle as ink only, no color fills.

   Anything wrong: fix and re-export. Never hand over a PDF you did not look at.

4. Deliver the PDF path and the HTML path.

## Superseded outputs

`render_interactive.py` (single-map web page) and `render_questions.py` (questions PDF) remain for old deliverables only. Their usage is in each script's header.

## Never

- Edit the map to make it render. Fix the map through the mapping skills, then re-render.
- Ship a PDF without the page-count and thumbnail check.
- Hide a DRAFT badge or UNKNOWN tag.
- Add a color or hex value that is not in a theme's token block. Print colours live in `assets/benali-print-theme.css`; site colours live in `assets/benali-review-theme.css`, synced from benali-design (Business system tokens, App system category hues). Re-sync from the design system; never invent a value.
- Put a person's name in a question, an update, or any site copy. Roles only.
- Show SOP checklists on the site.
