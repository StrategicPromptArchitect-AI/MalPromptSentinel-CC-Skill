# Test Coverage

> **Note:** This documentation was created with AI assistance and is provided for illustration purposes. Please verify in your specific setup before production use.

---

**What's Tested and What's Not**

---

## Coverage Summary

| Component | Tested | Coverage |
|-----------|--------|----------|
| Quick Scan | ✅ Yes | 66 tests |
| Deep Scan | ✅ Yes | 66 tests |
| Pattern Library | ✅ Yes | Via scanners |
| Error Handling | ⚠️ Partial | Manual only |
| Edge Cases | ⚠️ Partial | Some coverage |
| Performance | ⚠️ Partial | Latency only |
| Integration | ❌ No | Not automated |

---

## What IS Tested

### Baseline Attack Detection (33 tests)

| Pattern Category | Tests | Coverage |
|------------------|-------|----------|
| direct_override | 3 | ✅ Good |
| role_manipulation | 3 | ✅ Good |
| privilege_escalation | 3 | ✅ Good |
| context_confusion | 2 | ✅ Good |
| delimiter_injection | 2 | ⚠️ Partial |
| nested_injection | 2 | ⚠️ Partial |
| payload_delivery | 2 | ⚠️ Partial |
| semantic_attack | 2 | ⚠️ Partial |
| multimodal_injection | 2 | ⚠️ Partial |
| rag_poisoning | 2 | ✅ Good |
| session_persistence | 2 | ⚠️ Partial |
| agent_manipulation | 2 | ⚠️ Partial |
| compositional_attack | 5 | ✅ Good |
| combined_attack | 1 | ⚠️ Minimal |

### Evasion Technique Detection (18 tests)

| Technique | Tests | Coverage |
|-----------|-------|----------|
| Cyrillic substitution | 1 | ⚠️ Minimal |
| Zero-width insertion | 1 | ⚠️ Minimal |
| Base64 encoding | 2 | ⚠️ Partial |
| Leetspeak | 2 | ⚠️ Partial |
| Case manipulation | 2 | ⚠️ Partial |
| Fragmentation | 2 | ⚠️ Partial |
| Double encoding | 1 | ⚠️ Minimal |
| Hex encoding | 1 | ⚠️ Minimal |
| URL encoding | 1 | ⚠️ Minimal |
| Contextual camouflage | 2 | ⚠️ Partial |
| Combined evasion | 2 | ⚠️ Partial |
| RTL override | 1 | ⚠️ Minimal |

### Benign Content (False Positive Testing) (15 tests)

| Content Type | Tests | Coverage |
|--------------|-------|----------|
| Academic/research | 1 | ⚠️ Minimal |
| Conversations | 2 | ⚠️ Partial |
| Technical docs | 2 | ⚠️ Partial |
| Business content | 2 | ⚠️ Partial |
| Creative writing | 2 | ⚠️ Partial |
| Code samples | 2 | ⚠️ Partial |
| News/encyclopedia | 2 | ⚠️ Partial |
| Legal text | 1 | ⚠️ Minimal |
| Recipes | 1 | ⚠️ Minimal |

---

## What's NOT Tested

### Functional Gaps

| Area | Status | Risk |
|------|--------|------|
| Large files (>1MB) | ❌ Not tested | Medium |
| Binary files | ❌ Not tested | Low |
| Non-UTF-8 encoding | ❌ Not tested | Medium |
| Concurrent scanning | ❌ Not tested | Low |
| Memory limits | ❌ Not tested | Medium |
| Empty files | ❌ Not tested | Low |
| Unicode edge cases | ❌ Not tested | Medium |

### Integration Gaps

| Area | Status | Risk |
|------|--------|------|
| Web framework integration | ❌ Not tested | Medium |
| API usage patterns | ❌ Not tested | Medium |
| Error recovery | ❌ Not tested | Medium |
| Timeout handling | ❌ Not tested | Low |
| File permission errors | ❌ Not tested | Low |

### Pattern Gaps

| Category | Gap Description |
|----------|-----------------|
| New attack vectors | Emerging techniques not covered |
| Language variations | Non-English attacks minimal |
| Multi-modal | Image-in-text limited |
| Context-dependent | Same text, different intent |

---

## Test Quality Assessment

### Strengths

- ✅ Covers major attack categories
- ✅ Includes benign content validation
- ✅ Automated test runner
- ✅ JSON output for analysis
- ✅ Reproducible results

### Weaknesses

- ⚠️ Limited test cases per category
- ⚠️ No fuzzing or property-based testing
- ⚠️ No integration tests
- ⚠️ Manual edge case testing only
- ⚠️ Single language (English) focus

---

## Adding Test Coverage

### To Add Baseline Tests

1. Create test file in `test_inputs/baseline/`
2. Add manifest entry with expected risk level
3. Run test suite to validate

### To Add Evasion Tests

1. Create encoded/obfuscated attack in `test_inputs/evasion/`
2. Add manifest entry
3. Run test suite

### To Add Benign Tests

1. Create legitimate content in `test_inputs/benign/`
2. Add manifest entry with `expected_risk: WHITE`
3. Run test suite - should NOT be flagged

---

## Recommended Additional Testing

### High Priority

1. **Large file handling** - Test with 1MB, 5MB, 10MB files
2. **Encoding errors** - Test with ISO-8859-1, UTF-16
3. **Edge cases** - Empty files, single character, very long lines

### Medium Priority

4. **Non-English attacks** - Spanish, French, German variants
5. **Mixed content** - Code with comments, markdown with code
6. **Real-world samples** - Actual attack attempts (sanitized)

### Low Priority

7. **Performance regression** - Automated latency checks
8. **Memory profiling** - Peak memory usage
9. **Concurrent access** - Multiple simultaneous scans

---

## Running Coverage Analysis

### Basic Test Run

```bash
cd mps-test-agent
python -B scripts/run_tests.py
```

### Detailed Results

```bash
cat test_outputs/full_test_results.json | python -m json.tool
```

### Category Breakdown

```python
import json

with open("test_outputs/full_test_results.json") as f:
    results = json.load(f)

for category, data in results["summary"]["category_breakdown"].items():
    pct = data["passed"] / data["total"] * 100
    print(f"{category}: {data['passed']}/{data['total']} ({pct:.1f}%)")
```

---

## Coverage Goals

### Current (V2)

| Metric | Actual | Target | Status |
|--------|--------|--------|--------|
| Baseline | 48.5% | 50% | ⚠️ Close |
| Evasion | 5.6% | 35% | ❌ Below |
| Benign | 93.3% | 90% | ✅ Met |

### Future (V3)

| Metric | Target | Notes |
|--------|--------|-------|
| Baseline | 55% | With improved patterns |
| Evasion | 30% | With preprocessing |
| Benign | 90% | Maintain accuracy |
| Test count | 100+ | More edge cases |

---

© 2025 StrategicPromptArchitect
