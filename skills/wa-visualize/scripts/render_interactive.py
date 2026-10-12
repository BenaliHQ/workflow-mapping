#!/usr/bin/env python3
"""Render an ops-map Workflow Map markdown file to an interactive, scroll-based
Benali-branded HTML page.

The print pipeline (render.py -> Chrome -> PDF) stays the client-send artifact.
This renderer produces the *browsing* artifact: one continuous scroll, a single
sticky wordmark, click-to-expand activity detail, and the map's operator
questions pinned alongside the phase they belong to.

Question-to-phase anchoring uses an optional tag at the start of a question in
`### Operator questions`:

    1. [P3] How long does a typical cleanup run?
    2. Where do new clients come from?

`[P3]` pins the question to Phase 3's side rail. Untagged questions are
workflow-wide and appear in the closing questions index only. render.py strips
the tag for print output.
"""

import argparse
import html
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from render import (  # noqa: E402
    UNKNOWN,
    dedupe_cover_description,
    emphasize_title,
    load_theme_css,
    parse_workflow,
    phase_owner,
    titleize_slug,
)

# The interactive renderer uses optional phase anchors from operator questions;
# print output strips these before rendering.
QUESTION_TAG_RE = re.compile(r"^\[P(?P<phase>\d+)[^\]]*\]\s*")

# Only a handoff *in* earns the phase chip: the receiving phase's description
# opens with "begins with a <type> handoff" per the wa-workflow placement rule.
HANDOFF_IN_RE = re.compile(r"begins\s+with\s+an?\s+(functional|role|external)\s+handoff", re.IGNORECASE)
PHASE_WORDS = {
    1: "One", 2: "Two", 3: "Three", 4: "Four", 5: "Five", 6: "Six", 7: "Seven",
}


# ---------------------------------------------------------------- text helpers


def esc(text):
    return html.escape(text or "")


def inline(text):
    escaped = esc(text)
    escaped = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", escaped)
    escaped = escaped.replace("UNKNOWN", '<span class="unknown-tag">UNKNOWN</span>')
    return escaped.replace("\n", "<br>")


def render_note_table(entry):
    """A notes markdown table, wrapped so wide tables scroll in their own box."""
    head_cells = "".join(f"<th>{inline(cell)}</th>" for cell in entry["header"])
    body_rows = "".join(
        "<tr>" + "".join(f"<td>{inline(cell)}</td>" for cell in row) + "</tr>"
        for row in entry["rows"]
    )
    return (
        '<div class="note-table-wrap">'
        '<table class="note-table">'
        f"<thead><tr>{head_cells}</tr></thead>"
        f"<tbody>{body_rows}</tbody>"
        "</table></div>"
    )


def split_question(text):
    """Split a question into (question sentence, trailing context)."""
    match = re.search(r"\?", text)
    if match:
        head = text[: match.end()].strip()
        tail = text[match.end():].strip()
        return head, tail
    return text.strip(), ""


def parse_questions(data):
    """Return (by_phase: {int: [entry]}, general: [entry]) with 1-based numbers."""
    by_phase = {}
    general = []
    for number, raw in enumerate(data["notes"]["operator_questions"], 1):
        tag = QUESTION_TAG_RE.match(raw)
        text = QUESTION_TAG_RE.sub("", raw, count=1).strip()
        question, context = split_question(text)
        entry = {"number": number, "question": question, "context": context}
        if tag:
            by_phase.setdefault(int(tag.group(1)), []).append(entry)
        else:
            general.append(entry)
    return by_phase, general


def handoff_in_type(phase):
    match = HANDOFF_IN_RE.search(phase.get("description", ""))
    return match.group(1).capitalize() if match else None


def slate_compact(data):
    return data["frontmatter"].get("business", "").strip().lower() == "slate"


def phase_label(number):
    return f"Phase {PHASE_WORDS.get(int(number), str(number))}"


def extract_root_tokens(css):
    """Lift the :root token block out of the print theme so brand tokens stay
    single-source. Never re-declare a color here."""
    match = re.search(r":root\s*\{.*?\n\}", css, re.DOTALL)
    if not match:
        raise SystemExit("theme CSS: could not locate the :root token block")
    return match.group(0)


# ---------------------------------------------------------------- CSS / JS


