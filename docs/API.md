# MPS API Reference
Note: This documentation was created with AI assistance and examples are provided for illustration purposes. They have not been fully tested in all environments. Please verify functionality in your specific setup before production use.

**Scanner Command-Line Interface and Output Formats**

---

## Quick Scan API

### Command

```bash
python quick_scan.py --input <file> --output <result.json> [--mode <mode>]
```

### Arguments

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `--input` | Yes | - | Path to file to scan |
| `--output` | Yes | - | Path for JSON output |
| `--mode` | No | `auto` | Scan mode: `auto` or `shallow-only` |

### Example

```bash
python scripts/quick_scan.py --input uploaded.txt --output result.json
```

### Exit Codes

| Code | Risk Level | Meaning |
|------|------------|---------|
| 0 | WHITE | Safe content |
| 1 | ORANGE | Suspicious content |
| 2 | RED | Dangerous content |

### Output Format

```json
{
  "risk_score": 85,
  "risk_level": "RED",
  "recommendation": "BLOCK - High confidence attack detected",
  "matched_patterns": {
    "direct_override": [
      {
        "pattern": "\\b(ignore|disregard)\\s+.*",
        "text": "ignore all previous instructions",
        "position": [0, 32]
      }
    ]
  },
  "pattern_count": 1,
  "scan_type": "quick",
  "mode": "auto",
  "version": "2.0"
}
```

### Output Fields

| Field | Type | Description |
|-------|------|-------------|
| `risk_score` | int | 0-100 risk score |
| `risk_level` | string | WHITE, ORANGE, or RED |
| `recommendation` | string | Human-readable action |
| `matched_patterns` | object | Categories → match arrays |
| `pattern_count` | int | Total patterns matched |
| `scan_type` | string | Always "quick" |
| `mode` | string | Scan mode used |
| `version` | string | Scanner version |

### Match Object

| Field | Type | Description |
|-------|------|-------------|
| `pattern` | string | Regex pattern (truncated to 50 chars) |
| `text` | string | Matched text (truncated to 100 chars) |
| `position` | array | [start, end] character positions |

---

## Deep Scan API

### Command

```bash
python deep_scan.py --input <file> --output <result.json> [--mode <mode>]
```

### Arguments

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `--input` | Yes | - | Path to file to scan |
| `--output` | Yes | - | Path for JSON output |
| `--mode` | No | `thorough` | Scan mode: `thorough` or `quick` |

### Example

```bash
python scripts/deep_scan.py --input uploaded.txt --output deep_result.json
```

### Exit Codes

| Code | Risk Level | Meaning |
|------|------------|---------|
| 0 | WHITE | Safe content |
| 1 | ORANGE/RED | Suspicious or dangerous |

### Output Format

```json
{
  "risk_score": 65,
  "risk_level": "ORANGE",
  "recommendation": "REVIEW - Moderate risk detected",
  "matched_patterns": {
    "semantic_attack": [
      {
        "pattern": "\\bfor\\s+educational\\s+purposes\\b",
        "text": "for educational purposes only",
        "position": [0, 29]
      }
    ]
  },
  "pattern_count": 1,
  "evasion_detected": null,
  "scan_type": "deep",
  "mode": "thorough",
  "version": "2.0"
}
```

### Additional Output Fields

| Field | Type | Description |
|-------|------|-------------|
| `evasion_detected` | object/null | Evasion technique details if found |

### Evasion Detection Object

```json
{
  "evasion_detected": {
    "technique": "base64_encoding",
    "decoded_content": "decoded text here",
    "confidence": "high"
  }
}
```

---

## Pattern Library API

### Importing

```python
from mps_patterns import get_patterns_for_scanner, get_weights
```

### Functions

#### get_patterns_for_scanner(scanner_type)

Returns pattern dictionary for specified scanner.

**Parameters:**
- `scanner_type` (str): `'quick'` or `'deep'`

**Returns:**
- `dict`: Pattern category → regex list

**Example:**
```python
patterns = get_patterns_for_scanner('quick')
# Returns SHARED_PATTERNS only

patterns = get_patterns_for_scanner('deep')
# Returns SHARED_PATTERNS + DEEP_SCAN_ONLY
```

