# Copilot Sidecar — Non-Technical Experience PRD v2.0

**Product Name:** Copilot Sidecar — Non-Technical Track  
**Author:** Gregg Cochran (synthesized by Hackathon #48 — 23 AI agents, 13 models)  
**Status:** Ready for Dark Factory Build  
**Version:** 2.0  
**Supersedes:** Original PRD sections: User Personas §4, FR-3A (all), FR-3.7–3.9, FR-7, First Launch Experience, Interaction Examples  

---

## The Fundamental Reframe

**FROM:** "CLI learning tool for non-technical users"  
**TO:** "Developer understanding experience that bridges the technical/non-technical divide"

Non-technical users don't want to become developers. They want to **understand what developers do** so they can collaborate more effectively — evaluate technical proposals, ask better questions, recognize when "almost done" means three weeks of debugging.

The sidecar becomes a **cultural translator** between two professional languages.

---

## Design Mandate: The Asymmetric Default Problem

> *"The cost of defaulting wrong is ASYMMETRIC — tech users opt up in 30 seconds; non-tech users who hit dev defaults abandon PERMANENTLY."*

**The rule this upgrade enforces:**

Every design decision defaults to the non-technical track. Technical users unlock depth. Non-technical users never have to ask for simplification — it's already there.

- A developer who sees "checking what changed in the code" wastes 2 seconds and moves on.
- A non-technical user who sees `git diff --staged` panics and closes the terminal forever.

**Implementation:** Ship two experiences, not seven modes.

| Experience | Default? | Who | What changes |
|------------|----------|-----|--------------|
| **Guided Mode** | ✅ YES | Non-technical users, beginners, anyone | Narration ON, Question Chips ON, Jargon Firewall ON, Demo Mode available |
| **Expert Mode** | No | Developers who want less friction | Narration OFF, Chips collapsed, raw output, Relay available |

Switching: type `expert` or `I'm a developer` → toggle flips. Type `beginner` or `simple` → toggle back. Persisted in `~/.copilot/sidecar/user-profile.json`.

---

## §1 — Three Experiences, Not Seven Modes

The original PRD defines 7 modes: Observer, Tutor, Scout, Advisor, Relay, Narration, and configurable language levels. For non-technical users, this collapses to **three experiences** with automatic routing:

| Experience | User sees | Under the hood |
|------------|-----------|----------------|
| **👀 Watch** | Narrated play-by-play of main session | Observer + Narration, pane-capture diffing |
| **💬 Ask** | Answer to any question, jargon-free | Tutor + Scout (explore agents), Jargon Firewall |
| **💡 Suggest** | "Hey, I noticed…" cards | Advisor mode, throttled, Consequence Preview |

**Relay is REMOVED from the non-technical v1.** Non-technical users should not send commands to the main session. If they graduate to intermediate, Relay surfaces as a Phase 2 unlock.

---

## §2 — First-Launch Experience

### 2.1 Preflight System

Before opening any panes, `sidecar.sh` runs a silent preflight. This is the single most important non-technical UX fix (flagged by 12 of 13 models in Round 1). tmux failure must be intercepted before a non-technical user sees a cryptic error.

**File:** `sidecar.sh`

```bash
#!/usr/bin/env bash
# sidecar.sh — Copilot Sidecar launcher with preflight
# Install to: /usr/local/bin/sidecar (or ~/bin/sidecar)

SIDECAR_DIR="$HOME/.copilot/sidecar"
SKILL_PATH="$HOME/.copilot/skills/sidecar/SKILL.md"
SESSION_NAME="copilot-sidecar"
LOG_FILE="$SIDECAR_DIR/launcher.log"

mkdir -p "$SIDECAR_DIR"

# ─── PREFLIGHT ──────────────────────────────────────────────
preflight_pass=true
preflight_errors=()

echo "🔍 Checking your setup..."

# Check 1: tmux available
if ! command -v tmux &>/dev/null; then
  preflight_pass=false
  preflight_errors+=("tmux_missing")
fi

# Check 2: gh CLI available
if ! command -v gh &>/dev/null; then
  preflight_pass=false
  preflight_errors+=("gh_missing")
fi

# Check 3: Skill file installed
if [[ ! -f "$SKILL_PATH" ]]; then
  preflight_pass=false
  preflight_errors+=("skill_missing")
fi

# Check 4: Already in tmux?
already_in_tmux=false
[[ -n "$TMUX" ]] && already_in_tmux=true

# ─── PREFLIGHT FAILED ──────────────────────────────────────
if [[ "$preflight_pass" == "false" ]]; then
  echo ""
  echo "┌─────────────────────────────────────────────────────────┐"
  echo "│  ⚠️  Sidecar needs a quick one-time setup               │"
  echo "└─────────────────────────────────────────────────────────┘"
  echo ""

  for err in "${preflight_errors[@]}"; do
    case "$err" in
      tmux_missing)
        echo "  📦 tmux not found (splits your screen into two panels)."
        echo "     On Mac:    brew install tmux"
        echo "     On Ubuntu: sudo apt install tmux"
        echo "" ;;
      gh_missing)
        echo "  📦 GitHub CLI (gh) not found."
        echo "     Install: https://cli.github.com"
        echo "" ;;
      skill_missing)
        echo "  📦 Sidecar skill not installed."
        echo "     Run: gh copilot skill install sidecar"
        echo "" ;;
    esac
  done

  echo "  After fixing the above, run 'sidecar' again."
  echo ""
  echo "  ──────────────────────────────────────────────────────"
  echo "  🟢 Can't fix right now? You can still use Sidecar in"
  echo "     solo mode — no split screen needed:"
  echo ""
  echo "     gh copilot --skill sidecar"
  echo "  ──────────────────────────────────────────────────────"

  echo "{\"ts\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",\"event\":\"preflight_failed\",\"errors\":[\"${preflight_errors[*]}\"]}" >> "$LOG_FILE"
  exit 1
fi

# ─── LAUNCH ─────────────────────────────────────────────────
echo "✅ All checks passed."

cat > "$SIDECAR_DIR/session-link.json" <<EOF
{"cwd":"$(pwd)","started_at":"$(date -u +%Y-%m-%dT%H:%M:%SZ)","launcher_pid":$$,"mode":"split"}
EOF

if [[ "$already_in_tmux" == "true" ]]; then
  tmux split-window -h -p 35 "gh copilot --skill sidecar"
  tmux select-pane -L
  exit 0
fi

if tmux has-session -t "$SESSION_NAME" 2>/dev/null; then
  echo "🔄 Reconnecting to your Sidecar session..."
  tmux attach-session -t "$SESSION_NAME"
  exit 0
fi

tmux new-session -d -s "$SESSION_NAME" -x "$(tput cols)" -y "$(tput lines)"
tmux split-window -h -p 35 -t "$SESSION_NAME:0" "gh copilot --skill sidecar"
tmux select-pane -t "$SESSION_NAME:0.0"
tmux attach-session -t "$SESSION_NAME"
```

### 2.2 Four-Path Detection Matrix

On launch, the sidecar checks two things before showing any UI:

```
CHECK 1: Active session?   → ls ~/.copilot/session-state/*/inuse.*.lock → check PIDs
CHECK 2: User profile?     → stat ~/.copilot/sidecar/user-profile.json
```

| Session? | Profile? | Launch path |
|----------|----------|-------------|
| ✅ Found | ✅ Exists | **Resume** — skip onboarding, show status card |
| ✅ Found | ❌ First time | **Guided Onboarding** — 90-second script (§3) |
| ❌ None | ✅ Exists | **Demo Mode** — narrated replay (§6) |
| ❌ None | ❌ First time | **Demo Mode + Onboarding** — demo first, then prompt |

### 2.3 First-Time, Active Session Found

```
┌──────────────────────────────────────────────────────────────┐
│                                                              │
│   👋  Hi! I'm your Copilot companion.                       │
│                                                              │
│   I can see someone's working in the main terminal.          │
│   Let me show you what they're doing — in plain English.     │
│                                                              │
│     👀  Watch  — I'll narrate what's happening               │
│     💬  Ask    — Ask me anything, I'll never interrupt them  │
│     💡  Suggest — I'll point out interesting things          │
│                                                              │
│   Let's start by watching. Here's what's happening now...    │
└──────────────────────────────────────────────────────────────┘
```

### 2.4 First-Time, No Active Session

```
┌──────────────────────────────────────────────────────────────┐
│                                                              │
│   👋  Hi! I'm your Copilot companion.                       │
│                                                              │
│   No one's working in the main terminal right now,           │
│   so let me show you what this looks like when they are.     │
│                                                              │
│   ▶  Press Enter to start the demo                           │
│   ⏭  Type "skip" if you've seen this before                 │
└──────────────────────────────────────────────────────────────┘
```

### 2.5 Returning User, Active Session

```
┌─ 🔭 SIDECAR ────────────────────────────────────────────────┐
│  📋 Task: Building auth module                               │
│  ⏱  Running for: 4m 22s                                     │
│  📝 Last change: src/auth/middleware.ts (35s ago)            │
│  ✅ 5/8 todos done                                           │
│                                                              │
│  👀 Watch  ·  💬 Ask  ·  💡 Suggest                          │
└──────────────────────────────────────────────────────────────┘
```

---

## §3 — 90-Second Guided Onboarding

When `~/.copilot/sidecar/user-profile.json` does not exist, run this sequence. NOT a wall of text — a conversational 90-second flow.

**Step 1 — One question:**
```
╔══════════════════════════════════════════════════════════════╗
║  👋  Hi! I'm your Copilot Sidecar.                          ║
║                                                              ║
║  I live in this side panel so I never interrupt what's       ║
║  happening in the main window.                               ║
║                                                              ║
║  I have one job: make the terminal less mysterious.          ║
╚══════════════════════════════════════════════════════════════╝

  [3 second pause]

Let me ask one question to get started:

  1️⃣  I'm new to this — explain everything simply
  2️⃣  I know some basics — just flag unusual things
  3️⃣  I'm a developer — skip the hand-holding

  Type 1, 2, or 3:
```

**On input "1" (beginner):**
```
Perfect. I'll explain everything in plain language.
No jargon without a definition. Promise.

You can ask me anything, anytime. Some things to try:
  safe?     — tells you if anything risky is happening
  what?     — explains the last thing that happened
  chips     — shows a menu of things you can ask

One more thing: you cannot break anything by talking to me.
I'm read-only. I watch. I explain. I don't touch.

Ready? I'll speak up when I see something interesting.
```

**On input "2" (intermediate):**
```
Got it — I'll assume you know the basics but flag anything unusual.
Type 'beginner' anytime for plain language. Type 'expert' to go full technical.
```

**On input "3" (expert):**
```
Developer mode. Technical terminology, no analogies.
Type 'narrate on' for live command narration. Type 'beginner' to reset.
```

**After any selection — write profile:**
```json
{
  "version": 1,
  "language_level": "beginner",
  "onboarding_complete": true,
  "onboarding_completed_at": "2026-03-22T01:30:00Z",
  "narration": true,
  "chips_enabled": true,
  "sessions_count": 0,
  "glossary": {},
  "concepts_learned": [],
  "panic_count": 0,
  "role": null
}
```
**File path:** `~/.copilot/sidecar/user-profile.json`

---

## §4 — Guided Companion Loop: Watch → Explain → Offer

The core interaction pattern. One predictable loop that creates trust.

### 4.1 The Loop

```
┌─────────────────────────────────────────────────────┐
│  👀 WATCH — Narrate what happened                    │
│       ↓                                              │
│  💬 EXPLAIN — Answer questions about it              │
│       ↓                                              │
│  💡 OFFER — Suggest what to explore next             │
│       ↓                                              │
│  (loop back to Watch)                                │
└─────────────────────────────────────────────────────┘
```

### 4.2 Watch Phase — Command-to-Outcome Cards

Every observed command is displayed as a **3-line card**:

```
┌─ [emoji] CATEGORY ───────────────────────────────────┐
│  [What just happened — plain English, one sentence]   │
│  [Why it matters — one sentence]                      │
│  [What comes next — one sentence]                     │
└──────────────────────────────────────────────────────┘
```

**Examples:**
```
┌─ 🔍 CODE CHECK ─────────────────────────────────────┐
│  The main session compared the current code to the   │
│  last saved version to see what changed.             │
│  This helps catch mistakes before they're permanent. │
└──────────────────────────────────────────────────────┘

┌─ 🧪 QUALITY CHECK ──────────────────────────────────┐
│  Running 47 automated checks to make sure the code   │
│  works correctly. Like a spell-checker, but for      │
│  logic. 3 checks failed — will fix those next.       │
└──────────────────────────────────────────────────────┘

┌─ 💾 SAVING PROGRESS ────────────────────────────────┐
│  The main session saved a checkpoint — like hitting  │
│  'Save' on a document, but it remembers every        │
│  previous version too. 247 saves exist so far.       │
└──────────────────────────────────────────────────────┘
```

**Card lookup table** — stored at `~/.copilot/sidecar/narration-cards.json`:

```json
{
  "cards": [
    {"pattern": "^git diff", "emoji": "🔍", "title": "CODE CHECK",
     "what": "Compared the current code to the last saved version.",
     "why": "Helps catch mistakes before they're permanent.",
     "next": "Will probably save these changes next."},
    {"pattern": "^git commit", "emoji": "💾", "title": "SAVING PROGRESS",
     "what": "Saved a checkpoint — like hitting 'Save' but it remembers every version.",
     "why": "If anything breaks later, we can go back to this exact point.",
     "next": "The code is now safely saved."},
    {"pattern": "^npm test|^jest|^pytest|^go test", "emoji": "🧪", "title": "QUALITY CHECK",
     "what": "Running automated checks to make sure the code works correctly.",
     "why": "Like a spell-checker but for logic — catches bugs before users do.",
     "next": "Results coming shortly."},
    {"pattern": "^npm install|^pip install|^yarn add|^brew install", "emoji": "📦", "title": "INSTALLING TOOLS",
     "what": "Downloading helper code that other people already wrote.",
     "why": "Saves time — no need to reinvent the wheel.",
     "next": "Usually takes 30–60 seconds."},
    {"pattern": "^npm run build|^make|^cargo build|^go build", "emoji": "🏗️", "title": "BUILDING",
     "what": "Converting human-readable code into something the computer can run.",
     "why": "Like compiling a recipe into an actual meal.",
     "next": "If it succeeds, the code is ready to run."},
    {"pattern": "^git push", "emoji": "🚀", "title": "SHARING CODE",
     "what": "Sending the saved code to a shared server so the team can see it.",
     "why": "Like uploading a document to a shared drive.",
     "next": "The team can now review these changes."},
    {"pattern": "^git checkout|^git switch", "emoji": "🔀", "title": "SWITCHING VERSIONS",
     "what": "Jumping to a different version of the code.",
     "why": "Like opening a different draft of a document.",
     "next": "Now working on a different set of changes."},
    {"pattern": "^git status", "emoji": "📋", "title": "PROGRESS CHECK",
     "what": "Asking 'what files have I changed so far?'",
     "why": "A quick inventory before deciding what to do next.",
     "next": "Usually followed by saving or reviewing changes."},
    {"pattern": "^curl|^wget", "emoji": "🌐", "title": "TALKING TO A SERVER",
     "what": "Sending a request to another computer over the internet.",
     "why": "Checking if an online service is working, or getting data.",
     "next": "Waiting for a response."},
    {"pattern": "^rm |^del ", "emoji": "🗑️", "title": "REMOVING FILES",
     "what": "Deleting files that are no longer needed.",
     "why": "Cleaning up — like throwing away rough drafts.",
     "next": "These files are gone, but saved versions still exist."}
  ],
  "fallback": {
    "emoji": "⚙️", "title": "WORKING",
    "what": "The main session ran a command.",
    "why": "Part of the current task.",
    "next": "Watching for the result."
  }
}
```

### 4.3 Confidence + Freshness Badges

Every status answer carries badges so users know how current the information is:

| Badge | Meaning | Threshold |
|-------|---------|-----------|
| 🟢 `LIVE` | Observed in the last 10 seconds | ≤10s |
| 🟡 `RECENT` | Observed 11–60 seconds ago | 11–60s |
| 🔴 `STALE` | More than 60 seconds old | >60s |

**Display format:**
```
🟢 LIVE · 3s ago · Source: screen capture
```

When stale, always say so: *"This is what I saw 45 seconds ago — things may have changed."*

### 4.4 Narration Throttle Rules

| Condition | Behavior |
|-----------|----------|
| Rapid burst (>3 events in 10s) | Buffer, show most important card + "(+2 more events)" |
| Normal pace | 1 card per event, max 1 per 10 seconds |
| Idle (>60s no events) | Show "What Should I Ask?" chips |
| Long silence (>5min) | Show "Still watching. Nothing new has happened." |

---

## §5 — Panic Button: `safe?`

Typing `safe?` at ANY time produces an immediate safety status card. No delay, no research — instant reassurance.

### 5.1 Safety States

**🟢 ALL CLEAR:**
```
┌─ 🛡️ SAFETY CHECK ───────────────────────────────────┐
│                                                      │
│  ✅ Your files are safe — nothing has been deleted    │
│  ✅ All changes can be undone (247 saved versions)    │
│  ✅ The main session is working normally              │
│  ✅ No errors detected                               │
│                                                      │
│  🕐 Last checked: 3 seconds ago                      │
│  Remember: I never change files. I only watch.       │
└──────────────────────────────────────────────────────┘
```

**🟡 MINOR CONCERN:**
```
┌─ 🛡️ SAFETY CHECK ───────────────────────────────────┐
│                                                      │
│  ⚠️ 3 quality checks failed — this is normal during  │
│     development. The main session will fix them.     │
│  ✅ No files were deleted                            │
│  ✅ All changes can be undone                        │
│                                                      │
│  This is like a spell-checker finding typos — not    │
│  an emergency, just things to clean up.              │
└──────────────────────────────────────────────────────┘
```

**🔴 ATTENTION NEEDED:**
```
┌─ 🛡️ SAFETY CHECK ───────────────────────────────────┐
│                                                      │
│  🔴 The main session hit an error and may be stuck   │
│  ✅ Your files are still safe                        │
│  ✅ All changes can be undone                        │
│                                                      │
│  The developer should take a look. This isn't        │
│  something you caused or need to fix.                │
│                                                      │
│  Want me to explain what went wrong?                 │
│  [1] Yes, explain it simply                          │
│  [2] No, I'll wait for the developer                 │
└──────────────────────────────────────────────────────┘
```

---

## §6 — Demo Mode

When no active Copilot session is found, the sidecar enters Demo Mode automatically instead of showing a dead end.

### 6.1 Demo Menu

```
╔══════════════════════════════════════════════════════════════╗
║  🎬  DEMO MODE — Nothing's running yet. That's fine!        ║
╚══════════════════════════════════════════════════════════════╝

What would you like to do?

  1️⃣  Show me a replay of what AI work looks like
  2️⃣  Explain what this tool does in plain language
  3️⃣  I just started something — check again
  4️⃣  Ask me anything

  Type a number, or just ask a question:
```

### 6.2 Pre-Recorded Demos

**File structure:** `~/.copilot/sidecar/demos/`
```
demos/
├── index.json
├── 01-checking-code.jsonl
├── 02-running-tests.jsonl
└── 03-ai-agents.jsonl
```

**Demo manifest** (`index.json`):
```json
{
  "demos": [
    {"id": "01", "title": "Checking the Code", "file": "01-checking-code.jsonl", "duration_s": 30, "teaches": "git status, git diff"},
    {"id": "02", "title": "Running Quality Checks", "file": "02-running-tests.jsonl", "duration_s": 30, "teaches": "npm test, test failures"},
    {"id": "03", "title": "AI Helpers Working Together", "file": "03-ai-agents.jsonl", "duration_s": 30, "teaches": "sub-agents, explore"}
  ]
}
```

**Demo event format** (JSONL):
```json
{"type": "command", "text": "git status", "delay_ms": 1000}
{"type": "output", "text": "On branch main\nChanges not staged:\n  modified: src/auth/login.ts", "delay_ms": 500}
{"type": "narration", "text": "That command — 'git status' — is like asking 'what files have I changed?' The answer shows 1 file was edited: login.ts handles user login.", "delay_ms": 3000}
{"type": "prompt", "text": "Press Enter to continue, or ask a question..."}
```

### 6.3 Session Re-Detection

Every 30 seconds during Demo Mode, silently re-check for active sessions. If one appears:
```
🔭 A live session just started! Want me to switch from
   the demo to watching real work?
   [1] Yes, switch to live   [2] No, finish the demo
```

---

## §7 — Question Chips: "What Should I Ask?"

The biggest barrier for non-technical users isn't fear — it's **not knowing what questions to ask**.

### 7.1 Chip Display

After any significant event, OR when the user has been idle >60 seconds:

```
💬 Not sure what to ask? Try one of these:

  [1] What is the main session working on right now?
  [2] What does src/auth/middleware.ts do?
  [3] Why did that last command run?
  [4] Is anything broken?

  Type a number, or ask your own question.
```

### 7.2 Chip Generation Rules

1. Chip [1] is always a status question
2. Chip [2] references the most recently changed file, by name
3. Chip [3] references the last narrated command
4. Chip [4] is always a safety/health check
5. Chips refresh every 90 seconds while idle
6. Chips disappear when user types anything
7. Type `chips` to re-display current chips

### 7.3 Event-Specific Question Templates

```json
{
  "test_failure": [
    "What do these test failures mean?",
    "Is this a real problem or just a minor issue?",
    "What would fixing this involve?"
  ],
  "build_error": [
    "What's broken and why?",
    "How serious is this error?",
    "Can I still use the app while this is broken?"
  ],
  "file_created": [
    "What is {filename} for?",
    "How does this file connect to the rest?",
    "Is this file important or just temporary?"
  ],
  "git_commit": [
    "What changes were just saved?",
    "Can these changes be undone later?",
    "Who will see this commit?"
  ],
  "long_silence": [
    "Is something still running or is it stuck?",
    "Should I be worried about this silence?",
    "What's the overall progress?"
  ]
}
```

**File path:** `~/.copilot/sidecar/question-templates.json`

### 7.4 Freshness Badges on Chips

| Badge | Meaning |
|-------|---------|
| 🟢 **NOW** | About something from the last 30 seconds |
| 🟡 **RECENT** | About something from 30s–2min ago |
| ⚪ **CONTEXT** | General question about the project |

---

## §8 — Jargon Firewall

Blocks unexplained technical terms from leaking into beginner UX.

### 8.1 Firewall Algorithm

The firewall is applied as a **post-processing step** on every response in beginner mode:

```
FIREWALL ALGORITHM (applied before displaying any response):

1. Scan response text for terms matching jargon dictionary keys
   (case-insensitive, whole-word match: \bTERM\b)
   Also match aliases (e.g., "DB" → "database", "prod" → "production")

2. For each matching term:
   a. Check user-profile.json glossary — if graduated (count ≥ 5): skip
   b. If seen 1-4 times: brief inline gloss:
      {term} (= {short definition})
   c. If first use AND story_eligible: full explanation with analogy:
      {term} ❓(= {definition}. Think of it like {analogy}.)

3. After response:
   a. Increment term count in user-profile.json
   b. Write profile file atomically (temp → rename)

EXAMPLE BEFORE FIREWALL:
"The main session just ran git push to deploy the changes to the repository."

EXAMPLE AFTER FIREWALL (first use of these terms):
"The main session just ran git push ❓(= sending local changes to a shared
server — like emailing a document to the team) to deploy ❓(= making the
code live for real users) the changes to the repository ❓(= a project
folder with its complete version history)."

TERM GRADUATION:
- After a term has been explained 5+ times, it "graduates"
- Graduated terms are used naturally without explanation
- User can always type "what does X mean again?" for a refresher
```

### 8.2 Core Dictionary (40+ terms)

```json
{
  "git": "a tool that saves versions of code",
  "commit": "saving a checkpoint of your work",
  "branch": "a separate copy of the code for trying things",
  "merge": "combining two versions of the code together",
  "diff": "a comparison showing what changed",
  "repo": "a project folder tracked by git",
  "clone": "downloading a copy of a project",
  "push": "uploading your saved code to a shared server",
  "pull": "downloading the latest changes from the team",
  "PR": "a request to add your changes to the shared code",
  "npm": "a tool that downloads helper code for JavaScript",
  "pip": "a tool that downloads helper code for Python",
  "build": "converting code into something the computer can run",
  "deploy": "putting code onto a server where users can reach it",
  "CI/CD": "automatic quality checks that run when code changes",
  "API": "a menu of things one program can ask another to do",
  "endpoint": "a specific address where a program accepts requests",
  "middleware": "code that runs between a request and a response",
  "database": "where the app stores its information permanently",
  "query": "a question asked to a database",
  "schema": "the structure of a database — like column headers",
  "migration": "changing the structure of a database safely",
  "JWT": "a digital ID badge that proves you're logged in",
  "auth": "short for authentication — proving who you are",
  "token": "a temporary digital pass",
  "env": "settings that change between development and production",
  "production": "the live version that real users see",
  "staging": "a test version that mimics production",
  "localhost": "your own computer acting as a server",
  "port": "a numbered door on your computer for network traffic",
  "dependency": "helper code your project needs to work",
  "refactor": "reorganizing code without changing what it does",
  "lint": "automatic style and error checking for code",
  "test": "an automated check that code works correctly",
  "mock": "a fake version of something used during testing",
  "Docker": "a tool that packages code with everything it needs to run",
  "container": "a lightweight, isolated environment for running code",
  "CLI": "a text-based interface — type commands instead of clicking",
  "terminal": "the app where you type CLI commands",
  "stderr": "where error messages appear",
  "stdout": "where normal output appears"
}
```

**File path:** `~/.copilot/sidecar/jargon-dictionary.json`

### 8.3 Firewall Rules by Language Level

For **beginner** users:
1. **Unknown terms** (not in dictionary): Block from proactive content. Replace with generic phrase.
2. **Known but unlearned terms** (seen 1-4 times): Allow once per card, followed by inline definition: `running tests (automated checks that your code still works)`
3. **Graduated terms** (seen 5+ times): Allow without gloss.

For **intermediate** users: Allow terms but include first-mention gloss per session.

For **expert** users: Firewall disabled (still logs encounters for glossary).

### 8.4 Glossary-to-Story Memory

Instead of a static glossary, persist terms as **personal story cards** grounded in the user's actual sessions:

```json
{
  "commit": {
    "plain": "saving a checkpoint of your work",
    "story": "Remember when the main session finished the auth fix and saved it? That was a commit — a save point you can always go back to.",
    "first_seen": "2026-03-21T19:30:00Z",
    "times_seen": 4,
    "graduated": false,
    "session_id": "abc-123"
  }
}
```

**Story card creation trigger:**
```
When the sidecar explains a story_eligible term during a live session:
1. Save a Story Card linking the term to this specific moment
2. In future sessions, when the term comes up again, reference the story:
   "The main session just made a commit — a save point, like the one
    from yesterday when it fixed the login page."
3. After 5+ references, the term graduates to natural usage — no story needed
```

**Glossary access commands:**
- `glossary` → show all learned terms organized by mastery level
- `what does X mean again?` → look up specific term with story context
- `teach me about X` → enter "Teach Someone Else" mode for that term

**Glossary display format:**
```
╭──────────────────────────────────────────────────────────────────╮
│  📖 YOUR GLOSSARY                                   (12 terms)   │
╰──────────────────────────────────────────────────────────────────╯

🟢 COMFORTABLE (you've explained these)
───────────────────────────────────────
• git commit — saving a version of your work
• npm test — running quality checks
• api — a way for programs to talk to each other

🟡 LEARNING (seen multiple times)
───────────────────────────────────────
• jwt — a digital pass that proves you're logged in
• middleware — a security checkpoint for requests

⚪ NEW (just encountered)
───────────────────────────────────────
• refactor — reorganizing code without changing what it does

Type a term to see its full explanation, or "teach [term]" to
practice explaining it yourself!
```

---

## §9 — Story Mode: Narrative Templates

For high-impact events, the sidecar tells a **story** instead of just translating a command.

### 9.1 The Safety Net Story
**Trigger:** `git commit` observed
```
📚 The developer just created a "checkpoint" — imagine saving
a game before a difficult boss fight. If the next changes break
something, they can instantly restore to this exact moment.

This project now has 247 saved checkpoints.
```

### 9.2 The Detective Story
**Trigger:** Build/test failure detected
```
🔍 Something broke. The build system checks 1,247 things before
saying "this is safe to ship." Right now it's stuck on test #89:
"Make sure login still works after password reset."

The detective work begins — was it the code they just changed,
or did they accidentally break something else?
```

### 9.3 The Architecture Story
**Trigger:** User asks "What does this codebase do?"
```
🏗️ Think of this codebase as a small city:
• The Frontend (storefronts) — what users see and click
• The API (phone lines) — how different parts talk
• The Database (city records) — where everything is stored
• Authentication (security guards) — who's allowed where

The developer is working in the Authentication district right now.
```

---

## §10 — Stakeholder Lenses

Non-technical users have different professional contexts. The sidecar adapts.

### 10.1 Available Lenses

| Lens | Activate with | Focus |
|------|---------------|-------|
| 👔 Executive | `exec view` | Risk, timeline, cost, business impact |
| 📊 Product Manager | `pm view` | User impact, scope, feature complexity |
| 🎨 Designer | `design view` | User journey, interface changes, accessibility |
| 📈 Analyst | `data view` | Metrics, data flows, measurement opportunities |

### 10.2 Example — Executive Lens

```
👔 EXECUTIVE TRANSLATION

Current Status: Day 3 of 7-day sprint
Risk Level: YELLOW — on track but tight timeline
Business Impact: Authentication work unlocks 3 customer requests
If this slips: 2-week delay on customer delivery
```

### 10.3 Auto-Detection

If the user asks questions about timelines, costs, or risk → suggest Executive lens.
If they ask about users, features, or scope → suggest PM lens.
Never force — always offer: *"I can translate this for your role. Want the PM view?"*

---

## §11 — "Teach Someone Else" Learning Validation

Learning research shows explaining to someone else is the most effective way to solidify understanding. The sidecar inverts the tutoring relationship.

### 11.1 Activation

After the user has seen 5+ concepts explained:
```
🎓 You've learned about commits, tests, and builds.
   Want to test your understanding? Try explaining one
   of them back to me — I'll tell you how you did!

   Type: teach me about [concept]
```

### 11.2 Feedback Loop

User explains → sidecar evaluates:
- ✅ **Nailed it:** "That's exactly right! You could explain this to a coworker."
- 🟡 **Mostly right:** "Good foundation! One thing to add: [clarification]"
- 🔄 **Needs work:** "Not quite — here's a simpler way to think about it: [re-explanation]"

Tracks mastery in `user-profile.json` → `concepts_learned` array.

---

## §12 — Curiosity-Driven Learning Engine

Tracks concepts across sessions and progressively deepens explanations.

### 11A.1 Concept Tracking

```sql
CREATE TABLE user_concepts (
    concept_id TEXT PRIMARY KEY,
    concept_name TEXT,           -- 'git', 'API', 'database', 'testing'
    first_encountered TEXT,
    times_explained INTEGER DEFAULT 0,
    current_depth TEXT DEFAULT 'surface',  -- 'surface'|'functional'|'architectural'
    user_questions INTEGER DEFAULT 0,
    confidence_score INTEGER DEFAULT 1,    -- 1-10
    related_concepts TEXT        -- JSON array
);
```

### 11A.2 Progressive Revelation

```
Session 1:  "Git is like saving versions of a document"         (surface)
Session 5:  "Git is a collaborative editing system with history" (functional)
Session 15: "Git is distributed version control with branching"  (architectural)
```

**Depth selection algorithm:**
```
encounters = 0          → use metaphor (surface)
encounters < 3          → use functional description
encounters ≥ 3 AND confidence > 7 → use architectural language
otherwise               → stay at functional (safe default)
```

### 11A.3 Curiosity Breadcrumbs

When explaining concept A, drop hints about related concept B:
```
"The developer just committed to git — that's like saving a checkpoint.
In a few minutes, you might see them 'push' to something called a
'remote repository' — that's like backing up the checkpoint to the cloud."
```

### 11A.4 Learning Path Suggestions

After 5+ concepts learned:
```
🧭 YOUR LEARNING JOURNEY

You've now seen: Git commits (3x), Build systems (1x), Testing (2x)

Ready to explore next:
• "What's a pull request?" (connects to git commits)
• "How do tests prevent bugs?" (connects to testing)
• "What happens when code gets deployed?" (new frontier)

Or ask anything - I'm here to connect the dots.
```

---

## §13 — Consequence Preview

Before any action the sidecar takes (spawning research, showing technical details), show an impact panel:

```
┌─ ⚡ WHAT I'M ABOUT TO DO ────────────────────────────┐
│                                                       │
│  Action: Look through the project files to find       │
│          how the login system works                    │
│  Will change: Nothing — this is read-only             │
│  Time: About 10–15 seconds                            │
│  Risk: None                                           │
│                                                       │
│  [1] Go ahead   [2] Skip                              │
└───────────────────────────────────────────────────────┘
```

### 13.1 Risk Classification Table

```
RISK LEVELS:
  🟢 None    — read-only, checkpoint save, display-only
  🟡 Low     — new file creation, config change, test run
  🟠 Medium  — file modification, dependency install, git push
  🔴 High    — file deletion, database change, production deploy

CLASSIFICATION RULES:
  git add, git commit, git stash       → 🟢 None
  git push, git merge                  → 🟠 Medium
  npm install, pip install             → 🟡 Low
  npm test, pytest                     → 🟢 None
  rm, del, DROP TABLE                  → 🔴 High
  echo, cat, ls, pwd, git status      → 🟢 None
  touch, mkdir, cp                     → 🟡 Low
  chmod, chown                         → 🟠 Medium
  curl -X POST, curl -X DELETE         → 🟠 Medium
  deploy, publish                      → 🔴 High
```

### 13.2 Consequence Preview for Narrated Actions

When narrating a main session action with risk ≥ 🟡, prepend:
```
┌─ 🔮 WHAT THIS MEANS ────────────────────────────────┐
│  Action:   Sending saved code to the shared server   │
│  Changes:  7 files will become visible to the team   │
│  Risk:     🟠 Medium — others can see this now       │
│  Undo:     Can be reversed by deploying previous ver │
└──────────────────────────────────────────────────────┘
```

---

## §14 — Pane-Capture Narration Architecture

### 14.1 Capture System

```bash
# Capture last 2000 lines of main pane (clean text, no ANSI)
tmux capture-pane -t "$MAIN_PANE_ID" -p -S -2000 -E -1
```

**Storage:**
- `~/.copilot/sidecar/runtime/pane-capture/main.prev.txt`
- `~/.copilot/sidecar/runtime/pane-capture/main.curr.txt`
- `~/.copilot/sidecar/runtime/pane-capture/main.diff.json`
- `~/.copilot/sidecar/runtime/pane-capture/main.pane.json` (metadata)
- `~/.copilot/sidecar/runtime/pane-capture/screen-map.json` (for "Explain This Line")

**Pane metadata** (`main.pane.json`):
```json
{
  "tmux_session": "copilot-sidecar",
  "tmux_window": "0",
  "main_pane_id": "%12",
  "sidecar_pane_id": "%13",
  "attached_at": "2026-03-22T01:23:45Z",
  "cwd_hint": "/Users/greggcochran/project",
  "capture_lines": 2000
}
```

### 14.2 Diff Algorithm

1. **Fast path:** Detect appended lines (compare suffix boundaries — terminal output is mostly append-only)
2. **Fallback:** Line-based Myers diff on last ~300 lines

**Output format** (`main.diff.json`):
```json
{
  "captured_at": "2026-03-22T01:23:47Z",
  "freshness_ms": 0,
  "diff_kind": "append",
  "new_lines": ["> npm test", "FAIL src/auth.test.ts"],
  "context_tail": ["(last 20 lines for rendering)"]
}
```

### 14.3 Event Inference from Diff

From new lines, infer events with confidence scoring:

**Heuristic rules:**

| Pattern | Event Type | Base Confidence |
|---------|-----------|-----------------|
| `^(\$\|>\|❯)\s+.+$` | `command_detected` | 0.8 |
| `FAIL`, `Error:`, `Traceback`, `panic:` | `tool_failed` | 0.8 |
| `diff --git`, `@@` | `git_diff_view` | 0.9 |
| `\d+\/\d+` (e.g., "5/47") | `progress_indicator` | 0.6 |
| No new lines for 60s | `idle_prompt` | 0.7 |

**Confidence modifiers:**
- +0.3 if strong signature (e.g., `diff --git`, `FAIL`)
- +0.2 if command line detected
- +0.15 if corroborated by events.jsonl (same 10s window, same keyword)
- −0.2 if only 1–2 ambiguous lines
- Clamp to [0.1, 1.0]

**Write inferred events as JSONL:**
```
~/.copilot/sidecar/feed/narration-events.jsonl
```

### 14.4 Narration Pipeline

```
Capture (2s) → Diff → Classify → Jargon Firewall → Card → Display
```

**Update frequencies (hard requirements):**
- tmux capture: **2s** while Watch active; backoff to **15s** after 60s of no diffs
- staleness warning: **10s** without capture while Watch active
- session discovery refresh: **60s**

### 14.5 Multi-Signal Fusion

Pane capture is primary, but narration accuracy increases when corroborated with:

1. **Session events** (`events.jsonl`) — poll every 5s, track byte offset
2. **Plan + checkpoints** — `plan.md` mtime every 15s, checkpoints every 30s
3. **Git status** — `git status --porcelain` every 15s

**Fusion rule:** When pane-inferred event matches events.jsonl (same 10s window, same keyword), boost confidence +0.15 and prefer the events.jsonl label.

### 14.6 "Explain This Line"

Users can reference screen content without knowing file names:

| Reference | How it works |
|-----------|-------------|
| `"Explain line 38"` | Lookup line 38 in `main.curr.txt` via `screen-map.json` |
| `"Explain the error"` | Search for error patterns in capture |
| `"What just appeared?"` | Use `main.diff.json` new_lines |
| `"Explain the part with FAIL"` | Substring search in `main.curr.txt` |

**Screen map format** (`screen-map.json`):
```json
{
  "captured_at": "2026-03-22T01:23:47Z",
  "main_pane_id": "%12",
  "lines": [
    {"n": 1, "text": "..."},
    {"n": 2, "text": "> npm test"}
  ]
}
```

### 14.7 Safety Banner

Sidecar pane MUST show a persistent header (re-printed every 30s and on every mode change):
```
SIDECAR (READ‑ONLY) — Watching main session safely • Watch | Ask | Suggest • Narration: ON
```

Label tmux panes if supported:
```bash
tmux select-pane -t "$MAIN_PANE_ID" -T "MAIN" 2>/dev/null || true
tmux select-pane -t "$SIDECAR_PANE_ID" -T "SIDECAR (READ-ONLY)" 2>/dev/null || true
```

---

## §15 — Session Discovery for Non-Technical Users

### 15.1 Human-Readable Names

Never show PIDs or paths. Derive project names:

```bash
project_name=$(basename "$(git -C "$cwd" rev-parse --show-toplevel 2>/dev/null || echo "$cwd")")
task_label=$(head -1 "$session_dir/plan.md" 2>/dev/null | sed 's/^#\s*//')
```

**Displayed chooser:**
```
Which project should I watch?
  [1] stampede-ui — "Fix sidebar rendering" (active 12s ago)
  [2] my-api — "Draft submission" (active 3m ago)
```

### 15.2 Fallback When No Session Found

Never show "no session found" as an error. Enter Demo Mode (§6) with a friendly message.

---

## §16 — Breakage Map

| Component | #1 Failure for Non-Tech Users | Fix |
|-----------|-------------------------------|-----|
| **Launcher** | tmux missing → cryptic error | Preflight (§2.1) with guided install + solo mode fallback |
| **Watch** | Stale narration feels wrong/haunted | Freshness badges (§4.3) + "Last checked Xs ago" on every card |
| **Ask** | Answers drift into jargon | Jargon Firewall (§8) + beginner default + "simpler please" command |
| **Suggest** | Unsolicited suggestions feel like nagging | Default OFF for beginners; passive badge instead of interruption |
| **Demo Mode** | User thinks it's broken because nothing's "real" | Clear "DEMO" label + 30s re-check for live sessions |
| **Session Discovery** | Multiple sessions → "which PID?" | Human-readable names (§14) + auto-select most recent |
| **Panic Button** | User panics but doesn't know `safe?` exists | Teach in onboarding + show on first error event |

---

## §17 — Non-Technical Success Metrics

### 17.1 Core Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| First-session retention | >70% complete onboarding | Profile creation rate |
| Return rate | >50% use it again within 7 days | Session count in user-profile |
| Question diversity | 3+ question types per session | Message classification |
| Comprehension growth | Users explain concepts back accurately after 5 sessions | "Teach Someone Else" scores |
| Panic button usage | Decreasing over sessions (trust building) | `panic_count` in profile |
| Glossary growth | 10+ terms learned per user per month | Glossary entries |
| Chip click-through | >40% of displayed chips get selected | Chip interaction logs |
| Safety perception | >90% report feeling "safe" using sidecar | Post-session feedback |
| Stakeholder lens adoption | >30% of non-tech users try a lens | Lens activation logs |
| Demo-to-live conversion | >60% of Demo Mode users return when a session is active | Session re-detection |

### 17.2 Learning Progression Metrics

| Stage | Indicator | Target |
|-------|-----------|--------|
| **Observer** | Only watches, asks <3 questions | First session |
| **Questioner** | Asks 3+ questions per session | By session 2 |
| **Explainer** | Successfully completes Teach Mode | By session 5 |
| **Confident** | Uses "expert mode" toggle | Optional, tracked |

### 17.3 Trust Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Perceived safety | >90% say "I felt safe" | Post-session survey |
| Narration accuracy | <5% report stale/wrong narration | Feedback button |
| Clarity score | >4/5 "I understood the explanations" | Post-session survey |

### 17.4 Anti-Metrics (What We Don't Optimize For)

| Anti-Metric | Why We Avoid It |
|-------------|-----------------|
| Total questions asked | Encourages noise over learning |
| Time spent in sidecar | Gaming attention, not outcomes |
| Features used | Vanity metric, not value |

---

## §18 — Data Model: JSON Schemas

### 18.1 CommandToOutcomeCard Schema

```json
{
  "type": "object",
  "required": ["id", "session_id", "event_id", "stage", "lines", "confidence", "question_chips"],
  "properties": {
    "id": {"type": "string"},
    "session_id": {"type": "string"},
    "event_id": {"type": "string"},
    "stage": {"type": "string", "enum": ["WATCH", "EXPLAIN", "OFFER"]},
    "lines": {
      "type": "object",
      "properties": {
        "what": {"type": "string", "maxLength": 80},
        "why": {"type": "string", "maxLength": 80},
        "next": {"type": "string", "maxLength": 80}
      }
    },
    "context": {
      "type": "object",
      "properties": {
        "trigger_type": {"type": "string"},
        "command": {"type": ["string", "null"]},
        "cwd": {"type": "string"},
        "timestamp": {"type": "string", "format": "date-time"},
        "importance_score": {"type": "number", "minimum": 0.0, "maximum": 1.0}
      }
    },
    "confidence": {"$ref": "#/definitions/ConfidenceLabel"},
    "question_chips": {"type": "array", "items": {"$ref": "#/definitions/QuestionChip"}},
    "jargon_annotations": {"type": "array", "items": {"$ref": "#/definitions/JargonAnnotation"}}
  }
}
```

### 18.2 ConfidenceLabel Schema

```json
{
  "type": "object",
  "required": ["level", "score", "freshness_seconds", "freshness_bucket", "provenance"],
  "properties": {
    "level": {"type": "string", "enum": ["HIGH", "MED", "LOW", "UNK"]},
    "score": {"type": "number", "minimum": 0.0, "maximum": 1.0},
    "freshness_seconds": {"type": "integer", "minimum": 0},
    "freshness_bucket": {"type": "string", "enum": ["LIVE", "WARM", "STALE"]},
    "provenance": {"type": "array", "items": {"type": "string"}},
    "evidence": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "source_type": {"type": "string"},
          "description": {"type": "string"},
          "file_path": {"type": ["string", "null"]}
        }
      }
    }
  }
}
```

### 18.3 QuestionChip Schema

```json
{
  "type": "object",
  "required": ["id", "label_short", "prompt", "kind", "shortcut_number"],
  "properties": {
    "id": {"type": "string"},
    "label_short": {"type": "string"},
    "prompt": {"type": "string"},
    "kind": {"type": "string", "enum": ["clarify", "why", "how", "what_if", "sandbox", "safety"]},
    "icon": {"type": "string"},
    "shortcut_number": {"type": "integer", "minimum": 1, "maximum": 4},
    "linked_card_id": {"type": ["string", "null"]}
  }
}
```

### 18.4 GlossaryTerm Schema

```json
{
  "type": "object",
  "required": ["id", "term", "definition_beginner", "aliases", "learned_level"],
  "properties": {
    "id": {"type": "string"},
    "term": {"type": "string"},
    "definition_beginner": {"type": "string"},
    "definition_intermediate": {"type": "string"},
    "definition_technical": {"type": "string"},
    "aliases": {"type": "array", "items": {"type": "string"}},
    "story": {"type": ["string", "null"]},
    "learned_level": {"type": "string", "enum": ["none", "beginner", "intermediate", "technical"]},
    "times_seen": {"type": "integer", "default": 0},
    "graduated": {"type": "boolean", "default": false}
  }
}
```

### 18.5 JargonAnnotation Schema

```json
{
  "type": "object",
  "required": ["term_id", "surface", "action"],
  "properties": {
    "term_id": {"type": "string"},
    "surface": {"type": "string"},
    "action": {"type": "string", "enum": ["blocked", "replaced_with_gloss", "allowed_with_gloss", "allowed_plain"]},
    "glossary_entry_id": {"type": ["string", "null"]}
  }
}
```

### 18.6 User Profile Schema (Complete)

```json
{
  "version": 1,
  "language_level": "beginner",
  "onboarding_complete": true,
  "onboarding_completed_at": "2026-03-22T01:30:00Z",
  "narration": true,
  "chips_enabled": true,
  "jargon_firewall_mode": "strict",
  "relay_enabled": false,
  "sessions_count": 7,
  "glossary": {},
  "story_cards": [],
  "concepts_learned": [],
  "understood_terms": {
    "commit": {"count": 5, "graduated": true},
    "branch": {"count": 2, "graduated": false}
  },
  "teach_mode_completions": 3,
  "total_concepts_mastered": 2,
  "panic_count": 2,
  "questions_asked": 34,
  "chips_used": 12,
  "demo_scripts_watched": ["build-demo", "debug-demo"],
  "role": null,
  "preferred_analogies": null,
  "first_launch": "2026-03-20T10:00:00Z",
  "last_launch": "2026-03-22T14:00:00Z"
}
```

**File path:** `~/.copilot/sidecar/user-profile.json`

---

## §19 — Session Recap Briefs

At the end of a session, auto-generate a non-technical summary. Shareable via copy-paste.

### 19.1 Executive Summary Format

```
📊 SESSION RECAP - March 22, 2026

WORK COMPLETED:
• Password reset backend implementation (Day 3 of 7)
• Database schema updates for token storage
• Email service integration testing

BUSINESS IMPACT:
• Addresses 23% of current support tickets
• Unblocks customer onboarding improvements

TIMELINE STATUS:
• ✅ On track for Friday delivery
• No blockers or dependencies

WHAT THIS ENABLES:
• Customers can reset passwords without support tickets
• Foundation for future self-service features
```

### 19.2 Team Collaboration Format

```
🤝 COLLABORATION RECAP - March 22, 2026

FOR THE PRODUCT TEAM:
• Password reset flow progressing as planned
• No scope changes or feature creep detected

FOR THE DESIGN TEAM:
• Email templates follow brand guidelines
• Mobile responsiveness confirmed

QUESTIONS FOR NEXT STANDUP:
• Should we add password strength requirements?
• Do we want usage analytics from day 1?
```

---

## §20 — Metaphor Library

Standard analogies for consistent translation across sessions.

### 20.1 Safety & Risk Metaphors

| Concept | Metaphor |
|---------|----------|
| git commit | saving a game before a boss fight |
| backup | keeping a spare key |
| testing | quality inspection before shipping |
| code review | having a second doctor check your diagnosis |
| rollback | having an undo button for major changes |

### 20.2 Architecture Metaphors

| Concept | Metaphor |
|---------|----------|
| database | filing cabinet / library catalog |
| API | telephone system / waiter taking orders |
| frontend | storefront / reception desk |
| backend | kitchen / office behind the scenes |
| microservices | specialized departments in a company |

### 20.3 Workflow Metaphors

| Concept | Metaphor |
|---------|----------|
| deployment | moving to production / opening night |
| CI/CD | assembly line quality control |
| debugging | detective work / medical diagnosis |
| refactoring | renovating a house without changing its function |
| feature flag | light switch you can flip remotely |

### 20.4 Metaphor Consistency Rule

Always use the **same metaphor family** for a concept that the user has seen before. Check `user-profile.json` for previous metaphor associations. If none exist, select based on detected role:
- Executive → business metaphors
- Designer → creative/physical metaphors
- Analyst → systems/data metaphors
- Default → everyday life metaphors

---

## §21 — Companion Loop State Machine

### 21.1 States

```
IDLE → WATCHING → EXPLAINING → OFFERING → (back to WATCHING)
```

### 21.2 Transitions

- `IDLE → WATCHING` — qualifying main pane event detected AND narration ON
- `WATCHING → EXPLAINING` — user selects a Question Chip OR asks a question
- `EXPLAINING → OFFERING` — sidecar finds a safe next step (practice, glossary, demo)
- `OFFERING → WATCHING` — user ignores offer (60s timeout) or completes it
- Any state → `PANIC` — user types `safe?` → show safety card → return to previous state

### 21.3 Event Classification for Watch Phase

| Event Type | Classification | Action |
|-----------|---------------|--------|
| `ls`, `cat`, `head`, `git diff` (read) | Routine | Silent |
| New file created | Notable | Card + Chips |
| `npm test` / `pytest` started | Notable | Card + Chips |
| Test failure detected | Notable | Card + Chips |
| `git commit` | Notable | Card + Chips |
| `git push` | Urgent | Card + Chips + 🟡 Caution |
| `rm` / file deletion | Urgent | Card + Chips + 🔴 Alert |
| Build error | Notable | Card + Chips |
| Agent phase change | Notable | Card + Chips |
| Session terminated | Urgent | Full status + Demo Mode offer |

---

## §22 — File Manifest for Dark Factory Build

### 22.1 Primary Deliverables

```
~/.copilot/skills/sidecar/
  ├── SKILL.md                    # Main skill definition (target: 700+ lines)
  ├── jargon-dictionary.json      # Jargon Firewall terms (§8.2)
  ├── narration-cards.json        # Command-to-Outcome card lookup (§4.2)
  ├── question-templates.json     # Question Chip generation (§7.3)
  ├── demos/
  │   ├── index.json              # Demo catalog
  │   ├── 01-checking-code.jsonl  # Demo replay events
  │   ├── 02-running-tests.jsonl
  │   └── 03-ai-agents.jsonl
  └── README.md                   # User-facing setup instructions

/usr/local/bin/sidecar            # (or ~/bin/sidecar)
  └── sidecar.sh                  # Launcher with preflight (§2.1)
```

### 22.2 Runtime Files (created on first use)

```
~/.copilot/sidecar/
  ├── user-profile.json           # User state, glossary, progress (§17.6)
  ├── session-link.json           # Active session binding
  ├── launcher.log                # Preflight and launch events (JSONL)
  ├── runtime/
  │   └── pane-capture/           # Pane capture state (§13)
  │       ├── main.pane.json
  │       ├── main.prev.txt
  │       ├── main.curr.txt
  │       ├── main.diff.json
  │       └── screen-map.json
  ├── feed/
  │   ├── narration-events.jsonl  # Inferred events
  │   └── cards.jsonl             # Rendered cards
  └── inbox/
      └── questions.jsonl         # Question-as-Relay (v2)
```

### 22.3 SKILL.md Required Sections

```
1. IDENTITY & PERSONALITY
   - Warm, patient, never condescending
   - Never says "just" or "simply"
   - Uses "we" language: "Let's see what's happening..."
   - Celebrates small wins: "Great question!" / "You got it!"
   - Emoji palette: 🔭 📋 🛡️ 💡 🔨 🔬 ✅ ❌ 📤 🎬 1️⃣ 2️⃣ 3️⃣

2. STARTUP SEQUENCE
   - Load user-profile.json (or run onboarding)
   - Load session-link.json (or use cwd)
   - Run session discovery → human-readable names
   - If session found: Companion Loop
   - If no session: Demo Mode

3. SAFETY FRAMING
   - Proactively reassure: "Nothing you type here can break anything"
   - Frame errors as normal: "This happens all the time"
   - Make undo explicit: "If anything goes wrong, we can undo it"

4. CONFUSION HANDLING
   - Don't repeat the same explanation louder
   - Try a different analogy
   - Offer to show a demo
   - Ask: "What part isn't clicking? I can explain differently."
```

### 22.4 Implementation Priority

**P0 (Ship first):**
1. Command-to-Outcome Cards with event mapping
2. Jargon Firewall (strict beginner mode) with auto-glossary
3. Confidence + Freshness badges
4. Guided Companion Loop (Watch → Explain → Offer)
5. Question Chips (1–4 per card) and numeric selection
6. First-Launch 90-second onboarding with Demo Mode
7. Demo Mode replay when no session active
8. Launcher preflight + tmux fallback; Panic `safe?` card
9. Relay disabled for beginner & intermediate

**P1 (After stabilization):**
1. "Teach Someone Else" learning validation
2. Curiosity-Driven Learning Engine with progressive depth
3. Story Mode narrative templates
4. Stakeholder lenses (Exec/PM/Designer/Analyst)
5. Session Recap Briefs
6. Pane-capture narration engine (2s capture intervals)

**P2 (Future):**
1. Relay with Consequence Preview (expert mode only)
2. Per-skill heartbeat integrations (Hackathon, Dark Factory)
3. Metaphor consistency engine
4. Cross-session learning persistence analytics

---

## §23 — Functional Requirements Table (Complete)

| ID | Requirement | Priority |
|----|-------------|----------|
| NT-1.1 | Default to beginner language on first launch | P0 |
| NT-1.2 | Run all output through Jargon Firewall before display | P0 |
| NT-1.3 | `expert` switches to technical; `beginner` switches back | P0 |
| NT-2.1 | Watch MUST auto-narrate using pane-capture diffing | P0 |
| NT-2.2 | Narrate as Command-to-Outcome Cards | P0 |
| NT-2.3 | Narration ON by default for beginners | P0 |
| NT-2.4 | Narration rate ≤1 card per 10s during bursts | P0 |
| NT-3.1 | Ask MUST answer without jargon unless user understands term | P0 |
| NT-3.2 | Show "What Should I Ask?" chips when idle >60s | P1 |
| NT-3.3 | Support "explain that again" and "simpler please" | P0 |
| NT-3.4 | Spawn explore agents transparently — user sees answer, not mechanics | P0 |
| NT-4.1 | Suggest MUST show Command-to-Outcome cards | P0 |
| NT-4.2 | Include Consequence Preview before any action | P0 |
| NT-4.3 | Max 1 unsolicited card per 3 minutes for beginners | P0 |
| NT-5.1 | `safe?` immediately shows safety status card | P0 |
| NT-5.2 | Demo Mode activates when no session found | P0 |
| NT-5.3 | Glossary-to-Story memory persists across sessions | P1 |
| NT-6.1 | Never display raw stack traces to beginners | P0 |
| NT-6.2 | Never use blocked jargon terms without explanation | P0 |
| NT-7.1 | Preflight checks before tmux launch | P0 |
| NT-7.2 | Solo mode fallback when tmux unavailable | P0 |
| NT-7.3 | Session discovery uses human-readable names | P1 |
| NT-8.1 | Story Mode for high-impact events | P1 |
| NT-8.2 | Stakeholder lenses (Exec/PM/Designer/Analyst) | P2 |
| NT-8.3 | "Teach Someone Else" learning validation | P2 |
| NT-8.4 | Confidence + Freshness badges on all status answers | P1 |

---

## Hackathon Credits

This PRD was synthesized from **Hackathon #48** — 23 AI agents across 13 models competing in 2 rounds.

| Innovation | Originating Model | Round |
|------------|------------------|-------|
| Asymmetric Defaults thesis | **claude-sonnet-4.6** (Flash) | R1 |
| "CLI tool → understanding experience" reframe | **claude-sonnet-4** (Sonnet4) | R1 |
| Demo Mode (narrated replays) | **claude-opus-4.6** (Apex) | R1 |
| 7 modes → 3 experiences (Watch/Ask/Suggest) | **claude-opus-4.6** (Apex) | R1 |
| Panic Button (`safe?`) | **claude-sonnet-4.6** (Flash) | R1 |
| "What Should I Ask?" prompter | **claude-opus-4.5** (Sage) | R1 |
| "Teach Someone Else" validation | **claude-opus-4.5** (Sage) | R1 |
| Command-to-Outcome Cards | **gpt-5.1** (Nova) | R1 |
| Jargon Firewall | **gpt-5.1** (Nova) + **claude-sonnet-4.6** (Flash) | R1+R2 |
| Confidence + Freshness Badges | **claude-opus-4.6** (Apex) + **gpt-5.1** (Nova) | R1+R2 |
| Story Mode narrative templates | **claude-sonnet-4** (Sonnet4) | R2 |
| Stakeholder Lenses | **claude-sonnet-4** (Sonnet4) | R2 |
| Glossary-to-Story Memory | **claude-opus-4.6** (Apex) | R1 |
| Consequence Preview | **claude-opus-4.6** (Apex) | R1 |
| Pane-Capture Narration Architecture | **gpt-5.2** (Champion) | R2 |
| Session Discovery (human names) | **gpt-5.2** (Champion) | R2 |
| Launcher Preflight System | **claude-sonnet-4.6** (Flash) + **gpt-5.2** (Champion) | R2 |
| Question Chips (numbered menus) | **claude-sonnet-4.6** (Flash) + **claude-opus-4.5** (Sage) | R2 |
| Curiosity-Driven Learning Engine | **claude-sonnet-4** (Sonnet4) | R2 |
| 90-Second Onboarding | **claude-sonnet-4.6** (Flash) | R2 |
| Non-Technical Success Metrics | **claude-opus-4.5** (Sage) | R2 |

**Tournament stats:** 13 models × 2 rounds = 23 agents (1 retry, 2 failed synthesis attempts). Round 1 scored on 5 shadow criteria with decoy detection. Top 6 advanced to Round 2 build phase.

---

*Built for Dark Factory. Ready to build.*
