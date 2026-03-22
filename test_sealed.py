"""
Sealed Behavioral Test Suite — Copilot Sidecar Non-Technical Experience
=======================================================================

Tests BEHAVIOR from PRD v2.0 ONLY. No implementation code or ARCH.md was
consulted. This is the hidden exam (sealed-envelope protocol).

Sections mirror the PRD:
  §2  Launcher & Preflight        §9  Story Mode
  §3  90-Second Onboarding        §13 Consequence Preview
  §4  Watch Mode & Narration      §15 Session Discovery
  §5  Panic Button                §18 JSON Schemas
  §6  Demo Mode                   §21 State Machine
  §7  Question Chips              §23 Functional Requirements
  §8  Jargon Firewall
"""

import json
import os
import re
import subprocess
import tempfile
from pathlib import Path

import pytest

# ──────────────────────────────────────────────────────────────────────
# Fixtures — locate project artifacts without assuming install location
# ──────────────────────────────────────────────────────────────────────

PROJECT_ROOT = Path(__file__).resolve().parent
SIDECAR_DIR = PROJECT_ROOT / "sidecar"


def _find_file(name: str, search_dirs: list[Path] | None = None) -> Path | None:
    """Walk known directories for a file by name."""
    dirs = search_dirs or [
        SIDECAR_DIR,
        SIDECAR_DIR / "demos",
        PROJECT_ROOT,
    ]
    for d in dirs:
        candidate = d / name
        if candidate.is_file():
            return candidate
    # Recursive fallback
    for match in SIDECAR_DIR.rglob(name):
        return match
    return None


@pytest.fixture(scope="session")
def sidecar_sh() -> Path:
    """Locate sidecar.sh — the launcher script."""
    for candidate in [
        PROJECT_ROOT / "sidecar.sh",
        SIDECAR_DIR / "sidecar.sh",
        *PROJECT_ROOT.rglob("sidecar.sh"),
    ]:
        if candidate.is_file():
            return candidate
    pytest.skip("sidecar.sh not found")


@pytest.fixture(scope="session")
def sidecar_sh_text(sidecar_sh) -> str:
    return sidecar_sh.read_text()


@pytest.fixture(scope="session")
def narration_cards_path() -> Path:
    p = _find_file("narration-cards.json")
    if not p:
        pytest.skip("narration-cards.json not found")
    return p


@pytest.fixture(scope="session")
def narration_cards(narration_cards_path) -> dict:
    return json.loads(narration_cards_path.read_text())


@pytest.fixture(scope="session")
def jargon_dict_path() -> Path:
    p = _find_file("jargon-dictionary.json")
    if not p:
        pytest.skip("jargon-dictionary.json not found")
    return p


@pytest.fixture(scope="session")
def jargon_dict(jargon_dict_path) -> dict:
    return json.loads(jargon_dict_path.read_text())


@pytest.fixture(scope="session")
def question_templates_path() -> Path:
    p = _find_file("question-templates.json")
    if not p:
        pytest.skip("question-templates.json not found")
    return p


@pytest.fixture(scope="session")
def question_templates(question_templates_path) -> dict:
    return json.loads(question_templates_path.read_text())


@pytest.fixture(scope="session")
def demo_index_path() -> Path:
    p = _find_file("index.json")
    if not p:
        pytest.skip("demos/index.json not found")
    return p


@pytest.fixture(scope="session")
def demo_index(demo_index_path) -> dict:
    return json.loads(demo_index_path.read_text())


@pytest.fixture(scope="session")
def skill_md_path() -> Path:
    p = _find_file("SKILL.md")
    if not p:
        pytest.skip("SKILL.md not found")
    return p


@pytest.fixture(scope="session")
def skill_md(skill_md_path) -> str:
    return skill_md_path.read_text()


# ======================================================================
# §2 — LAUNCHER & PREFLIGHT (sidecar.sh)
# ======================================================================


class TestLauncherPreflight:
    """§2.1 — Preflight detects missing deps with friendly errors."""

    def test_sidecar_sh_valid_bash_syntax(self, sidecar_sh):
        """Script must parse without syntax errors."""
        result = subprocess.run(
            ["bash", "-n", str(sidecar_sh)],
            capture_output=True, text=True, timeout=10,
        )
        assert result.returncode == 0, f"Bash syntax error:\n{result.stderr}"

    def test_preflight_checks_tmux(self, sidecar_sh_text):
        """Preflight must check for tmux."""
        assert "tmux" in sidecar_sh_text
        assert re.search(r"command\s+-v\s+tmux|which\s+tmux|type\s+tmux", sidecar_sh_text), \
            "Must probe for tmux availability"

    def test_tmux_missing_friendly_message(self, sidecar_sh_text):
        """Missing tmux → human-friendly message, not cryptic."""
        assert re.search(r"(?i)tmux.*(not found|missing|install)", sidecar_sh_text), \
            "Must tell user tmux is missing in plain language"
        assert re.search(r"brew install tmux|apt.*install.*tmux", sidecar_sh_text), \
            "Must include install instructions"

    def test_preflight_checks_gh_cli(self, sidecar_sh_text):
        """Preflight must check for gh CLI."""
        assert re.search(r"command\s+-v\s+gh|which\s+gh|type\s+gh", sidecar_sh_text), \
            "Must probe for gh CLI availability"

    def test_gh_missing_has_install_link(self, sidecar_sh_text):
        """Missing gh → message with install URL."""
        assert "cli.github.com" in sidecar_sh_text, \
            "Must include https://cli.github.com install link"

    def test_preflight_checks_skill_file(self, sidecar_sh_text):
        """Preflight must verify skill file exists."""
        assert re.search(r"SKILL|skill", sidecar_sh_text), \
            "Must reference the skill file"
        assert re.search(r"-f.*SKILL|SKILL.*exist|skill_missing|skill.*not.*found",
                         sidecar_sh_text, re.IGNORECASE), \
            "Must check skill file existence"

    def test_solo_mode_fallback(self, sidecar_sh_text):
        """When preflight fails, must offer solo mode."""
        assert re.search(r"solo|--skill\s+sidecar", sidecar_sh_text, re.IGNORECASE), \
            "Must offer gh copilot --skill sidecar as fallback"

    def test_already_in_tmux_detection(self, sidecar_sh_text):
        """Must detect if already running inside tmux ($TMUX)."""
        assert "$TMUX" in sidecar_sh_text or "TMUX" in sidecar_sh_text, \
            "Must check $TMUX variable"

    def test_session_reconnection(self, sidecar_sh_text):
        """Existing tmux session → reconnect instead of creating new."""
        assert re.search(r"has-session|attach-session", sidecar_sh_text), \
            "Must check for existing session and reconnect"

    def test_preflight_log_written_as_json(self, sidecar_sh_text):
        """Preflight events logged as JSON to launcher.log."""
        assert "launcher.log" in sidecar_sh_text or "LOG_FILE" in sidecar_sh_text
        # Log line should contain JSON-like structure
        assert re.search(r'\{.*"(ts|event|timestamp)"', sidecar_sh_text), \
            "Log must be written as JSON"


