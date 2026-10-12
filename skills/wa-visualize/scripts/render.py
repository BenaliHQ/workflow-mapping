#!/usr/bin/env python3
"""Render an ops-map Workflow Map markdown file to Benali-branded print HTML."""

import argparse
import copy
import html
import json
import math
import re
import sys
from pathlib import Path


UNKNOWN = "UNKNOWN: not in source"

FIELD_RE = re.compile(r"^\*\*(?P<label>[^:*]+):\*\*\s*$")
HEADING_RE = re.compile(r"^(?P<marks>#{2,4})\s+(?P<title>.+?)\s*$")
PHASE_RE = re.compile(r"^Phase\s+(?P<number>\d+)\s*$", re.IGNORECASE)
PROCESS_RE = re.compile(r"^Process\s+(?P<number>\d+(?:\.\d+)*)\s*$", re.IGNORECASE)
ACTIVITY_RE = re.compile(
    r"^Core Activity\s+(?P<number>\d+(?:\.\d+)*)\s*$", re.IGNORECASE
)

# Markdown tables inside `### ...` blocks of `## Notes & Assumptions` only.
# A table is a header row, a `|---|---|` separator row, then contiguous body
# rows. Nothing else in the parser looks at pipes, so this stays scoped to the
# notes section.
TABLE_ROW_RE = re.compile(r"^\|.*\|$")
TABLE_SEP_RE = re.compile(r"^\|(?:\s*:?-+:?\s*\|)+$")

QUESTION_TAG_RE = re.compile(r"^\[P(?P<phase>\d+)[^\]]*\]\s*")

WORKFLOW_FIELDS = ("Title", "Description")
# Fields that may legitimately be empty (wa-workflow 1.4.0: Software is empty when no tool applies).
OPTIONAL_EMPTY_FIELDS = {"Software"}
PHASE_FIELDS = ("Title", "Description")
PROCESS_FIELDS = ("Title", "Role", "Description")
ACTIVITY_FIELDS = (
    "Title",
    "Sub-function",
    "Software",
    "Description",
    "Trigger",
    "End state",
    "Status",
)

PX_PER_IN = 96
PAGE_HEIGHT_PX = 8.5 * PX_PER_IN
PHASE_BODY_LIMIT = 575
PHASE_BODY_LIMIT_WITH_HANDOFF = 492
NOTES_COLUMN_LIMIT = 548
PROCESS_GAP = 10

# Notes-table geometry, used only to estimate pagination height. Values track
# the `.note-table` rules in assets/benali-print-theme.css. The width is the
# NARROW (two-column) notes track — tables also render in the single-column
# track, so estimating against the narrow one keeps pagination conservative.
NOTES_TABLE_WIDTH_PX = 457.0
NOTES_TABLE_CHAR_PX = 5.35
NOTES_TABLE_CELL_PAD_PX = 13.0
NOTES_TABLE_LINE_PX = 12.5
NOTES_TABLE_ROW_PAD_PX = 9.0
NOTES_TABLE_CHROME_PX = 14.0


def warn(warnings, message):
    warnings.append(message)


def read_text(path):
    return Path(path).read_text(encoding="utf-8")


def parse_frontmatter(lines):
    if not lines or lines[0].strip() != "---":
        return {}, 0

    frontmatter = {}
    end = None
    for idx in range(1, len(lines)):
        if lines[idx].strip() == "---":
            end = idx
            break

    if end is None:
        return {}, 0

    for raw in lines[1:end]:
        if ":" not in raw:
            continue
        key, value = raw.split(":", 1)
        key = key.strip()
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in ("'", '"'):
            value = value[1:-1]
        if key:
            frontmatter[key] = value

    return frontmatter, end + 1


def collect_headings(lines):
    headings = []
    for idx, line in enumerate(lines):
        match = HEADING_RE.match(line.rstrip("\n"))
        if not match:
            continue
        headings.append(
            {
                "line": idx,
                "level": len(match.group("marks")),
                "title": match.group("title").strip(),
            }
        )
    return headings


def section_body(lines, headings, heading_index):
    start = headings[heading_index]["line"] + 1
    end = headings[heading_index + 1]["line"] if heading_index + 1 < len(headings) else len(lines)
    return lines[start:end]