def build_css(tokens):
    return (
        tokens
        + """

* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
@media (prefers-reduced-motion: reduce) {
  html { scroll-behavior: auto; }
  * { transition: none !important; }
}
body {
  margin: 0;
  background: var(--paper);
  color: var(--ink);
  font-family: var(--font);
  font-weight: 400;
  line-height: 1.55;
}
.skip {
  position: absolute; left: -999px; top: 8px;
  background: var(--ink); color: var(--card); padding: 6px 14px; border-radius: 6px;
}
.skip:focus { left: 8px; z-index: 60; }

.kicker {
  color: var(--ink-mid);
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0;
  text-transform: none;
  line-height: 1.2;
}
.wordmark {
  width: 88px; height: 17px;
  background: var(--benali-wordmark) no-repeat left center / contain;
  flex: 0 0 auto;
}
.unknown-tag {
  border: 1px solid var(--line-strong);
  border-radius: 4px;
  color: var(--ink-mid);
  font-size: 0.72em;
  font-weight: 600;
  letter-spacing: 0;
  padding: 1px 6px;
  white-space: nowrap;
}

/* ------------------------------------------------ sticky top bar */
.topbar {
  position: sticky; top: 0; z-index: 50;
  background: var(--card);
  background: color-mix(in srgb, var(--card) 92%, transparent);
  backdrop-filter: blur(8px);
  border-bottom: 1px solid var(--line);
}
.topbar-inner {
  max-width: 1180px; margin: 0 auto;
  display: flex; align-items: center; gap: 20px;
  padding: 12px 28px;
}
.topbar-title {
  font-weight: 600; font-size: 14px; white-space: nowrap;
  overflow: hidden; text-overflow: ellipsis;
}
.topbar-nav { display: flex; gap: 4px; margin-left: auto; flex-wrap: wrap; }
.topbar-nav a {
  color: var(--ink-mid); text-decoration: none;
  font-size: 12px; font-weight: 600; letter-spacing: 0;
  padding: 5px 10px; border-radius: 999px; border: 1px solid transparent;
}
.topbar-nav a .n { color: var(--majorelle); margin-right: 5px; font-weight: 700; }
.topbar-nav a:hover { border-color: var(--line-strong); }
.topbar-nav a.active { background: var(--ink); color: var(--card); }
.topbar-nav a.navnum { padding: 5px 11px; }
.topbar-nav a.navnum .n { margin-right: 0; }
.topbar-nav a.active .n { color: var(--majorelle-lift); }
.toolbtn {
  font: 600 12px/1 var(--font); letter-spacing: 0;
  color: var(--ink); background: none;
  border: 1px solid var(--line-strong); border-radius: 999px;
  padding: 7px 14px; cursor: pointer; white-space: nowrap;
}
.toolbtn:hover { border-color: var(--ink); }

/* ------------------------------------------------ hero */
.hero { border-bottom: 1px solid var(--line); }
.hero-inner { max-width: 1180px; margin: 0 auto; padding: 72px 28px 56px; }
.hero-top { display: flex; align-items: center; justify-content: space-between; gap: 16px 24px; flex-wrap: wrap; }
.draft-badge {
  background: var(--ink);
  border-radius: 999px;
  color: var(--card);
  font-size: 10.5px;
  font-weight: 600;
  letter-spacing: 0;
  padding: 7px 15px;
  text-transform: none;
  white-space: nowrap;
}
h1 {
  font-size: clamp(38px, 6vw, 64px);
  font-weight: 700;
  letter-spacing: -0.02em;
  line-height: 1.04;
  margin: 22px 0 18px;
  text-wrap: balance;
}
.title-emphasis { color: var(--majorelle); }
.lede { max-width: 62ch; font-size: 17px; color: var(--ink-mid); margin: 0 0 30px; }

.state-strip { display: flex; align-items: stretch; gap: 14px; flex-wrap: wrap; margin-bottom: 30px; }
.state-card {
  background: var(--card);
  border: 1px solid var(--line);
  border-radius: 10px;
  padding: 14px 18px;
  flex: 1 1 300px;
  max-width: 480px;
}
.state-card .kicker { font-size: 12px; margin-bottom: 8px; }
.state-copy { font-size: 16px; font-weight: 600; line-height: 1.45; }
.state-arrow { align-self: center; color: var(--majorelle); font-size: 22px; }

.stats { display: flex; gap: 10px; flex-wrap: wrap; margin-bottom: 34px; }
.stat-chip {
  border: 1px solid var(--line);
  border-radius: 999px;
  background: var(--card);
  padding: 6px 14px;
  font-size: 12.5px; font-weight: 600; color: var(--ink-mid);
}
.stat-chip strong { color: var(--ink); font-weight: 700; margin-right: 4px; }

.phase-rail { display: grid; grid-template-columns: repeat(auto-fill, minmax(210px, 1fr)); gap: 12px; }
.rail-card {
  background: var(--card);
  border: 1px solid var(--line);
  border-radius: 10px;
  padding: 14px 16px;
  text-decoration: none;
  color: inherit;
  display: block;
  transition: border-color 120ms ease, transform 120ms ease;
}
.rail-card:hover { border-color: var(--majorelle); transform: translateY(-2px); }
.rail-number { color: var(--majorelle); font-size: 20px; font-weight: 700; }
.rail-title { font-weight: 600; font-size: 14px; margin: 4px 0 6px; }
.rail-role { color: var(--ink-mid); font-size: 10.5px; font-weight: 600; letter-spacing: 0; text-transform: none; }
.rail-qcount { margin-top: 8px; font-size: 11px; font-weight: 700; color: var(--majorelle); }

/* ------------------------------------------------ phases */
main { max-width: 1180px; margin: 0 auto; padding: 0 28px; }
.phase { padding: 60px 0 12px; border-bottom: 1px solid var(--line); scroll-margin-top: 70px; }
.phase-head { display: flex; align-items: baseline; gap: 20px; margin-bottom: 8px; }
.phase-num { color: var(--majorelle); font-size: 52px; font-weight: 700; line-height: 1; }
.phase-head h2 { font-size: 30px; font-weight: 700; letter-spacing: -0.015em; margin: 0; }
.phase-owner { color: var(--ink-mid); font-size: 11px; font-weight: 600; letter-spacing: 0; text-transform: none; margin-top: 5px; }

.handoff-chip {
  display: inline-flex; align-items: center; gap: 8px;
  border: 1px solid var(--majorelle);
  border-radius: 999px;
  color: var(--majorelle);
  font-size: 10.5px; font-weight: 700; letter-spacing: 0; text-transform: none;
  padding: 5px 13px;
  margin: 14px 0 10px;
}
.phase-desc { max-width: 72ch; color: var(--ink-mid); font-size: 14.5px; margin: 8px 0 26px; }

.phase-grid { display: grid; grid-template-columns: minmax(0, 1fr) 300px; gap: 34px; align-items: start; }
.phase-grid.no-aside { grid-template-columns: minmax(0, 1fr); }
@media (max-width: 980px) { .phase-grid { grid-template-columns: minmax(0, 1fr); } .phase-aside { position: static; } }

/* processes */
.process-card {
  background: var(--card);
  border: 1px solid var(--line);
  border-radius: 12px;
  margin-bottom: 22px;
  overflow: hidden;
}
.process-header { padding: 18px 22px 14px; border-bottom: 1px solid var(--line-faint); }
.process-kicker { color: var(--majorelle); font-size: 10.5px; font-weight: 700; letter-spacing: 0; }
.process-title { font-size: 18px; font-weight: 700; margin: 4px 0 12px; }
.process-meta { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 8px 22px; }
.process-meta .kicker { margin-bottom: 3px; }
.process-meta div p { margin: 0; font-size: 13px; }

.activity { border-top: 1px solid var(--line-faint); }
.activity:first-of-type { border-top: none; }
.act-head {
  display: grid;
  grid-template-columns: 14px auto minmax(0, 1fr) auto 14px;
  gap: 12px; align-items: baseline;
  width: 100%;
  padding: 12px 22px;
  background: none; border: none; border-left: 2px solid transparent;
  font: inherit; text-align: left; color: inherit; cursor: pointer;
  transition: background 120ms ease, border-color 120ms ease;
}
.act-head:hover { background: var(--tray); border-left-color: var(--majorelle); }
.activity.open .act-head { border-left-color: var(--majorelle); }
.status-dot {
  display: inline-block; width: 8px; height: 8px; border-radius: 50%;
  border: 1.5px solid var(--majorelle); background: transparent;
  position: relative; top: -1px;
}
.status-dot--active { background: var(--majorelle); }
.act-num { font-size: 11.5px; font-weight: 700; color: var(--majorelle); }
.act-title { font-size: 14.5px; font-weight: 600; }
.act-tags { display: inline-flex; gap: 6px; }
.tag {
  border: 1px solid var(--line-strong); border-radius: 4px;
  color: var(--ink-mid);
  font-size: 9.5px; font-weight: 700; letter-spacing: 0.1em;
  padding: 1px 6px; text-transform: none; white-space: nowrap;
}
.tag--sub { border: none; background: var(--tray); letter-spacing: 0; }
.tag--software { border: none; background: var(--tray); letter-spacing: 0; text-transform: none; }
.chev { color: var(--ink-mid); font-size: 11px; transition: transform 140ms ease; justify-self: end; }
.activity.open .chev { transform: rotate(180deg); }
.act-body { padding: 10px 22px 20px 48px; border-left: 2px solid var(--majorelle); }
.act-desc { margin: 0 0 12px; font-size: 13.5px; color: var(--ink-mid); max-width: 70ch; }
.act-flow { display: flex; gap: 16px; flex-wrap: wrap; }
.act-flow .cell { flex: 1 1 240px; max-width: 420px; background: var(--paper); border: 1px solid var(--line-faint); border-radius: 8px; padding: 13px 16px; }
.act-flow .cell .kicker { font-size: 12px; margin-bottom: 6px; }
.act-flow .cell p { margin: 0; font-size: 14.5px; font-weight: 600; line-height: 1.45; }
.sop-list { margin: 12px 0 0; padding-left: 18px; font-size: 12.5px; color: var(--ink-mid); }
.sop-list li { margin: 3px 0; }

/* questions aside */
.phase-aside { position: sticky; top: 70px; }
.aside-kicker { display: flex; align-items: center; gap: 8px; margin-bottom: 12px; }
.aside-kicker .count {
  background: var(--majorelle); color: var(--card);
  border-radius: 999px; font-size: 10.5px; font-weight: 700; padding: 2px 8px;
}
.q-card {
  background: var(--card);
  border: 1px solid var(--line);
  border-left: 3px solid var(--majorelle);
  border-radius: 10px;
  padding: 12px 15px;
  margin-bottom: 10px;
  transition: transform 120ms ease, border-color 120ms ease;
}
.q-card.has-context { cursor: pointer; }
.q-card.has-context:hover { transform: translateY(-1px); border-color: var(--majorelle); }
.q-num { color: var(--majorelle); font-size: 10.5px; font-weight: 700; letter-spacing: 0; margin-bottom: 4px; }
.q-text { margin: 0; font-size: 13px; font-weight: 600; line-height: 1.45; }
.q-context { margin: 8px 0 0; font-size: 12px; color: var(--ink-mid); }
.q-context[hidden] { display: none; }
.q-hint { margin: 6px 0 0; font-size: 10px; font-weight: 700; letter-spacing: 0.1em; color: var(--ink-mid); text-transform: none; }

/* ------------------------------------------------ closing sections */
.tail { padding: 60px 0; border-bottom: 1px solid var(--line); scroll-margin-top: 70px; }
.tail h2 { font-size: 30px; font-weight: 700; letter-spacing: -0.015em; margin: 6px 0 26px; }
.note-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 16px; }
.note-block { background: var(--card); border: 1px solid var(--line); border-radius: 12px; padding: 18px 20px; min-width: 0; }
.note-heading { font-size: 14px; font-weight: 700; margin: 0 0 10px; }
.note-block ul { margin: 0; padding-left: 18px; }
.note-block li, .note-block p { font-size: 13px; color: var(--ink-mid); margin: 5px 0; }
.note-block--wide { grid-column: 1 / -1; }
/* Notes tables scroll inside their own box; they never widen the page. */
.note-table-wrap { overflow-x: auto; max-width: 100%; margin: 10px 0 12px; -webkit-overflow-scrolling: touch; }
.note-table { border-collapse: collapse; color: var(--ink-mid); font-size: 12px; line-height: 1.4; width: 100%; min-width: 460px; }
.note-table th, .note-table td { border: 1px solid var(--line); padding: 6px 9px; text-align: left; vertical-align: top; }
.note-table th { border-bottom: 1px solid var(--line-strong); color: var(--ink); font-size: 10px; font-weight: 600; letter-spacing: 0; text-transform: none; }

.qindex-group { margin-bottom: 26px; }
.qindex-head { display: flex; align-items: baseline; gap: 10px; margin-bottom: 10px; }
.qindex-head a { color: var(--majorelle); text-decoration: none; font-size: 12px; font-weight: 700; }
.qindex-head a:hover { text-decoration: underline; }
.qindex { display: grid; grid-template-columns: repeat(auto-fill, minmax(430px, 1fr)); gap: 10px; margin: 0; padding: 0; list-style: none; }
@media (max-width: 560px) { .qindex { grid-template-columns: 1fr; } }
.qindex li { background: var(--card); border: 1px solid var(--line); border-radius: 10px; padding: 12px 15px; display: grid; grid-template-columns: auto 1fr; gap: 12px; }
.qindex .q-text { font-weight: 500; }
.qindex .q-context { margin-top: 5px; }

footer.page-end { max-width: 1180px; margin: 0 auto; padding: 34px 28px 46px; display: flex; align-items: flex-end; justify-content: space-between; gap: 16px; }
.footer-meta { color: var(--ink-mid); font-size: 11px; text-align: right; }

/* ------------------------------------------------ mobile (one-row nav, no overflow) */
@media (max-width: 760px) {
  .topbar-inner { gap: 12px; padding: 10px 16px; }
  .topbar-title { display: none; }
  .topbar-nav {
    margin-left: 0; flex: 1 1 auto; flex-wrap: nowrap;
    overflow-x: auto; -webkit-overflow-scrolling: touch;
    scrollbar-width: none; min-width: 0;
  }
  .topbar-nav::-webkit-scrollbar { display: none; }
  .topbar-nav a { flex: 0 0 auto; padding: 8px 12px; }
  .toolbtn { padding: 8px 12px; }
  .hero-inner { padding: 44px 20px 40px; }
  main { padding: 0 20px; }
  .phase { padding: 44px 0 10px; }
  .phase-head { gap: 14px; }
  .phase-num { font-size: 38px; }
  .phase-head h2 { font-size: 24px; }
  .state-arrow { display: none; }
  .draft-badge { white-space: normal; text-align: center; line-height: 1.5; }
  footer.page-end { padding: 28px 20px 40px; }
}
@media (max-width: 640px) {
  .act-head {
    grid-template-columns: 14px auto minmax(0, 1fr) 14px;
    grid-template-rows: auto auto;
    row-gap: 6px;
    padding: 12px 16px;
  }
  .act-head .status-dot { grid-row: 1; grid-column: 1; }
  .act-num { grid-row: 1; grid-column: 2; }
  .act-title { grid-row: 1; grid-column: 3; }
  .chev { grid-row: 1; grid-column: 4; }
  .act-tags { grid-row: 2; grid-column: 2 / 4; display: flex; flex-wrap: wrap; gap: 6px; }
  .act-body { padding: 2px 16px 16px 30px; }
  .process-header { padding: 16px 16px 12px; }
}
"""
    )


