# Sidecar Skill — Installation & Reference

> This is the skill package that gets installed to `~/.copilot/skills/sidecar/`.
> For the full project overview, see the [top-level README](../README.md).

## What's in This Folder

| File | Purpose |
|------|---------|
| `SKILL.md` | The core brain — 1,300 lines of prompt instructions that tell Copilot CLI how to behave as a non-technical companion |
| `jargon-dictionary.json` | 53 technical terms with plain-English definitions, used by the jargon firewall |
| `narration-cards.json` | 10 command patterns (git diff, npm test, etc.) mapped to 3-line explanation cards |
| `question-templates.json` | Context-aware suggested questions, organized by event type (test failure, build error, etc.) |
| `demos/` | 3 pre-recorded terminal walkthroughs for Demo Mode |
| `README.md` | This file |

## Install

```bash
cp -r sidecar/ ~/.copilot/skills/sidecar/
```

## What Gets Created at Runtime

When Sidecar runs for the first time, it creates these files automatically:

```
~/.copilot/sidecar/
├── user-profile.json        ← Your language level, glossary progress, session count
├── session-link.json        ← Which terminal session Sidecar is watching
├── launcher.log             ← Launch events (JSON, append-only)
└── runtime/pane-capture/    ← Screen capture state for live narration
```

## Customizing

**Add jargon terms:** Edit `jargon-dictionary.json` — add `"term": "plain English definition"`.

**Add narration cards:** Edit `narration-cards.json` — add a card with `pattern` (regex), `emoji`, `title`, `what`, `why`, `next`.

**Add demo replays:** Create a `.jsonl` file in `demos/` with events like `{"type": "command", "text": "git status", "delay_ms": 1000}` and register it in `demos/index.json`.

## Quick Command Reference

| Command | What it does |
|---------|-------------|
| `safe?` | Instant safety check |
| `what?` | Explain what just happened |
| `chips` | Show suggested questions |
| `glossary` | Show terms you've learned |
| `beginner` / `expert` | Switch language level |

## Troubleshooting

| Problem | Fix |
|---------|-----|
| "tmux not found" | `brew install tmux` (Mac) or `sudo apt install tmux` (Linux), or use `sidecar --solo` |
| "gh not found" | Install from [cli.github.com](https://cli.github.com) |
| Sidecar shows stale info | Type `what?` to refresh — check the freshness badge (🟢 🟡 🔴) |
| Profile seems corrupted | Delete `~/.copilot/sidecar/user-profile.json` — Sidecar will re-run onboarding |
