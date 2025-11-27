# Security Policy

## Reporting Security Vulnerabilities

MalPromptSentinel (MPS) is a security tool. We take security issues seriously.

---

## How to Report

**Email:** StrategicPromptArchitect@gmail.com

**Subject Line:** SECURITY - MPS Vulnerability Report

**Include:**
1. Description of the vulnerability
2. Steps to reproduce
3. Potential impact
4. Suggested fix (if any)

---

## What to Report

### Report These Issues:
- **Pattern bypasses** - Attacks that evade detection
- **False negatives** - Dangerous content marked as safe
- **Code vulnerabilities** - Bugs in scanner logic
- **Regex exploits** - ReDoS or other regex attacks
- **Information disclosure** - Unintended data exposure

### Do NOT Report:
- **Known limitations** - Evasion techniques (documented)
- **Performance issues** - Slow scans, high memory
- **Feature requests** - Use contribution process instead

---

## Response Timeline

| Action | Timeframe |
|--------|-----------|
| Acknowledgment | 48 hours |
| Initial Assessment | 1 week |
| Fix Development | 2-4 weeks |
| Public Disclosure | After fix released |

---

## Disclosure Policy

1. **Report privately** via email
2. **Allow time** for fix development
3. **Coordinate disclosure** timing with maintainer
4. **Credit given** to reporter (unless anonymity requested)

---

## Known Security Limitations

MPS has documented limitations that are NOT vulnerabilities:

### Evasion Techniques (6% detection)
- Base64 encoding bypasses pattern matching
- Hex/URL encoding not fully decoded
- Leetspeak substitution partially detected
- Unicode obfuscation limited detection

**This is by design** - Pattern-based detection has inherent limits.

### Single-Request Analysis
- No conversation state tracking
- Multi-turn attacks not detected
- Session manipulation limited detection

**Mitigation:** Use MPS as part of defense-in-depth strategy.

---

## Security Best Practices

When using MPS:

1. **Don't rely solely on MPS** - Use multiple security layers
2. **Review ORANGE results** - Require human judgment
3. **Always block RED** - High confidence attacks
4. **Monitor for bypasses** - Report new attack patterns
5. **Keep updated** - Use latest version

---

## Scope

This security policy covers:
- `quick_scan.py`
- `deep_scan.py`
- `mps_patterns.py`
- Supporting scripts

Does NOT cover:
- Test framework (mps-test-agent)
- Documentation
- Example code

---

## Contact

**Security Issues:** StrategicPromptArchitect@gmail.com

**General Questions:** Same email, different subject line

**Website:** https://StrategicPromptArchitect.ca

---

## Recognition

Security researchers who report valid vulnerabilities will be:
- Credited in CHANGELOG (unless anonymity requested)
- Acknowledged on website (with permission)
- Thanked publicly (with permission)

---

*Thank you for helping keep MPS secure!*