SCRIPT = """
(function () {
  var expanded = false;

  function setOpen(activity, open) {
    activity.classList.toggle('open', open);
    var head = activity.querySelector('.act-head');
    var body = activity.querySelector('.act-body');
    if (head) head.setAttribute('aria-expanded', String(open));
    if (body) body.hidden = !open;
  }

  document.querySelectorAll('.activity').forEach(function (activity) {
    var head = activity.querySelector('.act-head');
    if (!head) return;
    head.addEventListener('click', function () {
      setOpen(activity, !activity.classList.contains('open'));
    });
  });

  var toggle = document.getElementById('toggle-all');
  if (toggle) {
    toggle.addEventListener('click', function () {
      expanded = !expanded;
      document.querySelectorAll('.activity').forEach(function (a) { setOpen(a, expanded); });
      toggle.textContent = expanded ? 'Collapse all' : 'Expand all';
    });
  }

  document.querySelectorAll('.q-card.has-context').forEach(function (card) {
    card.addEventListener('click', function () {
      var ctx = card.querySelector('.q-context');
      var hint = card.querySelector('.q-hint');
      if (!ctx) return;
      ctx.hidden = !ctx.hidden;
      if (hint) hint.textContent = ctx.hidden ? 'Why we ask' : 'Hide';
    });
    card.setAttribute('tabindex', '0');
    card.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); card.click(); }
    });
  });

  var links = Array.prototype.slice.call(document.querySelectorAll('.topbar-nav a'));
  var sections = links
    .map(function (link) { return document.getElementById(link.getAttribute('href').slice(1)); })
    .filter(Boolean);
  var lastActive = null;
  function spy() {
    var fromTop = window.scrollY + 90;
    var current = sections[0];
    sections.forEach(function (section) {
      if (section.offsetTop <= fromTop) current = section;
    });
    var activeLink = null;
    links.forEach(function (link) {
      var on = link.getAttribute('href') === '#' + current.id;
      link.classList.toggle('active', on);
      if (on) activeLink = link;
    });
    if (activeLink && activeLink !== lastActive) {
      lastActive = activeLink;
      var nav = activeLink.parentElement;
      if (nav.scrollWidth > nav.clientWidth) {
        activeLink.scrollIntoView({ block: 'nearest', inline: 'nearest' });
      }
    }
  }
  window.addEventListener('scroll', spy, { passive: true });
  spy();
})();
"""