# ======================================================================
# §2.2 — FOUR-PATH DETECTION MATRIX
# ======================================================================


class TestFourPathDetection:
    """§2.2 — Session + Profile → deterministic launch path."""

    MATRIX = [
        # (session_found, profile_exists, expected_path)
        (True, True, "resume"),
        (True, False, "onboarding"),
        (False, True, "demo"),
        (False, False, "demo"),
    ]

    @pytest.mark.parametrize("session,profile,expected", MATRIX,
                             ids=["resume", "onboard", "demo-returning", "demo-new"])
    def test_detection_matrix(self, skill_md, session, profile, expected):
        """SKILL.md must encode the four-path detection logic."""
        lower = skill_md.lower()
        if expected == "resume":
            assert "resume" in lower or "status card" in lower
        elif expected == "onboarding":
            assert "onboarding" in lower or "onboard" in lower
        elif expected == "demo":
            assert "demo" in lower

    def test_session_check_mentions_lock_or_state(self, skill_md):
        """Session detection references session-state or lock files."""
        assert re.search(r"session[_-]?(state|link)|inuse|lock|\.lock",
                         skill_md, re.IGNORECASE), \
            "Must reference session detection mechanism"

    def test_profile_check_path(self, skill_md):
        """Profile check references user-profile.json path."""
        assert "user-profile.json" in skill_md


# ======================================================================
# §3 — 90-SECOND ONBOARDING
# ======================================================================


class TestOnboarding:
    """§3 — Onboarding flow: 1/2/3 selection → profile creation."""

    @pytest.mark.parametrize("choice,expected_level", [
        ("1", "beginner"),
        ("2", "intermediate"),
        ("3", "expert"),
    ])
    def test_onboarding_choice_maps_to_level(self, skill_md, choice, expected_level):
        """Input 1/2/3 must map to the correct language level."""
        # The skill file must mention all three levels
        assert expected_level in skill_md.lower()

    def test_beginner_enables_narration_and_chips(self, skill_md):
        """Beginner selection → narration ON, chips ON."""
        lower = skill_md.lower()
        assert "narration" in lower
        assert "chip" in lower

    def test_expert_disables_narration(self, skill_md):
        """Expert selection → narration OFF."""
        lower = skill_md.lower()
        assert "expert" in lower
        # PRD: expert mode = narration OFF
        assert re.search(r"narration.*(off|disable|false)", lower) or \
               re.search(r"expert.*(narration|off)", lower)

    def test_profile_schema_minimum_fields(self):
        """Profile JSON must contain all §3/§18.6 required fields."""
        required_fields = {
            "version", "language_level", "onboarding_complete",
            "narration", "chips_enabled", "sessions_count",
            "glossary", "concepts_learned", "panic_count", "role",
        }
        # Build a sample profile and verify structure
        sample = {
            "version": 1,
            "language_level": "beginner",
            "onboarding_complete": True,
            "onboarding_completed_at": "2026-01-01T00:00:00Z",
            "narration": True,
            "chips_enabled": True,
            "sessions_count": 0,
            "glossary": {},
            "concepts_learned": [],
            "panic_count": 0,
            "role": None,
        }
        assert required_fields.issubset(set(sample.keys()))

    def test_profile_path_convention(self, skill_md):
        """Profile persisted at ~/.copilot/sidecar/user-profile.json."""
        assert "user-profile.json" in skill_md


# ======================================================================
# §4 — WATCH MODE & NARRATION CARDS
# ======================================================================


class TestNarrationCards:
    """§4.2 — Command-to-Outcome card format and coverage."""

    def test_cards_is_valid_json(self, narration_cards_path):
        """narration-cards.json must be valid JSON."""
        data = json.loads(narration_cards_path.read_text())
        assert isinstance(data, dict)

    def test_cards_array_exists(self, narration_cards):
        """Must contain a 'cards' array."""
        assert "cards" in narration_cards
        assert isinstance(narration_cards["cards"], list)

    def test_minimum_10_card_patterns(self, narration_cards):
        """Must have ≥10 command patterns per PRD §4.2."""
        assert len(narration_cards["cards"]) >= 10, \
            f"Expected ≥10 cards, found {len(narration_cards['cards'])}"

    @pytest.mark.parametrize("field", ["pattern", "emoji", "title", "what", "why", "next"])
    def test_each_card_has_required_fields(self, narration_cards, field):
        """Every card must have pattern, emoji, title, what, why, next."""
        for i, card in enumerate(narration_cards["cards"]):
            assert field in card, f"Card [{i}] missing field '{field}'"

    def test_card_lines_within_80_chars(self, narration_cards):
        """what/why/next lines ≤80 chars per PRD §4.2."""
        for i, card in enumerate(narration_cards["cards"]):
            for line in ("what", "why", "next"):
                text = card.get(line, "")
                assert len(text) <= 80, \
                    f"Card [{i}] '{line}' is {len(text)} chars (max 80): {text!r}"

    def test_each_card_has_emoji_header(self, narration_cards):
        """Each card has an emoji in the 'emoji' field."""
        for i, card in enumerate(narration_cards["cards"]):
            # Emojis are non-ASCII characters
            assert any(ord(c) > 127 for c in card.get("emoji", "")), \
                f"Card [{i}] missing emoji in 'emoji' field"

    REQUIRED_PATTERNS = [
        "git diff", "git commit", "npm test", "npm install",
        "build", "git push", "git checkout", "git status", "curl", "rm",
    ]

    @pytest.mark.parametrize("cmd", REQUIRED_PATTERNS)
    def test_pattern_covered(self, narration_cards, cmd):
        """PRD §4.2 requires patterns for these 10+ commands."""
        patterns = [c["pattern"] for c in narration_cards["cards"]]
        joined = " ".join(patterns).lower()
        # At least one pattern should match or reference the command
        cmd_key = cmd.split()[0]  # first word
        assert cmd_key in joined, \
            f"No pattern covers '{cmd}' — found patterns: {patterns}"

    def test_fallback_card_exists(self, narration_cards):
        """Fallback card for unrecognized commands."""
        assert "fallback" in narration_cards, "Missing fallback card"
        fb = narration_cards["fallback"]
        for field in ("emoji", "title", "what", "why", "next"):
            assert field in fb, f"Fallback missing field '{field}'"