def parse_field_blocks(body_lines, required_fields, context, warnings):
    fields = {}
    idx = 0

    while idx < len(body_lines):
        line = body_lines[idx].strip()
        field_match = FIELD_RE.match(line)
        if not field_match:
            idx += 1
            continue

        label = field_match.group("label").strip()
        cursor = idx + 1
        while cursor < len(body_lines) and not body_lines[cursor].strip():
            cursor += 1

        if cursor >= len(body_lines) or not body_lines[cursor].lstrip().startswith("```"):
            fields[label] = UNKNOWN
            warn(warnings, f"{context}: field '{label}' is missing a fenced code block")
            idx = cursor + 1
            continue

        cursor += 1
        value_lines = []
        closed = False
        while cursor < len(body_lines):
            if body_lines[cursor].lstrip().startswith("```"):
                closed = True
                break
            value_lines.append(body_lines[cursor].rstrip("\n"))
            cursor += 1

        if not closed:
            fields[label] = UNKNOWN
            warn(warnings, f"{context}: field '{label}' has an unterminated fenced code block")
            idx = cursor
            continue

        value = "\n".join(value_lines).strip()
        if value:
            fields[label] = value
        elif label in OPTIONAL_EMPTY_FIELDS:
            fields[label] = ""
        else:
            fields[label] = UNKNOWN
            warn(warnings, f"{context}: field '{label}' has an empty fenced code block")
        idx = cursor + 1

    for label in required_fields:
        if label not in fields:
            fields[label] = UNKNOWN
            warn(warnings, f"{context}: required field '{label}' is missing")

    return fields


def split_sop_checklist(description):
    main_lines = []
    checklist = []
    in_checklist = False

    for raw in description.splitlines():
        stripped = raw.strip()
        if stripped.lower().startswith("sop checklist:"):
            in_checklist = True
            continue

        if in_checklist:
            if stripped.startswith("- "):
                checklist.append(stripped[2:].strip())
            elif stripped:
                checklist.append(stripped)
            continue

        main_lines.append(raw)

    return "\n".join(main_lines).strip(), checklist


def first_sentence_matching(text, patterns):
    compact = " ".join(text.split())
    for pattern in patterns:
        match = re.search(pattern, compact, re.IGNORECASE)
        if match:
            return match.group(1).strip()
    return UNKNOWN


def extract_workflow_trigger(description):
    return first_sentence_matching(
        description,
        [
            r"((?:Triggered)\s+(?:when|by)\s+.*?)(?:\.|$)",
            r"((?:Begins|Starts)\s+(?:when|with|by)\s+.*?)(?:\.|$)",
        ],
    )


def extract_workflow_end_state(description):
    return first_sentence_matching(
        description,
        [
            r"((?:The\s+)?workflow\s+ends\s+when\s+.*?)(?:\.|$)",
            r"((?:Ends)\s+when\s+.*?)(?:\.|$)",
        ],
    )


def extract_process_trigger(description):
    return first_sentence_matching(
        description,
        [
            r"((?:Triggered)\s+(?:when|by)\s+.*?)(?:\.|$)",
            r"((?:Begins|Starts)\s+(?:when|with|by)\s+.*?)(?:\.|$)",
        ],
    )


def extract_process_end_state(description):
    return first_sentence_matching(
        description,
        [
            r"((?:Ends)\s+when\s+.*?)(?:\.|$)",
            r"((?:The\s+process\s+ends)\s+when\s+.*?)(?:\.|$)",
        ],
    )


def split_table_row(stripped):
    inner = stripped[1:-1] if stripped.endswith("|") else stripped[1:]
    return [cell.strip() for cell in inner.split("|")]


def read_table_block(lines, index, end):
    """If a markdown table starts at `index`, return (entry, next_index).

    Otherwise return (None, index). Requires a header row plus a separator row
    with the same cell count.
    """
    header_line = lines[index].strip()
    if not TABLE_ROW_RE.match(header_line):
        return None, index
    if index + 1 >= end:
        return None, index
    separator_line = lines[index + 1].strip()
    if not TABLE_SEP_RE.match(separator_line):
        return None, index

    header = split_table_row(header_line)
    if len(split_table_row(separator_line)) != len(header):
        return None, index

    rows = []
    cursor = index + 2
    while cursor < end:
        candidate = lines[cursor].strip()
        if not TABLE_ROW_RE.match(candidate) or TABLE_SEP_RE.match(candidate):
            break
        cells = split_table_row(candidate)
        if len(cells) < len(header):
            cells = cells + [""] * (len(header) - len(cells))
        rows.append(cells[: len(header)])
        cursor += 1

    if not rows:
        return None, index

    entry = {
        "type": "table",
        "text": "",
        "header": header,
        "rows": rows,
        "continued": False,
    }
    return entry, cursor