#### get_weights()

Returns pattern weight dictionary.

**Parameters:** None

**Returns:**
- `dict`: Pattern category → weight (int)

**Example:**
```python
weights = get_weights()
print(weights['direct_override'])  # 70
print(weights['role_manipulation'])  # 120
```

---

## Programmatic Usage

### Python Integration

```python
import subprocess
import json

def scan_file(filepath: str, deep: bool = False) -> dict:
    """
    Scan a file and return results.
    
    Args:
        filepath: Path to file to scan
        deep: If True, use deep_scan; else quick_scan
    
    Returns:
        dict: Scan results
    """
    scanner = "deep_scan.py" if deep else "quick_scan.py"
    output_file = "scan_result.json"
    
    result = subprocess.run([
        "python",
        f"scripts/{scanner}",
        "--input", filepath,
        "--output", output_file
    ], capture_output=True, text=True)
    
    if result.returncode not in [0, 1, 2]:
        raise RuntimeError(f"Scan failed: {result.stderr}")
    
    with open(output_file) as f:
        return json.load(f)


def is_safe(filepath: str) -> bool:
    """Check if file is safe (WHITE risk level)."""
    result = scan_file(filepath)
    return result['risk_level'] == 'WHITE'


def get_risk_score(filepath: str) -> int:
    """Get numeric risk score for file."""
    result = scan_file(filepath)
    return result['risk_score']


def get_matched_patterns(filepath: str) -> list:
    """Get list of matched pattern categories."""
    result = scan_file(filepath)
    return list(result.get('matched_patterns', {}).keys())
```

### Batch Processing

```python
from pathlib import Path

def scan_directory(directory: str) -> dict:
    """
    Scan all .txt files in directory.
    
    Returns:
        dict: filepath → scan result
    """
    results = {}
    
    for filepath in Path(directory).glob('*.txt'):
        results[str(filepath)] = scan_file(str(filepath))
    
    return results


def filter_dangerous(scan_results: dict) -> list:
    """Return list of RED-level files."""
    return [
        filepath
        for filepath, result in scan_results.items()
        if result['risk_level'] == 'RED'
    ]
```

---

## Error Handling

### Error Output Format

```json
{
  "error": "Error message here",
  "exit_code": 1
}
```

### Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| `Input file not found` | File doesn't exist | Check path |
| `Error reading input file` | Permission or encoding | Check file access |
| `Unable to decode (not UTF-8)` | Binary or wrong encoding | Convert to UTF-8 |

### Handling Errors

```python
import subprocess
import json

def safe_scan(filepath: str) -> dict:
    """Scan with error handling."""
    try:
        result = subprocess.run([
            "python", "scripts/quick_scan.py",
            "--input", filepath,
            "--output", "result.json"
        ], capture_output=True, text=True, timeout=30)
        
        if result.stderr and "Error" in result.stderr:
            return {"error": result.stderr, "risk_level": "ERROR"}
        
        with open("result.json") as f:
            return json.load(f)
            
    except subprocess.TimeoutExpired:
        return {"error": "Scan timeout", "risk_level": "ERROR"}
    except FileNotFoundError:
        return {"error": "Scanner not found", "risk_level": "ERROR"}
    except json.JSONDecodeError:
        return {"error": "Invalid output", "risk_level": "ERROR"}
```

---

## Performance Characteristics

### Quick Scan

| Metric | Typical | Maximum |
|--------|---------|---------|
| Latency | 200ms | 500ms |
| Memory | 30MB | 50MB |
| File Size | Any | 1MB recommended |

### Deep Scan

| Metric | Typical | Maximum |
|--------|---------|---------|
| Latency | 150ms | 300ms |
| Memory | 60MB | 100MB |
| File Size | Any | 1MB recommended |

### Recommendations

- **Files > 1MB:** Consider chunking
- **Batch processing:** Add delays between scans
- **Production:** Set timeout (30s recommended)

---

## Version Compatibility

| Scanner Version | Pattern Library | Notes |
|-----------------|-----------------|-------|
| 2.0 | mps_patterns.py | Current release |
| 1.x | Inline patterns | Legacy, not compatible |

---

© 2025 StrategicPromptArchitect