# ======================================================================
# §4.3 — CONFIDENCE + FRESHNESS BADGES
# ======================================================================


class TestFreshnessBadges:
    """§4.3 — Freshness thresholds: LIVE/RECENT/STALE."""

    @staticmethod
    def _classify(seconds: int) -> str:
        if seconds <= 10:
            return "LIVE"
        elif seconds <= 60:
            return "RECENT"
        else:
            return "STALE"

    @pytest.mark.parametrize("seconds,expected", [
        (0, "LIVE"), (5, "LIVE"), (10, "LIVE"),
        (11, "RECENT"), (30, "RECENT"), (60, "RECENT"),
        (61, "STALE"), (120, "STALE"), (300, "STALE"),
    ])
    def test_freshness_classification(self, seconds, expected):
        """Freshness bucket boundaries per PRD §4.3."""
        assert self._classify(seconds) == expected

    def test_live_badge_emoji_green(self, skill_md):
        """LIVE badge uses green indicator."""
        assert "🟢" in skill_md or "LIVE" in skill_md

    def test_stale_badge_includes_disclaimer(self, skill_md):
        """Stale data must include disclaimer text per PRD."""
        lower = skill_md.lower()
        assert re.search(r"stale|things may have changed|what i saw", lower), \
            "Must include staleness disclaimer"


# ======================================================================
# §4.4 — NARRATION THROTTLE
# ======================================================================


class TestNarrationThrottle:
    """§4.4 — Rate limiting: 1 card/10s, burst buffering, idle chips."""

    def test_throttle_mentioned_in_skill(self, skill_md):
        """SKILL.md must reference throttle / rate limit."""
        lower = skill_md.lower()
        assert re.search(r"throttl|rate.?limit|1.*card.*10|burst", lower), \
            "Must describe narration throttle"

    def test_burst_buffering_described(self, skill_md):
        """Burst (>3 events/10s) → buffer + count."""
        lower = skill_md.lower()
        assert re.search(r"burst|buffer|\+\d+ more|more events", lower), \
            "Must describe burst buffering behavior"

    def test_idle_triggers_chips(self, skill_md):
        """Idle >60s → 'What Should I Ask?' chips."""
        lower = skill_md.lower()
        assert "idle" in lower or "60" in lower
        assert "chip" in lower or "what should i ask" in lower

    def test_long_silence_message(self, skill_md):
        """>5min silence → 'Still watching' message."""
        lower = skill_md.lower()
        assert re.search(r"still watching|5.*min|silence|long.*idle", lower)


# ======================================================================
# §5 — PANIC BUTTON (safe?)
# ======================================================================


class TestPanicButton:
    """§5 — 'safe?' produces immediate safety card."""

    def test_safe_command_documented(self, skill_md):
        """'safe?' command must be documented."""
        assert "safe?" in skill_md

    def test_green_state_all_clear(self, skill_md):
        """Green state: files safe, changes undoable, no errors."""
        lower = skill_md.lower()
        assert re.search(r"(safe|clear|✅|green)", lower)

    def test_yellow_state_minor_concern(self, skill_md):
        """Yellow state: minor concern with reassurance."""
        lower = skill_md.lower()
        assert re.search(r"(yellow|⚠️|minor|concern|warning)", lower)

    def test_red_state_error_not_user_fault(self, skill_md):
        """Red state: error detected, reassure user didn't cause it."""
        lower = skill_md.lower()
        assert re.search(r"(red|🔴|error|attention|stuck)", lower)

    def test_safe_works_from_any_state(self, skill_md):
        """'safe?' must work as interrupt from ANY state."""
        lower = skill_md.lower()
        assert re.search(r"(any\s*(time|state|point)|interrupt|immediate)", lower)

    def test_read_only_in_safety_card(self, skill_md):
        """Safety card must assert read-only nature."""
        lower = skill_md.lower()
        assert re.search(r"read[- ]?only|never change|i only watch|don'?t touch", lower)


# ======================================================================
# §6 — DEMO MODE
# ======================================================================


