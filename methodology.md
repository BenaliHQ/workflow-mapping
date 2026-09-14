---
date: 2026-03-25
type: reference
status: active
---

# Work Architecture Methodology

The complete methodology for mapping how a business works, organizing that work into a functional hierarchy, and optionally connecting it to an AI agent architecture. This is the canonical reference for the entire Work Architecture practice.

---

## What Work Architecture Produces

Two complementary views of a business:

1. **Workflow Map** — The sequential view. Phase → Process → Core Activity. Shows HOW work moves from start to finish. The discovery tool. Multiple workflows per business, each triggered by a different event.
2. **Function Chart** — The organizational view. Function → Subfunction → Core Activity. Shows WHAT the business does, independent of who does it. The organizing framework. One chart per business, built FROM workflow data.

Both share the same atomic unit: the **Core Activity** — a specific, repeatable unit of work that produces a distinct, observable outcome.

---

## The Engagement Methodology

### Phase 1: Discovery & Vocabulary Lock

**Goal:** Understand the business, name the functions, lock terminology.

**Activities:**
1. Gather all raw input — transcripts, interviews, process descriptions, existing documentation
2. Process raw input into extracted patterns, principles, and actions
3. Define the top-level functions (typically 5-10): what does this business do?
4. Validate functions against the business owner's mental model
5. Lock terminology — confirm the client understands Phase, Process, Core Activity, the three handoff types, Function, Subfunction

**Output:** Function list with definitions. Shared vocabulary document.

**Duration:** 1-2 sessions.

### Phase 2: Workflow Mapping

**Goal:** Map how work actually moves, one workflow at a time.

**Activities:**
1. Identify all workflows — every trigger and end state
2. Walk through each workflow phase by phase with the operator
3. For each phase: identify processes, then core activities within each process
4. Name handoffs between phases — type them (Functional, Role, External), specify all four components
5. Document assumptions and gaps
6. Identify reusable processes — modules that appear across multiple workflows (e.g., POBO planning, content extraction)

**Rules during this phase:**
- No personal names — roles only
- Every core activity follows action verb + object + context
- Every process has an owner, trigger, and end state
- 4-8 phases per workflow, 2-6 activities per process
- The operator walks through; the architect structures
- Cross-cutting principles (scope mode, failure modes, two-pass review, etc.) get applied as activities are documented

**Output:** First-draft Workflow Maps. One per workflow. Gaps and assumptions documented.

**Duration:** Varies by complexity. A solo operator with 6-8 workflows: approximately 6-8 hours of active session time.

### Phase 3: Condensation

**Goal:** Reduce granularity to the right level. Remove checklist items masquerading as core activities.

**Activities:**
1. Apply the core activity standards (see below) to each workflow
2. Apply the five tests: outcome, SOP, assignment, specialization, canonical title
3. Merge verification steps into parent activities
4. Merge single-activity processes with related processes (when they serve the same purpose)
5. Enforce naming rules: verb first, under 15 words, no em-dash explanations, no conditional language
6. Cross-reference activity titles across all workflows for consistency
7. Preserve condensed detail as future SOP content — the detail moves down, not out

