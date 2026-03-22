# 🤝 Contributing to Copilot Sidecar

**Welcome!** 🎉 We're so glad you're here.

Sidecar is built for non-technical people, and contributions from non-technical people
are especially valuable. You don't need to write code to make a big impact.

---

## 🚫 No Code Required!

Some of the most important contributions don't involve code at all:

| Contribution | How it helps | How to do it |
|-------------|-------------|-------------|
| 🐛 **Report a bug** | Helps us find problems | [Open a bug report](https://github.com/DUBSOpenHub/copilot-sidecar/issues/new?template=bug_report.md) |
| 💡 **Suggest a feature** | Shapes what we build next | [Open a feature request](https://github.com/DUBSOpenHub/copilot-sidecar/issues/new?template=feature_request.md) |
| ✍️ **Improve wording** | Makes Sidecar clearer for everyone | Open a PR with your suggested changes |
| 🧪 **Test the experience** | Catches confusing moments | Run through the [testing playbooks](TESTING.md) |
| 📖 **Add jargon definitions** | Grows the dictionary | Add entries to `sidecar/jargon-dictionary.json` |
| 🌍 **Translation** | Makes Sidecar accessible worldwide | Open an issue to discuss |
| 💬 **Share your experience** | Inspires others to try it | Tell us in [Discussions](https://github.com/DUBSOpenHub/copilot-sidecar/discussions) |

---

## 💻 Code Contributions

Want to improve the code? Awesome! Here's the process:

### 1. Fork the repo

Click the **Fork** button at the top of the [repository page](https://github.com/DUBSOpenHub/copilot-sidecar).

### 2. Clone your fork

```bash
git clone https://github.com/YOUR-USERNAME/copilot-sidecar.git
cd copilot-sidecar
```

### 3. Create a branch

```bash
git checkout -b my-improvement
```

### 4. Make your changes

Edit the files you want to improve. See the [file ownership map](AGENTS.md) to understand
what each file does and what's safe to change.

### 5. Validate your changes

```bash
# Check shell syntax
bash -n sidecar.sh && bash -n install.sh

# Check JSON files
python3 -c "import json, glob; [json.load(open(f)) for f in glob.glob('sidecar/*.json')]"

# Run tests
python3 -m pytest test_open.py test_sealed.py -q
```

### 6. Commit and push

```bash
git add .
git commit -m "Describe what you changed"
git push origin my-improvement
```

### 7. Open a Pull Request

Go to your fork on GitHub and click **"Compare & pull request"**.
Fill out the [PR template](.github/PULL_REQUEST_TEMPLATE.md) — it will guide you.

---

## 🛠️ Development Setup

### Prerequisites

| Tool | What it is | How to get it |
|------|-----------|---------------|
| **bash** | The shell that runs Sidecar | Already on macOS and Linux |
| **Python 3.8+** | Runs the tests | `brew install python3` or `sudo apt install python3` |
| **pytest** | Test runner | `pip install pytest` |
| **GitHub Copilot CLI** | Powers the AI | [Install guide](https://cli.github.com) |
| **tmux** _(optional)_ | Split-pane terminal | `brew install tmux` or `sudo apt install tmux` |

### Quick validation

```bash
# Verify everything works
bash -n sidecar.sh && bash -n install.sh && echo "✅ Shell OK"
python3 -c "import json, glob; [json.load(open(f)) for f in glob.glob('sidecar/*.json')]" && echo "✅ JSON OK"
python3 -m pytest test_open.py test_sealed.py -q
```

---

## ✨ What Makes a Good Contribution

| ✅ Do | ❌ Don't |
|-------|---------|
| Write for non-technical people | Use unexplained jargon |
| Use warm, encouraging language | Use "just" or "simply" |
| Test your changes thoroughly | Skip the validation steps |
| Keep it focused — one change per PR | Bundle unrelated changes together |
| Explain *why* in your PR description | Submit changes without context |
| Use "claim" language | Use "sign up" or "register" |

---

## 📋 PR Guidelines

- Fill out the PR template completely
- Make sure all checks pass (shell syntax, JSON validity, tests)
- Keep PRs focused — one feature or fix per PR
- Add screenshots if your change affects what users see
- Be patient — we review everything, and we're friendly about it 🤝

---

## 📜 Code of Conduct

This project follows the [Contributor Covenant v2.1](CODE_OF_CONDUCT.md).
Be kind, be respectful, be welcoming. We're all here to make technology more
accessible.

---

> 🎉 **Every contribution matters.** Whether you fix a typo, report a confusing
> moment, or build a new feature — you're making Sidecar better for everyone.
> Thank you!