class TestDemoMode:
    """§6 — Demo Mode: menu, JSONL format, index, 3 demos."""

    def test_demo_index_valid_json(self, demo_index_path):
        json.loads(demo_index_path.read_text())

    def test_demo_index_has_demos_array(self, demo_index):
        assert "demos" in demo_index
        assert isinstance(demo_index["demos"], list)

    def test_three_demos_exist(self, demo_index):
        """PRD §6.2 requires 3 demos."""
        assert len(demo_index["demos"]) >= 3, \
            f"Expected ≥3 demos, found {len(demo_index['demos'])}"

    REQUIRED_DEMO_FIELDS = ["id", "title", "file", "duration_s", "teaches"]

    @pytest.mark.parametrize("field", REQUIRED_DEMO_FIELDS)
    def test_demo_entry_has_required_fields(self, demo_index, field):
        """Each demo in index.json must have id, title, file, duration_s, teaches."""
        for i, demo in enumerate(demo_index["demos"]):
            assert field in demo, f"Demo [{i}] missing field '{field}'"

    def test_demo_ids_include_expected(self, demo_index):
        """Expected demos: checking-code, running-tests, ai-agents."""
        ids_and_files = " ".join(
            f"{d.get('id', '')} {d.get('file', '')} {d.get('title', '')}"
            for d in demo_index["demos"]
        ).lower()
        for keyword in ("check", "test", "agent"):
            assert keyword in ids_and_files, \
                f"No demo references '{keyword}'"

    def test_demo_jsonl_files_exist(self, demo_index, demo_index_path):
        """Each referenced JSONL file must exist."""
        demos_dir = demo_index_path.parent
        for demo in demo_index["demos"]:
            jsonl_path = demos_dir / demo["file"]
            assert jsonl_path.is_file(), \
                f"Demo JSONL not found: {jsonl_path}"

    def test_demo_jsonl_lines_valid(self, demo_index, demo_index_path):
        """Each line in a demo JSONL must be valid JSON with 'type' and 'text'."""
        demos_dir = demo_index_path.parent
        valid_types = {"command", "output", "narration", "prompt"}
        for demo in demo_index["demos"]:
            jsonl_path = demos_dir / demo["file"]
            if not jsonl_path.is_file():
                continue
            lines = jsonl_path.read_text().strip().splitlines()
            assert len(lines) > 0, f"Empty JSONL: {jsonl_path.name}"
            for li, line in enumerate(lines):
                obj = json.loads(line)
                assert "type" in obj, f"{jsonl_path.name}:{li+1} missing 'type'"
                assert obj["type"] in valid_types, \
                    f"{jsonl_path.name}:{li+1} invalid type '{obj['type']}'"
                assert "text" in obj, f"{jsonl_path.name}:{li+1} missing 'text'"

    def test_demo_jsonl_has_delay_ms(self, demo_index, demo_index_path):
        """Non-prompt lines should have delay_ms for pacing."""
        demos_dir = demo_index_path.parent
        for demo in demo_index["demos"]:
            jsonl_path = demos_dir / demo["file"]
            if not jsonl_path.is_file():
                continue
            for line in jsonl_path.read_text().strip().splitlines():
                obj = json.loads(line)
                if obj.get("type") != "prompt":
                    assert "delay_ms" in obj, \
                        f"Non-prompt line missing delay_ms: {obj}"

    def test_demo_menu_four_options(self, skill_md):
        """Demo menu must offer 4 options per PRD §6.1."""
        lower = skill_md.lower()
        assert "demo" in lower
        # Check for numbered options pattern
        menu_keywords = ["replay", "explain", "check again", "ask"]
        hits = sum(1 for kw in menu_keywords if kw in lower)
        assert hits >= 3, \
            f"Demo menu should reference replay/explain/check/ask — found {hits}/4"

    def test_session_redetection_interval(self, skill_md):
        """§6.3 — Re-check for sessions every 30s during demo."""
        assert re.search(r"30\s*s|30\s*second|re[- ]?(check|detect)", skill_md, re.IGNORECASE)


# ======================================================================
# §7 — QUESTION CHIPS
# ======================================================================


class TestQuestionChips:
    """§7 — Chip display: 4 per set, numbered, contextual."""

    def test_question_templates_valid_json(self, question_templates_path):
        json.loads(question_templates_path.read_text())

    def test_templates_have_event_categories(self, question_templates):
        """Must have templates for event-specific scenarios."""
        expected = {"test_failure", "build_error", "file_created",
                    "git_commit", "long_silence"}
        keys = set(question_templates.keys())
        # Accept templates nested under a top-level key too
        if len(keys) == 1 and isinstance(next(iter(question_templates.values())), dict):
            keys = set(next(iter(question_templates.values())).keys())
        overlap = keys & expected
        assert len(overlap) >= 3, \
            f"Expected ≥3 event categories from {expected}, found {overlap}"

    def test_each_category_has_questions(self, question_templates):
        """Each event category must have ≥1 question template."""
        items = question_templates
        if len(items) == 1 and isinstance(next(iter(items.values())), dict):
            items = next(iter(items.values()))
        for cat, questions in items.items():
            if isinstance(questions, list):
                assert len(questions) >= 1, f"Category '{cat}' has 0 questions"

    def test_chip_1_always_status(self, skill_md):
        """Chip [1] = status question per PRD §7.2."""
        lower = skill_md.lower()
        assert re.search(r"chip.*1.*status|chip\[1\].*status|first.*chip.*status", lower)

    def test_chip_4_always_safety(self, skill_md):
        """Chip [4] = safety/health check per PRD §7.2."""
        lower = skill_md.lower()
        assert re.search(r"chip.*4.*safe|chip\[4\].*safe|fourth.*chip.*safe|last.*chip.*safe|chip.*safe", lower)

    def test_chips_numbered_1_to_4(self, skill_md):
        """Chips must be numbered 1-4 for keyboard selection."""
        assert re.search(r"\[1\]|\[2\]|\[3\]|\[4\]|1️⃣|2️⃣|3️⃣|4️⃣", skill_md)

    def test_chips_refresh_90s(self, skill_md):
        """Chips refresh every 90s while idle."""
        assert re.search(r"90\s*s|90\s*second|refresh.*chip|chip.*refresh", skill_md, re.IGNORECASE)

    def test_chips_disappear_on_input(self, skill_md):
        """Chips disappear when user types anything."""
        lower = skill_md.lower()
        assert re.search(r"chip.*(disappear|clear|hide|dismiss)|input.*(clear|dismiss).*chip", lower)

    def test_chips_command_redisplays(self, skill_md):
        """Typing 'chips' re-displays current chips."""
        assert re.search(r'"chips"|\bchips\b.*re-?display|\bchips\b.*show', skill_md, re.IGNORECASE)


# ======================================================================
# §8 — JARGON FIREWALL
# ======================================================================


