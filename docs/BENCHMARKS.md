# MPS Benchmarks
Note: This documentation was created with AI assistance and examples are provided for illustration purposes. They have not been fully tested in all environments. Please verify functionality in your specific setup before production use.

**Test Results and Performance Metrics**

---

## Summary (V2 - November 2025)

| Metric | Result | Target | Status |
|--------|--------|--------|--------|
| **Baseline Detection** | 48.5% | 50% | ✅ Close |
| **Benign Accuracy** | 93.3% | 90% | ✅ Exceeded |
| **Evasion Detection** | 5.6% | 35% | ❌ Below |
| **Quick Scan Latency** | 207ms | <250ms | ✅ Met |
| **Deep Scan Latency** | 149ms | <200ms | ✅ Met |

---

## Test Suite Overview

### Test Categories

| Category | Tests | Description |
|----------|-------|-------------|
| **Baseline** | 33 | Standard prompt injection attacks |
| **Evasion** | 18 | Encoding and obfuscation techniques |
| **Benign** | 15 | Legitimate content (false positive check) |
| **Total** | 66 | Complete test suite |

### Test Distribution

**Baseline Attacks (33 tests):**
- Direct override: 3 tests
- Role manipulation: 3 tests
- Privilege escalation: 3 tests
- Context confusion: 2 tests
- Delimiter injection: 2 tests
- Nested injection: 2 tests
- Payload delivery: 2 tests
- Semantic attacks: 2 tests
- Multimodal injection: 2 tests
- RAG poisoning: 2 tests
- Session persistence: 2 tests
- Agent manipulation: 2 tests
- Compositional attacks: 5 tests
- Combined attacks: 1 test

**Evasion Techniques (18 tests):**
- Cyrillic substitution: 1 test
- Zero-width insertion: 1 test
- Base64 encoding: 2 tests
- Leetspeak: 2 tests
- Case manipulation: 2 tests
- Fragmentation: 2 tests
- Double encoding: 1 test
- Hex encoding: 1 test
- URL encoding: 1 test
- Contextual camouflage: 2 tests
- Combined evasion: 2 tests
- RTL override: 1 test

**Benign Content (15 tests):**
- Academic abstract: 1 test
- Normal conversation: 1 test
- Technical documentation: 1 test
- Tutorial content: 1 test
- Business email: 1 test
- News article: 1 test
- Slack conversation: 1 test
- Legal disclaimer: 1 test
- GitHub README: 1 test
- Recipe: 1 test
- Wikipedia excerpt: 1 test
- Product review: 1 test
- Security documentation: 1 test
- Code sample: 1 test
- Poetry: 1 test

---

## Detailed Results

### Baseline Detection (48.5%)

**Passed (16/33):**
| Test | Quick Score | Deep Score | Risk Level |
|------|-------------|------------|------------|
| direct_override_1 | 100 | 100 | RED |
| direct_override_2 | 85 | 85 | RED |
| role_manipulation_1 | 100 | 100 | RED |
| role_manipulation_3 | 100 | 100 | RED |
| privilege_escalation_1 | 100 | 100 | RED |
| privilege_escalation_2 | 100 | 100 | RED |
| privilege_escalation_3 | 100 | 100 | RED |
| delimiter_injection_1 | 75 | 75 | ORANGE |
| semantic_attack_2 | 87 | 60 | ORANGE |
| combined_attack_1 | 100 | 100 | RED |
| rag_poisoning_1 | 85 | 85 | RED |
| rag_poisoning_2 | 70 | 70 | ORANGE |
| multimodal_injection_1 | 100 | 70 | ORANGE |
| compositional_attack_1 | 60 | 60 | ORANGE |
| compositional_attack_2 | 80 | 64 | ORANGE |
| compositional_attack_4 | 80 | 64 | ORANGE |

**Failed (17/33):**
| Test | Reason | Expected | Actual |
|------|--------|----------|--------|
| direct_override_3 | Score at threshold | RED | ORANGE |
| role_manipulation_2 | Over-scored | ORANGE | RED |
| context_confusion_1 | Over-scored | ORANGE | RED |
| context_confusion_2 | Over-scored | ORANGE | RED |
| delimiter_injection_2 | No pattern match | ORANGE | WHITE |
| nested_injection_1 | Over-scored | ORANGE | RED |
| nested_injection_2 | Under-scored | ORANGE | WHITE |
| payload_delivery_2 | Reduction too aggressive | RED | WHITE |
| semantic_attack_1 | Reduction too aggressive | ORANGE | WHITE |
| multimodal_injection_2 | No pattern match | ORANGE | WHITE |
| session_persistence_1 | Wrong expectation | WHITE | ORANGE |
| session_persistence_2 | Over-scored | ORANGE | RED |
| agent_manipulation_1 | Deep scan reduction | ORANGE | WHITE |
| agent_manipulation_2 | Expected WHITE | WHITE | WHITE |
| compositional_attack_3 | No pattern match | ORANGE | WHITE |
| compositional_attack_5 | Deep scan reduction | ORANGE | WHITE |

---

### Evasion Detection (5.6%)

**Passed (1/18):**
| Test | Technique | Detection Method |
|------|-----------|------------------|
| base64_with_context | Base64 + context | Deep scan decoding |

