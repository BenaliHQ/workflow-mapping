#!/usr/bin/env python3
"""Render the operator questions from one or more Workflow Maps into a single
Atlas-branded, print-ready questions document (HTML -> Chrome -> PDF).

Built for mapping sessions: one document holding every open question, grouped
by workflow, each question carrying its phase anchor so the session can walk
a workflow on screen and answer its questions in order.

Usage:
    python3 render_questions.py map1.md map2.md ... -o questions.html \
        --title "Mapping Session Questions"
"""

import argparse
import html
import math
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from render import (  # noqa: E402
    QUESTION_TAG_RE,
    emphasize_title,
    estimate_text_lines,
    load_theme_css,
    parse_workflow,
    titleize_slug,
)

COLUMN_LIMIT = 560


def esc(text):
    return html.escape(text or "")


def inline(text):
    escaped = esc(text)
    escaped = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", escaped)
    return escaped


def split_question(text):
    match = re.search(r"\?", text)
    if match:
        return text[: match.end()].strip(), text[match.end():].strip()
    return text.strip(), ""


def collect(paths):
    """Parse every workflow and collect its questions with phase anchors."""
    workflows = []
    for path in paths:
        data = parse_workflow(path)
        phase_titles = {int(p["number"]): p["title"] for p in data["phases"]}
        questions = []
        for number, raw in enumerate(data["notes"]["operator_questions"], 1):
            tag = QUESTION_TAG_RE.match(raw)
            clean = QUESTION_TAG_RE.sub("", raw, count=1).strip()
            question, context = split_question(clean)
            phase = int(tag.group(1)) if tag else None
            questions.append(
                {
                    "number": number,
                    "phase": phase,
                    "phase_title": phase_titles.get(phase, ""),
                    "question": question,
                    "context": context,
                }
            )
        workflows.append(
            {
                "data": data,
                "title": data["workflow"]["title"],
                "questions": questions,
                "parse_warnings": data["parse_warnings"],
            }
        )
    return workflows


# ---------------------------------------------------------------- pagination


def estimate_entry_height(entry):
    height = 20 + estimate_text_lines(entry["question"], 58) * 15
    if entry["context"]:
        height += estimate_text_lines(entry["context"], 64) * 13 + 4
    if entry["phase"]:
        height += 15
    return height + 10


def paginate(questions, warnings, context):
    """Split one workflow's questions into pages of two sequential columns."""
    pages = []
    columns = []
    current = []
    height = 0
    for entry in questions:
        entry_height = estimate_entry_height(entry)
        if entry_height > COLUMN_LIMIT:
            warnings.append(f"{context}: question Q{entry['number']} exceeds the column box")
        if current and height + entry_height > COLUMN_LIMIT:
            columns.append(current)
            current = []
            height = 0
            if len(columns) == 2:
                pages.append(columns)
                columns = []
        current.append(entry)
        height += entry_height
    if current:
        columns.append(current)
    if columns:
        pages.append(columns)
    return pages or [[[]]]


# ---------------------------------------------------------------- rendering

DOC_CSS = """
.q-cover-rail { display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px; margin-top: 0.24in; }
.q-cover-card {
  background: var(--bone); border: 1px solid var(--line); border-radius: 10px;
  padding: 13px 16px; display: flex; align-items: baseline; justify-content: space-between; gap: 12px;
}
.q-cover-card .t { font-size: 14px; font-weight: 700; }
.q-cover-card .c { color: var(--majorelle); font-size: 12px; font-weight: 700; white-space: nowrap; }
.q-doc-header { display: flex; align-items: baseline; justify-content: space-between; gap: 16px; margin-bottom: 0.18in; }
.q-doc-title { font-size: 24px; font-weight: 700; letter-spacing: -0.015em; margin: 4px 0 0; }
.q-columns { display: grid; grid-template-columns: 1fr 1fr; gap: 0.34in; align-items: start; }
.q-entry { display: grid; grid-template-columns: 34px 1fr; gap: 10px; padding: 7px 0; border-bottom: 1px solid var(--line-faint); }
.q-entry-num { color: var(--majorelle); font-size: 11px; font-weight: 700; letter-spacing: 0.08em; }
.q-entry-phase {
  display: inline-block; border: 1px solid var(--line-strong); border-radius: 4px;
  color: var(--slate-mid); font-size: 8.5px; font-weight: 700; letter-spacing: 0.1em;
  padding: 0 5px; text-transform: uppercase; margin-bottom: 3px;
}
.q-entry-text { font-size: 12.5px; font-weight: 600; line-height: 1.4; margin: 0; }
.q-entry-context { color: var(--slate-mid); font-size: 11px; line-height: 1.4; margin: 3px 0 0; }
.q-answer-line { border-bottom: 1px dotted var(--line-strong); height: 16px; margin-top: 6px; }
"""


