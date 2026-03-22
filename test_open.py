"""Tests for Copilot Sidecar Non-Technical Experience."""

import json
import os
import subprocess

import pytest

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SIDECAR_DIR = os.path.join(BASE_DIR, "sidecar")
DEMOS_DIR = os.path.join(SIDECAR_DIR, "demos")


# ── JSON Validity ───────────────────────────────────────────


class TestJargonDictionary:
    """Tests for jargon-dictionary.json."""

    @pytest.fixture
    def data(self):
        with open(os.path.join(SIDECAR_DIR, "jargon-dictionary.json")) as f:
            return json.load(f)

    def test_is_valid_json(self, data):
        assert isinstance(data, dict)

    def test_has_at_least_40_terms(self, data):
        assert len(data) >= 40, f"Only {len(data)} terms, need 40+"

    def test_all_values_are_strings(self, data):
        for term, definition in data.items():
            assert isinstance(definition, str), f"'{term}' has non-string definition"

    def test_core_terms_present(self, data):
        core = ["git", "commit", "branch", "merge", "diff", "repo", "push",
                "pull", "API", "deploy", "test", "build", "CLI", "terminal"]
        for term in core:
            assert term in data, f"Missing core term: {term}"

    def test_definitions_are_non_empty(self, data):
        for term, definition in data.items():
            assert len(definition) > 5, f"'{term}' has too-short definition"


class TestNarrationCards:
    """Tests for narration-cards.json."""

    @pytest.fixture
    def data(self):
        with open(os.path.join(SIDECAR_DIR, "narration-cards.json")) as f:
            return json.load(f)

    def test_is_valid_json(self, data):
        assert isinstance(data, dict)

    def test_has_cards_array(self, data):
        assert "cards" in data
        assert isinstance(data["cards"], list)

    def test_has_at_least_10_cards(self, data):
        assert len(data["cards"]) >= 10

    def test_has_fallback(self, data):
        assert "fallback" in data
        fb = data["fallback"]
        assert "emoji" in fb
        assert "title" in fb
        assert "what" in fb

    def test_card_structure(self, data):
        required_keys = {"pattern", "emoji", "title", "what", "why", "next"}
        for card in data["cards"]:
            missing = required_keys - set(card.keys())
            assert not missing, f"Card '{card.get('title')}' missing: {missing}"

    def test_card_text_length(self, data):
        for card in data["cards"]:
            for field in ("what", "why", "next"):
                assert len(card[field]) <= 100, (
                    f"Card '{card['title']}' {field} too long: {len(card[field])} chars"
                )

    def test_patterns_are_valid_regex(self, data):
        import re
        for card in data["cards"]:
            try:
                re.compile(card["pattern"])
            except re.error as e:
                pytest.fail(f"Card '{card['title']}' has invalid regex: {e}")


class TestQuestionTemplates:
    """Tests for question-templates.json."""

    @pytest.fixture
    def data(self):
        with open(os.path.join(SIDECAR_DIR, "question-templates.json")) as f:
            return json.load(f)

    def test_is_valid_json(self, data):
        assert isinstance(data, dict)

    def test_required_event_types(self, data):
        required = ["test_failure", "build_error", "file_created",
                     "git_commit", "long_silence"]
        for event_type in required:
            assert event_type in data, f"Missing event type: {event_type}"

    def test_each_type_has_questions(self, data):
        for event_type, questions in data.items():
            assert isinstance(questions, list), f"'{event_type}' is not a list"
            assert len(questions) >= 2, f"'{event_type}' has fewer than 2 questions"

    def test_questions_are_strings(self, data):
        for event_type, questions in data.items():
            for q in questions:
                assert isinstance(q, str), f"Non-string question in '{event_type}'"


