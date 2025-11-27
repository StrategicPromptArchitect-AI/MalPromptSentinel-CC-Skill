# MPS Roadmap
Note: This documentation was created with AI assistance and examples are provided for illustration purposes. They have not been fully tested in all environments. Please verify functionality in your specific setup before production use.

**Future Development Plans**

---

## Current Status: V2 (November 2025)

| Metric | Current | Target |
|--------|---------|--------|
| Baseline Detection | 48.5% | 50% ✅ |
| Benign Accuracy | 93.3% | 90% ✅ |
| Evasion Detection | 5.6% | 35% ❌ |

**V2 is production-ready** for use as a defense-in-depth layer.

---

## V3: Evasion Detection (Planned)

**Goal:** Improve evasion detection from 6% to 30-35%

**Timeline:** TBD

**Approach:** Preprocessing Pipeline

### Planned Features

#### Multi-Layer Decoding
```
Input → Base64 Decode → Hex Decode → URL Decode → Pattern Match
```

- Automatic encoding detection
- Multi-pass decoding (up to 3 layers)
- Support for Base64, hex, URL, HTML entities

#### Unicode Normalization
- Cyrillic → Latin conversion
- Homoglyph detection
- Zero-width character removal
- Normalization form NFKC

#### Leetspeak Reversal
- Comprehensive substitution map
- Context-aware reversal
- Partial match handling

#### Whitespace Normalization
- Collapse excessive whitespace
- Remove fragmentation
- Preserve meaningful breaks

### Expected Impact

| Metric | V2 | V3 Target |
|--------|-----|-----------|
| Evasion Detection | 5.6% | 30-35% |
| Baseline Detection | 48.5% | 50%+ |
| Benign Accuracy | 93.3% | 90%+ |

### Implementation Plan

1. **Phase 1:** Encoding detection and decoding
2. **Phase 2:** Unicode normalization
3. **Phase 3:** Whitespace and fragmentation handling
4. **Phase 4:** Integration testing

---

## V4: Conversation State (Under Consideration)

**Goal:** Detect multi-turn attacks

**Timeline:** TBD (research phase)

**Challenge:** Single-request analysis cannot detect gradual attacks

### Potential Features

#### Session Tracking
- Track requests per session
- Accumulate risk scores
- Detect escalation patterns

#### Multi-Turn Pattern Detection
```
Turn 1: "Tell me about security" → LOW
Turn 2: "What are vulnerabilities?" → LOW
Turn 3: "How to exploit them?" → MEDIUM
Accumulated: → HIGH (escalation detected)
```

#### Temporal Analysis
- Request frequency monitoring
- Pattern evolution tracking
- Session risk scoring

### Challenges

- State storage requirements
- Privacy considerations
- Performance overhead
- False positive management

### Decision Factors

- Community demand
- Resource availability
- Alternative solutions
- Implementation complexity

---

## V5: ML Integration (Future Consideration)

**Goal:** Semantic understanding for intent detection

**Timeline:** Long-term (no commitment)

**Note:** This is exploratory, not planned.

### Potential Approaches

#### Embedding-Based Detection
- Encode prompts as vectors
- Compare to known attack embeddings
- Semantic similarity scoring

#### Fine-Tuned Classifier
- Train on labeled attack/benign data
- Binary classification
- Confidence scoring

#### Hybrid Approach
- Pattern matching first (fast)
- ML scoring for uncertain cases
- Human review for edge cases

### Considerations

- Model size and latency
- Training data requirements
- Maintenance burden
- False positive rates
- Dependency management

---

## Community Requests

### How to Request Features

**Email:** StrategicPromptArchitect@gmail.com

**Subject:** MPS Feature Request - [Brief Description]

**Include:**
1. What feature you need
2. Why it would help
3. Example use case
4. Suggested approach (optional)

### Current Requests (Tracking)

| Request | Priority | Status |
|---------|----------|--------|
| Better Base64 decoding | High | V3 planned |
| Unicode homoglyph detection | High | V3 planned |
| Leetspeak reversal | Medium | V3 planned |
| Session tracking | Low | Under consideration |
| ML classifier | Low | Future exploration |

---

## Non-Goals

Things MPS will NOT try to do:

### Real-Time Filtering
MPS is for file/content scanning, not real-time chat filtering.

### Complete Attack Prevention
MPS is one layer, not a complete solution.

### Zero False Positives
Some trade-off between detection and false positives is inevitable.

### Automatic Remediation
MPS detects and reports; it does not automatically fix or sanitize.

---

## Contributing to Roadmap

### Feedback Welcome

Your input shapes priorities. Contact:

**Email:** StrategicPromptArchitect@gmail.com

**Website:** https://StrategicPromptArchitect.ca

### What Helps Most

- Real-world attack samples (anonymized)
- False positive reports
- Integration experience
- Performance feedback
- Use case descriptions

---

## Version History Reference

| Version | Date | Key Changes |
|---------|------|-------------|
| V1 | 2024 | Initial release, inline patterns |
| V2 | Nov 2025 | Centralized patterns, OTA detection, context reductions |
| V3 | TBD | Preprocessing pipeline (planned) |
| V4 | TBD | Conversation state (under consideration) |
| V5 | TBD | ML integration (future exploration) |

---

## Disclaimer

This roadmap represents current thinking and is subject to change. Features may be added, removed, or reprioritized based on:

- Community feedback
- Resource availability
- Technical feasibility
- Changing threat landscape

No timelines are guaranteed.

---

© 2025 StrategicPromptArchitect
