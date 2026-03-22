# 🔭 Sidecar — A Terminal Translator for Non-Technical People

> **Claim yours in one command:**
> ```bash
> curl -fsSL https://raw.githubusercontent.com/DUBSOpenHub/copilot-sidecar/main/install.sh | bash
> ```

**Sidecar watches a developer's terminal and explains what's happening in plain English.**

It's for product managers, designers, executives, and anyone who works *with* developers but doesn't write code. Instead of watching a developer's screen and feeling lost, you get a running commentary — like a sports announcer for software development.

```
┌─── DEVELOPER'S TERMINAL ──────────┬─── YOUR SIDECAR PANEL ────────────┐
│                                    │                                    │
│  $ npm test                        │  🧪 QUALITY CHECK                  │
│  FAIL src/auth/login.test.ts       │  Running 47 automated checks to   │
│    ✕ should reject invalid pass    │  make sure the code works. Like a  │
│                                    │  spell-checker, but for logic.     │
│  Tests: 1 failed, 46 passed       │  3 checks failed — will fix next.  │
│                                    │                                    │
│                                    │  💬 Not sure what to ask? Try:     │
│                                    │    [1] What do these failures mean?│
│                                    │    [2] Is this a real problem?     │
│                                    │    [3] What would fixing involve?  │
│                                    │    [4] Is everything still safe?   │
└────────────────────────────────────┴────────────────────────────────────┘
```

---

## Why This Exists

Non-technical people don't want to become developers. They want to **understand what developers do** — evaluate technical proposals, ask better questions, and know when "almost done" really means three more weeks of debugging.

Sidecar bridges that gap. It sits in a side panel, watches the developer's work, and translates it — automatically, in real time, without interrupting anyone.

## What It Does

| | Feature | What you experience |
|---|---------|-------------------|
| 👀 | **Watch** | A running narration of what the developer is doing, like a commentator |
| 💬 | **Ask** | Ask any question and get a jargon-free answer |
| 💡 | **Suggest** | Contextual prompts when you're not sure what to ask |
| 🛡️ | **Safe?** | Instant reassurance that nothing is broken (type `safe?` anytime) |
| 📖 | **Learn** | A personal glossary that grows as you learn technical terms |
| 🎬 | **Demo** | Pre-recorded walkthroughs when no developer is actively working |

## Who It's For

- **Product managers** watching a sprint in progress
- **Designers** reviewing frontend work with an engineer
- **Executives** who want to understand what their engineering team does
- **Data analysts** collaborating on data pipeline work
- **Anyone** who's ever watched a developer's screen and thought "what is happening?"

---

## Quick Start

### What You Need