# ---------------------------------------------------------------- sections


def render_topbar(data, question_count):
    nav = ['<a href="#overview">Overview</a>']
    for phase in data["phases"]:
        nav.append(
            f'<a class="navnum" href="#phase-{esc(phase["number"])}" title="{esc(phase["title"])}"><span class="n">{esc(phase["number"])}</span></a>'
        )
    if data["notes"]["blocks"]:
        nav.append('<a href="#notes">Notes</a>')
    if question_count:
        nav.append(f'<a href="#questions">Questions ({question_count})</a>')
    return f"""
    <nav class="topbar" aria-label="Workflow phases">
      <div class="topbar-inner">
        <div class="wordmark" role="img" aria-label="Benali"></div>
        <div class="topbar-title">{inline(data["workflow"]["title"])}</div>
        <div class="topbar-nav">{''.join(nav)}</div>
        <button id="toggle-all" class="toolbtn" type="button">Expand all</button>
      </div>
    </nav>
    """


def render_hero(data, questions_by_phase, general_questions):
    workflow = data["workflow"]
    counts = data["counts"]
    total_questions = sum(len(v) for v in questions_by_phase.values()) + len(general_questions)
    draft = ""
    if data["frontmatter"].get("status", "").strip().lower() == "draft":
        draft = '<div class="draft-badge">Draft, pending operator review</div>'

    compact = slate_compact(data)
    rail = []
    for phase in data["phases"]:
        qcount = len(questions_by_phase.get(int(phase["number"]), []))
        qline = f'<div class="rail-qcount">{qcount} open question{"s" if qcount != 1 else ""}</div>' if qcount else ""
        rail.append(
            f"""
            <a class="rail-card" href="#phase-{esc(phase["number"])}">
              <div class="rail-number">{esc(phase_label(phase["number"]) if compact else phase["number"])}</div>
              <div class="rail-title">{inline(phase["title"])}</div>
              <div class="rail-role">{inline(phase_owner(phase))}</div>
              {qline}
            </a>
            """
        )

    stats = [
        f'<span class="stat-chip"><strong>{counts["phases"]}</strong> phases</span>',
        f'<span class="stat-chip"><strong>{counts["processes"]}</strong> processes</span>',
        f'<span class="stat-chip"><strong>{counts["activities"]}</strong> core activities</span>',
    ]
    if total_questions:
        stats.append(f'<span class="stat-chip"><strong>{total_questions}</strong> open questions</span>')

    return f"""
    <header class="hero" id="overview">
      <div class="hero-inner">
        <div class="hero-top">
          <div class="kicker">Work Architecture: workflow map</div>
          {draft}
        </div>
        <h1>{emphasize_title(workflow["title"])}</h1>
        {"" if compact else f'<p class="lede">{inline(dedupe_cover_description(workflow["description"]))}</p>'}
        <div class="state-strip">
          <div class="state-card"><div class="kicker">Trigger</div><div class="state-copy">{inline(workflow["trigger"])}</div></div>
          <div class="state-arrow">→</div>
          <div class="state-card"><div class="kicker">End state</div><div class="state-copy">{inline(workflow["end_state"])}</div></div>
        </div>
        <div class="stats">{''.join(stats)}</div>
        <div class="phase-rail">{''.join(rail)}</div>
      </div>
    </header>
    """


