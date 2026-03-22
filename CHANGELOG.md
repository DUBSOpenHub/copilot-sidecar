# 📋 Changelog

All notable changes to Copilot Sidecar will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

_Nothing yet — [open an issue](https://github.com/DUBSOpenHub/copilot-sidecar/issues) if you have ideas!_

## [1.0.0] - 2026-03-22

### Added

- 🔭 **Watch Mode** — real-time narration of developer terminal activity via `tmux capture-pane`
- 💬 **Ask Mode** — ask any question and get a jargon-free answer
- 💡 **Suggested Questions** — contextual numbered prompts (type `chips` or `1`–`4` to select)
- 🛡️ **Safety Check** — type `safe?` anytime for instant reassurance that nothing is broken
- 📖 **Personal Glossary** — tracks terms you've learned, auto-graduates after 5 exposures
- 🎬 **Demo Mode** — 3 pre-recorded walkthroughs for when no developer is actively working
- 🧠 **Jargon Firewall** — 53 technical terms with plain-English definitions in `jargon-dictionary.json`
- 🎯 **Narration Cards** — 10 command patterns mapped to structured explanation cards
- 🎚️ **Adaptive Language Levels** — beginner, intermediate, and expert modes
- 🖥️ **tmux Integration** — side-by-side split-pane experience with `sidecar.sh` launcher
- 🧍 **Solo Mode** — `sidecar --solo` for use without tmux
- 🔧 **One-Command Installer** — `curl -fsSL <url> | bash` installs everything in 30 seconds
- ✅ **270 Tests** — 196 sealed-envelope behavioral tests + 74 implementation tests
- 📄 **Full Documentation** — README, AGENTS.md, TESTING.md, CONTRIBUTING.md, and more

[Unreleased]: https://github.com/DUBSOpenHub/copilot-sidecar/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/DUBSOpenHub/copilot-sidecar/releases/tag/v1.0.0
