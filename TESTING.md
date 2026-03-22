# 🧪 TESTING.md — QA Playbooks & Checklists

> This document contains everything you need to test Copilot Sidecar.
> No testing experience required — follow the playbooks step by step.

---

## 🚀 How to Test Locally

### Quick validation (30 seconds)

```bash
# Shell syntax check
bash -n sidecar.sh && bash -n install.sh && echo "✅ Shell syntax OK"

# JSON validation
python3 -c "
import json, glob
for f in sorted(glob.glob('sidecar/*.json') + glob.glob('sidecar/**/*.json', recursive=True)):
    json.load(open(f))
    print(f'  ✅ {f}')
print('All JSON valid')
"

# Run automated tests
python3 -m pytest test_open.py test_sealed.py -q
```

### Full flow test (5 minutes)

1. Run the installer: `bash install.sh`
2. Launch Sidecar: `sidecar`
3. Run through Playbook 1 (Fresh Install) below
4. Try Playbook 4 (Watch Mode) with a real developer session

---

## 📋 Conversation Playbooks

### Playbook 1: Fresh Install Flow

| Step | Action | Expected |
|:----:|--------|----------|
| 1 | Run `bash install.sh` | Installer shows animated banner with 🔭 emoji |
| 2 | Wait for dependency checks | Shows ✅ for each found tool (gh, copilot extension) |
| 3 | Watch file copy | Shows progress for each file copied to `~/.copilot/skills/sidecar/` |
| 4 | Watch launcher install | `sidecar` copied to `~/bin/` and made executable |
| 5 | See completion message | "🎉 Sidecar is installed!" with launch instructions |
| 6 | Verify files exist | `ls ~/.copilot/skills/sidecar/` shows SKILL.md and JSON files |
| 7 | Verify launcher exists | `which sidecar` or `ls ~/bin/sidecar` shows the file |

### Playbook 2: First Launch (with tmux)

| Step | Action | Expected |
|:----:|--------|----------|
| 1 | Run `sidecar` | tmux session opens with two panes side by side |
| 2 | Look at right pane | Shows 🔭 banner and comfort level question (1/2/3) |
| 3 | Type `1` (beginner) | Sidecar confirms: "Great choice! I'll explain everything." |
| 4 | In left pane, type `ls` | Right pane shows narration: "📂 The developer is looking at files..." |
| 5 | In right pane, type `safe?` | Shows reassurance: "✅ Everything is fine..." |
| 6 | Type `chips` | Shows 4 numbered suggested questions |
| 7 | Type `1` | Sidecar answers the first suggested question |
| 8 | Type `glossary` | Shows terms learned so far (may be empty on first run) |

### Playbook 3: Solo Mode (without tmux)

| Step | Action | Expected |
|:----:|--------|----------|
| 1 | Run `sidecar --solo` | Single-pane Copilot CLI session starts |
| 2 | See banner | Shows 🔭 banner and comfort level question |
| 3 | Type `1` | Sidecar confirms beginner mode |
| 4 | Ask "What is git?" | Gets a warm, jargon-free explanation |
| 5 | Type `safe?` | Shows reassurance message |
| 6 | Type `chips` | Shows suggested questions |

### Playbook 4: Watch Mode Narration

| Step | Action | Expected |
|:----:|--------|----------|
| 1 | Launch with tmux: `sidecar` | Two-pane layout opens |
| 2 | In left pane: `git status` | Right pane narrates: "📋 The developer is checking..." |
| 3 | In left pane: `npm test` | Right pane narrates: "🧪 Running quality checks..." |
| 4 | In left pane: `git commit -m "fix"` | Right pane narrates: "💾 Saving a snapshot..." |
| 5 | Wait 30 seconds (idle) | Sidecar shows idle prompt or suggested questions |
| 6 | Run an unknown command | Sidecar attempts a general explanation or asks if you want details |

### Playbook 5: Ask Mode (Question Handling)

| Step | Action | Expected |
|:----:|--------|----------|
| 1 | Type a question: "What is Docker?" | Warm, jargon-free explanation with analogy |
| 2 | Type: "Is this safe?" | Reassurance about read-only nature |
| 3 | Type: "What just happened?" | Summary of most recent terminal activity |
| 4 | Type a follow-up question | Context-aware answer building on previous |
| 5 | Type `expert` | Switches to technical language mode |
| 6 | Ask same question again | Answer uses more technical detail |
| 7 | Type `beginner` | Switches back to simple mode |

### Playbook 6: Demo Mode

| Step | Action | Expected |
|:----:|--------|----------|
| 1 | Launch Sidecar with no active developer session | Demo mode should be available |
| 2 | Select a demo (e.g., "checking code") | Pre-recorded walkthrough plays |
| 3 | Watch narration cards | Each step shows title, explanation, and timing |
| 4 | Wait for demo to complete | Summary shown at the end |