**Output:** Condensed Workflow Maps. Core Activity Standards document (the rules used, which become the client's ongoing governance tool).

**Duration:** Typically 40-60% reduction from first-draft maps.

### Phase 4: Function Chart Construction

**Goal:** Reorganize activities from sequential to functional.

**Activities:**
1. Extract every core activity from every condensed workflow with its source process
2. Group activities by function (the top-level functions from Phase 1)
3. Define subfunctions within each function using the specialization test
4. Place each activity under exactly one subfunction
5. Mark activities that appear in multiple workflows — these are canonical activities
6. Unify near-duplicate titles into canonical names — the function chart is the source of truth
7. Validate: no orphaned activities, balanced subfunctions (3-15 activities each)
8. Identify Orphaned Functions (work nobody owns) and Unicorn Roles (roles built around one person)

**Output:** Complete Function Chart with source traceability. Canonical activity list.

**Duration:** 1-2 sessions after workflows are condensed.

### Phase 5: Gap Analysis & Optimization

**Goal:** Identify what is missing, redundant, or misplaced.

**Activities:**
1. Run workflow gap analysis against industry best practices
2. Run function chart gap analysis for structural issues
3. Identify missing functions, subfunctions, and activities
4. Identify redundancies and overlap
5. Prioritize gaps by impact, frequency, and effort
6. Present recommendations with concrete additions

**Output:** Gap analysis report. Enhanced maps and chart with markers.

### Phase 6: Architecture Mapping *(optional — for AI-ready clients)*

**Goal:** Map the function chart to an AI agent architecture.

**Activities:**
1. Map functions to agents/orchestrators
2. Map subfunctions to skill domains/sub-agents
3. Map core activities to individual skill files
4. Identify which activities are candidates for automation vs human judgment
5. Define execution models (5-10-80-5 for agent-led, 10-80-10 for operator-led)
6. Define the build-review loop pattern (builder ≠ reviewer)
7. Specify non-negotiables and rules

**Output:** Agent architecture spec. Skill manifest. Rule definitions.

---

## Core Concepts

### The Core Activity

The atomic unit of work. A core activity is the smallest unit of work that:
- Produces a distinct, observable outcome
- Can stand alone as an assignable task
- Warrants its own documentation (SOP, checklist, examples)
- Would require the same training and expertise regardless of context

**The formula:** action verb + object + context

**What a core activity is NOT:**
- A step within a larger activity (those become checklist items in the SOP)
- A verification that doesn't produce new output (those fold into the parent activity's checklist)
- The same work repeated on different inputs (reviewing 6 files in a folder is one activity with a checklist)

### The Five Tests

Apply these in order when determining whether something is a core activity:

| Test | Question | If yes... | If no... |
|---|---|---|---|
| **Outcome test** | Does this produce a distinct result the next activity depends on? | Core activity | Checklist item |
| **SOP test** | Would you write a separate SOP for this? | Core activity | Fold into another activity's SOP |
| **Assignment test** | Could this be a standalone task on someone's to-do list? | Core activity | Step within a task |
| **Specialization test** | Does this require distinct expertise? | May be its own subfunction | Stays within current subfunction |
| **Canonical test** | Does this same work appear in another workflow? | Must use identical title everywhere | Title is local to this workflow |

### Reusable Processes

