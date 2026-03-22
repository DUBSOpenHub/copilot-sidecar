#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────
# 🔭 Copilot Sidecar — One-Command Installer
#
# Usage:
#   curl -fsSL https://raw.githubusercontent.com/DUBSOpenHub/copilot-sidecar/main/install.sh | bash
#
# Or run locally:
#   bash install.sh
#
# What it does:
#   1. Checks your operating system (macOS or Linux)
#   2. Installs the GitHub CLI (gh) if you don't have it
#   3. Installs the Copilot CLI extension if you don't have it
#   4. Copies Sidecar skill files to ~/.copilot/skills/sidecar/
#   5. Copies the launcher to ~/bin/sidecar
#   6. Launches Sidecar
# ─────────────────────────────────────────────────────────────

set -u

# ─── CONSTANTS ──────────────────────────────────────────────
REPO_URL="https://raw.githubusercontent.com/DUBSOpenHub/copilot-sidecar/main"
SKILL_DIR="$HOME/.copilot/skills/sidecar"
BIN_DIR="$HOME/bin"
SIDECAR_DIR="$HOME/.copilot/sidecar"
TMPDIR_INSTALL="${TMPDIR:-/tmp}/copilot-sidecar-install-$$"

# Files to download for the skill
SKILL_FILES=(
  "sidecar/SKILL.md"
  "sidecar/jargon-dictionary.json"
  "sidecar/narration-cards.json"
  "sidecar/question-templates.json"
  "sidecar/demos/index.json"
  "sidecar/demos/01-checking-code.jsonl"
  "sidecar/demos/02-running-tests.jsonl"
  "sidecar/demos/03-ai-agents.jsonl"
  "sidecar/README.md"
)

# ─── CLEANUP ────────────────────────────────────────────────
cleanup() {
  rm -rf "$TMPDIR_INSTALL" 2>/dev/null || true
}
trap cleanup EXIT INT TERM

# ─── HELPERS ────────────────────────────────────────────────
# Colors (with fallback for pipes)
if [ -t 1 ] 2>/dev/null; then
  GREEN=$'\033[0;32m'
  YELLOW=$'\033[0;33m'
  RED=$'\033[0;31m'
  BLUE=$'\033[0;34m'
  BOLD=$'\033[1m'
  DIM=$'\033[2m'
  RESET=$'\033[0m'
else
  GREEN="" YELLOW="" RED="" BLUE="" BOLD="" DIM="" RESET=""
fi

info()    { printf "${BLUE}  ℹ ${RESET} %s\n" "$1"; }
success() { printf "${GREEN}  ✅${RESET} %s\n" "$1"; }
warn()    { printf "${YELLOW}  ⚠️ ${RESET} %s\n" "$1"; }
fail()    { printf "${RED}  ❌${RESET} %s\n" "$1"; }

spin() {
  local msg="$1"
  local pid="$2"
  local frames='⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏'
  local i=0
  while kill -0 "$pid" 2>/dev/null; do
    local frame="${frames:i%${#frames}:1}"
    printf "\r  ${BLUE}%s${RESET} %s" "$frame" "$msg"
    i=$((i + 1))
    sleep 0.1
  done
  printf "\r"
}

banner() {
  echo ""
  printf "${BOLD}"
  echo "  ╔═══════════════════════════════════════════╗"
  echo "  ║                                           ║"
  echo "  ║   🔭  Copilot Sidecar Installer           ║"
  echo "  ║                                           ║"
  echo "  ║   Your friendly terminal translator       ║"
  echo "  ║                                           ║"
  echo "  ╚═══════════════════════════════════════════╝"
  printf "${RESET}"
  echo ""
}

# ─── OS DETECTION ───────────────────────────────────────────
detect_os() {
  case "$(uname -s)" in
    Darwin) OS="macos" ;;
    Linux)  OS="linux" ;;
    *)
      fail "Unsupported operating system: $(uname -s)"
      echo "  Sidecar works on macOS and Linux."
      echo "  For Windows, use WSL (Windows Subsystem for Linux)."
      exit 1
      ;;
  esac
  success "Detected operating system: ${BOLD}$OS${RESET}"
}

