#!/usr/bin/env python3
"""wa-visualize `site` output: a client review site for one or more workflow maps.

Writes, into the output folder:
  index.html          the workflows, plus a review card when there are open questions
  review.html         every workflow with question cards, response boxes, and Copy responses;
                      when questions.json exists but holds none, a page saying there is nothing to review
  <slug>.html         one read-only page per workflow (no questions)
  assets/benali-review-theme.css

Inputs (paths in site.json are relative to site.json):
  site.json      {"client", "title", "base", "out", "maps": [{"source", "slug", "tab"}],
                  "updates": "updates.json", "questions": "questions.json"}
  updates.json   optional. Agreed changes on top of each map, keyed by map slug. See SKILL.md.
  questions.json optional. Open questions per map slug: [{"at", "q", "guess"}].

Plain Python 3, no dependencies. The maps stay the source of truth; this only renders.
"""
import argparse, html, json, os, re, shutil, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "..", "assets")
E = html.escape


# ---------------------------------------------------------------- parsing

def parse_map(path):
    """Read an ops-map source markdown file into phases, processes and activities."""
    text = open(path, encoding="utf-8").read()
    title = (re.search(r"## Workflow\s+\*\*Title:\*\*\n```\n(.*?)\n```", text, re.S) or [None, ""])[1].strip()
    body = text.partition("## Notes & Assumptions")[0]
    blocks = re.split(r"\n(?=#{2,4} (?:Phase|Process|Core Activity) )", body)[1:]
    items, ph, pr = [], None, None
    for b in blocks:
        head = b.split("\n", 1)[0].strip("# ").strip()
        f = {k: v.strip() for k, v in re.findall(r"\*\*(\w[\w ]*):\*\*\n```\n(.*?)\n?```", b, re.S)}
        n = head.split()[-1]
        if head.startswith("Phase"):
            ph = {"n": n, "title": f.get("Title", ""), "desc": f.get("Description", "")}
        elif head.startswith("Process"):
            pr = {"n": n, "title": f.get("Title", ""), "role": f.get("Role", ""), "desc": f.get("Description", "")}
            items.append({"kind": "process", "phase": ph, "proc": pr})
        else:
            items.append({"kind": "act", "n": n, "title": f.get("Title", ""), "sw": f.get("Software", ""),
                          "status": f.get("Status", ""), "desc": f.get("Description", ""),
                          "trigger": f.get("Trigger", ""), "end": f.get("End state", ""), "phase": ph, "proc": pr})
    if not items:
        sys.exit(f"{path}: no phases, processes or activities found. Is this an ops-map source file?")
    return title, items


# ---------------------------------------------------------------- pieces

TOOLS = json.load(open(os.path.join(ASSETS, "tool-colors.json")))
FREE = TOOLS.pop("_free_hues")
TOOLS.pop("_note", None)


def tool_pills(sw):
    names = [x.strip() for x in (sw or "").split(",") if x.strip()]
    if not names:
        return '<span class="none">No software</span>'
    out = []
    for n in names:
        hue = TOOLS.get(n) or FREE[sum(map(ord, n)) % len(FREE)]
        out.append(f'<span class="tool" style="--hue: var(--cat-{hue})">{E(n)}</span>')
    return "".join(out)


def para(text):
    """Description prose only. The maps' 'SOP checklist:' tails stay out of the site on purpose."""
    body = (text or "").partition("SOP checklist:")[0]
    return "".join(f"<p>{E(p.strip())}</p>" for p in body.strip().split("\n\n") if p.strip())


def label(at):
    kind, _, n = at.partition(":")
    return "Activity " + at if not n else ("Phase " if kind == "phase" else "Process ") + n


def rowid(key, at):
    return f'r-{key}-{at.replace(":", "-").replace(".", "_")}'


# ---------------------------------------------------------------- one workflow