### Playbook 7: Edge Cases

| Step | Action | Expected |
|:----:|--------|----------|
| 1 | Launch without tmux installed | Helpful error: "tmux not found — try `sidecar --solo`" |
| 2 | Launch without Copilot CLI | Helpful error with install instructions |
| 3 | Type random gibberish | Sidecar responds gracefully, doesn't crash |
| 4 | Rapidly type multiple commands | Sidecar handles queue without freezing |
| 5 | Run `sidecar --help` | Shows usage information with all options |
| 6 | Send Ctrl+C during operation | Clean exit, no orphan processes |
| 7 | Run installer twice | Second run updates files, doesn't duplicate or break |

### Playbook 8: Language & Tone Check

| Step | Action | Expected |
|:----:|--------|----------|
| 1 | Read all narration cards | No use of "just" or "simply" |
| 2 | Read all suggested questions | Warm, encouraging tone throughout |
| 3 | Read jargon dictionary definitions | Every definition understandable by non-technical person |
| 4 | Read error messages in sidecar.sh | Friendly, not intimidating — includes fix suggestions |
| 5 | Read install.sh output | Animated, warm, celebratory on success |
| 6 | Check all README content | No unexplained jargon |

---

## ✅ QA Checklist

Run through this before any release:

### Shell & Syntax
- [ ] `bash -n sidecar.sh` passes
- [ ] `bash -n install.sh` passes
- [ ] All JSON files parse without errors
- [ ] `shellcheck sidecar.sh` has no critical warnings (if shellcheck available)
- [ ] `shellcheck install.sh` has no critical warnings (if shellcheck available)

### Automated Tests
- [ ] `python3 -m pytest test_open.py -q` — all pass
- [ ] `python3 -m pytest test_sealed.py -q` — all pass
- [ ] No test warnings or deprecations

### Installation
- [ ] `bash install.sh` completes successfully on macOS
- [ ] `bash install.sh` completes successfully on Linux
- [ ] `curl -fsSL <url> | bash` works (pipe-safe)
- [ ] Re-running installer updates cleanly
- [ ] All files land in correct locations

### Core Experience
- [ ] `sidecar` launches tmux split correctly
- [ ] `sidecar --solo` works without tmux
- [ ] `sidecar --help` shows usage
- [ ] Comfort level selection (1/2/3) works
- [ ] `safe?` command works
- [ ] `chips` command shows suggestions
- [ ] `glossary` command works
- [ ] `beginner` / `expert` mode switching works

### Tone & Language
- [ ] No instances of "just" or "simply" in user-facing text
- [ ] No unexplained jargon
- [ ] All error messages are friendly and include next steps
- [ ] Emoji usage is warm but not excessive

---

## 🔧 Shell & JSON Validation Commands

```bash
# Shell syntax (must pass — these run in CI)
bash -n sidecar.sh
bash -n install.sh

# JSON validation (must pass — runs in CI)
python3 -c "
import json, glob, sys
errors = 0
for f in sorted(glob.glob('sidecar/*.json') + glob.glob('sidecar/**/*.json', recursive=True)):
    try:
        json.load(open(f))
        print(f'  ✅ {f}')
    except Exception as e:
        print(f'  ❌ {f}: {e}')
        errors += 1
if errors:
    print(f'\n❌ {errors} file(s) failed')
    sys.exit(1)
else:
    print('\n✅ All JSON valid')
"

# Full test suite
python3 -m pytest test_open.py test_sealed.py -v
```

---

## 📊 Coverage Matrix

| Area | Automated Tests | Manual Playbook | CI Check |
|------|:---:|:---:|:---:|
| Shell syntax | — | — | ✅ `bash -n` |
| JSON validity | — | — | ✅ Python validation |
| SKILL.md behavior | ✅ 196 sealed tests | Playbooks 2–6 | ✅ pytest |
| Launcher logic | ✅ 74 open tests | Playbooks 2, 3, 7 | ✅ pytest |
| Install flow | — | Playbook 1 | — |
| Narration quality | ✅ Sealed tests | Playbook 4 | ✅ pytest |
| Ask mode | ✅ Sealed tests | Playbook 5 | ✅ pytest |
| Demo mode | ✅ Open tests | Playbook 6 | ✅ pytest |
| Edge cases | ✅ Open tests | Playbook 7 | ✅ pytest |
| Tone & language | ✅ Sealed tests | Playbook 8 | — |
| Install (macOS) | — | Playbook 1 | — |
| Install (Linux) | — | Playbook 1 | — |

---

> 🧪 *Testing Sidecar is easy — if something confuses you during testing, that's a bug worth reporting!*