def parse_notes_and_quality(lines, headings):
    notes_heading = None
    quality_heading = None
    for idx, heading in enumerate(headings):
        if heading["level"] == 2 and heading["title"].lower().startswith("notes & assumptions"):
            notes_heading = idx
        if heading["level"] == 2 and heading["title"].lower().startswith("quality checklist"):
            quality_heading = idx

    notes = {"blocks": [], "operator_questions": []}
    quality = {"items": [], "paragraphs": []}

    if notes_heading is not None:
        start = headings[notes_heading]["line"] + 1
        end = (
            headings[quality_heading]["line"]
            if quality_heading is not None and headings[quality_heading]["line"] > start
            else len(lines)
        )
        current = None
        cursor = start
        while cursor < end:
            stripped = lines[cursor].strip()
            if not stripped or stripped == "---":
                cursor += 1
                continue
            subheading = re.match(r"^###\s+(.+?)\s*$", stripped)
            if subheading:
                current = {"heading": subheading.group(1).strip(), "entries": []}
                notes["blocks"].append(current)
                cursor += 1
                continue
            if current is None:
                cursor += 1
                continue

            table_entry, next_cursor = read_table_block(lines, cursor, end)
            if table_entry is not None:
                current["entries"].append(table_entry)
                cursor = next_cursor
                continue

            numbered = re.match(r"^\d+\.\s+(.*)$", stripped)
            if "operator questions" in current["heading"].lower() and numbered:
                notes["operator_questions"].append(numbered.group(1).strip())
                cursor += 1
                continue

            if stripped.startswith("- "):
                current["entries"].append({"type": "bullet", "text": stripped[2:].strip()})
            else:
                current["entries"].append({"type": "paragraph", "text": stripped})
            cursor += 1

    if quality_heading is not None:
        start = headings[quality_heading]["line"] + 1
        end = headings[quality_heading + 1]["line"] if quality_heading + 1 < len(headings) else len(lines)
        for raw in lines[start:end]:
            stripped = raw.strip()
            if not stripped or stripped == "---":
                continue
            if stripped.startswith("- "):
                quality["items"].append(stripped[2:].strip())
            else:
                quality["paragraphs"].append(stripped)

    notes["blocks"] = [
        block
        for block in notes["blocks"]
        if "operator questions" not in block["heading"].lower() and block["entries"]
    ]
    return notes, quality


def parse_workflow(path):
    source_path = str(Path(path))
    lines = read_text(path).splitlines()
    frontmatter, _ = parse_frontmatter(lines)
    headings = collect_headings(lines)
    warnings = []

    workflow = {
        "title": UNKNOWN,
        "description": UNKNOWN,
        "trigger": UNKNOWN,
        "end_state": UNKNOWN,
    }
    phases = []
    current_phase = None
    current_process = None

    for idx, heading in enumerate(headings):
        title = heading["title"]
        body = section_body(lines, headings, idx)

        if heading["level"] == 2 and title.lower() == "workflow":
            fields = parse_field_blocks(body, WORKFLOW_FIELDS, "Workflow", warnings)
            workflow["title"] = fields["Title"]
            workflow["description"] = fields["Description"]
            workflow["trigger"] = extract_workflow_trigger(workflow["description"])
            workflow["end_state"] = extract_workflow_end_state(workflow["description"])
            continue

        phase_match = PHASE_RE.match(title)
        if heading["level"] == 2 and phase_match:
            fields = parse_field_blocks(
                body, PHASE_FIELDS, f"Phase {phase_match.group('number')}", warnings
            )
            current_phase = {
                "number": phase_match.group("number"),
                "title": fields["Title"],
                "description": fields["Description"],
                "processes": [],
            }
            current_process = None
            phases.append(current_phase)
            continue

        process_match = PROCESS_RE.match(title)
        if heading["level"] == 3 and process_match:
            fields = parse_field_blocks(
                body, PROCESS_FIELDS, f"Process {process_match.group('number')}", warnings
            )
            process = {
                "number": process_match.group("number"),
                "title": fields["Title"],
                "role": fields["Role"],
                "description": fields["Description"],
                "trigger": extract_process_trigger(fields["Description"]),
                "end_state": extract_process_end_state(fields["Description"]),
                "activities": [],
            }
            if current_phase is None:
                warn(warnings, f"Process {process['number']}: appears before any phase")
            else:
                current_phase["processes"].append(process)
            current_process = process
            continue

        activity_match = ACTIVITY_RE.match(title)
        if heading["level"] == 4 and activity_match:
            fields = parse_field_blocks(
                body,
                ACTIVITY_FIELDS,
                f"Core Activity {activity_match.group('number')}",
                warnings,
            )
            description, checklist = split_sop_checklist(fields["Description"])
            activity = {
                "number": activity_match.group("number"),
                "title": fields["Title"],
                "sub_function": fields["Sub-function"],
                "software": fields.get("Software", ""),
                "description": description or UNKNOWN,
                "sop_checklist": checklist,
                "trigger": fields["Trigger"],
                "end_state": fields["End state"],
                "status": fields["Status"].strip().lower(),
            }
            if current_process is None:
                warn(warnings, f"Core Activity {activity['number']}: appears before any process")
            else:
                current_process["activities"].append(activity)

    notes, quality = parse_notes_and_quality(lines, headings)
    counts = count_items(phases)

    return {
        "source_path": source_path,
        "frontmatter": frontmatter,
        "workflow": workflow,
        "phases": phases,
        "notes": notes,
        "quality_checklist": quality,
        "counts": counts,
        "parse_warnings": warnings,
    }


