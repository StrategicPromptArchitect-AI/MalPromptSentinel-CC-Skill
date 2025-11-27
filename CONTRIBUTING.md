# Contributing to MalPromptSentinel

Thank you for your interest in contributing to MalPromptSentinel (MPS)!

---

## Contribution Process

**MPS uses a contact-first contribution model.**

Before making any changes or submitting contributions, please contact the maintainer:

**Email:** StrategicPromptArchitect@gmail.com

**Subject Line:** MPS Contribution - [Brief Description]

**Include:**
1. What you want to change or add
2. Why it would improve MPS
3. Your relevant experience
4. Proposed approach

---

## Why Contact First?

1. **Coordination** - Avoid duplicate work
2. **Architecture** - Ensure changes fit the design
3. **Quality** - Discuss approach before implementation
4. **Focus** - Keep MPS aligned with its goals

---

## Types of Contributions Welcome

### High Priority
- **New injection patterns** - Real-world attack patterns you've encountered
- **False positive fixes** - Benign content incorrectly flagged
- **Bug fixes** - Issues in scanning logic
- **Performance improvements** - Faster scanning, lower memory

### Medium Priority
- **Documentation improvements** - Clearer explanations, examples
- **Test cases** - New baseline, evasion, or benign tests
- **Integration examples** - How you're using MPS

### Lower Priority (Discuss First)
- **Architecture changes** - Major refactoring
- **New features** - Additional capabilities
- **Dependency additions** - External libraries

---

## Code Style

If your contribution is approved:

### Python
- Follow PEP 8 style guide
- Use meaningful variable names
- Comment complex regex patterns
- Include docstrings for functions

### Patterns
- Add to `mps_patterns.py` (not scanner files)
- Include comment explaining what pattern catches
- Test against both attack and benign content
- Document false positive potential

### Example Pattern Addition
```python
# In SHARED_PATTERNS dictionary:
'new_category': [
    # Catches: "malicious phrase here"
    # False positives: May match in security documentation
    r'\bmalicious\s+phrase\s+here\b',
],
```

---

## Testing Requirements

All contributions must:

1. **Pass existing tests**
   ```bash
   python -B run_tests.py
   ```

2. **Not decrease benign accuracy** (currently 93.3%)

3. **Include test cases** for new patterns

4. **Document expected impact** on detection rates

---

## What Happens After Contact

1. **Review** - I'll review your proposal (typically within 1 week)
2. **Discussion** - We'll discuss approach if needed
3. **Approval** - You'll get go-ahead to implement
4. **Submission** - Send completed code via email
5. **Integration** - I'll review, test, and integrate
6. **Credit** - You'll be acknowledged in CHANGELOG

---

## Code of Conduct

- Be respectful and professional
- Focus on technical merit
- Accept feedback gracefully
- Give credit where due

---

## Questions?

**Email:** StrategicPromptArchitect@gmail.com

**Website:** https://StrategicPromptArchitect.ca

---

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

*Thank you for helping improve AI security!*