class TestDemoIndex:
    """Tests for demos/index.json."""

    @pytest.fixture
    def data(self):
        with open(os.path.join(DEMOS_DIR, "index.json")) as f:
            return json.load(f)

    def test_is_valid_json(self, data):
        assert isinstance(data, dict)

    def test_has_demos_array(self, data):
        assert "demos" in data
        assert isinstance(data["demos"], list)

    def test_has_three_demos(self, data):
        assert len(data["demos"]) == 3

    def test_demo_structure(self, data):
        required = {"id", "title", "file", "duration_s", "teaches"}
        for demo in data["demos"]:
            missing = required - set(demo.keys())
            assert not missing, f"Demo '{demo.get('id')}' missing: {missing}"

    def test_demo_files_exist(self, data):
        for demo in data["demos"]:
            path = os.path.join(DEMOS_DIR, demo["file"])
            assert os.path.isfile(path), f"Demo file missing: {demo['file']}"


# ── JSONL Demo Files ────────────────────────────────────────


class TestDemoFiles:
    """Tests for demo JSONL files."""

    DEMO_FILES = [
        "01-checking-code.jsonl",
        "02-running-tests.jsonl",
        "03-ai-agents.jsonl",
    ]

    @pytest.mark.parametrize("filename", DEMO_FILES)
    def test_valid_jsonl(self, filename):
        path = os.path.join(DEMOS_DIR, filename)
        with open(path) as f:
            for i, line in enumerate(f, 1):
                line = line.strip()
                if line:
                    try:
                        json.loads(line)
                    except json.JSONDecodeError as e:
                        pytest.fail(f"{filename} line {i}: {e}")

    @pytest.mark.parametrize("filename", DEMO_FILES)
    def test_has_required_event_types(self, filename):
        path = os.path.join(DEMOS_DIR, filename)
        types_seen = set()
        with open(path) as f:
            for line in f:
                line = line.strip()
                if line:
                    event = json.loads(line)
                    assert "type" in event, f"Missing 'type' in {filename}"
                    assert "text" in event, f"Missing 'text' in {filename}"
                    types_seen.add(event["type"])
        assert "narration" in types_seen, f"{filename} has no narration events"
        assert "command" in types_seen, f"{filename} has no command events"

    @pytest.mark.parametrize("filename", DEMO_FILES)
    def test_has_delay_ms(self, filename):
        path = os.path.join(DEMOS_DIR, filename)
        with open(path) as f:
            for line in f:
                line = line.strip()
                if line:
                    event = json.loads(line)
                    if event["type"] != "prompt":
                        assert "delay_ms" in event, (
                            f"Non-prompt event in {filename} missing delay_ms"
                        )

    @pytest.mark.parametrize("filename", DEMO_FILES)
    def test_minimum_event_count(self, filename):
        path = os.path.join(DEMOS_DIR, filename)
        count = 0
        with open(path) as f:
            for line in f:
                if line.strip():
                    count += 1
        assert count >= 10, f"{filename} has only {count} events, need 10+"


# ── sidecar.sh ──────────────────────────────────────────────


class TestSidecarSh:
    """Tests for sidecar.sh launcher script."""

    SCRIPT = os.path.join(BASE_DIR, "sidecar.sh")

    def test_file_exists(self):
        assert os.path.isfile(self.SCRIPT)

    def test_is_executable(self):
        assert os.access(self.SCRIPT, os.X_OK)

    def test_valid_bash_syntax(self):
        result = subprocess.run(
            ["bash", "-n", self.SCRIPT],
            capture_output=True, text=True
        )
        assert result.returncode == 0, f"Bash syntax error: {result.stderr}"

    def test_has_shebang(self):
        with open(self.SCRIPT) as f:
            first_line = f.readline().strip()
        assert first_line == "#!/usr/bin/env bash"

    def test_checks_for_tmux(self):
        with open(self.SCRIPT) as f:
            content = f.read()
        assert "command -v tmux" in content

    def test_checks_for_gh(self):
        with open(self.SCRIPT) as f:
            content = f.read()
        assert "command -v gh" in content

    def test_checks_for_skill_file(self):
        with open(self.SCRIPT) as f:
            content = f.read()
        assert "SKILL_PATH" in content
        assert "SKILL.md" in content

    def test_has_solo_mode(self):
        with open(self.SCRIPT) as f:
            content = f.read()
        assert "--solo" in content

    def test_has_session_link_creation(self):
        with open(self.SCRIPT) as f:
            content = f.read()
        assert "session-link.json" in content

    def test_has_help_option(self):
        with open(self.SCRIPT) as f:
            content = f.read()
        assert "--help" in content