def count_items(phases):
    processes = sum(len(phase["processes"]) for phase in phases)
    activities = sum(
        len(process["activities"])
        for phase in phases
        for process in phase["processes"]
    )
    return {"phases": len(phases), "processes": processes, "activities": activities}


def compact_spaces(text):
    return " ".join((text or "").split())


def is_unknown(text):
    return "UNKNOWN" in (text or "")


def render_inline(text):
    escaped = html.escape(text or "")
    escaped = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", escaped)
    escaped = escaped.replace("UNKNOWN", '<span class="unknown-tag">UNKNOWN</span>')
    return escaped.replace("\n", "<br>")


def render_copy(text, class_name=""):
    classes = [class_name] if class_name else []
    if is_unknown(text):
        classes.append("unknown-copy")
    class_attr = f' class="{" ".join(classes)}"' if classes else ""
    return f"<span{class_attr}>{render_inline(text)}</span>"


def emphasize_title(title):
    words = title.split()
    escaped_words = [html.escape(word) for word in words]
    for idx, word in enumerate(words):
        clean = re.sub(r"[^A-Za-z0-9]", "", word)
        if len(clean) >= 5 and clean.lower() != "workflow":
            escaped_words[idx] = f'<span class="title-emphasis">{html.escape(word)}</span>'
            return " ".join(escaped_words)
    return " ".join(escaped_words)


def phase_owner(phase):
    roles = []
    for process in phase["processes"]:
        # A process may carry more than one role, comma-separated (wa-workflow 1.4.0).
        for role in [r.strip() for r in process["role"].split(",") if r.strip()]:
            if role not in roles:
                roles.append(role)
    if not roles:
        return UNKNOWN
    if len(roles) == 1:
        return roles[0]
    if len(roles) == 2:
        return f"{roles[0]} + {roles[1]}"
    return "Multiple roles"


def phase_has_handoff(phase):
    description = phase.get("description", "")
    return "handoff" in description.lower() and "begins" in description.lower()


def estimate_text_lines(text, chars_per_line):
    text = compact_spaces(text)
    if not text:
        return 1
    return max(1, int(math.ceil(len(text) / float(chars_per_line))))


def estimate_activity_height(activity):
    title_lines = estimate_text_lines(activity["title"], 54)
    flow_text = f"Trigger → {activity['trigger']}  End → {activity['end_state']}"
    flow_lines = estimate_text_lines(flow_text, 122)
    checklist_count = min(len(activity["sop_checklist"]), 4)
    more = 1 if len(activity["sop_checklist"]) > 4 else 0
    return 34 + (title_lines * 14) + (flow_lines * 13) + (checklist_count + more) * 14


def estimate_process_header_height(process):
    title_lines = estimate_text_lines(process["title"], 60)
    meta_lines = max(
        estimate_text_lines(process["role"], 28),
        estimate_text_lines(process["trigger"], 46),
        estimate_text_lines(process["end_state"], 46),
    )
    return 38 + (title_lines * 15) + (meta_lines * 13)


def estimate_process_fragment_height(process, activities):
    return estimate_process_header_height(process) + sum(
        estimate_activity_height(activity) for activity in activities
    )


def render_status(activity):
    status = (activity.get("status") or "").lower()
    if status == "active":
        return '<span class="status-dot status-dot--active"></span>'
    if status == "gap":
        return '<span><span class="status-dot"></span><span class="gap-tag">GAP</span></span>'
    return '<span class="status-dot"></span>'


def render_activity(activity):
    checklist = ""
    if activity["sop_checklist"]:
        shown = activity["sop_checklist"][:4]
        items = "".join(f"<li>{render_inline(item)}</li>" for item in shown)
        if len(activity["sop_checklist"]) > 4:
            items += f'<li><span class="more-tag">+{len(activity["sop_checklist"]) - 4} more in SOP</span></li>'
        checklist = f'<ul class="sop-list">{items}</ul>'

    software = f'<div class="activity-software">{render_copy(activity["software"])}</div>' if activity.get("software") else ""
    return f"""
      <div class="activity-row">
        <div>{render_status(activity)}</div>
        <div>
          <div class="activity-title"><span class="activity-number">{html.escape(activity["number"])}</span>{render_copy(activity["title"])}</div>
          <div class="activity-flow">Trigger → {render_copy(activity["trigger"])} &nbsp; End → {render_copy(activity["end_state"])}</div>
          {checklist}
        </div>
        <div class="sub-function">{render_copy(activity["sub_function"])}{software}</div>
      </div>
    """


