# Copilot Sidecar — Architecture

## Overview

A Copilot CLI skill that runs in a tmux side pane, watches a developer's terminal, and narrates what's happening in plain English. Not a traditional app — it's a markdown skill definition (`SKILL.md`) that instructs `gh copilot` how to behave, plus JSON config files and a bash launcher.

The skill reads the main pane via `tmux capture-pane`, diffs the output, classifies events, passes everything through a jargon firewall, and renders 3-line narration cards. All state lives in `~/.copilot/sidecar/`.

## Components

| Component | File | Purpose |
|-----------|------|---------|
| Launcher | `sidecar.sh` | Preflight checks (tmux, gh, skill file), tmux session setup, solo-mode fallback |
| Skill Definition | `SKILL.md` | Prompt instructions: personality, state machine, card rendering, firewall rules |
| Jargon Dictionary | `jargon-dictionary.json` | 40+ terms with plain-English definitions; keyed by term slug |
| Narration Cards | `narration-cards.json` | Regex→card mapping: `pattern`, `emoji`, `title`, `what`, `why`, `next` |
| Question Templates | `question-templates.json` | Event-type→question arrays for chip generation |
| Demo Replays | `demos/*.jsonl` | Pre-recorded terminal sessions as `{type, text, delay_ms}` events |
| User Profile | `user-profile.json` (runtime) | Language level, glossary progress, session count, panic count |
| Pane Capture | `runtime/pane-capture/` (runtime) | `main.prev.txt`, `main.curr.txt`, `main.diff.json`, `screen-map.json` |

## Data Flow (numbered steps)

```
1. sidecar.sh          → preflight checks → tmux split → launches `gh copilot --skill sidecar`
2. SKILL.md startup    → reads user-profile.json (or runs onboarding if missing)
                       → reads session-link.json for tmux pane IDs
                       → checks for active Copilot session (lock files in ~/.copilot/session-state/)
3. Pane capture        → `tmux capture-pane -t $MAIN_PANE_ID -p -S -2000 -E -1`
                       → writes main.curr.txt, diffs against main.prev.txt
4. Diff                → fast path: detect appended lines (suffix comparison)
                       → writes main.diff.json: {new_lines[], diff_kind, freshness_ms}
5. Event inference     → regex match new_lines against heuristic patterns
                       → assign event_type + base confidence (0.1–1.0)
                       → boost +0.15 if corroborated by events.jsonl
                       → writes to feed/narration-events.jsonl
6. Card lookup         → match event command against narration-cards.json patterns
                       → fallback card if no pattern matches
                       → attach confidence label + freshness bucket (LIVE/WARM/STALE)
7. Jargon firewall     → scan card text for dictionary terms (\bTERM\b, case-insensitive)
                       → check user-profile.json glossary: graduated (≥5) → pass, seen 1-4 → inline gloss, first use → full analogy
                       → increment term counts in profile
8. Chip generation     → select 4 questions: [1] status, [2] last-changed file, [3] last command, [4] safety
                       → source from question-templates.json keyed by event type
9. Display             → render 3-line card with emoji header + chips below
                       → apply throttle: max 1 card/10s, buffer bursts as "(+N more)"
```

## SKILL.md Structure (~700 lines)

```
Lines 1-40      IDENTITY — personality rules, emoji palette, banned words ("just", "simply")
Lines 41-80     STARTUP SEQUENCE — profile load, session detection, 4-path matrix
Lines 81-140    ONBOARDING — 90-second flow, 3 levels, profile creation
Lines 141-200   STATE MACHINE — IDLE/WATCHING/EXPLAINING/OFFERING/PANIC transitions
Lines 201-300   WATCH MODE — pane capture instructions, card rendering format, throttle rules
Lines 301-370   ASK MODE — question handling, "simpler please", explore agent delegation
Lines 371-420   SUGGEST MODE — proactive cards, consequence preview, 1-per-3min limit
Lines 421-500   JARGON FIREWALL — algorithm pseudocode, graduation logic, glossary commands
Lines 501-560   PANIC HANDLER — safe? command, 3 safety states (green/yellow/red)
Lines 561-620   DEMO MODE — replay engine, session re-detection every 30s
Lines 621-680   SAFETY FRAMING — reassurance rules, error normalization, undo messaging
Lines 681-700+  REFERENCE — command shortcuts (safe?, chips, glossary, expert, beginner, teach)
```

## State Machine

```
                    ┌──────────────────────────────────────────────┐
                    │                                              │
    ┌───────┐  pane event   ┌──────────┐  user question  ┌────────────┐
    │ IDLE  │──────────────→│ WATCHING │────────────────→│ EXPLAINING │
    └───────┘               └──────────┘                 └────────────┘
        ↑                       ↑                              │
        │ no session            │ ignore/timeout 60s           │ found offer
        │                       │                              ↓
    ┌─────────┐                 │                        ┌──────────┐
    │DEMO MODE│                 └────────────────────────│ OFFERING │
    └─────────┘                                          └──────────┘

    ANY STATE ──"safe?"──→ PANIC (show safety card) ──→ return to previous state
```

**Transitions:**
- `IDLE → WATCHING`: qualifying pane event detected, narration ON
- `WATCHING → EXPLAINING`: user types a question or selects a chip (1-4)
- `EXPLAINING → OFFERING`: sidecar identifies a safe follow-up (demo, glossary, practice)
- `OFFERING → WATCHING`: user ignores (60s timeout) or completes action
- `IDLE → DEMO MODE`: no active session found; replays `demos/*.jsonl`
- `DEMO MODE → WATCHING`: live session detected on 30s re-check, user confirms switch

