#!/usr/bin/env bash
# sidecar.sh — Copilot Sidecar launcher with preflight
# Install to: /usr/local/bin/sidecar (or ~/bin/sidecar)
#
# Usage:
#   sidecar          — launch with tmux split pane
#   sidecar --solo   — launch without tmux (solo mode)
#   sidecar --help   — show usage

set -euo pipefail

# ─── CONFIG ─────────────────────────────────────────────────
SIDECAR_DIR="$HOME/.copilot/sidecar"
SKILL_DIR="$HOME/.copilot/skills/sidecar"
SKILL_PATH="$SKILL_DIR/SKILL.md"
SESSION_NAME="copilot-sidecar"
LOG_FILE="$SIDECAR_DIR/launcher.log"
SIDECAR_VERSION="1.0.0"

# ─── HELPERS ────────────────────────────────────────────────
log_event() {
  local event="$1"
  local detail="${2:-}"
  mkdir -p "$SIDECAR_DIR"
  printf '{"ts":"%s","event":"%s","detail":"%s","pid":%d}\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$event" "$detail" $$ >> "$LOG_FILE"
}

print_banner() {
  echo ""
  echo "  🔭 Copilot Sidecar v${SIDECAR_VERSION}"
  echo "  ─────────────────────────────"
  echo "  Your friendly terminal companion"
  echo ""
}

print_usage() {
  print_banner
  echo "  Usage:"
  echo "    sidecar          Launch with tmux (side-by-side panels)"
  echo "    sidecar --solo   Launch without tmux (single panel)"
  echo "    sidecar --help   Show this help message"
  echo ""
  echo "  Commands (inside Sidecar):"
  echo "    safe?       Check if everything is OK"
  echo "    chips       Show suggested questions"
  echo "    glossary    See terms you've learned"
  echo "    expert      Switch to developer mode"
  echo "    beginner    Switch to simple mode"
  echo ""
}

# ─── ARGS ───────────────────────────────────────────────────
SOLO_MODE=false

for arg in "$@"; do
  case "$arg" in
    --solo)
      SOLO_MODE=true
      ;;
    --help|-h)
      print_usage
      exit 0
      ;;
    *)
      echo "Unknown option: $arg"
      print_usage
      exit 1
      ;;
  esac
done

# ─── RUNTIME DIRS ───────────────────────────────────────────
mkdir -p "$SIDECAR_DIR"
mkdir -p "$SIDECAR_DIR/runtime/pane-capture"
mkdir -p "$SIDECAR_DIR/feed"

# ─── PREFLIGHT ──────────────────────────────────────────────
preflight_pass=true
preflight_errors=()

print_banner
echo "  🔍 Checking your setup..."
echo ""

# Check 1: gh CLI available (required for all modes)
if ! command -v gh &>/dev/null; then
  preflight_pass=false
  preflight_errors+=("gh_missing")
fi

# Check 2: Skill file installed
if [[ ! -f "$SKILL_PATH" ]]; then
  preflight_pass=false
  preflight_errors+=("skill_missing")
fi

# Check 3: tmux available (required for split mode only)
tmux_available=true
if ! command -v tmux &>/dev/null; then
  tmux_available=false
  if [[ "$SOLO_MODE" == "false" ]]; then
    preflight_errors+=("tmux_missing")
  fi
fi

# Check 4: Already inside tmux?
already_in_tmux=false
if [[ -n "${TMUX:-}" ]]; then
  already_in_tmux=true
fi

# ─── PREFLIGHT REPORT ──────────────────────────────────────
if [[ ${#preflight_errors[@]} -gt 0 ]]; then
  echo "  ┌─────────────────────────────────────────────────────────┐"
  echo "  │  ⚠️  Sidecar needs a quick one-time setup               │"
  echo "  └─────────────────────────────────────────────────────────┘"
  echo ""

  has_blocking_error=false

  for err in "${preflight_errors[@]}"; do
    case "$err" in
      tmux_missing)
        echo "    📦 tmux not found (splits your screen into two panels)."
        echo "       On Mac:    brew install tmux"
        echo "       On Ubuntu: sudo apt install tmux"
        echo ""
        ;;
      gh_missing)
        echo "    📦 GitHub CLI (gh) not found."
        echo "       Install: https://cli.github.com"
        echo ""
        has_blocking_error=true
        ;;
      skill_missing)
        echo "    📦 Sidecar skill not installed."
        echo "       Run: gh copilot skill install sidecar"
        echo ""
        has_blocking_error=true
        ;;
    esac
  done

  if [[ "$has_blocking_error" == "true" ]]; then
    echo "    After fixing the above, run 'sidecar' again."
    echo ""
    echo "    ──────────────────────────────────────────────────────"
    echo "    🟢 Can't fix right now? You can still try Sidecar in"
    echo "       solo mode — no split screen needed:"
    echo ""
    echo "       gh copilot --skill sidecar"
    echo "    ──────────────────────────────────────────────────────"
    echo ""

    log_event "preflight_failed" "$(IFS=,; echo "${preflight_errors[*]}")"
    exit 1
  fi

  # tmux missing but gh and skill are fine → suggest solo mode
  if [[ "$tmux_available" == "false" && "$SOLO_MODE" == "false" ]]; then
    echo "    ──────────────────────────────────────────────────────"
    echo "    tmux isn't available, so I'll launch in solo mode."
    echo "    (Install tmux for the side-by-side experience.)"
    echo "    ──────────────────────────────────────────────────────"
    echo ""
    SOLO_MODE=true
  fi