def render_process_fragment(fragment):
    process = fragment["process"]
    title = process["title"] + (" (continued)" if fragment.get("continued") else "")
    activities = "\n".join(render_activity(activity) for activity in fragment["activities"])
    return f"""
      <section class="process-card">
        <div class="process-header">
          <div class="process-kicker">PROCESS {html.escape(process["number"])}</div>
          <h3 class="process-title">{render_copy(title)}</h3>
          <div class="process-meta">
            <div>
              <div class="meta-label">Role</div>
              <div class="meta-value">{render_copy(process["role"])}</div>
            </div>
            <div>
              <div class="meta-label">Trigger</div>
              <div class="meta-value">{render_copy(process["trigger"])}</div>
            </div>
            <div>
              <div class="meta-label">End state</div>
              <div class="meta-value">{render_copy(process["end_state"])}</div>
            </div>
          </div>
        </div>
        <div class="activity-list">
          {activities}
        </div>
      </section>
    """


def append_phase_page(pages, phase, fragments, content_height, limit, continued, page_index, warnings):
    if content_height > limit:
        warn(
            warnings,
            f"Phase {phase['number']} page {page_index}: estimated content {content_height}px exceeds {limit}px",
        )
    pages.append(
        {
            "type": "phase",
            "phase": phase,
            "fragments": fragments,
            "continued": continued,
            "estimated_height": content_height,
            "limit": limit,
        }
    )


def paginate_phase(phase, warnings):
    limit = PHASE_BODY_LIMIT_WITH_HANDOFF if phase_has_handoff(phase) else PHASE_BODY_LIMIT
    pages = []
    current = []
    current_height = 0
    page_number = 1

    def flush():
        nonlocal current, current_height, page_number
        if not current:
            return
        append_phase_page(
            pages,
            phase,
            current,
            current_height,
            limit,
            page_number > 1,
            page_number,
            warnings,
        )
        page_number += 1
        current = []
        current_height = 0

    def add_fragment(fragment):
        nonlocal current_height
        height = estimate_process_fragment_height(fragment["process"], fragment["activities"])
        gap = PROCESS_GAP if current else 0
        if current and current_height + gap + height > limit:
            flush()
            gap = 0
        current.append(fragment)
        current_height += gap + height

    for process in phase["processes"]:
        full_height = estimate_process_fragment_height(process, process["activities"])
        if full_height <= limit:
            add_fragment({"process": process, "activities": process["activities"], "continued": False})
            continue

        if current:
            flush()

        index = 0
        continued = False
        while index < len(process["activities"]):
            chunk = []
            chunk_height = estimate_process_header_height(process)
            while index < len(process["activities"]):
                activity = process["activities"][index]
                activity_height = estimate_activity_height(activity)
                proposed = chunk_height + activity_height
                if chunk and proposed > limit:
                    break
                if not chunk and proposed > limit:
                    warn(
                        warnings,
                        f"Phase {phase['number']} process {process['number']} activity {activity['number']}: estimated row exceeds the page box",
                    )
                    chunk.append(activity)
                    chunk_height = proposed
                    index += 1
                    break
                chunk.append(activity)
                chunk_height = proposed
                index += 1
            add_fragment({"process": process, "activities": chunk, "continued": continued})
            continued = True
            if index < len(process["activities"]):
                flush()

    if not phase["processes"]:
        append_phase_page(pages, phase, [], 0, limit, False, page_number, warnings)
    else:
        flush()

    return pages


def estimate_table_row_height(cells, column_count):
    """Height of one rendered `.note-table` row, in px.

    Conservative on purpose: it assumes the narrow (two-column) notes track,
    and it models `table-layout: auto` by letting the widest cell claim at
    most ~55% of the row so a single fat cell is not averaged away.
    """
    usable = max(80.0, NOTES_TABLE_WIDTH_PX - NOTES_TABLE_CELL_PAD_PX * column_count)
    chars_per_row = usable / NOTES_TABLE_CHAR_PX
    lengths = [len(compact_spaces(cell)) for cell in cells] or [0]
    proportional = sum(lengths) / chars_per_row
    dominant = max(lengths) / (chars_per_row * 0.55)
    rows = max(1, int(math.ceil(max(proportional, dominant))))
    return NOTES_TABLE_ROW_PAD_PX + rows * NOTES_TABLE_LINE_PX


def estimate_table_height(entry):
    column_count = max(1, len(entry["header"]))
    height = NOTES_TABLE_CHROME_PX
    height += estimate_table_row_height(entry["header"], column_count)
    for row in entry["rows"]:
        height += estimate_table_row_height(row, column_count)
    return height


def split_table_entry(entry, available):
    """Split a table entry so the first part fits in `available` px.

    Returns (head, tail). `head` is None when not even the header plus one
    body row fits — the caller then warns instead of clipping silently.
    """
    column_count = max(1, len(entry["header"]))
    base = NOTES_TABLE_CHROME_PX + estimate_table_row_height(entry["header"], column_count)
    taken = []
    height = base
    for row in entry["rows"]:
        row_height = estimate_table_row_height(row, column_count)
        if taken and height + row_height > available:
            break
        taken.append(row)
        height += row_height
        if height > available:
            break
    if not taken or height > available:
        return None, entry
    remainder = entry["rows"][len(taken) :]
    head = dict(entry, rows=taken)
    if not remainder:
        return head, None
    tail = dict(entry, rows=remainder, continued=True)
    return head, tail


