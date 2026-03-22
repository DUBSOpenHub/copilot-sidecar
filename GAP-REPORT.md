# Gap Report

## Summary

| Metric | Value |
|--------|-------|
| Open Tests Run | 74 |
| Open Tests Passed | 74 |
| Open Tests Failed | 0 |
| Sealed Tests Run | 196 |
| Sealed Tests Passed | 191 |
| Sealed Tests Failed | 5 |
| **Gap Score** | **2.6%** |

Gap Score = (sealed_failures / sealed_total) x 100
A score of 0% means the implementation fully satisfies the spec.

## Open Test Results

| # | Test | Status |
|---|------|--------|
| 1 | TestJargonDictionary::test_is_valid_json | PASS |
| 2 | TestJargonDictionary::test_has_at_least_40_terms | PASS |
| 3 | TestJargonDictionary::test_all_values_are_strings | PASS |
| 4 | TestJargonDictionary::test_core_terms_present | PASS |
| 5 | TestJargonDictionary::test_definitions_are_non_empty | PASS |
| 6 | TestNarrationCards::test_is_valid_json | PASS |
| 7 | TestNarrationCards::test_has_cards_array | PASS |
| 8 | TestNarrationCards::test_has_at_least_10_cards | PASS |
| 9 | TestNarrationCards::test_has_fallback | PASS |
| 10 | TestNarrationCards::test_card_structure | PASS |
| 11 | TestNarrationCards::test_card_text_length | PASS |
| 12 | TestNarrationCards::test_patterns_are_valid_regex | PASS |
| 13 | TestQuestionTemplates::test_is_valid_json | PASS |
| 14 | TestQuestionTemplates::test_required_event_types | PASS |
| 15 | TestQuestionTemplates::test_each_type_has_questions | PASS |
| 16 | TestQuestionTemplates::test_questions_are_strings | PASS |
| 17 | TestDemoIndex::test_is_valid_json | PASS |
| 18 | TestDemoIndex::test_has_demos_array | PASS |
| 19 | TestDemoIndex::test_has_three_demos | PASS |
| 20 | TestDemoIndex::test_demo_structure | PASS |
| 21 | TestDemoIndex::test_demo_files_exist | PASS |
| 22 | TestDemoFiles::test_valid_jsonl[01-checking-code.jsonl] | PASS |
| 23 | TestDemoFiles::test_valid_jsonl[02-running-tests.jsonl] | PASS |
| 24 | TestDemoFiles::test_valid_jsonl[03-ai-agents.jsonl] | PASS |
| 25 | TestDemoFiles::test_has_required_event_types[01-checking-code.jsonl] | PASS |
| 26 | TestDemoFiles::test_has_required_event_types[02-running-tests.jsonl] | PASS |
| 27 | TestDemoFiles::test_has_required_event_types[03-ai-agents.jsonl] | PASS |
| 28 | TestDemoFiles::test_has_delay_ms[01-checking-code.jsonl] | PASS |
| 29 | TestDemoFiles::test_has_delay_ms[02-running-tests.jsonl] | PASS |
| 30 | TestDemoFiles::test_has_delay_ms[03-ai-agents.jsonl] | PASS |
| 31 | TestDemoFiles::test_minimum_event_count[01-checking-code.jsonl] | PASS |
| 32 | TestDemoFiles::test_minimum_event_count[02-running-tests.jsonl] | PASS |
| 33 | TestDemoFiles::test_minimum_event_count[03-ai-agents.jsonl] | PASS |
| 34 | TestSidecarSh::test_file_exists | PASS |
| 35 | TestSidecarSh::test_is_executable | PASS |
| 36 | TestSidecarSh::test_valid_bash_syntax | PASS |
| 37 | TestSidecarSh::test_has_shebang | PASS |
| 38 | TestSidecarSh::test_checks_for_tmux | PASS |
| 39 | TestSidecarSh::test_checks_for_gh | PASS |
| 40 | TestSidecarSh::test_checks_for_skill_file | PASS |
| 41 | TestSidecarSh::test_has_solo_mode | PASS |
| 42 | TestSidecarSh::test_has_session_link_creation | PASS |
| 43 | TestSidecarSh::test_has_help_option | PASS |
| 44 | TestSkillMd::test_file_exists | PASS |
| 45 | TestSkillMd::test_minimum_line_count | PASS |
| 46 | TestSkillMd::test_has_identity_section | PASS |
| 47 | TestSkillMd::test_has_startup_section | PASS |
| 48 | TestSkillMd::test_has_onboarding_section | PASS |
| 49 | TestSkillMd::test_has_state_machine_section | PASS |
| 50 | TestSkillMd::test_has_watch_mode_section | PASS |
| 51 | TestSkillMd::test_has_ask_mode_section | PASS |
| 52 | TestSkillMd::test_has_suggest_mode_section | PASS |
| 53 | TestSkillMd::test_has_jargon_firewall_section | PASS |
| 54 | TestSkillMd::test_has_panic_handler_section | PASS |
| 55 | TestSkillMd::test_has_demo_mode_section | PASS |
| 56 | TestSkillMd::test_has_safety_framing_section | PASS |
| 57 | TestSkillMd::test_has_command_reference | PASS |
| 58 | TestSkillMd::test_mentions_banned_words | PASS |
| 59 | TestSkillMd::test_mentions_safe_command | PASS |
| 60 | TestSkillMd::test_mentions_chips | PASS |
| 61 | TestSkillMd::test_mentions_narration_cards | PASS |
| 62 | TestSkillMd::test_mentions_jargon_dictionary | PASS |
| 63 | TestSkillMd::test_mentions_user_profile | PASS |
| 64 | TestSkillMd::test_mentions_pane_capture | PASS |
| 65 | TestSkillMd::test_mentions_tmux | PASS |
| 66 | TestSkillMd::test_has_card_format | PASS |
| 67 | TestSkillMd::test_mentions_three_experiences | PASS |
| 68 | TestSkillMd::test_has_four_states | PASS |
| 69 | TestSkillMd::test_has_freshness_buckets | PASS |
| 70 | TestSkillMd::test_has_throttle_rules | PASS |
| 71 | TestReadme::test_file_exists | PASS |
| 72 | TestReadme::test_has_prerequisites | PASS |
| 73 | TestReadme::test_has_installation | PASS |
| 74 | TestReadme::test_has_commands | PASS |