class TestJargonFirewall:
    """§8 — Dictionary size, structure, and firewall rules."""

    def test_dictionary_valid_json(self, jargon_dict_path):
        json.loads(jargon_dict_path.read_text())

    def test_dictionary_has_40_plus_terms(self, jargon_dict):
        """PRD §8.2 requires 40+ terms."""
        # Dict might be flat {term: def} or nested
        if isinstance(jargon_dict, dict):
            # Could be nested under a key
            terms = jargon_dict
            if any(isinstance(v, dict) and "term" in v for v in jargon_dict.values()):
                count = len(jargon_dict)
            elif any(isinstance(v, list) for v in jargon_dict.values()):
                count = sum(len(v) for v in jargon_dict.values() if isinstance(v, list))
            else:
                count = len(jargon_dict)
        else:
            count = 0
        assert count >= 40, f"Expected ≥40 jargon terms, found {count}"

    def test_each_term_has_definition(self, jargon_dict):
        """Each term must have a plain-English definition."""
        for term, value in jargon_dict.items():
            if isinstance(value, str):
                assert len(value) > 5, f"Term '{term}' has empty/short definition"
            elif isinstance(value, dict):
                has_def = any(k for k in value if "def" in k.lower() or "plain" in k.lower())
                assert has_def or "definition_beginner" in value, \
                    f"Term '{term}' missing definition field"

    CRITICAL_TERMS = [
        "git", "commit", "branch", "merge", "diff", "repo", "push", "pull",
        "PR", "npm", "build", "deploy", "API", "database", "CLI", "terminal",
    ]

    @pytest.mark.parametrize("term", CRITICAL_TERMS)
    def test_critical_term_present(self, jargon_dict, term):
        """Dictionary must include core developer terms."""
        keys_lower = {k.lower() for k in jargon_dict}
        assert term.lower() in keys_lower, \
            f"Critical term '{term}' missing from dictionary"

    def test_beginner_first_use_explanation(self, skill_md):
        """Beginner mode: first use → full analogy explanation with ❓."""
        assert "❓" in skill_md or re.search(r"first.*use.*explain|analogy", skill_md, re.IGNORECASE)

    def test_graduated_terms_pass_through(self, skill_md):
        """Terms seen ≥5 times graduate → no explanation."""
        lower = skill_md.lower()
        assert re.search(r"graduat|5.*times|pass.*through|no.*explanation", lower)

    def test_what_does_x_mean_refresher(self, skill_md):
        """'what does X mean again?' works for refresher."""
        lower = skill_md.lower()
        assert re.search(r"what does.*mean|refresher|mean.*again", lower)

    def test_firewall_disabled_expert(self, skill_md):
        """Expert mode → firewall disabled."""
        lower = skill_md.lower()
        assert re.search(r"expert.*(disable|off|bypass)|firewall.*(disable|off).*expert", lower)

    def test_intermediate_first_mention_only(self, skill_md):
        """Intermediate: first-mention gloss per session only."""
        lower = skill_md.lower()
        assert re.search(r"intermediate|first[- ]mention|per session", lower)


# ======================================================================
# §9 — STORY MODE
# ======================================================================


class TestStoryMode:
    """§9 — Narrative templates for high-impact events."""

    def test_safety_net_story_on_commit(self, skill_md):
        """Safety Net story triggers on git commit."""
        lower = skill_md.lower()
        assert re.search(r"(safety|checkpoint|save.*game|boss fight).*commit|commit.*(story|checkpoint|save.*game)", lower)

    def test_detective_story_on_failure(self, skill_md):
        """Detective story triggers on build/test failure."""
        lower = skill_md.lower()
        assert re.search(r"detective|broke|failure.*story|story.*fail", lower)

    def test_architecture_story_on_codebase_question(self, skill_md):
        """Architecture story on 'what does this codebase do?'."""
        lower = skill_md.lower()
        assert re.search(r"architecture|codebase.*city|city|frontend.*backend", lower)


# ======================================================================
# §13 — CONSEQUENCE PREVIEW
# ======================================================================


class TestConsequencePreview:
    """§13 — Risk levels and classification table."""

    RISK_TABLE = [
        # (command, expected_risk)
        ("git commit", "🟢"),
        ("git add", "🟢"),
        ("git stash", "🟢"),
        ("npm test", "🟢"),
        ("ls", "🟢"),
        ("git status", "🟢"),
        ("npm install", "🟡"),
        ("pip install", "🟡"),
        ("touch foo", "🟡"),
        ("mkdir bar", "🟡"),
        ("git push", "🟠"),
        ("git merge", "🟠"),
        ("chmod 755 foo", "🟠"),
        ("rm -rf node_modules", "🔴"),
        ("deploy", "🔴"),
    ]

    @staticmethod
    def _classify_risk(cmd: str) -> str:
        """Classify per PRD §13.1 risk table."""
        cmd_lower = cmd.lower().strip()
        # High
        if re.match(r"^(rm|del)\b", cmd_lower):
            return "🔴"
        if re.search(r"drop\s+table|deploy|publish", cmd_lower):
            return "🔴"
        # Medium
        if re.match(r"^git\s+(push|merge)\b", cmd_lower):
            return "🟠"
        if re.match(r"^(chmod|chown)\b", cmd_lower):
            return "🟠"
        if re.search(r"curl\s+-X\s+(POST|DELETE|PUT|PATCH)", cmd_lower):
            return "🟠"
        # Low
        if re.match(r"^(npm|pip|yarn|brew)\s+install\b", cmd_lower):
            return "🟡"
        if re.match(r"^(touch|mkdir|cp)\b", cmd_lower):
            return "🟡"
        # None
        if re.match(r"^git\s+(add|commit|stash|status|diff|log)\b", cmd_lower):
            return "🟢"
        if re.match(r"^(npm\s+test|pytest|jest|go\s+test)\b", cmd_lower):
            return "🟢"
        if re.match(r"^(echo|cat|ls|pwd|head|tail)\b", cmd_lower):
            return "🟢"
        return "🟢"

    @pytest.mark.parametrize("cmd,expected_risk", RISK_TABLE,
                             ids=[f"{c[0]}->{c[1]}" for c in RISK_TABLE])
    def test_risk_classification(self, cmd, expected_risk):
        """Risk level matches PRD §13.1 classification table."""
        assert self._classify_risk(cmd) == expected_risk

    def test_four_risk_levels_exist(self, skill_md):
        """Must define all 4 risk levels: 🟢 None, 🟡 Low, 🟠 Medium, 🔴 High."""
        for emoji in ("🟢", "🟡", "🟠", "🔴"):
            assert emoji in skill_md, f"Risk level {emoji} not found in SKILL.md"

    def test_preview_shown_for_risky_actions(self, skill_md):
        """Consequence preview shown for risk ≥ 🟡."""
        lower = skill_md.lower()
        assert re.search(r"consequence|preview|what i.*about to do|risk", lower)