def estimate_note_entry_height(entry):
    if isinstance(entry, dict) and entry.get("type") == "table":
        return estimate_table_height(entry)
    text = entry["text"] if isinstance(entry, dict) else entry
    lines = estimate_text_lines(text, 78)
    return 8 + lines * 15


def paginate_note_blocks(blocks, warnings):
    pages = []
    current = []
    current_height = 0

    def flush():
        nonlocal current, current_height
        if current:
            pages.append({"blocks": current, "estimated_height": current_height})
            current = []
            current_height = 0

    for block in blocks:
        heading_height = 22
        entry_heights = [estimate_note_entry_height(entry) for entry in block["entries"]]
        block_height = heading_height + sum(entry_heights)
        if block_height <= NOTES_COLUMN_LIMIT:
            if current and current_height + block_height > NOTES_COLUMN_LIMIT:
                flush()
            current.append(block)
            current_height += block_height
            continue

        if current:
            flush()
        index = 0
        continued = False
        while index < len(block["entries"]):
            chunk_entries = []
            chunk_height = heading_height
            heading = block["heading"] + (" (continued)" if continued else "")
            while index < len(block["entries"]):
                entry = block["entries"][index]
                entry_height = estimate_note_entry_height(entry)
                if chunk_height + entry_height > NOTES_COLUMN_LIMIT and entry["type"] == "table":
                    # Tables are the one splittable entry: carve off the rows
                    # that fit, leave the rest for the next page (header is
                    # re-emitted there), so nothing clips.
                    head, tail = split_table_entry(entry, NOTES_COLUMN_LIMIT - chunk_height)
                    if head is not None and chunk_entries and len(head["rows"]) < 2:
                        # Not worth a header plus a single orphan row at the
                        # bottom of a page — start the table on the next one.
                        break
                    if head is not None:
                        chunk_entries.append(head)
                        chunk_height += estimate_table_height(head)
                        if tail is None:
                            index += 1
                        else:
                            block["entries"][index] = tail
                        break
                    if chunk_entries:
                        break
                    warn(
                        warnings,
                        f"Notes block '{block['heading']}': a single table row exceeds the page box",
                    )
                    chunk_entries.append(entry)
                    chunk_height += entry_height
                    index += 1
                    break
                if chunk_entries and chunk_height + entry_height > NOTES_COLUMN_LIMIT:
                    break
                if not chunk_entries and chunk_height + entry_height > NOTES_COLUMN_LIMIT:
                    warn(warnings, f"Notes block '{block['heading']}': estimated item exceeds page box")
                    chunk_entries.append(entry)
                    chunk_height += entry_height
                    index += 1
                    break
                chunk_entries.append(entry)
                chunk_height += entry_height
                index += 1
            pages.append(
                {
                    "blocks": [{"heading": heading, "entries": chunk_entries}],
                    "estimated_height": chunk_height,
                }
            )
            continued = True

    flush()
    return pages or [{"blocks": [], "estimated_height": 0}]


def paginate_questions(questions, warnings):
    entries = [
        {"type": "question", "text": question, "number": number}
        for number, question in enumerate(questions, 1)
    ]
    pages = []
    current = []
    current_height = 0
    for entry in entries:
        height = estimate_note_entry_height(entry)
        if current and current_height + height > NOTES_COLUMN_LIMIT:
            pages.append({"entries": current, "estimated_height": current_height})
            current = []
            current_height = 0
        if height > NOTES_COLUMN_LIMIT:
            warn(warnings, "Operator question: estimated item exceeds page box")
        current.append(entry)
        current_height += height
    if current:
        pages.append({"entries": current, "estimated_height": current_height})
    return pages or [{"entries": [], "estimated_height": 0}]


def build_pages(data):
    pagination_warnings = []
    pages = [{"type": "cover"}]

    for phase in data["phases"]:
        pages.extend(paginate_phase(phase, pagination_warnings))

    notes_blocks = copy.deepcopy(data["notes"]["blocks"])
    quality = data["quality_checklist"]
    if quality["items"] or quality["paragraphs"]:
        entries = [{"type": "bullet", "text": item} for item in quality["items"]]
        entries.extend({"type": "paragraph", "text": paragraph} for paragraph in quality["paragraphs"])
        notes_blocks.append({"heading": "Quality checklist", "entries": entries})

    note_pages = paginate_note_blocks(notes_blocks, pagination_warnings)
    question_pages = paginate_questions(data["notes"]["operator_questions"], pagination_warnings)
    notes_count = max(len(note_pages), len(question_pages))

    for idx in range(notes_count):
        pages.append(
            {
                "type": "notes",
                "note_blocks": note_pages[idx]["blocks"] if idx < len(note_pages) else [],
                "questions": question_pages[idx]["entries"] if idx < len(question_pages) else [],
                "continued": idx > 0,
            }
        )

    return pages, pagination_warnings