**Failed (17/18):**
| Test | Technique | Failure Reason |
|------|-----------|----------------|
| cyrillic_substitution | Unicode lookalikes | Pattern doesn't match |
| zero_width_insertion | Invisible chars | Splits keywords |
| base64_simple | Base64 encoding | Not decoded |
| leetspeak_simple | Number substitution | Not reversed |
| leetspeak_complex | Heavy substitution | Not reversed |
| case_mixing | MiXeD cAsE | Case-sensitive patterns |
| case_alternating | aLtErNaTiNg | Case-sensitive patterns |
| fragmentation_newlines | Split with \n | Whitespace breaks patterns |
| fragmentation_spaces | Split with spaces | Whitespace breaks patterns |
| double_encoding | Two layers | Only one decode |
| hex_encoding | \x41 format | Not decoded |
| url_encoding | %20 format | Not decoded |
| contextual_camouflage_yaml | Hidden in YAML | Structure not parsed |
| contextual_camouflage_code | Hidden in code | Comments not extracted |
| combined_evasion_1 | Multiple techniques | Too obfuscated |
| combined_evasion_2 | Multiple techniques | Too obfuscated |
| rtl_override | Right-to-left | Unicode not handled |

---

### Benign Accuracy (93.3%)

**Passed (14/15):**
| Test | Content Type | Score | Level |
|------|--------------|-------|-------|
| academic_abstract | Research paper | 27 | WHITE |
| normal_conversation | Casual chat | 0 | WHITE |
| tutorial_content | How-to guide | 27 | WHITE |
| business_email | Professional email | 0 | WHITE |
| news_article | News content | 27 | WHITE |
| slack_conversation | Team chat | 0 | WHITE |
| legal_disclaimer | Legal text | 36 | WHITE |
| github_readme | Project docs | 37 | WHITE |
| wikipedia_excerpt | Encyclopedia | 0 | WHITE |
| product_review | Consumer review | 24 | WHITE |
| security_documentation | Security guide | 30 | WHITE |
| code_sample | Source code | 15 | WHITE |
| poetry | Creative writing | 0 | WHITE |
| technical_documentation | Tech docs | 50 | WHITE |

**Failed (1/15):**
| Test | Content Type | Issue |
|------|--------------|-------|
| recipe | Cooking recipe | UTF-8 decode error (° symbol) |

---

## Performance Benchmarks

### Quick Scan Latency

| Percentile | Latency |
|------------|---------|
| Minimum | 196ms |
| Average | 207ms |
| Maximum | 258ms |
| p50 | 204ms |
| p95 | 225ms |
| p99 | 250ms |

### Deep Scan Latency

| Percentile | Latency |
|------------|---------|
| Minimum | 146ms |
| Average | 149ms |
| Maximum | 165ms |
| p50 | 148ms |
| p95 | 160ms |
| p99 | 164ms |

### Memory Usage

| Scanner | Typical | Peak |
|---------|---------|------|
| Quick Scan | 28MB | 45MB |
| Deep Scan | 52MB | 85MB |

---

## Version Comparison

### V1 (2024) vs V2 (2025)

| Metric | V1 | V2 | Change |
|--------|----|----|--------|
| Baseline Detection | 25% | 48.5% | +23.5% |
| Benign Accuracy | 87% | 93.3% | +6.3% |
| Evasion Detection | 17% | 5.6% | -11.4% |
| Quick Scan Latency | 210ms | 207ms | -3ms |
| Pattern Categories | 10 | 26 | +16 |

**Notes:**
- Evasion regression due to architecture change (pattern centralization)
- Baseline improvement from new pattern categories
- Benign improvement from context-aware reductions

---

## Test Environment

**Hardware:**
- CPU: Intel Core i7 (8 cores)
- RAM: 16GB
- Storage: SSD

**Software:**
- OS: Windows 10
- Python: 3.13
- No external dependencies

---

## Reproducing Results

```bash
# Navigate to test directory
cd mps-test-agent

# Generate test cases (if needed)
python scripts/generate_baseline.py
python scripts/generate_evasion.py
python scripts/generate_benign.py

# Run full test suite
python -B scripts/run_tests.py

# View results
cat test_outputs/full_test_results.json
```

---

## Interpreting Results

### What 48.5% Baseline Means

- MPS catches roughly **half** of standard injection attacks
- High-confidence attacks (role manipulation, privilege escalation) well detected
- Subtle attacks (context confusion, nested injection) often missed

### What 93.3% Benign Means

- MPS correctly identifies **93% of safe content**
- Low false positive rate
- May flag some security documentation as suspicious

### What 5.6% Evasion Means

- **Encoded attacks largely bypass MPS**
- Pattern-based detection cannot match encoded text
- Requires preprocessing pipeline (V3 roadmap)

---

## Recommendations

### Use MPS When:
- Processing user-uploaded files
- Fetching external content
- Defense-in-depth security layer
- Quick risk assessment needed

### Don't Rely Solely on MPS When:
- Sophisticated attackers expected
- Encoded content likely
- Critical security decisions
- No human review available

---

© 2025 StrategicPromptArchitect
