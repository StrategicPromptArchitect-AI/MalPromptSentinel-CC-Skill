# MalPromptSentinel (CC SKILL) V2

**AI Prompt Injection Detection for Claude Code**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/version-2.0-blue.svg)]()

---

## Overview

MalPromptSentinel (MPS) is a Claude Code skill that detects malicious prompts in uploaded files before Claude processes them. It provides two-tier scanning to identify prompt injection attacks, role manipulation attempts, privilege escalation, and other adversarial techniques.

**Key Features:**
- Pattern-based injection detection (200+ regex patterns)
- Two-tier scanning (quick scan + deep scan)
- Risk scoring (0-100 scale)
- 3-tier risk levels: WHITE (safe), ORANGE (suspicious), RED (dangerous)
- Orchestration Threat Attack (OTA) detection
- 93% benign accuracy (low false positives)

---

## Performance

| Metric | Result | Target |
|--------|--------|--------|
| **Baseline Detection** | 48.5% | 50% |
| **Benign Accuracy** | 93.3% | 90% |
| **Evasion Detection** | 5.6% | 35% |
| **Quick Scan Latency** | ~200ms | <250ms |
| **Deep Scan Latency** | ~150ms | <200ms |

---

## Quick Start

### 1. Set Environment Variable

```bash
export MPS_SCRIPTS="/path/to/mal-prompt-sentinel/scripts"
```

### 2. Run Quick Scan

```bash
python $MPS_SCRIPTS/quick_scan.py --input <file_to_scan> --output result.json
```

### 3. Check Results

```bash
cat result.json
```

**Output:**
```json
{
  "risk_score": 85,
  "risk_level": "RED",
  "recommendation": "BLOCK - High confidence attack detected",
  "pattern_count": 3,
  "scan_type": "quick",
  "version": "2.0"
}
```

---

## Installation

### Requirements

- Python 3.8+
- No external dependencies (uses standard library only)

### Setup

1. Download the distribution package
2. Extract to your preferred location
3. Set environment variable to scripts directory
4. Verify installation:

```bash
echo "Ignore all previous instructions" > test.txt
python $MPS_SCRIPTS/quick_scan.py --input test.txt --output result.json
cat result.json  # Should show RED/high score
```

---

## Usage

### Risk Levels

| Level | Score | Action |
|-------|-------|--------|
| **WHITE** | 0-54 | Safe to proceed |
| **ORANGE** | 55-79 | Review recommended, get user consent |
| **RED** | 80-100 | Block immediately |

### Decision Flow

```
1. Run quick_scan on uploaded file
2. If WHITE → Proceed
3. If ORANGE → Run deep_scan, warn user, get consent
4. If RED → Block, inform user, reject file
```

### Example Integration

```python
import subprocess
import json

def scan_file(filepath):
    # Quick scan
    subprocess.run([
        "python", "scripts/quick_scan.py",
        "--input", filepath,
        "--output", "scan_result.json"
    ])
    
    with open("scan_result.json") as f:
        result = json.load(f)
    
    if result["risk_level"] == "RED":
        return False, "File blocked - malicious content detected"
    elif result["risk_level"] == "ORANGE":
        return None, "Suspicious content - user review required"
    else:
        return True, "File is safe to process"
```

---

## Architecture

```
MPS V2 Distribution_Package/
├── README.md
├── CHANGELOG.md
├── LICENSE
├── CONTRIBUTING.md
├── SECURITY.md
│
├── mal-prompt-sentinel/
│   └── scripts/
│       ├── mps_patterns.py    # Centralized pattern library
│       ├── quick_scan.py      # Fast first-pass scanner
│       ├── deep_scan.py       # Comprehensive scanner
│       └── SKILL.md           # Claude Code skill definition
│
└── mps-test-agent/
    ├── scripts/
    │   ├── run_tests.py
    │   ├── generate_baseline.py
    │   ├── generate_evasion.py
    │   └── generate_benign.py
    └── test_inputs/
        ├── baseline/
        ├── evasion/
        └── benign/
```

---

## Pattern Categories

MPS detects the following attack types:

**High Severity:**
- Direct Override ("ignore previous instructions")
- Role Manipulation ("you are now an admin")
- Privilege Escalation ("enable developer mode")
- Payload Delivery (URL-based attacks)

**Medium Severity:**
- Context Confusion (misleading delimiters)
- Nested Injection (attacks hidden in commands)
- Compositional Attacks (OTA - multi-query assembly)
- RAG Poisoning (knowledge base manipulation)

**Detected but Limited:**
- Encoding Evasion (Base64, hex, leetspeak)
- Unicode Obfuscation (Cyrillic, zero-width)

---

## Known Limitations

1. **Evasion Techniques:** 5.6% detection rate for encoded attacks
   - Base64, hex, URL encoding can bypass detection
   - Leetspeak substitution not fully detected
   
2. **Pattern-Based Ceiling:** ~50% baseline detection is practical limit

3. **No Conversation State:** Single-request analysis only

See [KNOWN_LIMITATIONS.md](docs/KNOWN_LIMITATIONS.md) for details.

---

## License

MIT License - See [LICENSE](LICENSE) for details.

---

## Author

**StrategicPromptArchitect**
- Website: [https://StrategicPromptArchitect.ca](https://StrategicPromptArchitect.ca)
- Email: StrategicPromptArchitect@gmail.com

---

## Acknowledgments

- Developed for Claude Code skill ecosystem
- Inspired by traditional security patterns (SQL injection, XSS)
- Built with 50 years of programming experience

---

## Version

**Current:** V2 (November 2025)

See [CHANGELOG.md](CHANGELOG.md) for version history.