## Sealed Test Results

| # | Test | Status |
|---|------|--------|
| 1 | TestLauncherPreflight::test_sidecar_sh_valid_bash_syntax | PASS |
| 2 | TestLauncherPreflight::test_preflight_checks_tmux | PASS |
| 3 | TestLauncherPreflight::test_tmux_missing_friendly_message | PASS |
| 4 | TestLauncherPreflight::test_preflight_checks_gh_cli | PASS |
| 5 | TestLauncherPreflight::test_gh_missing_has_install_link | PASS |
| 6 | TestLauncherPreflight::test_preflight_checks_skill_file | PASS |
| 7 | TestLauncherPreflight::test_solo_mode_fallback | PASS |
| 8 | TestLauncherPreflight::test_already_in_tmux_detection | PASS |
| 9 | TestLauncherPreflight::test_session_reconnection | PASS |
| 10 | TestLauncherPreflight::test_preflight_log_written_as_json | FAIL |
| 11 | TestFourPathDetection::test_detection_matrix[resume] | PASS |
| 12 | TestFourPathDetection::test_detection_matrix[onboard] | PASS |
| 13 | TestFourPathDetection::test_detection_matrix[demo-returning] | PASS |
| 14 | TestFourPathDetection::test_detection_matrix[demo-new] | PASS |
| 15 | TestFourPathDetection::test_session_check_mentions_lock_or_state | PASS |
| 16 | TestFourPathDetection::test_profile_check_path | PASS |
| 17 | TestOnboarding::test_onboarding_choice_maps_to_level[1-beginner] | PASS |
| 18 | TestOnboarding::test_onboarding_choice_maps_to_level[2-intermediate] | PASS |
| 19 | TestOnboarding::test_onboarding_choice_maps_to_level[3-expert] | PASS |
| 20 | TestOnboarding::test_beginner_enables_narration_and_chips | PASS |
| 21 | TestOnboarding::test_expert_disables_narration | PASS |
| 22 | TestOnboarding::test_profile_schema_minimum_fields | PASS |
| 23 | TestOnboarding::test_profile_path_convention | PASS |
| 24 | TestNarrationCards::test_cards_is_valid_json | PASS |
| 25 | TestNarrationCards::test_cards_array_exists | PASS |
| 26 | TestNarrationCards::test_minimum_10_card_patterns | PASS |
| 27 | TestNarrationCards::test_each_card_has_required_fields[pattern] | PASS |
| 28 | TestNarrationCards::test_each_card_has_required_fields[emoji] | PASS |
| 29 | TestNarrationCards::test_each_card_has_required_fields[title] | PASS |
| 30 | TestNarrationCards::test_each_card_has_required_fields[what] | PASS |
| 31 | TestNarrationCards::test_each_card_has_required_fields[why] | PASS |
| 32 | TestNarrationCards::test_each_card_has_required_fields[next] | PASS |
| 33 | TestNarrationCards::test_card_lines_within_80_chars | PASS |
| 34 | TestNarrationCards::test_each_card_has_emoji_header | PASS |
| 35 | TestNarrationCards::test_pattern_covered[git diff] | PASS |
| 36 | TestNarrationCards::test_pattern_covered[git commit] | PASS |
| 37 | TestNarrationCards::test_pattern_covered[npm test] | PASS |
| 38 | TestNarrationCards::test_pattern_covered[npm install] | PASS |
| 39 | TestNarrationCards::test_pattern_covered[build] | PASS |
| 40 | TestNarrationCards::test_pattern_covered[git push] | PASS |
| 41 | TestNarrationCards::test_pattern_covered[git checkout] | PASS |
| 42 | TestNarrationCards::test_pattern_covered[git status] | PASS |
| 43 | TestNarrationCards::test_pattern_covered[curl] | PASS |
| 44 | TestNarrationCards::test_pattern_covered[rm] | PASS |
| 45 | TestNarrationCards::test_fallback_card_exists | PASS |
| 46 | TestFreshnessBadges::test_freshness_classification[0-LIVE] | PASS |
| 47 | TestFreshnessBadges::test_freshness_classification[5-LIVE] | PASS |
| 48 | TestFreshnessBadges::test_freshness_classification[10-LIVE] | PASS |
| 49 | TestFreshnessBadges::test_freshness_classification[11-RECENT] | PASS |
| 50 | TestFreshnessBadges::test_freshness_classification[30-RECENT] | PASS |
| 51 | TestFreshnessBadges::test_freshness_classification[60-RECENT] | PASS |
| 52 | TestFreshnessBadges::test_freshness_classification[61-STALE] | PASS |
| 53 | TestFreshnessBadges::test_freshness_classification[120-STALE] | PASS |
| 54 | TestFreshnessBadges::test_freshness_classification[300-STALE] | PASS |
| 55 | TestFreshnessBadges::test_live_badge_emoji_green | PASS |
| 56 | TestFreshnessBadges::test_stale_badge_includes_disclaimer | PASS |
| 57 | TestNarrationThrottle::test_throttle_mentioned_in_skill | PASS |
| 58 | TestNarrationThrottle::test_burst_buffering_described | PASS |
| 59 | TestNarrationThrottle::test_idle_triggers_chips | PASS |
| 60 | TestNarrationThrottle::test_long_silence_message | PASS |
| 61 | TestPanicButton::test_safe_command_documented | PASS |
| 62 | TestPanicButton::test_green_state_all_clear | PASS |
| 63 | TestPanicButton::test_yellow_state_minor_concern | PASS |
| 64 | TestPanicButton::test_red_state_error_not_user_fault | PASS |
| 65 | TestPanicButton::test_safe_works_from_any_state | PASS |
| 66 | TestPanicButton::test_read_only_in_safety_card | PASS |
| 67 | TestDemoMode::test_demo_index_valid_json | PASS |
| 68 | TestDemoMode::test_demo_index_has_demos_array | PASS |
| 69 | TestDemoMode::test_three_demos_exist | PASS |
| 70 | TestDemoMode::test_demo_entry_has_required_fields[id] | PASS |
| 71 | TestDemoMode::test_demo_entry_has_required_fields[title] | PASS |
| 72 | TestDemoMode::test_demo_entry_has_required_fields[file] | PASS |
| 73 | TestDemoMode::test_demo_entry_has_required_fields[duration_s] | PASS |
| 74 | TestDemoMode::test_demo_entry_has_required_fields[teaches] | PASS |
| 75 | TestDemoMode::test_demo_ids_include_expected | PASS |
| 76 | TestDemoMode::test_demo_jsonl_files_exist | PASS |
| 77 | TestDemoMode::test_demo_jsonl_lines_valid | PASS |
| 78 | TestDemoMode::test_demo_jsonl_has_delay_ms | PASS |
| 79 | TestDemoMode::test_demo_menu_four_options | PASS |
| 80 | TestDemoMode::test_session_redetection_interval | PASS |
| 81 | TestQuestionChips::test_question_templates_valid_json | PASS |
| 82 | TestQuestionChips::test_templates_have_event_categories | PASS |
| 83 | TestQuestionChips::test_each_category_has_questions | PASS |
| 84 | TestQuestionChips::test_chip_1_always_status | PASS |
| 85 | TestQuestionChips::test_chip_4_always_safety | PASS |
| 86 | TestQuestionChips::test_chips_numbered_1_to_4 | PASS |
| 87 | TestQuestionChips::test_chips_refresh_90s | PASS |
| 88 | TestQuestionChips::test_chips_disappear_on_input | PASS |
| 89 | TestQuestionChips::test_chips_command_redisplays | PASS |
| 90 | TestJargonFirewall::test_dictionary_valid_json | PASS |
| 91 | TestJargonFirewall::test_dictionary_has_40_plus_terms | PASS |
| 92 | TestJargonFirewall::test_each_term_has_definition | PASS |
| 93 | TestJargonFirewall::test_critical_term_present[git] | PASS |
| 94 | TestJargonFirewall::test_critical_term_present[commit] | PASS |
| 95 | TestJargonFirewall::test_critical_term_present[branch] | PASS |
| 96 | TestJargonFirewall::test_critical_term_present[merge] | PASS |
| 97 | TestJargonFirewall::test_critical_term_present[diff] | PASS |
| 98 | TestJargonFirewall::test_critical_term_present[repo] | PASS |
| 99 | TestJargonFirewall::test_critical_term_present[push] | PASS |
| 100 | TestJargonFirewall::test_critical_term_present[pull] | PASS |
| 101 | TestJargonFirewall::test_critical_term_present[PR] | PASS |
| 102 | TestJargonFirewall::test_critical_term_present[npm] | PASS |
| 103 | TestJargonFirewall::test_critical_term_present[build] | PASS |
| 104 | TestJargonFirewall::test_critical_term_present[deploy] | PASS |
| 105 | TestJargonFirewall::test_critical_term_present[API] | PASS |
| 106 | TestJargonFirewall::test_critical_term_present[database] | PASS |
| 107 | TestJargonFirewall::test_critical_term_present[CLI] | PASS |
| 108 | TestJargonFirewall::test_critical_term_present[terminal] | PASS |
| 109 | TestJargonFirewall::test_beginner_first_use_explanation | PASS |
| 110 | TestJargonFirewall::test_graduated_terms_pass_through | PASS |
| 111 | TestJargonFirewall::test_what_does_x_mean_refresher | PASS |
| 112 | TestJargonFirewall::test_firewall_disabled_expert | FAIL |
| 113 | TestJargonFirewall::test_intermediate_first_mention_only | PASS |
| 114 | TestStoryMode::test_safety_net_story_on_commit | PASS |
| 115 | TestStoryMode::test_detective_story_on_failure | PASS |
| 116 | TestStoryMode::test_architecture_story_on_codebase_question | PASS |
| 117 | TestConsequencePreview::test_risk_classification[git commit->🟢] | PASS |
| 118 | TestConsequencePreview::test_risk_classification[git add->��] | PASS |
| 119 | TestConsequencePreview::test_risk_classification[git stash->🟢] | PASS |
| 120 | TestConsequencePreview::test_risk_classification[npm test->🟢] | PASS |
| 121 | TestConsequencePreview::test_risk_classification[ls->🟢] | PASS |
| 122 | TestConsequencePreview::test_risk_classification[git status->🟢] | PASS |
| 123 | TestConsequencePreview::test_risk_classification[npm install->🟡] | PASS |
| 124 | TestConsequencePreview::test_risk_classification[pip install->🟡] | PASS |
| 125 | TestConsequencePreview::test_risk_classification[touch foo->🟡] | PASS |
| 126 | TestConsequencePreview::test_risk_classification[mkdir bar->🟡] | PASS |
| 127 | TestConsequencePreview::test_risk_classification[git push->🟠] | PASS |
| 128 | TestConsequencePreview::test_risk_classification[git merge->🟠] | PASS |
| 129 | TestConsequencePreview::test_risk_classification[chmod 755 foo->🟠] | PASS |
| 130 | TestConsequencePreview::test_risk_classification[rm -rf node_modules->🔴] | PASS |
| 131 | TestConsequencePreview::test_risk_classification[deploy->🔴] | PASS |
| 132 | TestConsequencePreview::test_four_risk_levels_exist | PASS |
| 133 | TestConsequencePreview::test_preview_shown_for_risky_actions | PASS |
| 134 | TestSessionDiscovery::test_human_readable_project_names | PASS |
| 135 | TestSessionDiscovery::test_no_session_enters_demo_mode | PASS |
| 136 | TestSchemas::test_command_to_outcome_card_required_fields | PASS |
| 137 | TestSchemas::test_card_stage_enum | PASS |
| 138 | TestSchemas::test_card_lines_max_length | PASS |
| 139 | TestSchemas::test_confidence_label_required_fields | PASS |
| 140 | TestSchemas::test_confidence_level_enum | PASS |
| 141 | TestSchemas::test_freshness_bucket_enum | PASS |
| 142 | TestSchemas::test_question_chip_required_fields | PASS |
| 143 | TestSchemas::test_chip_shortcut_range_1_to_4 | PASS |
| 144 | TestSchemas::test_chip_kind_enum | PASS |
| 145 | TestSchemas::test_glossary_term_required_fields | PASS |
| 146 | TestSchemas::test_jargon_annotation_required_fields | PASS |
| 147 | TestSchemas::test_jargon_action_enum | PASS |
| 148 | TestSchemas::test_user_profile_full_schema | PASS |
| 149 | TestStateMachine::test_valid_transitions[IDLE-WATCHING] | PASS |
| 150 | TestStateMachine::test_valid_transitions[WATCHING-EXPLAINING] | PASS |
| 151 | TestStateMachine::test_valid_transitions[EXPLAINING-OFFERING] | PASS |
| 152 | TestStateMachine::test_valid_transitions[OFFERING-WATCHING] | PASS |
| 153 | TestStateMachine::test_invalid_transitions[IDLE-EXPLAINING] | PASS |
| 154 | TestStateMachine::test_invalid_transitions[IDLE-OFFERING] | PASS |
| 155 | TestStateMachine::test_invalid_transitions[WATCHING-IDLE] | PASS |
| 156 | TestStateMachine::test_invalid_transitions[OFFERING-EXPLAINING] | PASS |
| 157 | TestStateMachine::test_idle_to_demo_when_no_session | PASS |
| 158 | TestStateMachine::test_demo_to_watching_on_session_detected | PASS |
| 159 | TestStateMachine::test_panic_from_any_state | PASS |
| 160 | TestStateMachine::test_panic_returns_to_previous_state | PASS |
| 161 | TestFunctionalRequirements::test_nt_1_1_default_beginner | FAIL |
| 162 | TestFunctionalRequirements::test_nt_1_2_jargon_firewall_all_output | PASS |
| 163 | TestFunctionalRequirements::test_nt_1_3_expert_beginner_toggle | PASS |
| 164 | TestFunctionalRequirements::test_nt_2_1_watch_auto_narrates | PASS |
| 165 | TestFunctionalRequirements::test_nt_2_2_command_to_outcome_cards | PASS |
| 166 | TestFunctionalRequirements::test_nt_2_4_throttle_1_per_10s | PASS |
| 167 | TestFunctionalRequirements::test_nt_5_1_safe_immediate | PASS |
| 168 | TestFunctionalRequirements::test_nt_5_2_demo_mode_no_session | PASS |
| 169 | TestFunctionalRequirements::test_nt_6_1_no_raw_stack_traces | FAIL |
| 170 | TestFunctionalRequirements::test_nt_6_2_no_unexplained_jargon | PASS |
| 171 | TestFunctionalRequirements::test_nt_7_1_preflight_before_tmux | PASS |
| 172 | TestFunctionalRequirements::test_nt_7_2_solo_mode_fallback | PASS |
| 173 | TestSkillMdSections::test_identity_and_personality | PASS |
| 174 | TestSkillMdSections::test_never_says_just_or_simply | FAIL |
| 175 | TestSkillMdSections::test_uses_we_language | PASS |
| 176 | TestSkillMdSections::test_startup_sequence_section | PASS |
| 177 | TestSkillMdSections::test_safety_framing_section | PASS |
| 178 | TestSkillMdSections::test_confusion_handling_section | PASS |
| 179 | TestSkillMdSections::test_emoji_palette | PASS |
| 180 | TestEdgeCases::test_empty_command_matches_fallback | PASS |
| 181 | TestEdgeCases::test_freshness_boundary_at_10s | PASS |
| 182 | TestEdgeCases::test_freshness_boundary_at_11s | PASS |
| 183 | TestEdgeCases::test_freshness_boundary_at_60s | PASS |
| 184 | TestEdgeCases::test_freshness_boundary_at_61s | PASS |
| 185 | TestEdgeCases::test_risk_rm_always_high | PASS |
| 186 | TestEdgeCases::test_risk_git_commit_always_none | PASS |
| 187 | TestEdgeCases::test_narration_cards_patterns_are_valid_regex | PASS |
| 188 | TestEdgeCases::test_demo_duration_positive | PASS |
| 189 | TestEdgeCases::test_jargon_dict_no_empty_definitions | PASS |
| 190 | TestEdgeCases::test_profile_schema_version_is_integer | PASS |
| 191 | TestEdgeCases::test_state_machine_no_self_transitions | PASS |
| 192 | TestEdgeCases::test_chip_shortcut_numbers_are_contiguous | PASS |
| 193 | TestEdgeCases::test_onboarding_invalid_input_no_crash | PASS |
| 194 | TestReadOnlySafety::test_skill_md_asserts_read_only | PASS |
| 195 | TestReadOnlySafety::test_sidecar_sh_no_destructive_commands | PASS |
| 196 | TestReadOnlySafety::test_safety_card_always_mentions_read_only | PASS |

