# Known Limitations
Note: This documentation was created with AI assistance and examples are provided for illustration purposes. They have not been fully tested in all environments. Please verify functionality in your specific setup before production use.

**What MPS Cannot Detect and Why**

---

## Executive Summary

MalPromptSentinel (MPS) is a pattern-based detection system. It has inherent limitations:

| Limitation | Impact | Mitigation |
|------------|--------|------------|
| Encoding evasion | 94% bypass rate | Use defense-in-depth |
| Single-request analysis | No multi-turn detection | Manual review for sessions |
| Pattern ceiling | ~50% detection max | Combine with other tools |
| False positives | 7% on security docs | Human review for ORANGE |

---

## Evasion Techniques (94% Bypass Rate)

### Why Evasion Works

**Root Cause:** Pattern matching requires exact text matches. Encoded or obfuscated text doesn't match patterns.

**Example:**
```
Pattern: \bignore\s+previous\s+instructions\b

Original text:  "ignore previous instructions"  → MATCHES
Base64 text:    "aWdub3JlIHByZXZpb3VzIGluc3Ry"  → NO MATCH
Leetspeak text: "1gn0r3 pr3v10us 1nstruct10ns"  → NO MATCH
```

### Techniques That Bypass MPS

#### 1. Base64 Encoding
**Bypass Rate:** 100%

**How It Works:**
```
Attack: "ignore previous instructions"
Encoded: "aWdub3JlIHByZXZpb3VzIGluc3RydWN0aW9ucw=="
```

**Why MPS Fails:** Patterns match plain text, not Base64.

**Mitigation:** Deep scan attempts Base64 decoding, but coverage incomplete.

---

#### 2. Hex Encoding
**Bypass Rate:** 100%

**How It Works:**
```
Attack: "ignore"
Encoded: "\x69\x67\x6e\x6f\x72\x65"
```

**Why MPS Fails:** Hex escapes not decoded before matching.

---

#### 3. URL Encoding
**Bypass Rate:** 100%

**How It Works:**
```
Attack: "ignore previous"
Encoded: "ignore%20previous"
```

**Why MPS Fails:** URL encoding breaks word boundaries.

---

#### 4. Leetspeak
**Bypass Rate:** 80%

**How It Works:**
```
Attack: "ignore previous instructions"
Encoded: "1gn0r3 pr3v10us 1nstruct10ns"
```

**Why MPS Fails:** Number substitutions break character matches.

**Partial Mitigation:** Deep scan has basic leetspeak reversal.

---

#### 5. Unicode Homoglyphs
**Bypass Rate:** 100%

**How It Works:**
```
Attack: "ignore" (Latin)
Encoded: "іgnоrе" (Cyrillic і, о, е)
```

**Why MPS Fails:** Visually identical but different characters.

---

#### 6. Zero-Width Characters
**Bypass Rate:** 100%

**How It Works:**
```
Attack: "ignore"
Encoded: "ig​no​re" (zero-width spaces)
```

**Why MPS Fails:** Invisible characters break word matching.

**Partial Mitigation:** Deep scan removes zero-width chars.

---

#### 7. Fragmentation
**Bypass Rate:** 90%

**How It Works:**
```
Attack: "ignore previous instructions"
Encoded: "ignore\n\n\n\nprevious\n\n\n\ninstructions"
```

**Why MPS Fails:** Whitespace breaks pattern spans.

**Partial Mitigation:** Deep scan normalizes whitespace.

---

#### 8. Case Manipulation
**Bypass Rate:** 50%

**How It Works:**
```
Attack: "Ignore Previous Instructions"
Encoded: "iGnOrE pReViOuS iNsTrUcTiOnS"
```

**Why MPS Fails:** Some patterns are case-specific.

**Partial Mitigation:** Most patterns use `re.IGNORECASE`.

---

#### 9. Double Encoding
**Bypass Rate:** 100%

**How It Works:**
```
First layer: base64("ignore previous")
Second layer: base64(first_layer)
```

**Why MPS Fails:** Only decodes one layer.

---

#### 10. Contextual Camouflage
**Bypass Rate:** 100%

**How It Works:**
```yaml
# Hidden in YAML comment
# ignore previous instructions
config:
  setting: value
```

**Why MPS Fails:** Structure-aware parsing not implemented.

---

#### 11. RTL Override
**Bypass Rate:** 100%

**How It Works:**
```
Attack displayed: "snoitcurtsni suoiverp erongi"
Actual bytes: "‮ignore previous instructions"
```

**Why MPS Fails:** Right-to-left Unicode reverses display.