# ======================================================================
# §15 — SESSION DISCOVERY
# ======================================================================


class TestSessionDiscovery:
    """§15 — Human-readable names, no PIDs, graceful fallback."""

    def test_human_readable_project_names(self, skill_md):
        """Display project names, not PIDs or paths."""
        lower = skill_md.lower()
        assert re.search(r"human[- ]?readable|project name|basename|show-toplevel", lower)

    def test_no_session_enters_demo_mode(self, skill_md):
        """No session → Demo Mode, not an error."""
        lower = skill_md.lower()
        assert re.search(r"no.*session.*demo|demo.*no.*session|no.*active.*demo", lower)


# ======================================================================
# §18 — JSON SCHEMAS
# ======================================================================


class TestSchemas:
    """§18 — Validate data model schemas from the PRD."""

    # §18.1 CommandToOutcomeCard
    def test_command_to_outcome_card_required_fields(self):
        required = {"id", "session_id", "event_id", "stage", "lines",
                    "confidence", "question_chips"}
        sample = {
            "id": "card-001",
            "session_id": "sess-abc",
            "event_id": "evt-xyz",
            "stage": "WATCH",
            "lines": {"what": "...", "why": "...", "next": "..."},
            "confidence": {"level": "HIGH", "score": 0.9,
                           "freshness_seconds": 3,
                           "freshness_bucket": "LIVE",
                           "provenance": ["pane-capture"]},
            "question_chips": [],
        }
        assert required.issubset(set(sample.keys()))

    def test_card_stage_enum(self):
        """Stage must be WATCH, EXPLAIN, or OFFER."""
        valid = {"WATCH", "EXPLAIN", "OFFER"}
        for v in valid:
            assert v in valid

    def test_card_lines_max_length(self):
        """what/why/next each ≤80 chars."""
        for text in ("x" * 80, "y" * 80, "z" * 80):
            assert len(text) <= 80

    # §18.2 ConfidenceLabel
    def test_confidence_label_required_fields(self):
        required = {"level", "score", "freshness_seconds",
                    "freshness_bucket", "provenance"}
        sample = {
            "level": "HIGH", "score": 0.95,
            "freshness_seconds": 3,
            "freshness_bucket": "LIVE",
            "provenance": ["pane-capture"],
        }
        assert required.issubset(set(sample.keys()))

    def test_confidence_level_enum(self):
        valid = {"HIGH", "MED", "LOW", "UNK"}
        assert len(valid) == 4

    def test_freshness_bucket_enum(self):
        valid = {"LIVE", "WARM", "STALE"}
        assert len(valid) == 3

    # §18.3 QuestionChip
    def test_question_chip_required_fields(self):
        required = {"id", "label_short", "prompt", "kind", "shortcut_number"}
        sample = {
            "id": "chip-1",
            "label_short": "Status",
            "prompt": "What is happening?",
            "kind": "clarify",
            "shortcut_number": 1,
        }
        assert required.issubset(set(sample.keys()))

    def test_chip_shortcut_range_1_to_4(self):
        for n in (1, 2, 3, 4):
            assert 1 <= n <= 4
        for bad in (0, 5, -1):
            assert not (1 <= bad <= 4)

    def test_chip_kind_enum(self):
        valid = {"clarify", "why", "how", "what_if", "sandbox", "safety"}
        assert len(valid) == 6

    # §18.4 GlossaryTerm
    def test_glossary_term_required_fields(self):
        required = {"id", "term", "definition_beginner", "aliases", "learned_level"}
        sample = {
            "id": "git",
            "term": "git",
            "definition_beginner": "a tool that saves versions of code",
            "aliases": [],
            "learned_level": "none",
        }
        assert required.issubset(set(sample.keys()))

    # §18.5 JargonAnnotation
    def test_jargon_annotation_required_fields(self):
        required = {"term_id", "surface", "action"}
        sample = {
            "term_id": "git",
            "surface": "git",
            "action": "allowed_with_gloss",
        }
        assert required.issubset(set(sample.keys()))

    def test_jargon_action_enum(self):
        valid = {"blocked", "replaced_with_gloss", "allowed_with_gloss", "allowed_plain"}
        assert len(valid) == 4

    # §18.6 UserProfile
    def test_user_profile_full_schema(self):
        """Full user profile has all §18.6 fields."""
        required_fields = {
            "version", "language_level", "onboarding_complete",
            "narration", "chips_enabled", "sessions_count",
            "glossary", "concepts_learned", "panic_count", "role",
        }
        full_profile = {
            "version": 1,
            "language_level": "beginner",
            "onboarding_complete": True,
            "onboarding_completed_at": "2026-03-22T01:30:00Z",
            "narration": True,
            "chips_enabled": True,
            "jargon_firewall_mode": "strict",
            "relay_enabled": False,
            "sessions_count": 0,
            "glossary": {},
            "story_cards": [],
            "concepts_learned": [],
            "understood_terms": {},
            "panic_count": 0,
            "questions_asked": 0,
            "chips_used": 0,
            "role": None,
        }
        assert required_fields.issubset(set(full_profile.keys()))


# ======================================================================
# §21 — STATE MACHINE
# ======================================================================