## Failure Details

### TestLauncherPreflight::test_preflight_log_written_as_json
- **Expected:** sidecar.sh log_event function writes JSON with a quoted key like `"ts"`, `"event"`, or `"timestamp"` inside curly braces (regex: `\{.*"(ts|event|timestamp)"`)
- **Actual:** sidecar.sh has a `log_event` function and writes to `launcher.log` / `LOG_FILE`, but the log format does not use JSON with quoted keys — it uses a plain-text format
- **Error:** `AssertionError: Log must be written as JSON` — `re.search(r'\{.*"(ts|event|timestamp)"', sidecar_sh_text)` returned None

### TestJargonFirewall::test_firewall_disabled_expert
- **Expected:** SKILL.md contains text matching the pattern `expert.*(disable|off|bypass)` or `firewall.*(disable|off).*expert` — i.e., an explicit statement that the jargon firewall is disabled/off/bypassed in expert mode
- **Actual:** SKILL.md does not contain phrasing that matches either pattern; the expert-mode firewall behavior is not explicitly stated with the words "disable", "off", or "bypass"
- **Error:** `assert None` — `re.search(r"expert.*(disable|off|bypass)|firewall.*(disable|off).*expert", lower)` returned None

### TestFunctionalRequirements::test_nt_1_1_default_beginner
- **Expected:** SKILL.md contains text matching `default.*beginner`, `beginner.*default`, or `first.*launch.*beginner` — an explicit statement that the default experience level is beginner
- **Actual:** SKILL.md does not contain phrasing that matches any of these patterns; no explicit "default is beginner" or "first launch beginner" statement found
- **Error:** `assert None` — `re.search(r"default.*beginner|beginner.*default|first.*launch.*beginner", lower)` returned None

