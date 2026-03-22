# Copilot Sidecar — Non-Technical Experience

> Your friendly terminal companion. Watches what developers do and explains it in plain English.

## What Is Sidecar?

Copilot Sidecar sits in a side panel next to a developer's terminal. It watches what's happening and translates everything into plain language — no coding knowledge required.

**Three things Sidecar does:**

| Mode | What it does |
|------|-------------|
| 👀 **Watch** | Narrates what the developer is doing, like a sports commentator |
| 💬 **Ask** | Answers any question in plain English — no jargon |
| 💡 **Suggest** | Points out interesting things happening in the code |

## Prerequisites

| Tool | What it does | Install |
|------|-------------|---------|
| **GitHub CLI** (`gh`) | Connects to GitHub Copilot | [cli.github.com](https://cli.github.com) |
| **tmux** (optional) | Splits your terminal into two panels | `brew install tmux` (Mac) or `sudo apt install tmux` (Linux) |

## Installation

1. **Install the Sidecar skill:**
   ```bash
   # Copy the sidecar/ folder to your Copilot skills directory
   cp -r sidecar/ ~/.copilot/skills/sidecar/
   ```

2. **Install the launcher:**
   ```bash
   cp sidecar.sh ~/bin/sidecar
   chmod +x ~/bin/sidecar
   ```

3. **Launch Sidecar:**
   ```bash
   sidecar
   ```

   Or without tmux (solo mode):
   ```bash
   sidecar --solo
   ```

## Quick Start

After launching, Sidecar will:

1. **Check your setup** — makes sure everything is installed
2. **Ask one question** — to set your experience level
3. **Start watching** — begins narrating what the developer does

That's it! You're ready to go.

## Commands

Type any of these at any time:

| Command | What it does |
|---------|-------------|
| `safe?` | Instantly shows whether everything is OK |
| `chips` | Shows suggested questions you can ask |
| `what?` | Explains the last thing that happened |
| `glossary` | Shows terms you've learned so far |
| `beginner` | Switch to simple explanations |
| `expert` | Switch to technical mode |
| `teach me about X` | Practice explaining a concept |
| `1`, `2`, `3`, `4` | Select a suggested question |

## How It Works

Sidecar reads the developer's terminal screen (read-only — it never changes anything) and:

1. **Detects commands** — recognizes what the developer typed
2. **Translates** — explains it in plain English using narration cards
3. **Filters jargon** — replaces technical terms with simple definitions
4. **Suggests questions** — shows things you might want to ask about

## Demo Mode

If no developer is actively working, Sidecar enters **Demo Mode** — a guided replay showing what AI-assisted development looks like. Three demos are included:

1. **Checking the Code** — watching a developer review changes
2. **Running Quality Checks** — seeing how automated testing works
3. **AI Helpers Working Together** — watching AI agents collaborate

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "tmux not found" | Install tmux or use `sidecar --solo` |
| "gh not found" | Install GitHub CLI from [cli.github.com](https://cli.github.com) |
| "Skill not installed" | Copy sidecar/ to `~/.copilot/skills/sidecar/` |
| Sidecar shows stale info | Type `what?` to refresh, or check the freshness badge |

## Files

```
~/.copilot/skills/sidecar/     ← Skill files (you install these)
├── SKILL.md                    ← Main brain of the skill
├── jargon-dictionary.json      ← Technical term definitions
├── narration-cards.json        ← Command explanation cards
├── question-templates.json     ← Suggested question templates
├── demos/                      ← Pre-recorded demo replays
│   ├── index.json
│   ├── 01-checking-code.jsonl
│   ├── 02-running-tests.jsonl
│   └── 03-ai-agents.jsonl
└── README.md                   ← This file

~/.copilot/sidecar/            ← Runtime data (created automatically)
├── user-profile.json           ← Your preferences and progress
├── session-link.json           ← Current session info
└── runtime/                    ← Screen capture data
```

---

*Built with ❤️ for people who work with developers but don't write code.*