| Requirement | What it is | How to get it |
|-------------|-----------|---------------|
| **macOS or Linux** | Your operating system | You probably already have one |
| **GitHub Copilot CLI** | The AI assistant that powers Sidecar | [Install guide →](https://cli.github.com) |
| **tmux** *(optional)* | Splits your screen into two panels | Mac: `brew install tmux` · Linux: `sudo apt install tmux` |

### Install (30 seconds)

```bash
# 1. Copy the skill files
cp -r sidecar/ ~/.copilot/skills/sidecar/

# 2. Copy the launcher
cp sidecar.sh ~/bin/sidecar && chmod +x ~/bin/sidecar

# 3. Launch
sidecar
```

No tmux? No problem — use solo mode:
```bash
sidecar --solo
```

### First Launch

Sidecar asks **one question** to learn your comfort level, then starts narrating. That's it.

```
  1️⃣  I'm new to this — explain everything simply
  2️⃣  I know some basics — just flag unusual things
  3️⃣  I'm a developer — skip the hand-holding
```

---

## How It Works (Non-Technical Version)

Sidecar reads the developer's terminal screen — **read-only, it never changes anything** — and:

1. **Recognizes commands** → "The developer just ran quality checks"
2. **Translates to plain English** → Shows a narration card explaining what happened and why
3. **Filters jargon** → Replaces technical terms with definitions you can understand
4. **Suggests questions** → Shows numbered prompts you can select with one keystroke

The first time Sidecar sees a term like "git commit," it explains it fully. After you've seen it 5 times, it stops explaining — you've graduated that term.

## How It Works (Technical Version)

Sidecar is a [GitHub Copilot CLI skill](https://docs.github.com/en/copilot/github-copilot-in-the-cli) — a markdown prompt file (`SKILL.md`) that instructs the Copilot CLI how to behave. It runs in a tmux side pane and reads the main pane via `tmux capture-pane`, diffs the output, classifies events against pattern-matched narration cards, applies a jargon firewall, and renders 3-line explanation cards with confidence/freshness badges. All user state (glossary progress, language level) persists in `~/.copilot/sidecar/user-profile.json`.

No server. No database. No daemon. Just a skill file, some JSON configs, and a bash launcher.

---

## Commands

Type any of these in the Sidecar panel at any time:

| Command | What it does |
|---------|-------------|
| `safe?` | Am I safe? Instant status check |
| `what?` | What just happened? |
| `chips` | Show me suggested questions |
| `glossary` | Show terms I've learned |
| `beginner` | Switch to simple explanations |
| `expert` | Switch to technical mode |
| `1` `2` `3` `4` | Pick a suggested question |

---

## Project Structure

```
sidecar/                    ← The skill (install this)
├── SKILL.md                 ← Core brain — 1,300 lines of prompt engineering
├── jargon-dictionary.json   ← 53 technical terms with plain-English definitions
├── narration-cards.json     ← 10 command patterns mapped to explanation cards
├── question-templates.json  ← Context-aware suggested questions
├── demos/                   ← 3 pre-recorded walkthroughs
└── README.md                ← Setup guide

sidecar.sh                  ← Launcher script with preflight checks

PRD.md                      ← Product requirements (what to build and why)
ARCH.md                     ← Architecture design (how it's built)
test_sealed.py              ← Spec-driven behavioral tests (196 cases)
test_open.py                ← Implementation tests (74 cases)
GAP-REPORT.md               ← QA validation results
OUTCOME-REPORT.md           ← Final scorecard against requirements
```

## How This Was Built

This project was built using the [Dark Factory](https://github.com/DUBSOpenHub/dark-factory) pipeline — an agentic build system that orchestrates 6 specialist AI agents through a checkpoint-gated process with sealed-envelope testing:

1. **Product Manager** → Wrote the PRD (actually pre-written by [Havoc Hackathon](https://github.com/DUBSOpenHub/havoc-hackathon) #48 — 23 AI agents across 13 models)
2. **Architect** → Designed the system (ARCH.md)
3. **QA Engineer** → Wrote behavioral tests from the spec alone, never seeing code (sealed-envelope protocol)
4. **Lead Engineer** → Built the implementation and open tests
5. **QA Validator** → Ran both test suites, computed a gap score
6. **Lead Engineer (Hardening)** → Fixed the 5 gaps the sealed tests found
7. **Outcome Evaluator** → Scored the final build: **100/100, 270/270 tests passing**

*"Sealed-envelope testing"* means the QA engineer writes tests from the spec before any code exists, and never sees the implementation. The engineer never sees the QA tests. This catches spec-vs-implementation drift that traditional TDD misses.

---

---

## 📸 Screenshots

<!-- Screenshots coming soon! If you'd like to contribute screenshots, open a PR. -->

_Screenshots of the Sidecar experience will be added here. Want to help? Run Sidecar and share a screenshot in a [pull request](https://github.com/DUBSOpenHub/copilot-sidecar/pulls)!_

## Platform Support

| Platform | Status |
|----------|--------|
| macOS | ✅ Fully supported |
| Linux | ✅ Fully supported |
| Windows (WSL) | 🟡 Should work via WSL, untested |
| Windows (native) | ❌ Not supported (requires bash + tmux) |

## Status

**v1.0.0** — All P0 features shipped. 270 tests passing. Ready for use.

---

*Built for people who work with developers but don't write code.*