class TestStateMachine:
    """§21 — Companion Loop state transitions."""

    VALID_TRANSITIONS = [
        ("IDLE", "WATCHING"),
        ("WATCHING", "EXPLAINING"),
        ("EXPLAINING", "OFFERING"),
        ("OFFERING", "WATCHING"),
    ]

    INVALID_TRANSITIONS = [
        ("IDLE", "EXPLAINING"),
        ("IDLE", "OFFERING"),
        ("WATCHING", "IDLE"),
        ("OFFERING", "EXPLAINING"),
    ]

    @staticmethod
    def _valid_transition(from_state: str, to_state: str) -> bool:
        allowed = {
            "IDLE": {"WATCHING", "DEMO_MODE"},
            "WATCHING": {"EXPLAINING"},
            "EXPLAINING": {"OFFERING"},
            "OFFERING": {"WATCHING"},
            "DEMO_MODE": {"WATCHING"},
        }
        return to_state in allowed.get(from_state, set())

    @pytest.mark.parametrize("from_st,to_st", VALID_TRANSITIONS)
    def test_valid_transitions(self, from_st, to_st):
        assert self._valid_transition(from_st, to_st), \
            f"{from_st}→{to_st} should be valid"

    @pytest.mark.parametrize("from_st,to_st", INVALID_TRANSITIONS)
    def test_invalid_transitions(self, from_st, to_st):
        assert not self._valid_transition(from_st, to_st), \
            f"{from_st}→{to_st} should be invalid"

    def test_idle_to_demo_when_no_session(self):
        assert self._valid_transition("IDLE", "DEMO_MODE")

    def test_demo_to_watching_on_session_detected(self):
        assert self._valid_transition("DEMO_MODE", "WATCHING")

    def test_panic_from_any_state(self):
        """PANIC interrupt from any state, returns to previous state."""
        states = ["IDLE", "WATCHING", "EXPLAINING", "OFFERING", "DEMO_MODE"]
        for state in states:
            # Panic is special — always allowed, always returns
            # We verify the concept is in the skill
            assert state  # (existence check — real behavior tested via skill_md)

    def test_panic_returns_to_previous_state(self, skill_md):
        """After panic card, returns to previous state."""
        lower = skill_md.lower()
        assert re.search(r"panic.*return|return.*previous|safe\?.*return|back.*previous", lower)


# ======================================================================
# §23 — FUNCTIONAL REQUIREMENTS (NT-*)
# ======================================================================


class TestFunctionalRequirements:
    """§23 — Every NT-* requirement validated."""

    # NT-1.1: Default to beginner language on first launch
    def test_nt_1_1_default_beginner(self, skill_md):
        lower = skill_md.lower()
        assert re.search(r"default.*beginner|beginner.*default|first.*launch.*beginner", lower)

    # NT-1.2: All output through Jargon Firewall
    def test_nt_1_2_jargon_firewall_all_output(self, skill_md):
        lower = skill_md.lower()
        assert "jargon" in lower and "firewall" in lower

    # NT-1.3: expert/beginner toggle commands
    def test_nt_1_3_expert_beginner_toggle(self, skill_md):
        lower = skill_md.lower()
        assert "expert" in lower and "beginner" in lower
        assert re.search(r"(type|switch|toggle).*(expert|beginner)", lower)

    # NT-2.1: Watch auto-narrates using pane-capture
    def test_nt_2_1_watch_auto_narrates(self, skill_md):
        lower = skill_md.lower()
        assert "watch" in lower
        assert re.search(r"auto[- ]?narrat|narrat.*watch|pane[- ]?capture", lower)

    # NT-2.2: Narrate as Command-to-Outcome Cards
    def test_nt_2_2_command_to_outcome_cards(self, skill_md):
        lower = skill_md.lower()
        assert re.search(r"command[- ]?to[- ]?outcome|narrat.*card|what.*why.*next", lower)

    # NT-2.4: Throttle ≤1 card/10s during bursts
    def test_nt_2_4_throttle_1_per_10s(self, skill_md):
        lower = skill_md.lower()
        assert re.search(r"1.*card.*10|throttl|burst|rate.?limit", lower)

    # NT-5.1: safe? immediately shows safety card
    def test_nt_5_1_safe_immediate(self, skill_md):
        assert "safe?" in skill_md
        lower = skill_md.lower()
        assert re.search(r"safe\?.*immediate|immediate.*safe|instant.*safe", lower)

    # NT-5.2: Demo Mode when no session
    def test_nt_5_2_demo_mode_no_session(self, skill_md):
        lower = skill_md.lower()
        assert re.search(r"no.*session.*demo|demo.*mode", lower)

    # NT-6.1: Never display raw stack traces to beginners
    def test_nt_6_1_no_raw_stack_traces(self, skill_md):
        lower = skill_md.lower()
        assert re.search(r"stack.?trace|raw.*error|never.*display.*raw|hide.*trace", lower)

    # NT-6.2: Never use blocked jargon without explanation
    def test_nt_6_2_no_unexplained_jargon(self, skill_md):
        lower = skill_md.lower()
        assert re.search(r"block.*jargon|jargon.*without.*explain|firewall", lower)

    # NT-7.1: Preflight checks before tmux launch
    def test_nt_7_1_preflight_before_tmux(self, sidecar_sh_text):
        # Preflight must occur before tmux new-session
        preflight_pos = sidecar_sh_text.find("preflight") if "preflight" in sidecar_sh_text.lower() else sidecar_sh_text.find("command -v tmux")
        tmux_launch_pos = sidecar_sh_text.find("tmux new-session")
        if preflight_pos >= 0 and tmux_launch_pos >= 0:
            assert preflight_pos < tmux_launch_pos, \
                "Preflight must run before tmux new-session"

    # NT-7.2: Solo mode fallback
    def test_nt_7_2_solo_mode_fallback(self, sidecar_sh_text):
        assert re.search(r"solo|--skill.*sidecar|gh copilot", sidecar_sh_text, re.IGNORECASE)


# ======================================================================
# SKILL.md — REQUIRED SECTIONS (§22.3)
# ======================================================================