# ─── DEPENDENCY CHECKS ─────────────────────────────────────
check_curl() {
  if ! command -v curl >/dev/null 2>&1; then
    fail "curl is not installed"
    echo "  curl is a tool for downloading files from the internet."
    if [ "$OS" = "macos" ]; then
      echo "  On macOS, it should be pre-installed. Try restarting your terminal."
    else
      echo "  Install it with: sudo apt install curl"
    fi
    exit 1
  fi
  success "curl is available"
}

check_gh() {
  if command -v gh >/dev/null 2>&1; then
    success "GitHub CLI (gh) is installed"
    return 0
  fi

  warn "GitHub CLI (gh) is not installed — installing now..."
  echo ""
  info "The GitHub CLI is a tool that lets you interact with GitHub from your terminal."
  echo ""

  if [ "$OS" = "macos" ]; then
    if command -v brew >/dev/null 2>&1; then
      info "Installing via Homebrew (the macOS package manager)..."
      if brew install gh --quiet 2>/dev/null; then
        success "GitHub CLI installed"
        return 0
      fi
    fi
    fail "Could not install GitHub CLI automatically."
    echo "  Please install it manually: https://cli.github.com"
    exit 1

  elif [ "$OS" = "linux" ]; then
    if command -v apt-get >/dev/null 2>&1; then
      info "Installing via apt (the Linux package manager)..."
      (
        curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg \
          | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg 2>/dev/null \
        && sudo chmod go+r /usr/share/keyrings/githubcli-archive-keyring.gpg \
        && echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" \
          | sudo tee /etc/apt/sources.list.d/github-cli.list >/dev/null \
        && sudo apt-get update -qq \
        && sudo apt-get install -y -qq gh
      ) 2>/dev/null
      if command -v gh >/dev/null 2>&1; then
        success "GitHub CLI installed"
        return 0
      fi
    fi
    fail "Could not install GitHub CLI automatically."
    echo "  Please install it manually: https://cli.github.com"
    exit 1
  fi
}

check_copilot_extension() {
  # Copilot may be built-in to gh CLI (newer versions) or an extension (older)
  if gh copilot --version >/dev/null 2>&1; then
    success "GitHub Copilot CLI is available"
    return 0
  fi

  # Try installing as extension (older gh versions)
  warn "Copilot CLI is not available — installing now..."
  info "This lets GitHub Copilot work in your terminal."
  echo ""

  if gh extension install github/gh-copilot 2>/dev/null; then
    success "Copilot CLI extension installed"
    return 0
  fi

  # Check again — might have become available after extension install
  if gh copilot --version >/dev/null 2>&1; then
    success "GitHub Copilot CLI is available"
    return 0
  fi

  fail "Could not set up the Copilot CLI."
  echo "  Make sure you're logged in to GitHub CLI: gh auth login"
  echo "  Then try running this installer again."
  exit 1
}

# ─── INSTALL SKILL FILES ───────────────────────────────────
install_skill_files() {
  info "Copying Sidecar skill files..."
  echo ""

  mkdir -p "$SKILL_DIR/demos"

  # Determine source: local checkout or remote download
  local source_mode="remote"
  local script_dir
  script_dir="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" 2>/dev/null && pwd)"

  # If running from a local checkout with the sidecar/ directory, copy locally
  if [ -f "${script_dir}/sidecar/SKILL.md" ]; then
    source_mode="local"
  fi

  local file
  for file in "${SKILL_FILES[@]}"; do
    local basename
    basename="$(echo "$file" | sed 's|^sidecar/||')"
    local dest="$SKILL_DIR/$basename"

    mkdir -p "$(dirname "$dest")"

    if [ "$source_mode" = "local" ]; then
      cp "${script_dir}/${file}" "$dest"
    else
      if ! curl -fsSL "${REPO_URL}/${file}" -o "$dest" 2>/dev/null; then
        fail "Failed to download: $file"
        echo "  Check your internet connection and try again."
        exit 1
      fi
    fi
    success "$basename"
  done

  echo ""
  success "Skill files installed to ${DIM}~/.copilot/skills/sidecar/${RESET}"
}