def render_entry(entry):
    phase_chip = ""
    if entry["phase"]:
        phase_chip = f'<span class="q-entry-phase">Phase {entry["phase"]}</span><br>'
    context = ""
    if entry["context"]:
        context = f'<p class="q-entry-context">{inline(entry["context"])}</p>'
    return f"""
      <div class="q-entry">
        <div class="q-entry-num">Q{entry["number"]}</div>
        <div>
          {phase_chip}
          <p class="q-entry-text">{inline(entry["question"])}</p>
          {context}
          <div class="q-answer-line"></div>
        </div>
      </div>
    """


def render_footer(meta):
    return f"""
      <footer class="page-footer">
        <div class="wordmark" aria-label="Benali"></div>
        <div class="footer-meta">{esc(meta)}</div>
      </footer>
    """


def render_cover(title, workflows, meta):
    total = sum(len(w["questions"]) for w in workflows)
    cards = "".join(
        f"""
        <div class="q-cover-card">
          <span class="t">{inline(w["title"])}</span>
          <span class="c">{len(w["questions"])} questions</span>
        </div>
        """
        for w in workflows
    )
    return f"""
    <div class="page page--grid cover">
      <div class="cover-top"><div class="kicker">WORK ARCHITECTURE — SESSION QUESTIONS</div></div>
      <h1>{emphasize_title(title)}</h1>
      <p class="workflow-description">{total} open questions across {len(workflows)} workflow maps.
      Each question is anchored to the workflow and phase it belongs to; answer them in order while
      walking the maps, and the answers become the next revision of each map.</p>
      <div class="q-cover-rail">{cards}</div>
      {render_footer(meta)}
    </div>
    """


def render_question_page(workflow, columns, page_index, page_count, meta):
    continued = " (continued)" if page_index > 0 else ""
    cols = "".join(
        f'<div>{"".join(render_entry(entry) for entry in column)}</div>' for column in columns
    )
    if len(columns) == 1:
        cols += "<div></div>"
    return f"""
    <div class="page page--bone">
      <header class="q-doc-header">
        <div>
          <div class="kicker">OPERATOR QUESTIONS · {esc(str(page_index + 1))}/{esc(str(page_count))}</div>
          <h2 class="q-doc-title">{inline(workflow["title"])}{continued}</h2>
        </div>
      </header>
      <main class="q-columns">{cols}</main>
      {render_footer(meta)}
    </div>
    """


def render_document(title, workflows, meta):
    warnings = []
    pages = [render_cover(title, workflows, meta)]
    for workflow in workflows:
        if not workflow["questions"]:
            continue
        workflow_pages = paginate(workflow["questions"], warnings, workflow["title"])
        for idx, columns in enumerate(workflow_pages):
            pages.append(
                render_question_page(workflow, columns, idx, len(workflow_pages), meta)
            )
    css = load_theme_css() + DOC_CSS
    doc = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{esc(title)}</title>
<style>{css}</style>
</head>
<body>
<div class="document">
{''.join(pages)}
</div>
</body>
</html>
"""
    return doc, warnings, len(pages)


def parse_args(argv):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("workflows", nargs="+", help="Ops-map workflow markdown files")
    parser.add_argument("-o", "--output", required=True, help="Output HTML path")
    parser.add_argument("--title", default="Mapping Session Questions", help="Document title")
    parser.add_argument("--business", default="", help="Footer business name (defaults to the first map's frontmatter)")
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv if argv is not None else sys.argv[1:])
    workflows = collect(args.workflows)

    business = args.business or workflows[0]["data"]["frontmatter"].get("business", "")
    meta_parts = []
    if business:
        meta_parts.append(titleize_slug(business))
    meta_parts.append("Session Questions")
    meta = "  ·  ".join(meta_parts)

    doc, warnings, page_count = render_document(args.title, workflows, meta)
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(doc, encoding="utf-8")

    parse_warnings = [w for workflow in workflows for w in workflow["parse_warnings"]]
    for message in parse_warnings:
        print(f"PARSE WARNING: {message}", file=sys.stderr)
    for message in warnings:
        print(f"PAGINATION WARNING: {message}", file=sys.stderr)
    print(f"Parse warnings: {len(parse_warnings)}", file=sys.stderr)
    print(f"Pagination warnings: {len(warnings)}", file=sys.stderr)
    print(f"Rendered pages: {page_count}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