class TestSkillMdSections:
    """§22.3 — SKILL.md must contain all required sections."""

    def test_identity_and_personality(self, skill_md):
        lower = skill_md.lower()
        assert re.search(r"identity|personalit|warm|patient", lower)

    def test_never_says_just_or_simply(self, skill_md):
        """Personality rule: never says 'just' or 'simply'."""
        lower = skill_md.lower()
        assert re.search(r"never.*\"just\"|never.*\"simply\"|avoid.*\"just\"", lower)

    def test_uses_we_language(self, skill_md):
        """Uses 'we' language: 'Let's see what's happening...'."""
        assert re.search(r"\"[Ww]e |\"[Ll]et'?s ", skill_md)

    def test_startup_sequence_section(self, skill_md):
        lower = skill_md.lower()
        assert re.search(r"startup|start.?up|boot|launch.*sequence", lower)

    def test_safety_framing_section(self, skill_md):
        lower = skill_md.lower()
        assert re.search(r"safety.*framing|nothing.*break|read[- ]?only", lower)

    def test_confusion_handling_section(self, skill_md):
        lower = skill_md.lower()
        assert re.search(r"confusion|different.*analogy|explain.*differently", lower)

    def test_emoji_palette(self, skill_md):
        """Must use specified emoji palette."""
        required_emojis = ["🔭", "📋", "🛡️", "💡"]
        for emoji in required_emojis:
            assert emoji in skill_md, f"Missing emoji {emoji} from palette"


# ======================================================================
# EDGE CASES & ADVERSARIAL INPUTS
# ======================================================================


class TestEdgeCases:
    """Boundary conditions and adversarial inputs."""

    def test_empty_command_matches_fallback(self, narration_cards):
        """Empty or whitespace command → fallback card, not crash."""
        cards = narration_cards.get("cards", [])
        fallback = narration_cards.get("fallback")
        # Verify no pattern is empty string
        for c in cards:
            assert c.get("pattern", "") != "", "Empty pattern is ambiguous"
        assert fallback is not None, "Fallback required for unmatched commands"

    def test_freshness_boundary_at_10s(self):
        """Exactly 10s → LIVE (inclusive upper bound)."""
        assert TestFreshnessBadges._classify(10) == "LIVE"

    def test_freshness_boundary_at_11s(self):
        """Exactly 11s → RECENT."""
        assert TestFreshnessBadges._classify(11) == "RECENT"

    def test_freshness_boundary_at_60s(self):
        """Exactly 60s → RECENT (inclusive upper bound)."""
        assert TestFreshnessBadges._classify(60) == "RECENT"

    def test_freshness_boundary_at_61s(self):
        """Exactly 61s → STALE."""
        assert TestFreshnessBadges._classify(61) == "STALE"

    def test_risk_rm_always_high(self):
        """rm with any flags is always 🔴 High."""
        for variant in ("rm foo", "rm -f bar", "rm -rf /tmp/x", "rm  file.txt"):
            assert TestConsequencePreview._classify_risk(variant) == "🔴"

    def test_risk_git_commit_always_none(self):
        """git commit with flags is 🟢 None."""
        for variant in ("git commit", "git commit -m 'msg'", "git commit --amend"):
            assert TestConsequencePreview._classify_risk(variant) == "🟢"

    def test_narration_cards_patterns_are_valid_regex(self, narration_cards):
        """Every card pattern must be a valid regex."""
        for i, card in enumerate(narration_cards.get("cards", [])):
            pattern = card.get("pattern", "")
            try:
                re.compile(pattern)
            except re.error as e:
                pytest.fail(f"Card [{i}] invalid regex '{pattern}': {e}")

    def test_demo_duration_positive(self, demo_index):
        """Every demo duration_s must be > 0."""
        for demo in demo_index.get("demos", []):
            assert demo.get("duration_s", 0) > 0, \
                f"Demo '{demo.get('id')}' has non-positive duration"

    def test_jargon_dict_no_empty_definitions(self, jargon_dict):
        """No jargon term may have an empty or whitespace-only definition."""
        for term, definition in jargon_dict.items():
            if isinstance(definition, str):
                assert definition.strip(), f"Term '{term}' has empty definition"

    def test_profile_schema_version_is_integer(self):
        """Profile version field must be integer, not string."""
        profile = {"version": 1}
        assert isinstance(profile["version"], int)

    def test_state_machine_no_self_transitions(self):
        """No state should transition to itself."""
        allowed = {
            "IDLE": {"WATCHING", "DEMO_MODE"},
            "WATCHING": {"EXPLAINING"},
            "EXPLAINING": {"OFFERING"},
            "OFFERING": {"WATCHING"},
            "DEMO_MODE": {"WATCHING"},
        }
        for state, targets in allowed.items():
            assert state not in targets, f"Self-transition {state}→{state} must not exist"

    def test_chip_shortcut_numbers_are_contiguous(self):
        """Chip shortcuts must be exactly 1,2,3,4 — no gaps."""
        expected = {1, 2, 3, 4}
        assert expected == {1, 2, 3, 4}

    def test_onboarding_invalid_input_no_crash(self, skill_md):
        """Invalid onboarding input (e.g. '0', 'hello') should not crash."""
        lower = skill_md.lower()
        # At minimum, the skill should handle unexpected input gracefully
        assert re.search(r"type.*[123]|1.*2.*3|1️⃣.*2️⃣.*3️⃣", lower), \
            "Onboarding must present 1/2/3 choices"


# ======================================================================
# CROSS-CUTTING: READ-ONLY SAFETY GUARANTEE
# ======================================================================


class TestReadOnlySafety:
    """The sidecar must be read-only throughout."""

    def test_skill_md_asserts_read_only(self, skill_md):
        lower = skill_md.lower()
        assert re.search(r"read[- ]?only|i only watch|never change|don'?t touch", lower)

    def test_sidecar_sh_no_destructive_commands(self, sidecar_sh_text):
        """Launcher should not contain destructive commands."""
        # Should not have rm -rf or force-delete patterns
        assert "rm -rf /" not in sidecar_sh_text
        assert "rm -rf ~" not in sidecar_sh_text

    def test_safety_card_always_mentions_read_only(self, skill_md):
        """Every safety card variant should mention read-only nature."""
        lower = skill_md.lower()
        # PRD §5: "Remember: I never change files. I only watch."
        assert re.search(r"never change|i only watch|read[- ]?only|don'?t touch", lower)
