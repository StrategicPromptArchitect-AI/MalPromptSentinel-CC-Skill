# MPS Test Agent (CC SKILL) V2

> **Note:** This documentation was created with AI assistance and is provided for illustration purposes. Please verify in your specific setup before production use.

---

**Claude Code Skill for Testing MalPromptSentinel**

---

## Skill Overview

| Property | Value |
|----------|-------|
| **Name** | MPS Test Agent |
| **Version** | 2.0 |
| **Type** | Test Framework |
| **Purpose** | Validate MalPromptSentinel detection accuracy |
| **Author** | StrategicPromptArchitect |

---

## When to Use This Skill

**Activate MPS Test Agent when:**
- Validating MPS installation
- Testing after pattern changes
- Benchmarking detection rates
- Generating new test cases
- Debugging false positives/negatives

---

## Quick Start

### Run Full Test Suite

```bash
cd mps-test-agent
python -B scripts/run_tests.py
```

### Expected Output

```
MPS Test Suite - Running 66 tests
================================

Results Summary:
  Baseline: 16/33 (48.5%)
  Evasion:  1/18  (5.6%)
  Benign:   14/15 (93.3%)
  Total:    31/66 (47.0%)
```

---

## Files

### Scripts

| File | Purpose |
|------|---------|
| `scripts/run_tests.py` | Main test runner |
| `scripts/generate_baseline.py` | Generate attack tests |
| `scripts/generate_evasion.py` | Generate evasion tests |
| `scripts/generate_benign.py` | Generate benign tests |

### Test Inputs

| Directory | Contents | Count |
|-----------|----------|-------|
| `test_inputs/baseline/` | Standard attack files | 33 |
| `test_inputs/evasion/` | Encoded attack files | 18 |
| `test_inputs/benign/` | Legitimate content files | 15 |

### Test Outputs

| File | Contents |
|------|----------|
| `test_outputs/full_test_results.json` | Detailed results |

---

## Test Categories

### Baseline Tests (33)

Standard prompt injection attacks without obfuscation.

**Categories tested:**
- direct_override (3 tests)
- role_manipulation (3 tests)
- privilege_escalation (3 tests)
- context_confusion (2 tests)
- delimiter_injection (2 tests)
- nested_injection (2 tests)
- payload_delivery (2 tests)
- semantic_attack (2 tests)
- multimodal_injection (2 tests)
- rag_poisoning (2 tests)
- session_persistence (2 tests)
- agent_manipulation (2 tests)
- compositional_attack (5 tests)
- combined_attack (1 test)

**Pass criteria:** Detected at expected risk level (ORANGE or RED)

---

### Evasion Tests (18)

Attacks using encoding and obfuscation techniques.

**Techniques tested:**
- Cyrillic substitution
- Zero-width characters
- Base64 encoding
- Leetspeak
- Case manipulation
- Whitespace fragmentation
- Double encoding
- Hex encoding
- URL encoding
- Contextual camouflage
- Combined techniques
- RTL override

**Pass criteria:** Detected despite obfuscation

**Note:** Current detection rate is 5.6% - most evasion tests fail by design.

---

### Benign Tests (15)

Legitimate content that should NOT be flagged.

**Content types:**
- Academic abstracts
- Normal conversations
- Technical documentation
- Tutorials
- Business emails
- News articles
- Chat logs
- Legal text
- GitHub READMEs
- Recipes
- Encyclopedia excerpts
- Product reviews
- Security documentation
- Code samples
- Poetry

**Pass criteria:** Classified as WHITE (not flagged)

---

## Running Tests

### Full Suite

```bash
python -B scripts/run_tests.py
```

### With Detailed Output

```bash
python -B scripts/run_tests.py --verbose
```

### Check Results

```bash
cat test_outputs/full_test_results.json | python -m json.tool
```

---

## Generating Test Cases

### Regenerate All Tests

```bash
python scripts/generate_baseline.py
python scripts/generate_evasion.py
python scripts/generate_benign.py
```

### Add Custom Test

1. Create file in appropriate directory:
   ```bash
   echo "Your test content" > test_inputs/baseline/my_test.txt
   ```

2. Update manifest (if required by your test runner)

3. Run tests:
   ```bash
   python -B scripts/run_tests.py
   ```

---

## Output Format

### Summary

```json
{
  "summary": {
    "total_tests": 66,
    "passed": 31,
    "failed": 35,
    "errors": 0,
    "pass_rate": 47.0,
    "category_breakdown": {
      "baseline": {"passed": 16, "total": 33},
      "evasion": {"passed": 1, "total": 18},
      "benign": {"passed": 14, "total": 15}
    }
  }
}
```

### Detailed Results

```json
{
  "detailed_results": [
    {
      "test_id": "direct_override_1",
      "category": "baseline",
      "file": "test_inputs/baseline/direct_override_1.txt",
      "quick_scan": {
        "risk_score": 100,
        "risk_level": "RED",
        "latency_ms": 205
      },
      "deep_scan": {
        "risk_score": 100,
        "risk_level": "RED",
        "latency_ms": 148
      },
      "validation": {
        "status": "PASS",
        "expected_risk": "RED",
        "actual_risk": "RED"
      }
    }
  ]
}
```

---

## Interpreting Results

### Pass/Fail Logic

**Baseline & Evasion Tests:**
```
PASS if actual_risk >= expected_risk

RED expected    + RED actual    = PASS
ORANGE expected + ORANGE actual = PASS
ORANGE expected + RED actual    = PASS (over-detection OK)
ORANGE expected + WHITE actual  = FAIL (missed detection)
```

**Benign Tests:**
```
PASS if actual_risk == WHITE

WHITE expected + WHITE actual  = PASS
WHITE expected + ORANGE actual = FAIL (false positive)
WHITE expected + RED actual    = FAIL (false positive)
```

### Metrics Meaning

| Metric | Meaning | Target |
|--------|---------|--------|
| Baseline % | Attack detection rate | 50%+ |
| Evasion % | Encoded attack detection | 35%+ |
| Benign % | Correct non-flagging | 90%+ |

---

## Troubleshooting

### "Module not found: mps_patterns"

Ensure mal-prompt-sentinel scripts are accessible:
```bash
ls ../mal-prompt-sentinel/scripts/mps_patterns.py
```

### Different Results Each Run

Clear Python cache:
```bash
rm -rf __pycache__ scripts/__pycache__
python -B scripts/run_tests.py
```

### Test File Not Found

Regenerate test inputs:
```bash
python scripts/generate_baseline.py
python scripts/generate_evasion.py
python scripts/generate_benign.py
```

---

## Current Benchmarks (V2)

| Metric | Result |
|--------|--------|
| Baseline Detection | 48.5% (16/33) |
| Evasion Detection | 5.6% (1/18) |
| Benign Accuracy | 93.3% (14/15) |
| Total Pass Rate | 47.0% (31/66) |

---

## Support

**Website:** https://StrategicPromptArchitect.ca

**Email:** StrategicPromptArchitect@gmail.com

---

## License

MIT License - See LICENSE file for details.

---

© 2025 StrategicPromptArchitect