## File Structure

```
~/.copilot/skills/sidecar/           # SHIPPED — installed files
├── SKILL.md                          # Main skill prompt (700+ lines)
├── jargon-dictionary.json            # {term: definition} × 40+ entries
├── narration-cards.json              # {cards: [{pattern, emoji, title, what, why, next}], fallback: {...}}
├── question-templates.json           # {event_type: [question_string, ...]}
├── demos/
│   ├── index.json                    # [{id, title, file, duration_s, teaches}]
│   ├── 01-checking-code.jsonl        # {type, text, delay_ms} per line
│   ├── 02-running-tests.jsonl
│   └── 03-ai-agents.jsonl
└── README.md                         # Setup instructions for end users

~/bin/sidecar.sh                      # SHIPPED — launcher script

~/.copilot/sidecar/                   # RUNTIME — created on first use
├── user-profile.json                 # language_level, glossary, sessions_count, panic_count
├── session-link.json                 # {cwd, started_at, launcher_pid, mode}
├── launcher.log                      # JSONL preflight/launch events
├── runtime/pane-capture/
│   ├── main.pane.json                # {tmux_session, main_pane_id, sidecar_pane_id}
│   ├── main.prev.txt                 # Previous capture (raw text)
│   ├── main.curr.txt                 # Current capture (raw text)
│   ├── main.diff.json                # {new_lines[], diff_kind, freshness_ms}
│   └── screen-map.json               # [{n, text}] for "explain line N"
└── feed/
    ├── narration-events.jsonl        # Inferred events with confidence scores
    └── cards.jsonl                   # Rendered card history
```

## Technology Choices

| Choice | Rationale |
|--------|-----------|
| Bash for `sidecar.sh` | No dependencies; runs on macOS/Linux; handles tmux lifecycle |
| Markdown for `SKILL.md` | Copilot CLI skill format — prompt engineering, not code |
| JSON for all config | Native to `gh copilot`; no parsers needed; human-editable |
| JSONL for events/demos | Append-only, streamable, one event per line |
| `tmux capture-pane` | Only reliable way to read another pane's content without ptrace |
| `~/.copilot/sidecar/` for runtime | Follows Copilot CLI conventions; survives session restarts |
| Atomic file writes (temp→rename) | Prevents partial reads of user-profile.json mid-update |

## JSON Schemas (Summary)

| Schema | Key Fields | Used By |
|--------|-----------|---------|
| **CommandToOutcomeCard** | `id`, `stage` (WATCH/EXPLAIN/OFFER), `lines.{what,why,next}` (80 char max each), `confidence`, `question_chips[]` | Card rendering in SKILL.md |
| **ConfidenceLabel** | `level` (HIGH/MED/LOW/UNK), `score` (0-1), `freshness_bucket` (LIVE/WARM/STALE), `provenance[]` | Attached to every card |
| **QuestionChip** | `shortcut_number` (1-4), `prompt`, `kind` (clarify/why/how/what_if/safety) | Numbered menu after cards |
| **GlossaryTerm** | `term`, `definition_beginner`, `aliases[]`, `times_seen`, `graduated` (bool) | Jargon firewall lookups |
| **JargonAnnotation** | `term_id`, `surface`, `action` (blocked/replaced_with_gloss/allowed_plain) | Firewall audit trail |
| **UserProfile** | `language_level`, `narration`, `chips_enabled`, `glossary{}`, `panic_count`, `sessions_count` | Persisted user state |

## Error Handling

| Failure | Detection | Response |
|---------|-----------|----------|
| tmux not installed | `sidecar.sh` preflight: `command -v tmux` | Print install instructions + offer solo mode: `gh copilot --skill sidecar` |
| gh CLI missing | `sidecar.sh` preflight: `command -v gh` | Print install link, exit 1 |
| SKILL.md not found | `sidecar.sh` preflight: `[[ -f $SKILL_PATH ]]` | Print `gh copilot skill install sidecar` |
| No active session | SKILL.md startup: check `~/.copilot/session-state/*/inuse.*.lock` | Enter Demo Mode (not an error) |
| Pane capture fails | `tmux capture-pane` returns non-zero | Show "I can't see the main window right now" + retry in 5s |
| Stale data (>60s) | `freshness_ms` in `main.diff.json` | Badge 🔴 STALE + disclaimer: "Things may have changed" |
| user-profile.json corrupt | JSON parse fails | Rename to `.bak`, create fresh profile, re-run onboarding |
| Rapid event burst | >3 events in 10s | Buffer; show highest-importance card + "(+N more events)" |

## What NOT to Build

- **No Relay mode** — non-tech users must not send commands to the main session (P2 future)
- **No web UI** — this is terminal-only; no HTTP server, no browser
- **No database** — all state is flat JSON files; the SQL schema in §12 is a conceptual model only
- **No daemon process** — the skill runs inside `gh copilot`; no separate process to manage
- **No real-time IPC** — communication is via filesystem polling (capture files), not sockets
- **No auth/permissions** — single-user tool; no multi-user concerns
- **No telemetry backend** — metrics are local counters in `user-profile.json`
- **No custom diff library** — use line-by-line string comparison in the SKILL.md prompt logic
- **No stakeholder lenses in v1** — exec/PM/designer views are P2
- **No cross-session analytics** — learning progression tracking is P1/P2