fi

echo "  ✅ All checks passed."
echo ""

# ─── WRITE SESSION LINK ────────────────────────────────────
if [[ "$SOLO_MODE" == "true" ]]; then
  session_mode="solo"
else
  session_mode="split"
fi

cat > "$SIDECAR_DIR/session-link.json" <<EOF
{
  "cwd": "$(pwd)",
  "started_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "launcher_pid": $$,
  "mode": "$session_mode"
}
EOF

log_event "launch" "mode=$session_mode"

# ─── SOLO MODE ──────────────────────────────────────────────
if [[ "$SOLO_MODE" == "true" ]]; then
  echo "  🚀 Launching Sidecar in solo mode..."
  echo "  ─────────────────────────────────────"
  echo "  (Tip: Install tmux for a side-by-side experience)"
  echo ""
  exec gh copilot --skill sidecar
fi

# ─── TMUX SPLIT MODE ───────────────────────────────────────

# If already inside tmux, split the current window
if [[ "$already_in_tmux" == "true" ]]; then
  echo "  🔭 Splitting your current tmux window..."
  MAIN_PANE_ID=$(tmux display-message -p '#{pane_id}')
  tmux split-window -h -p 35 "gh copilot --skill sidecar"
  SIDECAR_PANE_ID=$(tmux display-message -p '#{pane_id}')

  # Label panes (silently fail if unsupported)
  tmux select-pane -t "$MAIN_PANE_ID" -T "MAIN" 2>/dev/null || true
  tmux select-pane -t "$SIDECAR_PANE_ID" -T "SIDECAR (READ-ONLY)" 2>/dev/null || true

  # Write pane metadata
  cat > "$SIDECAR_DIR/runtime/pane-capture/main.pane.json" <<EOF
{
  "tmux_session": "$(tmux display-message -p '#{session_name}')",
  "tmux_window": "$(tmux display-message -p '#{window_index}')",
  "main_pane_id": "$MAIN_PANE_ID",
  "sidecar_pane_id": "$SIDECAR_PANE_ID",
  "attached_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "cwd_hint": "$(pwd)",
  "capture_lines": 2000
}
EOF

  # Return focus to the main pane
  tmux select-pane -t "$MAIN_PANE_ID"
  log_event "tmux_split" "pane=$SIDECAR_PANE_ID"
  exit 0
fi

# Not in tmux — check for existing sidecar session
if tmux has-session -t "$SESSION_NAME" 2>/dev/null; then
  echo "  🔄 Reconnecting to your Sidecar session..."
  log_event "tmux_reattach" "session=$SESSION_NAME"
  exec tmux attach-session -t "$SESSION_NAME"
fi

# Create a new tmux session with sidecar pane
echo "  🚀 Launching Sidecar..."
tmux new-session -d -s "$SESSION_NAME" -x "$(tput cols)" -y "$(tput lines)"

MAIN_PANE_ID=$(tmux display-message -t "$SESSION_NAME:0" -p '#{pane_id}')
tmux split-window -h -p 35 -t "$SESSION_NAME:0" "gh copilot --skill sidecar"
SIDECAR_PANE_ID=$(tmux display-message -t "$SESSION_NAME:0" -p '#{pane_id}')

# Label panes
tmux select-pane -t "$MAIN_PANE_ID" -T "MAIN" 2>/dev/null || true
tmux select-pane -t "$SIDECAR_PANE_ID" -T "SIDECAR (READ-ONLY)" 2>/dev/null || true

# Write pane metadata
cat > "$SIDECAR_DIR/runtime/pane-capture/main.pane.json" <<EOF
{
  "tmux_session": "$SESSION_NAME",
  "tmux_window": "0",
  "main_pane_id": "$MAIN_PANE_ID",
  "sidecar_pane_id": "$SIDECAR_PANE_ID",
  "attached_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "cwd_hint": "$(pwd)",
  "capture_lines": 2000
}
EOF

# Focus on the main pane and attach
tmux select-pane -t "$SESSION_NAME:0.0"
log_event "tmux_new_session" "session=$SESSION_NAME"
exec tmux attach-session -t "$SESSION_NAME"
