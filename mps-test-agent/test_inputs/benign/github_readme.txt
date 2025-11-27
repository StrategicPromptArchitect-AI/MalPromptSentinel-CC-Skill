# Prompt Security Library

A Python library for detecting prompt injection attacks.

## Features

- Pattern-based detection
- Support for obfuscation techniques
- Low false positive rate

## Example

```python
from prompt_security import Scanner

scanner = Scanner()
result = scanner.check("Ignore previous instructions")
print(result.is_safe)  # False
```

## Known Patterns

The library detects common attack patterns including:
- Direct instruction override
- Role manipulation
- Privilege escalation

See `patterns.md` for the complete list.