Some processes appear across multiple workflows. When this happens:
- The process is defined in full in ONE canonical location (typically the workflow where it's most detailed)
- Other workflows reference it by name — one line expands to the full process when executed
- The function chart treats the activities within the reusable process the same as any other — each activity maps to one subfunction

Examples from practice: POBO planning (appears in daily planning, project planning, engagement scoping, build scoping, night shift speccing), content extraction (appears in daily processing and content creation).

### Two Production Modes

Service businesses commonly have two distinct types of production:

1. **Session-based production** — the deliverable is the session itself (coaching, workshops, discovery calls, presentations). Calendar-driven. The workflow follows: prep → deliver → debrief → follow-up.
2. **Build-based production** — the deliverable is an artifact (reports, maps, frameworks, documents). Plan-driven. The workflow follows: scope → execute → review → deliver.

Both can run against the same project. The project plan determines which phases are session-based and which are build-based.

### Subfunctions

A distinct type of work within a function, characterized by a shared skill set, shared procedures, and shared judgment criteria. Activities within a subfunction use similar thinking and produce similar types of output. Not distinguished by cadence, workflow source, or who performs the work — only by the nature of the work itself.

**The test:** If you hired someone to do the activities in a subfunction, would they need the same training and apply the same expertise across all of them? If yes, it's one subfunction.

### Handoff Types

| Type | What crosses | Risk level |
|---|---|---|
| **Functional Handoff** | Work crosses between functions | Highest — different skills, different context |
| **Role Handoff** | Work transfers within the same function | Medium — same skills, different person |
| **External Handoff** | Work leaves the organization | Variable — loss of control and visibility |

Every handoff has four components: sender, receiver, what transfers, and acceptance criteria.

---

## Cross-Cutting Principles

These principles get applied across all workflows during Phase 2 mapping. They are not workflow-specific — they're operating principles that improve any process.

### Scope Mode
Before starting any planning work, commit to a scope mode: expand (dream big), hold (maximum rigor), or reduce (strip to essentials). This prevents scope drift by making the scope decision explicit before the work begins.

### Two-Pass Review
Separate critical review (does it solve the problem? are there structural issues?) from refinement review (is it polished? is it complete? is it accurate?). Structural issues get caught before polish work begins.

### Builder ≠ Reviewer
The person or agent that builds a deliverable does not review their own work. A separate reviewer brings fresh perspective. The builder addresses review feedback, then the operator reviews the polished result.

### Concrete Options at Checkpoints
Never present open-ended questions. Present 2-3 concrete options with tradeoffs at every decision point. This makes checkpoints faster and more decisive.

### Failure Mode Mapping
Before committing to a plan, identify what could go wrong. Applied to daily planning, session prep, project scoping, build definition, and deal management.

### Reversibility Rating
Rate key decisions on reversibility — how easily can this be undone? Prefer approaches that can be iterated on. One-way decisions require explicit justification.

### Data-Driven Debrief
After execution, review what happened with actual metrics and specific evidence, not feelings. Applied to build debriefs, engagement debriefs, weekly operating discipline review, and content performance tracking.

### Priority Hierarchy Under Pressure
When the plan breaks, define what gets protected (never skip), what gets compressed (do the minimum), and what gets deferred (handle later). Every workflow should have this defined.

### Signal Over Noise
When synthesizing information for the operator, present conclusions and recommendations — not raw data. Cap the number of attention items and questions. The operator should be able to review and respond in a defined time window.

---

## Execution Models

### 5-10-80-5 (Agent-Led Work)
When the agent proactively surfaces work:
- **First 5% (Agent):** Identifies the opportunity, surfaces candidates, drafts concept and questions
- **10% (Operator):** Reviews, approves, answers questions, provides input and direction
- **80% (Agent):** Executes the full build
- **Final 5% (Operator):** Reviews and polishes the output

Applies to: content creation, night shift specs, proactive build deliverables, and anything the agent surfaces.

### 10-80-10 (Operator-Led Work)
When the operator initiates the work:
- **10% (Operator):** Has the idea, provides input and direction
- **80% (Agent):** Executes
- **10% (Operator):** Reviews and polishes

Applies to: operator-initiated projects, ad hoc requests, strategy work.

### Autonomous Execution
The agent does not pause mid-build for operator approval. The operator sees a finished, reviewed deliverable — not a work-in-progress. Checkpoints are self-assessments, not handoffs. There is no schedule pressure for autonomous builds — the agent executes until the deliverable is complete.

### The Build-Review Loop
Build → Review → Address Feedback → Review Again → (loop until approved) → Operator Review.

Independent of who builds and who reviews. The pattern works for: agent builds / different agent reviews, agent builds / human reviews, human builds / agent reviews. The key: builder ≠ reviewer.

---

## Naming Rules

### Core Activity Titles
1. Always start with an action verb
2. No em-dash explanations in the title — detail goes in the SOP
3. Context only when needed to distinguish from other activities
4. Under 15 words
5. No conditional language ("if applicable," "if needed")
6. Same work, same title, everywhere — the function chart is the source of truth

### Process Names
- Named by the type of work, not by the workflow they live in
- Processes with the same name in different workflows must contain the same activities (or be explicitly distinguished)

### Subfunction Names
- Named by the specialization, not by the cadence or trigger
- Two-word maximum when possible (e.g., "Lead Management," "Build Execution," "Personal Reflection")

---

## Process Rules

- Single-activity processes are a smell — either merge with a related process or confirm it genuinely stands alone
- Processes should have 2-6 activities
- Processes merge when they serve the same purpose (the "one unit of work" test)
- Processes keep separate when they serve different purposes, even if small

---

## Condensation Rules

When condensing first-draft workflows:
1. Multiple activities producing the same outcome → one activity
2. Verification steps → fold into parent activity or process audit
3. Em-dash explanations → remove from title, preserve as SOP content
4. Canonical activities that appear across workflows → keep exact title, never condense
5. Detail moves to SOP level, not deleted — the detail is the future skill folder content
6. Audits stay inline — they're the enforcement mechanism
7. Logging and updating activities condense when the target is the same type
8. Routing activities stay separate when destinations are canonical

---

## Connection to AI Agent Architecture

| Function Chart Level | Agent Architecture Equivalent | Example |
|---|---|---|
| **Function** | Orchestrating agent | Strategy agent, Sales agent |
| **Subfunction** | Sub-agent or skill domain folder | Planning & Prioritization, Lead Management |
| **Core Activity** | Individual skill file (SOP + checklist + examples) | "Process meeting transcripts into vault" |

**Sub-agent vs skill folder test:** Does the subfunction need its own context, memory, and decision-making? If yes → sub-agent. If it just needs instructions → skill folder. Most subfunctions are skill folders.

**The practical floor:** Not every core activity needs a full folder. If it requires judgment, context, or has multiple ways to fail — it gets a folder. If it's mechanical — it's a line item in a broader skill file. The test: if a 5-10 item checklist could be written for it, it's the right level.

Each core activity skill file contains:
- **SOP** — Standard operating procedure (the how)
- **Checklist** — Quality gate (the minimum)
- **Examples** — Reference outputs (the standard)
- **Templates** — Starting points
- **Software guidance** — Tool-specific documentation
- **Responsible roles** — Who does this today (for trust and escalation)

---

## Standard Project Folder Structure

Every mapped engagement produces a standard project folder (documented in [[project-folder-spec]]):

```
project-name/
  _brief.md              ← What and why (stable)
  _plan.md               ← Phases, sequence, ownership (evolves)
  _status.md             ← Current state, next action (updated constantly)
  specs/                 ← Execution instructions for autonomous work
  reference/             ← Inputs — research, client docs, thinking material
  deliverables/          ← Outputs — what ships
  notes/                 ← Working space — drafts, thinking, scratch
```

---

## Benchmarks

From the first full mapping (solo operator, consulting business, 2026):
- 6 functions, 32 subfunctions
- 8 workflows, 120 processes
- 353 total workflow activities → 328 unique on function chart (25 canonical duplicates)
- First-draft activities before condensation: ~696
- Condensation rate: ~49%

---

## Key Terminology

- **Phase** — Structural grouping of Processes. Phase boundaries = Functional Handoffs.
- **Process** — Ordered sequence of Core Activities producing a specific result. Required level — never skip.
- **Core Activity** — The atomic unit of work. Produces a distinct, observable outcome. Lives in one Subfunction, can appear in multiple Processes.
- **Function** — Major area of responsibility. Exists whether or not anyone is assigned.
- **Subfunction** — Distinct area within a Function. Specialization test: could someone specialize in it?
- **Functional Handoff** — Work crosses between functions. Highest risk.
- **Role Handoff** — Work transfers within the same function.
- **External Handoff** — Work leaves the organization.
- **Orphaned Function** — Work nobody is formally responsible for.
- **Unicorn Role** — Role built around one person rather than business needs.
- **Constraint** — The single point limiting system throughput.
- **Canonical Activity** — A core activity that appears in multiple workflows. Must use identical title everywhere. The function chart is the source of truth.
- **Reusable Process** — A process that appears across multiple workflows. Defined in full in one location, referenced by name elsewhere.

---

## Skill Pipeline

```
Phase 1: /work-architecture (router) → Discovery & vocabulary lock
Phase 2: /workflow architect      → First-draft workflow maps
Phase 3: /condense                → Condensed workflow maps
Phase 4: /function-chart architect → Function chart from condensed workflows
Phase 5: /workflow gap-analysis + /function-chart gap-analysis → Gap reports
Phase 6: /agent-architect         → AI agent/skill architecture (optional)

Cross-cutting: /reconcile → Title consistency and governance across workflows
```

## Skill Files

- Workflow skills: `.claude/skills/workflow/`
- Function chart skills: `.claude/skills/function-chart/`
- Core activity standards: [[core-activity-standards]] (governance reference)
- Industry discovery questions: [[industry-discovery-questions]]
- Project folder spec: [[project-folder-spec]]