# ─── INSTALL LAUNCHER ──────────────────────────────────────
install_launcher() {
  info "Installing the sidecar launcher..."
  echo ""

  mkdir -p "$BIN_DIR"

  local script_dir
  script_dir="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" 2>/dev/null && pwd)"

  if [ -f "${script_dir}/sidecar.sh" ]; then
    cp "${script_dir}/sidecar.sh" "$BIN_DIR/sidecar"
  else
    if ! curl -fsSL "${REPO_URL}/sidecar.sh" -o "$BIN_DIR/sidecar" 2>/dev/null; then
      fail "Failed to download the launcher"
      exit 1
    fi
  fi

  chmod +x "$BIN_DIR/sidecar"
  success "Launcher installed to ${DIM}~/bin/sidecar${RESET}"

  # Ensure ~/bin is in PATH
  if ! echo "$PATH" | tr ':' '\n' | grep -q "^${BIN_DIR}$"; then
    warn "~/bin is not in your PATH yet"
    echo ""
    info "Add this line to your shell profile (~/.bashrc, ~/.zshrc, or similar):"
    echo ""
    echo "    export PATH=\"\$HOME/bin:\$PATH\""
    echo ""
    info "Then restart your terminal, or run:"
    echo ""
    echo "    export PATH=\"\$HOME/bin:\$PATH\""
    echo ""
    # Add to PATH for this session
    export PATH="$BIN_DIR:$PATH"
  fi
}

# ─── CREATE RUNTIME DIRECTORY ──────────────────────────────
create_runtime_dir() {
  mkdir -p "$SIDECAR_DIR"
  success "Runtime directory ready: ${DIM}~/.copilot/sidecar/${RESET}"
}

# ─── SUCCESS BANNER ────────────────────────────────────────
show_success() {
  echo ""
  printf "${GREEN}${BOLD}"
  echo "  ╔═══════════════════════════════════════════╗"
  echo "  ║                                           ║"
  echo "  ║   🎉  Sidecar is installed!               ║"
  echo "  ║                                           ║"
  echo "  ╚═══════════════════════════════════════════╝"
  printf "${RESET}"
  echo ""
  echo "  To launch Sidecar, run:"
  echo ""
  printf "    ${BOLD}sidecar${RESET}          ← with tmux (side-by-side panels)\n"
  printf "    ${BOLD}sidecar --solo${RESET}   ← without tmux (single panel)\n"
  echo ""
  echo "  📖 Learn more: https://github.com/DUBSOpenHub/copilot-sidecar"
  echo ""

  if command -v tmux >/dev/null 2>&1; then
    info "tmux is installed — you'll get the full side-by-side experience!"
  else
    info "tmux is not installed — that's OK! Use ${BOLD}sidecar --solo${RESET} for now."
    if [ "$OS" = "macos" ]; then
      echo "  To get the full experience later: brew install tmux"
    else
      echo "  To get the full experience later: sudo apt install tmux"
    fi
  fi
  echo ""
}

# ─── OFFER TO LAUNCH ───────────────────────────────────────
offer_launch() {
  # Only prompt if we have a TTY (interactive)
  if [ -t 0 ] 2>/dev/null || [ -e /dev/tty ]; then
    echo "  🚀 Want to launch Sidecar now?"
    echo ""
    printf "  Type ${BOLD}y${RESET} and press Enter (or just press Enter to skip): "

    local answer=""
    if [ -t 0 ] 2>/dev/null; then
      read -r answer
    elif [ -e /dev/tty ]; then
      read -r answer < /dev/tty
    fi

    if [ "${answer:-}" = "y" ] || [ "${answer:-}" = "Y" ] || [ "${answer:-}" = "yes" ]; then
      echo ""
      info "Launching Sidecar..."
      echo ""
      if command -v tmux >/dev/null 2>&1; then
        exec sidecar
      else
        exec sidecar --solo
      fi
    else
      echo ""
      echo "  No problem! Run ${BOLD}sidecar${RESET} whenever you're ready. 🔭"
      echo ""
    fi
  fi
}

# ─── MAIN ───────────────────────────────────────────────────
main() {
  banner

  echo "  ${DIM}Step 1 of 5:${RESET} Checking your system..."
  echo ""
  detect_os
  check_curl
  echo ""

  echo "  ${DIM}Step 2 of 5:${RESET} Checking for GitHub CLI..."
  echo ""
  check_gh
  echo ""

  echo "  ${DIM}Step 3 of 5:${RESET} Checking for Copilot CLI extension..."
  echo ""
  check_copilot_extension
  echo ""

  echo "  ${DIM}Step 4 of 5:${RESET} Installing Sidecar files..."
  echo ""
  install_skill_files
  install_launcher
  create_runtime_dir
  echo ""

  echo "  ${DIM}Step 5 of 5:${RESET} All done!"
  show_success
  offer_launch
}

main "$@"