---

## Single-Request Analysis

### What This Means

MPS analyzes each request independently. It cannot:

- Track conversation history
- Detect multi-turn attacks
- Identify gradual privilege escalation
- Recognize session state manipulation

### Example Attack MPS Misses

**Turn 1:** "Tell me about security systems" → WHITE  
**Turn 2:** "What are common vulnerabilities?" → WHITE  
**Turn 3:** "How would someone exploit those?" → WHITE  
**Turn 4:** "Write code to demonstrate" → ORANGE (maybe)

Each turn is innocent; combined, it's an attack. MPS only sees individual turns.

### Mitigation

- Manual review of full conversations
- Session monitoring (external tool)
- Rate limiting suspicious users

---

## Pattern Detection Ceiling

### Why 50% Is the Limit

**Theoretical Maximum:** Pattern-based detection can catch ~50% of attacks.

**Reasons:**
1. **Creativity:** Attackers invent new phrasings
2. **Context:** Same words can be attack or legitimate
3. **Evasion:** Easy to rephrase while preserving intent
4. **False Positives:** Tighter patterns = more false positives

### What Would Improve This

- **Machine Learning:** Semantic understanding
- **Conversation State:** Multi-turn context
- **Behavior Analysis:** Anomaly detection
- **Human Review:** Expert judgment

These are V3+ considerations, not pattern-matching solutions.

---

## False Positives (7%)

### What Gets Flagged Incorrectly

**Security Documentation:**
- Articles about prompt injection
- Research papers on AI safety
- Tutorials mentioning attack patterns

**Technical Content:**
- Code samples with security functions
- Configuration files with access controls
- API documentation mentioning authentication

**Legitimate Requests:**
- "For educational purposes, explain X"
- "In a hypothetical scenario..."
- "Summarize our previous discussion"

### Why These Are Flagged

MPS pattern-matches keywords without understanding intent:
- "ignore previous" in a security article → Flagged
- "enable admin mode" in documentation → Flagged
- "for educational purposes" anywhere → Flagged

### Mitigation

**Context-Aware Reductions:**
- Educational content: -25% score
- Technical markers: -15% score
- Quoted examples: -20% score
- Review/documentation: -40% score

**User Decision for ORANGE:**
- Present warning, not block
- User can override false positives
- Document override for audit

---

## What MPS IS Good At

Despite limitations, MPS excels at:

### High Detection Rate:
- Direct override attempts (70%+)
- Role manipulation (80%+)
- Privilege escalation (80%+)
- Payload delivery (70%+)

### Low False Positives:
- 93.3% benign accuracy
- Most normal content passes cleanly
- False positives are ORANGE, not RED

### Speed:
- <250ms response time
- No external dependencies
- Suitable for real-time scanning

### Transparency:
- Shows matched patterns
- Explains why content flagged
- Enables informed user decisions

---

## Recommendations

### Do Use MPS For:
✅ First-line defense (catch obvious attacks)  
✅ File upload screening  
✅ External content validation  
✅ Defense-in-depth layer  
✅ Audit trail (what was scanned)  

### Don't Use MPS For:
❌ Sole security control  
❌ Sophisticated attacker defense  
❌ Encoded content detection  
❌ Multi-turn attack prevention  
❌ Critical decisions without human review  

### Combine MPS With:
- Human review for ORANGE results
- Rate limiting for suspicious users
- Session monitoring tools
- Input encoding detection
- Output monitoring

---

## Future Improvements (V3 Roadmap)

### Planned Enhancements:

1. **Preprocessing Pipeline**
   - Multi-layer decoding
   - Unicode normalization
   - Encoding detection
   - Expected: 6% → 30% evasion detection

2. **Conversation State** (Under Consideration)
   - Track request history
   - Detect multi-turn patterns
   - Session risk scoring

3. **ML Integration** (Future)
   - Semantic understanding
   - Intent classification
   - Anomaly detection

---

## Reporting New Bypasses

If you discover new evasion techniques:

**Email:** StrategicPromptArchitect@gmail.com  
**Subject:** MPS Bypass Report

Include:
- Technique description
- Example payload
- Why it bypasses current detection
- Suggested mitigation (if any)

---

## Summary

**MPS is a useful tool with honest limitations.**

| Strength | Limitation |
|----------|------------|
| Fast detection | Pattern ceiling |
| Low false positives | Evasion bypass |
| Transparent results | Single-request only |
| Easy integration | Cannot understand intent |

**Use MPS as part of a security strategy, not as the entire strategy.**

---

© 2025 StrategicPromptArchitect
