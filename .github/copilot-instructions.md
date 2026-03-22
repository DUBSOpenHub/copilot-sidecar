# 🤖 Copilot Instructions for Sidecar

> These rules apply to any AI agent (GitHub Copilot, Copilot CLI, or other LLMs)
> working on files in this repository.

## 🎯 Audience

The primary audience for Copilot Sidecar is **non-technical people** — product managers,
designers, executives, and anyone who works with developers but doesn't write code.

Every word you write should be understandable by someone who has never opened a terminal.

## ✍️ Language Rules

| Rule | Example |
|------|---------|
| Use **"claim"** not "sign up" or "register" | "Claim your Sidecar" |
| Use **"your computer"** not "local machine" | "Saved on your computer" |
| Use **warm, encouraging** tone | "Great question!" not "See the docs" |
| **Never** use "just" or "simply" | ❌ "Just run..." → ✅ "Run this command:" |
| **Never** use unexplained jargon | ❌ "SSH into the box" → ✅ "Connect to the server" |
| **Explain every technical term** on first use | "tmux (a tool that splits your terminal into panels)" |
| Use **emoji** to add warmth | 🔭 🎬 💬 🛡️ — but don't overdo it |
| **One thing at a time** | Don't list 5 options — guide to the best one |

## 📁 File Ownership

| File | Role | Can AI modify? |
|------|------|:-:|
| `sidecar/SKILL.md` | Core AI brain — the main prompt | ⚠️ With care |
| `sidecar/*.json` | Config files (jargon, narrations, questions) | ⚠️ With care |
| `sidecar/demos/*` | Pre-recorded demo scripts | ⚠️ With care |
| `sidecar.sh` | Launcher script | ⚠️ With care |
| `install.sh` | One-command installer | ⚠️ With care |
| `test_sealed.py` | Sealed behavioral tests — never change | 🚫 Never |
| `test_open.py` | Implementation tests | ✅ Yes |
| `README.md` | Main landing page | ✅ Yes |
| `AGENTS.md` | AI agent guide (this pattern) | ✅ Yes |
| `TESTING.md` | QA playbooks | ✅ Yes |
| `.github/*` | CI, templates, config | ✅ Yes |

## 🧪 Testing Requirements

Before any PR or commit:

1. **Shell syntax:** `bash -n sidecar.sh && bash -n install.sh`
2. **JSON validity:** `python3 -c "import json, glob; [json.load(open(f)) for f in glob.glob('sidecar/*.json')]"`
3. **All tests pass:** `python3 -m pytest test_open.py test_sealed.py -q`
4. **Full flow test:** Run `sidecar` and verify narration appears

## 🚫 Things to Never Do

- Never modify `test_sealed.py` — these are sealed-envelope tests
- Never add jargon without a plain-English definition
- Never use "just" or "simply" in user-facing text
- Never break the `curl | bash` install flow
- Never add features that require the user to understand programming
- Never store credentials or PII anywhere