### TestFunctionalRequirements::test_nt_6_1_no_raw_stack_traces
- **Expected:** SKILL.md contains text matching `stack.?trace`, `raw.*error`, `never.*display.*raw`, or `hide.*trace` — an explicit rule about suppressing raw stack traces
- **Actual:** SKILL.md does not contain any of these phrases; there is an error recovery section but no explicit mention of stack traces or hiding raw errors
- **Error:** `assert None` — `re.search(r"stack.?trace|raw.*error|never.*display.*raw|hide.*trace", lower)` returned None

### TestSkillMdSections::test_never_says_just_or_simply
- **Expected:** SKILL.md contains text matching `never.*"just"`, `never.*"simply"`, or `avoid.*"just"` — the banned-word rule stated with the words in double quotes
- **Actual:** SKILL.md has a banned words section that lists "just" and "simply" using markdown formatting (dashes and em-dashes), but uses curly/smart quotes or a format that does not match the straight-double-quote regex pattern `never.*\"just\"`
- **Error:** `assert None` — `re.search(r'never.*"just"|never.*"simply"|avoid.*"just"', lower)` returned None

## Hardening Payload

```
SEALED TEST FAILURES:
- test_preflight_log_written_as_json: expected JSON log format with {{"ts"|"event"|"timestamp"}} keys, got plain-text log format
- test_firewall_disabled_expert: expected "expert.*(disable|off|bypass)" in SKILL.md, got no match
- test_nt_1_1_default_beginner: expected "default.*beginner" or equivalent in SKILL.md, got no match
- test_nt_6_1_no_raw_stack_traces: expected "stack trace" or "raw error" or "hide trace" in SKILL.md, got no match
- test_never_says_just_or_simply: expected never.*"just" (straight double quotes) in SKILL.md, got no match (quotes may be curly/smart or formatting differs)
```