def build(key, items, updates, questions, with_q, problems):
    ch = updates.get(key, {})
    qs = questions.get(key, []) if with_q else []
    open_at = {q["at"] for q in questions.get(key, [])}  # an open question keeps an activity in draft
    by_at = {}
    for i, q in enumerate(qs):
        by_at.setdefault(q["at"], []).append((i, q))
    seen, used, cards, phases = set(), set(), [], []

    def marker(at):
        qa = by_at.get(at, [])
        if not qa:
            return "", ""
        used.add(at)
        cards.extend((at, i, q) for i, q in qa)
        first = qa[0][0]
        return (f'<a class="qm" href="#q-{key}-{first}" data-card="q-{key}-{first}" '
                f'aria-label="{len(qa)} open question{"s" if len(qa) > 1 else ""}">{len(qa)}</a>', " hasq")

    def expandable(at, cls, head, detail):
        seen.add(at)
        mk, hq = marker(at)
        if not detail:
            return f'<div class="row{cls}{hq}" id="{rowid(key, at)}"><div class="a">{head}{mk}</div></div>'
        return (f'<details class="row{cls}{hq}" id="{rowid(key, at)}"><summary class="a">{head}{mk}</summary>'
                f'<div class="more">{detail}</div></details>')

    def act(rows, n, title, who, sw, st, base_desc, note, trig, end):
        if n in open_at and st == "active":
            st = "draft"
        head = (f'<div class="t"><span class="n">{E(n)}</span><span>{E(title)}</span></div>'
                f'<div class="m"><span class="who">{E(who)}</span><span class="tools">{tool_pills(sw)}</span>'
                f'<span class="st st-{E(st)}">{E(st or "unknown")}</span></div>')
        desc = (f"<p>{E(note)}</p>" if note else "") + para(base_desc)
        detail = f'<div class="desc">{desc}</div>' if desc else ""
        if trig or end:
            detail += '<div class="te">'
            if trig:
                detail += f'<span class="pill trig">Trigger</span><span class="tv">{E(trig)}</span>'
            if end:
                detail += f'<span class="pill endst">End state</span><span class="tv">{E(end)}</span>'
            detail += "</div>"
        rows.append(expandable(n, "", head, detail))

    for it in items:
        ph = it["phase"]
        if not phases or phases[-1]["n"] != ph["n"]:
            seen.add("phase:" + ph["n"])
            mk, hq = marker("phase:" + ph["n"])
            phases.append({"n": ph["n"], "rows": [],
                           "head": f'<header class="ph{hq}" id="{rowid(key, "phase:" + ph["n"])}"><p class="ph-k">Phase {E(ph["n"])}</p><h3>{E(ph["title"])}</h3>{mk}</header>'})
        rows = phases[-1]["rows"]
        if it["kind"] == "process":
            p = it["proc"]
            role = (ch.get("proc:" + p["n"]) or {}).get("role", p["role"])
            head = f'<div class="t pr"><span class="n">{E(p["n"])}</span><span>{E(p["title"])}<span class="role">{E(role)}</span></span></div>'
            rows.append(expandable("proc:" + p["n"], " proc", head, f'<div class="desc">{para(p.get("desc"))}</div>' if para(p.get("desc")) else ""))
            continue
        c = ch.get(it["n"]) or {}
        role = (ch.get("proc:" + it["proc"]["n"]) or {}).get("role", it["proc"]["role"])
        bf = ch.get("before:" + it["n"])
        if bf:
            act(rows, bf["n"], bf["title"], bf.get("doer", role), bf.get("sw", ""), bf.get("status", "gap"), "", bf.get("desc"), bf.get("trigger", ""), bf.get("end", ""))
        q_only = c.get("type") == "question"
        act(rows, c.get("n", it["n"]), it["title"] if q_only else c.get("title", it["title"]), c.get("doer", role),
            it["sw"] if q_only else c.get("sw", it["sw"]), c.get("status", it["status"]),
            it.get("desc"), c.get("desc"), it.get("trigger"), it.get("end"))
        ad = ch.get("add:" + it["n"])
        if ad:
            act(rows, ad["n"], ad["title"], ad.get("doer", role), ad.get("sw", ""), ad.get("status", "gap"), "", ad.get("desc"), ad.get("trigger", ""), ad.get("end", ""))

    # every update and question must point at something that exists
    known = {it["n"] for it in items if it["kind"] == "act"} | {"proc:" + it["proc"]["n"] for it in items if it["kind"] == "process"}
    for k in ch:
        target = k.split(":", 1)[1] if k.startswith(("add:", "before:")) else k
        if target not in known:
            problems.append(f"updates.json {key}: '{k}' does not match an activity or process in the map")
    for q in questions.get(key, []):
        if q["at"] not in seen:
            problems.append(f"questions.json {key}: question pinned to '{q['at']}', which is not on the rendered map")

    qcards = "".join(
        f'<div class="qc" id="q-{key}-{i}" data-row="{rowid(key, at)}" data-map="{{MAPNAME}}" data-at="{E(label(at))}" data-q="{E(q["q"])}">'
        f'<div class="qc-h"><button type="button" class="qc-jump" data-row="{rowid(key, at)}">{E(label(at))}</button>'
        f'<span class="qc-i" aria-hidden="true">?</span></div><p class="qq">{E(q["q"])}</p>'
        + (f'<p class="qg">Our guess: {E(q["guess"])}</p>' if q.get("guess") else "")
        + f'<label class="sr" for="a-{key}-{i}">Response</label><textarea id="a-{key}-{i}" class="qa" rows="2" placeholder="Type a response"></textarea></div>'
        for at, i, q in cards)
    body = "".join(f'<article class="wm-phase">{p["head"]}{"".join(p["rows"])}</article>' for p in phases)
    stats = (len(phases), sum(1 for x in items if x["kind"] == "process"),
             sum(1 for x in items if x["kind"] == "act") + sum(1 for k in ch if k.startswith(("add:", "before:"))))
    qcol = f'<div class="qcol">{qcards}</div>' if with_q else ""
    return f'<section class="map{"" if with_q else " solo"}" data-k="{key}"><div class="wf">{body}</div>{qcol}</section>', len(qs), stats