def render_activity(activity, compact=False):
    status = (activity.get("status") or "").lower()
    dot = '<span class="status-dot status-dot--active"></span>' if status == "active" else '<span class="status-dot"></span>'
    tags = []
    if status == "gap":
        tags.append('<span class="tag">GAP</span>')
    elif status == "draft":
        tags.append('<span class="tag">DRAFT</span>')
    tags.append(f'<span class="tag tag--sub">{inline(activity["sub_function"])}</span>')
    if activity.get("software"):
        tags.append(f'<span class="tag tag--software">{inline(activity["software"])}</span>')

    sop = ""
    if not compact and activity["sop_checklist"]:
        items = "".join(f"<li>{inline(item)}</li>" for item in activity["sop_checklist"])
        sop = f'<ul class="sop-list">{items}</ul>'

    return f"""
      <div class="activity">
        <button class="act-head" type="button" aria-expanded="false">
          {dot}
          <span class="act-num">{esc(activity["number"])}</span>
          <span class="act-title">{inline(activity["title"])}</span>
          <span class="act-tags">{''.join(tags)}</span>
          <span class="chev">▾</span>
        </button>
        <div class="act-body" hidden>
          {"" if compact else f'<p class="act-desc">{inline(activity["description"])}</p>'}
          <div class="act-flow">
            <div class="cell"><div class="kicker">Trigger</div><p>{inline(activity["trigger"])}</p></div>
            <div class="cell"><div class="kicker">End state</div><p>{inline(activity["end_state"])}</p></div>
          </div>
          {sop}
        </div>
      </div>
    """


