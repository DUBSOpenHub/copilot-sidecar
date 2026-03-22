# 🤖 AGENTS.md — AI Agent Working Guide

> This file tells AI agents (GitHub Copilot, Copilot CLI, and other LLMs)
> how this project works and what rules to follow when making changes.

---

## 🔭 What Is This Project?

**Copilot Sidecar** is a terminal translator for non-technical people. It watches a
developer's terminal and explains what's happening in plain English — like a sports
announcer for software development.

It's a [GitHub Copilot CLI skill](https://docs.github.com/en/copilot/github-copilot-in-the-cli)
powered by a markdown prompt file (`SKILL.md`), JSON configuration, and a bash launcher.

**Primary audience:** Product managers, designers, executives — people who work *with*
developers but don't write code.

---

## 📁 File Ownership Map

| File | Role | Mutable? | Notes |
|------|------|:--------:|-------|
| `sidecar/SKILL.md` | Core AI brain — the main prompt (~1,300 lines) | ⚠️ Careful | Changes here affect all AI behavior |
| `sidecar/jargon-dictionary.json` | 53 technical terms → plain English | ⚠️ Careful | Add terms, never remove working ones |
| `sidecar/narration-cards.json` | 10 command patterns → explanation cards | ⚠️ Careful | Each card maps a regex to a narration |
| `sidecar/question-templates.json` | Context-aware suggested questions | ⚠️ Careful | Powers the `chips` / numbered prompts |
| `sidecar/demos/index.json` | Demo mode manifest | ⚠️ Careful | References the .jsonl demo scripts |
| `sidecar/demos/*.jsonl` | Pre-recorded demo walkthroughs | ⚠️ Careful | 3 demos: code check, tests, AI agents |
| `sidecar/README.md` | Setup guide for the skill directory | ✅ Yes | |
| `sidecar.sh` | Launcher with preflight checks | ⚠️ Careful | Must pass `bash -n`; handles tmux + solo |
| `install.sh` | One-command installer (`curl \| bash`) | ⚠️ Careful | Must pass `bash -n`; pipe-safe |
| `test_sealed.py` | 196 sealed-envelope behavioral tests | 🚫 Never | Written from spec, never sees code |
| `test_open.py` | 74 implementation tests | ✅ Yes | |
| `README.md` | Main landing page | ✅ Yes | Non-technical-first |
| `AGENTS.md` | This file — AI agent guide | ✅ Yes | |
| `TESTING.md` | QA playbooks and checklists | ✅ Yes | |
| `CONTRIBUTING.md` | Contribution guide | ✅ Yes | |
| `SECURITY.md` | Security policy | ✅ Yes | |
| `CHANGELOG.md` | Version history | ✅ Yes | |
| `CODE_OF_CONDUCT.md` | Contributor Covenant v2.1 | ✅ Yes | |
| `LICENSE` | MIT License | 🚫 Never | |
| `PRD.md` | Product Requirements Document | 📖 Read-only | Reference material |
| `ARCH.md` | Architecture Design | 📖 Read-only | Reference material |
| `GAP-REPORT.md` | QA validation results | 📖 Read-only | Reference material |
| `OUTCOME-REPORT.md` | Final scorecard | 📖 Read-only | Reference material |
| `.github/copilot-instructions.md` | AI rules for this repo | ✅ Yes | |
| `.github/CODEOWNERS` | Code ownership | ✅ Yes | |
| `.github/dependabot.yml` | Dependabot config | ✅ Yes | |
| `.github/workflows/ci.yml` | CI pipeline | ✅ Yes | |
| `.github/workflows/codeql.yml` | Security scanning | ✅ Yes | |
| `.github/ISSUE_TEMPLATE/*` | Issue templates | ✅ Yes | |
| `.github/PULL_REQUEST_TEMPLATE.md` | PR template | ✅ Yes | |

---

## 🏗️ What Gets Created on the User's Machine

When someone installs and runs Sidecar, these files appear:

```
~/.copilot/skills/sidecar/          ← Skill files (copied by installer)
├── SKILL.md
├── jargon-dictionary.json
├── narration-cards.json
├── question-templates.json
├── demos/
│   ├── index.json
│   ├── 01-checking-code.jsonl
│   ├── 02-running-tests.jsonl
│   └── 03-ai-agents.jsonl
└── README.md

~/bin/sidecar                       ← Launcher script (copied by installer)

~/.copilot/sidecar/                 ← Runtime state (created on first launch)
├── user-profile.json                ← Language level, glossary progress
└── launcher.log                     ← Event log (timestamps only, no PII)
```

---

## 🌳 Architecture