def titleize_slug(value):
    return " ".join(word.capitalize() for word in value.replace("-", " ").split())


def render_footer(data):
    """One quiet line: what this document is. Provenance stays in the
    source markdown's frontmatter — the client-facing PDF doesn't carry it."""
    frontmatter = data["frontmatter"]
    parts = []
    show = frontmatter.get("show", "").strip()
    business = frontmatter.get("business", "").strip()
    if show:
        parts.append(titleize_slug(show))
    if business and titleize_slug(business) not in parts:
        parts.append(titleize_slug(business))
    parts.append("Workflow Map")
    meta = html.escape("  ·  ".join(parts))
    return f"""
      <footer class="page-footer">
        <div class="wordmark" aria-label="Benali"></div>
        <div class="footer-meta">{meta}</div>
      </footer>
    """


def dedupe_cover_description(description):
    """Drop the trigger/end-state sentences from the cover paragraph — they
    live in the TRIGGER and END STATE cards; repeating them reads redundant."""
    sentences = re.split(r"(?<=[.!?])\s+", description.strip())
    kept = []
    for idx, sentence in enumerate(sentences):
        s = sentence.strip()
        if idx == 0 and s.lower().startswith("triggered"):
            continue
        if s.lower().startswith("the workflow ends"):
            continue
        kept.append(sentence)
    return " ".join(kept).strip() or description


def render_cover(data):
    workflow = data["workflow"]
    frontmatter = data["frontmatter"]
    draft_badge = ""
    if frontmatter.get("status", "").strip().lower() == "draft":
        draft_badge = '<div class="draft-badge">Draft, pending operator review</div>'

    rail_cards = []
    for phase in data["phases"]:
        rail_cards.append(
            f"""
            <div class="rail-card">
              <div class="rail-number">{html.escape(phase["number"])}</div>
              <div class="rail-title">{render_copy(phase["title"])}</div>
              <div class="rail-role">{render_copy(phase_owner(phase))}</div>
            </div>
            """
        )

    return f"""
    <div class="page page--grid cover">
      <div class="cover-top">
        <div class="kicker">Work Architecture: workflow map</div>
        {draft_badge}
      </div>
      <h1>{emphasize_title(workflow["title"])}</h1>
      <p class="workflow-description">{render_copy(dedupe_cover_description(workflow["description"]))}</p>
      <div class="state-strip">
        <div class="state-card">
          <div class="kicker">Trigger</div>
          <div class="state-copy">{render_copy(workflow["trigger"])}</div>
        </div>
        <div class="state-arrow">→</div>
        <div class="state-card">
          <div class="kicker">End state</div>
          <div class="state-copy">{render_copy(workflow["end_state"])}</div>
        </div>
      </div>
      <div class="phase-rail">
        {''.join(rail_cards)}
      </div>
      {render_footer(data)}
    </div>
    """


def render_phase_page(data, page):
    phase = page["phase"]
    continued = '<span class="continued-label">continued</span>' if page.get("continued") else ""
    handoff = ""
    if phase_has_handoff(phase):
        handoff = f"""
          <div class="handoff-banner">
            <div class="kicker">HANDOFF IN</div>
            <div class="handoff-copy">{render_copy(phase["description"])}</div>
          </div>
        """
    fragments = "\n".join(render_process_fragment(fragment) for fragment in page["fragments"])
    return f"""
    <div class="page page--grid phase-page">
      <header class="phase-header">
        <div class="phase-number">{html.escape(phase["number"])}</div>
        <div>
          <div class="phase-title-row">
            <h2 class="phase-title">{render_copy(phase["title"])}</h2>
            {continued}
          </div>
          <div class="phase-role">{render_copy(phase_owner(phase))}</div>
        </div>
      </header>
      {handoff}
      <main class="process-stack">
        {fragments}
      </main>
      {render_footer(data)}
    </div>
    """


def render_note_table(entry, wrapper_class="note-table-wrap", table_class="note-table"):
    head_cells = "".join(f"<th>{render_inline(cell)}</th>" for cell in entry["header"])
    body_rows = "".join(
        "<tr>" + "".join(f"<td>{render_inline(cell)}</td>" for cell in row) + "</tr>"
        for row in entry["rows"]
    )
    return (
        f'<div class="{wrapper_class}">'
        f'<table class="{table_class}">'
        f"<thead><tr>{head_cells}</tr></thead>"
        f"<tbody>{body_rows}</tbody>"
        "</table></div>"
    )


def render_note_entry(entry):
    if entry["type"] == "table":
        return render_note_table(entry)
    text = render_inline(entry["text"])
    if entry["type"] == "paragraph":
        return f'<p class="note-copy">{text}</p>'
    return f"<li>{text}</li>"