def render_process(process, compact=False):
    activities = "".join(render_activity(activity, compact) for activity in process["activities"])
    return f"""
      <section class="process-card">
        <div class="process-header">
          <div class="process-kicker">PROCESS {esc(process["number"])}</div>
          <h3 class="process-title">{inline(process["title"])}</h3>
          <div class="process-meta">
            <div><div class="kicker">Role</div><p>{inline(process["role"])}</p></div>
            <div><div class="kicker">Trigger</div><p>{inline(process["trigger"])}</p></div>
            <div><div class="kicker">End state</div><p>{inline(process["end_state"])}</p></div>
          </div>
        </div>
        {activities}
      </section>
    """


def render_question_card(entry):
    has_context = bool(entry["context"])
    context = ""
    hint = ""
    if has_context:
        context = f'<p class="q-context" hidden>{inline(entry["context"])}</p>'
        hint = '<p class="q-hint">Why we ask</p>'
    return f"""
      <div class="q-card{' has-context' if has_context else ''}" id="q-{entry["number"]}">
        <div class="q-num">Q{entry["number"]}</div>
        <p class="q-text">{inline(entry["question"])}</p>
        {context}{hint}
      </div>
    """


def render_phase(phase, questions, compact=False):
    chip = ""
    handoff = handoff_in_type(phase)
    if handoff:
        chip = f'<div class="handoff-chip">{esc(handoff)} handoff in</div>'

    aside = ""
    grid_class = "phase-grid no-aside"
    if questions:
        cards = "".join(render_question_card(entry) for entry in questions)
        aside = f"""
        <aside class="phase-aside" aria-label="Open questions for this phase">
          <div class="aside-kicker"><span class="kicker">Open questions</span><span class="count">{len(questions)}</span></div>
          {cards}
        </aside>
        """
        grid_class = "phase-grid"

    processes = "".join(render_process(process, compact) for process in phase["processes"])
    return f"""
    <section class="phase" id="phase-{esc(phase["number"])}">
      <div class="phase-head">
        <div class="phase-num">{esc(phase_label(phase["number"]) if compact else phase["number"])}</div>
        <div>
          <h2>{inline(phase["title"])}</h2>
          <div class="phase-owner">{inline(phase_owner(phase))}</div>
        </div>
      </div>
      {chip}
      {"" if compact else f'<p class="phase-desc">{inline(phase["description"])}</p>'}
      <div class="{grid_class}">
        <div class="phase-main">{processes}</div>
        {aside}
      </div>
    </section>
    """


