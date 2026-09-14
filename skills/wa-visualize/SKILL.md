---
name: wa-visualize
description: "Turn a finished Workflow Map into something people can read: a Benali-branded print PDF, an interactive scrolling web page, or a session questions document that gathers every open operator question across several maps."
argument-hint: "<workflow.md> [print | web | questions]"
---

# wa-visualize

## What this skill does

You take a map in the ops map source format and render it into one of three outputs. The map stays the source of truth; every render is an export.

| Output | Script | Use it for |
|---|---|---|
| print | `scripts/render.py` | A client-facing PDF: cover, one page per phase, notes page |
| web | `scripts/render_interactive.py` | A scrolling HTML page for a review site or a phone |
| questions | `scripts/render_questions.py` | One PDF holding every open operator question across several maps, grouped by workflow with phase anchors, for a mapping session |

If the user did not say which, ask once. Default to print for a single map going to a client.

The scripts ship in this skill's folder. They are plain Python with no dependencies. Missing fields render as UNKNOWN; they are never filled in.

## Before rendering

A map full of unresolved UNKNOWNs renders with a DRAFT badge and UNKNOWN tags. That is deliberate. If the audience is the client, resolve the operator questions first, or tell the user the badge will show.

Use the directory the map lives in as the working directory unless the user names another.

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

## Web

```bash
python3 <skill-dir>/scripts/render_interactive.py <map.md> -o <workdir>/<slug>.html
```

Open it in a browser and check it on a narrow viewport too. Deliver the HTML path. If it is going onto a review site, follow that repo's deploy pattern; do not improvise one.

## Questions

```bash
python3 <skill-dir>/scripts/render_questions.py map1.md map2.md ... \
  -o <workdir>/questions.html --title "[Client] Mapping Session Questions"
```

Then export and verify the PDF exactly as for print. Deliver both paths.

## Never

- Edit the map to make it render. Fix the map through the mapping skills, then re-render.
- Ship a PDF without the page-count and thumbnail check.
- Hide a DRAFT badge or UNKNOWN tag.
- Add a color or hex value that is not in the theme's token block. Brand changes land in `assets/atlas-workflow-theme.css`, from the brand guidelines, first.