```
copilot-sidecar/
├── sidecar/                        ← THE SKILL (install this)
│   ├── SKILL.md                     ← Core AI brain
│   ├── jargon-dictionary.json       ← Term definitions
│   ├── narration-cards.json         ← Command → explanation mapping
│   ├── question-templates.json      ← Suggested questions
│   ├── demos/                       ← Pre-recorded walkthroughs
│   │   ├── index.json
│   │   ├── 01-checking-code.jsonl
│   │   ├── 02-running-tests.jsonl
│   │   └── 03-ai-agents.jsonl
│   └── README.md
│
├── sidecar.sh                      ← Launcher (tmux + solo mode)
├── install.sh                      ← One-command installer
│
├── test_sealed.py                  ← Sealed behavioral tests (196)
├── test_open.py                    ← Implementation tests (74)
│
├── README.md                       ← Landing page
├── AGENTS.md                       ← This file
├── TESTING.md                      ← QA playbooks
├── CONTRIBUTING.md                 ← How to contribute
├── SECURITY.md                     ← Security policy
├── CHANGELOG.md                    ← Version history
├── CODE_OF_CONDUCT.md              ← Contributor Covenant
├── LICENSE                         ← MIT
│
├── PRD.md                          ← Product requirements
├── ARCH.md                         ← Architecture design
├── GAP-REPORT.md                   ← QA gap analysis
├── OUTCOME-REPORT.md               ← Final scorecard
│
└── .github/
    ├── copilot-instructions.md     ← AI rules
    ├── CODEOWNERS                  ← @DUBSOpenHub
    ├── dependabot.yml
    ├── workflows/
    │   ├── ci.yml                  ← Shell + JSON + test validation
    │   └── codeql.yml              ← Security scanning
    ├── ISSUE_TEMPLATE/
    │   ├── bug_report.md
    │   └── feature_request.md
    └── PULL_REQUEST_TEMPLATE.md
```

---

## 📏 Change Rules

### Shell Scripts (`sidecar.sh`, `install.sh`)

- Must pass `bash -n <file>` (syntax check) before commit
- Use `set -euo pipefail` (sidecar.sh) or `set -u` (install.sh)
- Quote all variables: `"$VAR"` not `$VAR`
- Handle missing commands gracefully (check with `command -v`)
- install.sh must be pipe-safe (`curl | bash`) — use `/dev/tty` for interactive input
- Always trap cleanup on EXIT INT TERM
- Test on both macOS and Linux when possible

### SKILL.md (`sidecar/SKILL.md`)

- This is the AI's brain — changes here affect everything
- Never use "just" or "simply" in any user-facing text
- Every technical term must have a plain-English explanation
- Maintain the section structure (Identity → Modes → Narration → etc.)
- Test changes by running `sidecar` and verifying narration quality
- The sealed tests (`test_sealed.py`) validate SKILL.md behavior — run them

### JSON Configs (`sidecar/*.json`)

- Must be valid JSON (test with `python3 -c "import json; json.load(open('file'))"`)
- `jargon-dictionary.json`: Each entry needs `term`, `definition`, `example`
- `narration-cards.json`: Each card needs `pattern`, `title`, `explanation`
- `question-templates.json`: Each template needs `context`, `questions` array
- Never remove working entries — add new ones alongside existing ones

### All User-Facing Text

- **Audience is non-technical** — explain everything
- Use warm, encouraging language with appropriate emoji
- Say **"claim"** not "sign up" or "register"
- Say **"your computer"** not "local machine" or "localhost"
- Never use "just" or "simply"
- One thing at a time — don't overwhelm with choices
- When in doubt, read the existing README.md for tone reference

---

## ⚠️ Common Pitfalls

| Pitfall | Consequence | Prevention |
|---------|-------------|------------|
| Editing `test_sealed.py` | Breaks the sealed-envelope testing protocol | Never touch it — it was written from the spec before code existed |
| Using jargon without definition | Confuses the target audience | Check `jargon-dictionary.json`; add missing terms |
| Breaking `bash -n` syntax | CI fails, install breaks | Run `bash -n` before every commit |
| Invalid JSON | Sidecar crashes on launch | Validate with `python3 -c "import json; json.load(open(f))"` |
| Forgetting `/dev/tty` in installer | `curl \| bash` hangs or breaks | Always read interactive input from `/dev/tty` |
| Using "just run..." in docs | Makes non-technical users feel dumb | Use "Run this command:" instead |
| Storing state outside `~/.copilot/sidecar/` | Files get lost, permissions break | All runtime state in one directory |
| Hardcoding paths | Breaks on different machines | Use `$HOME` and detect OS dynamically |

---

## 🚀 Running It

### With tmux (recommended)

```bash
sidecar
```

This opens a split-pane terminal: developer's work on the left, Sidecar narration on the right.

### Without tmux (solo mode)

```bash
sidecar --solo
```

Sidecar runs in a single panel — you can switch between windows manually.

### Quick install (one command)

```bash
curl -fsSL https://raw.githubusercontent.com/DUBSOpenHub/copilot-sidecar/main/install.sh | bash
```

---

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for the full guide. Quick version:

1. Fork → Clone → Branch
2. Make changes (follow the rules above)
3. Validate: `bash -n sidecar.sh && bash -n install.sh`
4. Test: `python3 -m pytest test_open.py test_sealed.py -q`
5. Open a PR using the template

---

> 🔭 *Built for people who work with developers but don't write code.*
