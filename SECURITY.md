# 🛡️ Security Policy

## Supported Versions

| Version | Supported |
|---------|:---------:|
| 1.0.x   | ✅ Yes    |
| < 1.0   | ❌ No     |

## 🔒 Reporting a Vulnerability

**Please do NOT open a public issue for security vulnerabilities.**

Instead, use one of these methods:

1. **GitHub Private Vulnerability Reporting** _(preferred)_
   → [Report here](https://github.com/DUBSOpenHub/copilot-sidecar/security/advisories/new)

2. **Email**
   → Open a GitHub Discussion marked **[Security]** with minimal details,
   and we'll arrange a private channel.

### What to Include

| Detail | Why it helps |
|--------|-------------|
| Description of the vulnerability | So we understand the issue |
| Steps to reproduce | So we can verify it |
| Which files/components are affected | So we can scope the fix |
| Potential impact | So we can prioritize correctly |
| Suggested fix _(optional)_ | If you have ideas, we'd love to hear them |

### What to Expect

| Timeframe | What happens |
|-----------|-------------|
| **48 hours** | We acknowledge your report |
| **7 days** | Initial assessment and severity rating |
| **30 days** | Fix developed, tested, and released |
| **After fix** | Public disclosure with credit to reporter |

We take every report seriously. If we determine the issue isn't a security vulnerability,
we'll explain why and suggest the right channel (bug report, feature request, etc.).

## 🔐 Security Features

This repository uses several GitHub security features:

| Feature | Status | What it does |
|---------|:------:|-------------|
| **Dependabot** | ✅ Enabled | Watches for vulnerable dependencies |
| **Secret Scanning** | ✅ Enabled | Catches accidentally committed secrets |
| **CodeQL** | ✅ Enabled | Finds security bugs in Python code automatically |
| **Branch Protection** | ✅ Enabled | Requires reviews before merging to `main` |
| **CODEOWNERS** | ✅ Enabled | Ensures the right people review every change |

## 🔏 Privacy & Data Practices

Copilot Sidecar is designed with privacy as a core principle:

| Practice | Detail |
|----------|--------|
| **Read-only** | Sidecar reads the developer's terminal screen via `tmux capture-pane`. It **never** modifies files, runs commands, or changes anything in the main session. |
| **Local state only** | All user data (glossary progress, language level) is stored in `~/.copilot/sidecar/` on your computer. Nothing is sent to external servers by Sidecar itself. |
| **No PII transmitted** | Sidecar does not collect, store, or transmit personally identifiable information. |
| **No credentials stored** | Sidecar never asks for or stores passwords, tokens, or API keys. Authentication is handled entirely by the GitHub Copilot CLI. |
| **No telemetry** | Sidecar does not phone home. Usage data stays on your machine. |
| **Copilot CLI data** | The underlying Copilot CLI has its own [privacy practices](https://docs.github.com/en/copilot/overview-of-github-copilot/about-github-copilot-individual#about-privacy). Sidecar adds no additional data collection. |

## 🧑‍💻 Best Practices for Contributors

- **Never commit secrets** — API keys, tokens, passwords. Use environment variables instead.
- **Never log PII** — The launcher log (`~/.copilot/sidecar/launcher.log`) records only events and timestamps, never terminal content.
- **Validate all inputs** — Shell scripts should quote variables and handle edge cases.
- **Test security changes** — Run the full test suite before submitting security-related PRs.
- **Keep dependencies minimal** — Sidecar intentionally has zero runtime dependencies beyond bash and the Copilot CLI.

---

> 🙏 **Thank you** for helping keep Sidecar safe for everyone.
> Security reports are handled with urgency, discretion, and gratitude.