# ── SKILL.md Structure ──────────────────────────────────────


class TestSkillMd:
    """Tests for SKILL.md structure and content."""

    @pytest.fixture
    def content(self):
        with open(os.path.join(SIDECAR_DIR, "SKILL.md")) as f:
            return f.read()

    @pytest.fixture
    def lines(self, content):
        return content.split("\n")

    def test_file_exists(self):
        assert os.path.isfile(os.path.join(SIDECAR_DIR, "SKILL.md"))

    def test_minimum_line_count(self, lines):
        assert len(lines) >= 700, f"SKILL.md has {len(lines)} lines, need 700+"

    def test_has_identity_section(self, content):
        assert "## Identity" in content or "IDENTITY" in content

    def test_has_startup_section(self, content):
        assert "## Startup Sequence" in content or "STARTUP" in content

    def test_has_onboarding_section(self, content):
        assert "## Onboarding" in content or "ONBOARDING" in content

    def test_has_state_machine_section(self, content):
        assert "## State Machine" in content or "STATE MACHINE" in content

    def test_has_watch_mode_section(self, content):
        assert "## Watch Mode" in content or "WATCH MODE" in content

    def test_has_ask_mode_section(self, content):
        assert "## Ask Mode" in content or "ASK MODE" in content

    def test_has_suggest_mode_section(self, content):
        assert "## Suggest Mode" in content or "SUGGEST MODE" in content

    def test_has_jargon_firewall_section(self, content):
        assert "## Jargon Firewall" in content or "JARGON FIREWALL" in content

    def test_has_panic_handler_section(self, content):
        assert "## Panic Handler" in content or "PANIC" in content

    def test_has_demo_mode_section(self, content):
        assert "## Demo Mode" in content or "DEMO MODE" in content

    def test_has_safety_framing_section(self, content):
        assert "## Safety Framing" in content or "SAFETY FRAMING" in content

    def test_has_command_reference(self, content):
        assert "## Command Reference" in content or "REFERENCE" in content

    def test_mentions_banned_words(self, content):
        assert "just" in content.lower()
        assert "simply" in content.lower()
        assert "Banned" in content or "banned" in content

    def test_mentions_safe_command(self, content):
        assert "safe?" in content

    def test_mentions_chips(self, content):
        assert "chips" in content.lower()

    def test_mentions_narration_cards(self, content):
        assert "narration-cards.json" in content

    def test_mentions_jargon_dictionary(self, content):
        assert "jargon-dictionary.json" in content

    def test_mentions_user_profile(self, content):
        assert "user-profile.json" in content

    def test_mentions_pane_capture(self, content):
        assert "capture-pane" in content or "pane capture" in content.lower()

    def test_mentions_tmux(self, content):
        assert "tmux" in content

    def test_has_card_format(self, content):
        assert "┌─" in content and "└─" in content

    def test_mentions_three_experiences(self, content):
        assert "Watch" in content
        assert "Ask" in content
        assert "Suggest" in content

    def test_has_four_states(self, content):
        for state in ["IDLE", "WATCHING", "EXPLAINING", "OFFERING"]:
            assert state in content, f"Missing state: {state}"

    def test_has_freshness_buckets(self, content):
        assert "LIVE" in content
        assert "STALE" in content

    def test_has_throttle_rules(self, content):
        assert "throttle" in content.lower() or "THROTTLE" in content


# ── README ──────────────────────────────────────────────────


class TestReadme:
    """Tests for README.md."""

    def test_file_exists(self):
        assert os.path.isfile(os.path.join(SIDECAR_DIR, "README.md"))

    def test_has_prerequisites(self):
        with open(os.path.join(SIDECAR_DIR, "README.md")) as f:
            content = f.read()
        assert "tmux" in content
        assert "gh" in content

    def test_has_installation(self):
        with open(os.path.join(SIDECAR_DIR, "README.md")) as f:
            content = f.read()
        assert "install" in content.lower() or "Installation" in content

    def test_has_commands(self):
        with open(os.path.join(SIDECAR_DIR, "README.md")) as f:
            content = f.read()
        assert "safe?" in content
        assert "chips" in content
        assert "glossary" in content