def render_notes(data):
    blocks = data["notes"]["blocks"]
    if not blocks:
        return ""
    rendered = []
    for block in blocks:
        bullets = [entry for entry in block["entries"] if entry["type"] == "bullet"]
        paragraphs = [entry for entry in block["entries"] if entry["type"] != "bullet"]
        body = "".join(
            render_note_table(entry)
            if entry["type"] == "table"
            else f"<p>{inline(entry['text'])}</p>"
            for entry in paragraphs
        )
        if bullets:
            body += "<ul>" + "".join(f"<li>{inline(entry['text'])}</li>" for entry in bullets) + "</ul>"
        # A block carrying a table spans the full grid row — a table squeezed
        # into a 320px card is unreadable.
        wide = " note-block--wide" if any(e["type"] == "table" for e in block["entries"]) else ""
        rendered.append(
            f'<div class="note-block{wide}"><h3 class="note-heading">{inline(block["heading"])}</h3>{body}</div>'
        )
    return f"""
    <section class="tail" id="notes">
      <div class="kicker">WORKFLOW MAP REVIEW</div>
      <h2>Notes &amp; Assumptions</h2>
      <div class="note-grid">{''.join(rendered)}</div>
    </section>
    """


def render_question_index(data, questions_by_phase, general_questions):
    total = sum(len(v) for v in questions_by_phase.values()) + len(general_questions)
    if not total:
        return ""
    groups = []
    for phase in data["phases"]:
        number = int(phase["number"])
        entries = questions_by_phase.get(number, [])
        if not entries:
            continue
        items = "".join(
            f'<li><span class="q-num">Q{e["number"]}</span><div><p class="q-text">{inline(e["question"])}</p>'
            + (f'<p class="q-context">{inline(e["context"])}</p>' if e["context"] else "")
            + "</div></li>"
            for e in entries
        )
        groups.append(
            f"""
            <div class="qindex-group">
              <div class="qindex-head">
                <h3 class="note-heading">Phase {number}: {inline(phase["title"])}</h3>
                <a href="#phase-{number}">Jump to phase ↑</a>
              </div>
              <ul class="qindex">{items}</ul>
            </div>
            """
        )
    if general_questions:
        items = "".join(
            f'<li><span class="q-num">Q{e["number"]}</span><div><p class="q-text">{inline(e["question"])}</p>'
            + (f'<p class="q-context">{inline(e["context"])}</p>' if e["context"] else "")
            + "</div></li>"
            for e in general_questions
        )
        groups.append(
            f"""
            <div class="qindex-group">
              <div class="qindex-head"><h3 class="note-heading">Workflow-wide</h3></div>
              <ul class="qindex">{items}</ul>
            </div>
            """
        )
    return f"""
    <section class="tail" id="questions">
      <div class="kicker">FOR THE MAPPING SESSION</div>
      <h2>All open questions ({total})</h2>
      {''.join(groups)}
    </section>
    """


