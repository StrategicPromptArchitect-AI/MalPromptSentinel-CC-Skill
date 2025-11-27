# Changelog

All notable changes to MalPromptSentinel (CC SKILL) are documented in this file.

---

## [V2] - November 2025

### Added
- **Centralized Pattern Library** (`mps_patterns.py`)
  - Single source of truth for all patterns
  - Shared between quick_scan and deep_scan
  - 25+ pattern categories, 200+ regex patterns

- **New Pattern Categories**
  - `payload_delivery` - URL exfiltration detection
  - `multimodal_injection` - Image-based attack detection
  - `rag_poisoning` - Knowledge base manipulation
  - `session_persistence` - Conversation state attacks
  - `agent_manipulation` - Tool parameter injection
  - `delimiter_injection_advanced` - Enhanced delimiter detection
  - `unicode_evasion` - Cyrillic, CJK, zero-width detection
  - `whitespace_obfuscation` - Fragmentation detection

- **Orchestration Threat Attack (OTA) Detection**
  - `compositional_attack` patterns
  - Multi-query assembly detection
  - Temporal reference indicators

- **Context-Aware Reductions**
  - Educational content handling
  - Technical documentation handling
  - Review/documentation false positive reduction
  - Compositional pattern legitimate use detection
  - Session persistence innocent context handling

- **3-Tier Risk System**
  - WHITE (0-54): Safe
  - ORANGE (55-79): Suspicious
  - RED (80-100): Dangerous
  - Removed YELLOW tier for simplicity

### Changed
- **Pattern Architecture**
  - Refactored from inline patterns to centralized library
  - Both scanners now import from `mps_patterns.py`
  - Eliminates sync issues between scanners

- **Deep Scan Reductions**
  - Educational content: 50% → 20% reduction
  - Added multimodal/image handling: 30% reduction
  - OTA patterns: Light 20% reduction (was 100%)

- **Performance Improvements**
  - Baseline detection: 25% → 48.5%
  - Benign accuracy: 86.7% → 93.3%
  - Quick scan latency: ~208ms average
  - Deep scan latency: ~150ms average

### Fixed
- `FULL_PATTERNS` → `DEEP_PATTERNS` variable reference bug
- Pattern weights sync between scanners
- YELLOW risk level removed from all code paths
- Python bytecode cache issues documented

### Removed
- **Sanitize Function**
  - Removed `sanitize.py` entirely
  - 50% false positive rate made it ineffective
  - Replaced with block/warn strategy

- **YELLOW Risk Level**
  - Simplified to 3-tier system
  - Reduces complexity and edge cases

---

## [V1] - 2024

### Added
- Initial release
- Quick scan with pattern-based detection
- Deep scan with evasion detection
- Basic risk scoring (0-100)
- 4-tier risk system (WHITE, YELLOW, ORANGE, RED)
- Core pattern categories:
  - `direct_override`
  - `role_manipulation`
  - `privilege_escalation`
  - `context_confusion`
  - `delimiter_injection`
  - `nested_injection`
  - `semantic_attack`
  - `jailbreak_personas`
  - `template_extraction`
  - `secret_detection`
- Sanitize function for suspicious content
- SKILL.md for Claude Code integration
- Test framework with baseline, evasion, benign tests

### Performance (V1)
- Baseline detection: ~25%
- Benign accuracy: ~87%
- Evasion detection: ~17%

---

## Roadmap

### V3 (Planned)
- Preprocessing pipeline for evasion detection
- Multi-pass decoding (Base64, hex, URL)
- Unicode normalization
- Leetspeak reversal
- Expected evasion improvement: 6% → 30-35%

### Future Considerations
- Conversation state tracking (multi-turn detection)
- Machine learning classifier integration
- Real-time pattern updates
- Integration with Claude's built-in safety systems

---

## Migration Guide

### V1 → V2

1. **Pattern Changes**
   - No action needed if using scanners as-is
   - If extending patterns, add to `mps_patterns.py` instead of scanner files

2. **Risk Levels**
   - YELLOW no longer exists
   - Update any code checking for YELLOW to check ORANGE instead

3. **Sanitize Function**
   - `sanitize.py` removed
   - Replace sanitization with user warning + consent flow

4. **Test Expectations**
   - Regenerate test manifests if using custom tests
   - Remove YELLOW from expected_risk values

---

## Version Numbering

- **Major versions** (V1, V2, V3): Significant feature changes
- **Minor updates**: Bug fixes, pattern additions (no version bump)
- **Distribution packages**: Include version in folder name

---

*Maintained by StrategicPromptArchitect*