# ---------------------------------------------------------------- site

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("site", help="path to site.json")
    ap.add_argument("-o", "--out", help="output folder (overrides site.json 'out')")
    a = ap.parse_args()
    root = os.path.dirname(os.path.abspath(a.site))
    cfg = json.load(open(a.site))
    rel = lambda p: os.path.join(root, p)
    out = os.path.abspath(a.out or rel(cfg.get("out", "site")))
    base = cfg.get("base", "").rstrip("/")
    link = (lambda slug: f"{base}/{slug}") if base else (lambda slug: f"{slug}.html")
    home = base or "index.html"
    assets = f"{base}/assets" if base else "assets"
    updates = json.load(open(rel(cfg["updates"]))) if cfg.get("updates") else {}
    questions = json.load(open(rel(cfg["questions"]))) if cfg.get("questions") else {}
    client, title = cfg.get("client", ""), cfg.get("title", "Workflow maps")

    maps = []
    for m in cfg["maps"]:
        wtitle, items = parse_map(rel(m["source"]))
        maps.append({"slug": m["slug"], "tab": m.get("tab", wtitle), "title": m.get("title", wtitle), "items": items})

    problems, secs, tabs, cards = [], [], [], []
    total = sum(len(questions.get(m["slug"], [])) for m in maps)
    for m in maps:
        sec, n, _ = build(m["slug"], m["items"], updates, questions, True, problems)
        secs.append(sec.replace("{MAPNAME}", E(m["tab"])))
        tabs.append(f'<a href="#{m["slug"]}" class="tab" data-k="{m["slug"]}">{E(m["tab"])}<span class="cnt" data-cnt="{m["slug"]}">{n}</span></a>')
    if problems:
        sys.exit("Not rendered:\n  " + "\n  ".join(problems))

    tpl = lambda name: open(os.path.join(ASSETS, name), encoding="utf-8").read()
    fill = lambda s, **kw: re.sub(r"\{\{(\w+)\}\}", lambda x: str(kw.get(x.group(1), x.group(0))), s)
    common = dict(ASSETS=assets, CLIENT=E(client), TITLE=E(title), HOME=home, STORE=E("wa-review:" + (base or title)))
    os.makedirs(os.path.join(out, "assets"), exist_ok=True)
    shutil.copy(os.path.join(ASSETS, "benali-review-theme.css"), os.path.join(out, "assets"))

    has_review = bool(total) or bool(cfg.get("questions"))
    if total:
        page = fill(tpl("site-review.html"), TABS="".join(tabs) if len(maps) > 1 else "", SECTIONS="".join(secs),
                    TOTAL=total, SINGLE=" single" if len(maps) == 1 else "", HIDE="", **common)
        open(os.path.join(out, "review.html"), "w").write(page)
    elif has_review:
        # Keep the review URL working once every question is answered, instead of leaving a stale page behind.
        empty = ('<section class="nothing"><h2>Nothing to review</h2>'
                 '<p>Every open question on these workflows has been answered. New questions will appear here.</p></section>')
        page = fill(tpl("site-review.html"), TABS="", SECTIONS=empty, TOTAL=0, SINGLE=" single", HIDE=" hidden", **common)
        open(os.path.join(out, "review.html"), "w").write(page)
    for m in maps:
        sec, _, (np, npr, na) = build(m["slug"], m["items"], updates, questions, False, [])
        st = f"{np} phases · {npr} processes · {na} activities"
        open(os.path.join(out, m["slug"] + ".html"), "w").write(
            fill(tpl("site-workflow.html"), WTITLE=E(m["title"]), SECTION=sec, STATS=st, **common))
        cards.append(f'<a class="wcard" href="{link(m["slug"])}"><span class="wname">{E(m["title"])}</span><span class="wstats">{st}</span></a>')
    review_card = (f'<a class="review" href="{link("review")}"><div><p class="k">Review</p><h2>'
                   f'{"All workflows" if len(maps) > 1 else "The workflow"} with open questions</h2><p>{total} question{"s" if total != 1 else ""}. '
                   f'Answer them in place, then copy your responses into an email.</p></div><span class="go">Open review</span></a>') if total else (
                   f'<a class="review" href="{link("review")}"><div><p class="k">Review</p><h2>Nothing to review</h2>'
                   f'<p>Every open question has been answered.</p></div><span class="go">Open review</span></a>' if has_review else "")
    open(os.path.join(out, "index.html"), "w").write(fill(tpl("site-index.html"), CARDS="".join(cards), REVIEW=review_card, **common))
    print(f"Wrote {out}: index, {'review, ' if has_review else ''}{len(maps)} workflow page(s); {total} open question(s)")


if __name__ == "__main__":
    main()