def render_footer(data):
    frontmatter = data["frontmatter"]
    parts = []
    show = frontmatter.get("show", "").strip()
    business = frontmatter.get("business", "").strip()
    if show:
        parts.append(titleize_slug(show))
    if business and titleize_slug(business) not in parts:
        parts.append(titleize_slug(business))
    parts.append("Workflow Map")
    meta = esc("  ·  ".join(parts))
    return f"""
    <footer class="page-end">
      <div class="wordmark" role="img" aria-label="Benali"></div>
      <div class="footer-meta">{meta}</div>
    </footer>
    """


def render_document(data):
    questions_by_phase, general_questions = parse_questions(data)
    total_questions = sum(len(v) for v in questions_by_phase.values()) + len(general_questions)
    compact = slate_compact(data)
    phases = "".join(
        render_phase(phase, questions_by_phase.get(int(phase["number"]), []), compact)
        for phase in data["phases"]
    )
    css = build_css(extract_root_tokens(load_theme_css()))
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex">
<title>{esc(data["workflow"]["title"])}</title>
<style>{css}</style>
</head>
<body>
<a class="skip" href="#phase-1">Skip to workflow</a>
{render_topbar(data, total_questions)}
{render_hero(data, questions_by_phase, general_questions)}
<main>
{phases}
{render_notes(data)}
{render_question_index(data, questions_by_phase, general_questions)}
</main>
{render_footer(data)}
<script>{SCRIPT}</script>
</body>
</html>
"""


def parse_args(argv):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("workflow", help="Path to the ops-map workflow markdown file")
    parser.add_argument("-o", "--output", required=True, help="Output HTML path")
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv if argv is not None else sys.argv[1:])
    data = parse_workflow(args.workflow)
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(render_document(data), encoding="utf-8")

    for message in data["parse_warnings"]:
        print(f"PARSE WARNING: {message}", file=sys.stderr)
    print(f"Parse warnings: {len(data['parse_warnings'])}", file=sys.stderr)
    questions_by_phase, general = parse_questions(data)
    tagged = sum(len(v) for v in questions_by_phase.values())
    print(f"Questions: {tagged} phase-tagged, {len(general)} workflow-wide", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
