# Usage Examples

> **Note:** This documentation was created with AI assistance and examples are provided for illustration purposes. They have not been fully tested in all environments. Please verify functionality in your specific setup before production use.

---

**Simple Integration Patterns for MPS**

---

## ⚠️ Important Notice

These examples demonstrate basic MPS usage. They are:
- **Illustrative** - Show concepts, not production-ready code
- **Untested** - May require adjustments for your environment
- **Simplified** - Error handling minimal for clarity

For advanced integration patterns, see [ADVANCED_EXAMPLES.md](ADVANCED_EXAMPLES.md).

---

## Example 1: Scan a Single File

**What it does:** Scans a text file and outputs results to JSON.

**Skill level:** Beginner

```bash
python quick_scan.py --input document.txt --output result.json
```

**Output:** Creates `result.json` with risk assessment.

---

## Example 2: Check Risk Level (Linux/macOS)

**What it does:** Scans a file and takes action based on exit code.

**Skill level:** Beginner

```bash
python quick_scan.py --input file.txt --output result.json
EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    echo "Safe to proceed"
elif [ $EXIT_CODE -eq 1 ]; then
    echo "Review recommended"
else
    echo "Blocked - dangerous content"
fi
```

**Exit codes:**
- 0 = WHITE (safe)
- 1 = ORANGE (suspicious)
- 2 = RED (dangerous)

---

## Example 3: Check Risk Level (Windows)

**What it does:** Same as above, for Windows command prompt.

**Skill level:** Beginner

```batch
python quick_scan.py --input file.txt --output result.json
if %ERRORLEVEL% EQU 0 (
    echo Safe to proceed
) else if %ERRORLEVEL% EQU 1 (
    echo Review recommended
) else (
    echo Blocked - dangerous content
)
```

---

## Example 4: Basic Python Integration

**What it does:** Python function to scan a file and return results.

**Skill level:** Beginner-Intermediate

**Prerequisites:** Basic Python knowledge

```python
import subprocess
import json

def scan_file(filepath):
    """
    Scan a file for prompt injection.
    Returns dict with risk_score and risk_level.
    """
    # Run the scanner
    subprocess.run([
        "python", "scripts/quick_scan.py",
        "--input", filepath,
        "--output", "result.json"
    ])
    
    # Read results
    with open("result.json") as f:
        return json.load(f)


# Usage
result = scan_file("user_upload.txt")
print(f"Risk Level: {result['risk_level']}")
print(f"Risk Score: {result['risk_score']}")
```

**What the code does:**
- `subprocess.run()` - Runs the scanner as a separate process
- `json.load()` - Reads the JSON output file
- Returns a dictionary with scan results

---

## Example 5: Simple Safe/Unsafe Check

**What it does:** Returns True if file is safe, False otherwise.

**Skill level:** Beginner-Intermediate

```python
import subprocess
import json

def is_safe(filepath):
    """
    Check if a file is safe to process.
    Returns True for WHITE, False for ORANGE/RED.
    """
    subprocess.run([
        "python", "scripts/quick_scan.py",
        "--input", filepath,
        "--output", "result.json"
    ])
    
    with open("result.json") as f:
        result = json.load(f)
    
    return result["risk_level"] == "WHITE"


# Usage
if is_safe("document.txt"):
    print("File is safe - proceed")
else:
    print("File flagged - review needed")
```

---

## Example 6: View Matched Patterns

**What it does:** Shows which attack patterns were detected.

**Skill level:** Beginner-Intermediate

```python
import subprocess
import json

def show_patterns(filepath):
    """Show what patterns were detected in a file."""
    subprocess.run([
        "python", "scripts/quick_scan.py",
        "--input", filepath,
        "--output", "result.json"
    ])
    
    with open("result.json") as f:
        result = json.load(f)
    
    print(f"Risk Level: {result['risk_level']}")
    print(f"Risk Score: {result['risk_score']}")
    
    patterns = result.get("matched_patterns", {})
    if patterns:
        print("\nDetected Patterns:")
        for category in patterns.keys():
            print(f"  - {category}")
    else:
        print("\nNo suspicious patterns detected.")


# Usage
show_patterns("suspicious_file.txt")
```

---

## Quick Reference

| Task | Command/Code |
|------|--------------|
| Scan file | `python quick_scan.py --input FILE --output result.json` |
| Deep scan | `python deep_scan.py --input FILE --output result.json` |
| Check if safe | `result["risk_level"] == "WHITE"` |
| Get score | `result["risk_score"]` |
| Get patterns | `result["matched_patterns"].keys()` |

---

## Next Steps

- **More complex integrations:** See [ADVANCED_EXAMPLES.md](ADVANCED_EXAMPLES.md)
- **API details:** See [API.md](API.md)
- **Testing:** See [TESTING.md](TESTING.md)

---

© 2025 StrategicPromptArchitect