def render_note_blocks(blocks):
    if not blocks:
        return '<div class="empty-note">No notes in this column.</div>'

    rendered = []
    for block in blocks:
        bullets = []
        paragraphs = []
        for entry in block["entries"]:
            # Tables ride the paragraph stream so non-table content keeps its
            # existing paragraphs-then-bullets order untouched.
            if entry["type"] in ("paragraph", "table"):
                paragraphs.append(render_note_entry(entry))
            else:
                bullets.append(render_note_entry(entry))
        list_html = f'<ul class="note-list">{"".join(bullets)}</ul>' if bullets else ""
        rendered.append(
            f"""
            <div class="note-block">
              <h3 class="note-heading">{render_inline(block["heading"])}</h3>
              {''.join(paragraphs)}
              {list_html}
            </div>
            """
        )
    return "\n".join(rendered)


def render_questions(questions):
    if not questions:
        return '<div class="empty-note">No operator questions in this slice.</div>'
    start = int(questions[0].get("number", 1))
    return f"""
      <ol class="question-list" start="{start}">
        {''.join(f"<li>{render_inline(entry['text'])}</li>" for entry in questions)}
      </ol>
    """


def render_notes_page(data, page):
    continued = " (continued)" if page.get("continued") else ""
    # Wordmark lives in the footer only — no duplicate in the header.
    if page["questions"]:
        columns_class = "notes-columns"
        questions_section = f"""
        <section>
          <div class="kicker">OPERATOR QUESTIONS</div>
          {render_questions(page["questions"])}
        </section>
        """
    else:
        # No questions on this slice: notes span the full width.
        columns_class = "notes-columns notes-columns--single"
        questions_section = ""
    return f"""
    <div class="page page--bone notes-page">
      <header class="notes-header">
        <div>
          <div class="kicker">WORKFLOW MAP REVIEW</div>
          <h2 class="notes-title">Notes &amp; Assumptions{continued}</h2>
        </div>
      </header>
      <main class="{columns_class}">
        <section>
          <div class="kicker">NOTES &amp; ASSUMPTIONS</div>
          {render_note_blocks(page["note_blocks"])}
        </section>
        {questions_section}
      </main>
      {render_footer(data)}
    </div>
    """


def render_document(data, css):
    pages, pagination_warnings = build_pages(data)
    data["counts"]["pages"] = len(pages)

    rendered_pages = []
    for page in pages:
        if page["type"] == "cover":
            rendered_pages.append(render_cover(data))
        elif page["type"] == "phase":
            rendered_pages.append(render_phase_page(data, page))
        elif page["type"] == "notes":
            rendered_pages.append(render_notes_page(data, page))

    title = html.escape(data["workflow"]["title"])
    return (
        "<!doctype html>\n"
        '<html lang="en">\n'
        "<head>\n"
        '  <meta charset="utf-8">\n'
        '  <meta name="viewport" content="width=device-width, initial-scale=1">\n'
        f"  <title>{title}</title>\n"
        '  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Hanken+Grotesk:wght@300;400;500;600;700&display=swap">\n'
        f"  <style>\n{css}\n  </style>\n"
        "</head>\n"
        "<body>\n"
        '  <div class="document">\n'
        f"{''.join(rendered_pages)}\n"
        "  </div>\n"
        "</body>\n"
        "</html>\n"
    ), pagination_warnings


def load_theme_css():
    script_dir = Path(__file__).resolve().parent
    css_path = script_dir.parent / "assets" / "benali-print-theme.css"
    return css_path.read_text(encoding="utf-8")


def parse_args(argv):
    parser = argparse.ArgumentParser(
        description="Render an ops-map Workflow Map markdown file to Benali-branded print HTML."
    )
    parser.add_argument("workflow", help="Path to workflow markdown file")
    parser.add_argument("-o", "--output", required=True, help="Output HTML path")
    parser.add_argument("--json", action="store_true", help="Dump parsed data to stdout")
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv if argv is not None else sys.argv[1:])
    data = parse_workflow(args.workflow)
    css = load_theme_css()
    html_doc, pagination_warnings = render_document(data, css)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html_doc, encoding="utf-8")

    for message in data["parse_warnings"]:
        print(f"PARSE WARNING: {message}", file=sys.stderr)
    for message in pagination_warnings:
        print(f"PAGINATION WARNING: {message}", file=sys.stderr)
    print(f"Parse warnings: {len(data['parse_warnings'])}", file=sys.stderr)
    print(f"Pagination warnings: {len(pagination_warnings)}", file=sys.stderr)
    print(f"Rendered pages: {data['counts']['pages']}", file=sys.stderr)

    if args.json:
        debug = copy.deepcopy(data)
        debug["pagination_warnings"] = pagination_warnings
        json.dump(debug, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
