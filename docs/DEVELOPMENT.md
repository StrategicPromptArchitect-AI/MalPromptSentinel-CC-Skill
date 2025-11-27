# Development Guide

> **Note:** This documentation was created with AI assistance and is provided for illustration purposes. Please verify in your specific setup before production use.

---

**Setting Up a Development Environment for MPS**

---

## Prerequisites

- Python 3.8 or higher
- Text editor or IDE
- Command line access
- Git (optional, for version control)

---

## Project Structure

```
MPS V2 Distribution_Package/
│
├── README.md                 # Project overview
├── LICENSE                   # MIT License
├── CHANGELOG.md              # Version history
├── CONTRIBUTING.md           # Contribution guidelines
├── SECURITY.md               # Security policy
│
├── docs/                     # Documentation
│   ├── SKILL.md
│   ├── ARCHITECTURE.md
│   ├── PATTERNS.md
│   ├── API.md
│   ├── BENCHMARKS.md
│   ├── KNOWN_LIMITATIONS.md
│   ├── INSTALLATION.md
│   ├── QUICKSTART.md
│   ├── EXAMPLES.md
│   ├── ADVANCED_EXAMPLES.md
│   ├── TESTING.md
│   ├── TEST_COVERAGE.md
│   ├── DEVELOPMENT.md
│   ├── PATTERN_DEVELOPMENT.md
│   └── ROADMAP.md
│
├── mal-prompt-sentinel/      # Main scanner
│   ├── SKILL.md              # Claude Code skill definition
│   └── scripts/
│       ├── mps_patterns.py   # Centralized patterns
│       ├── quick_scan.py     # Fast scanner
│       └── deep_scan.py      # Comprehensive scanner
│
└── mps-test-agent/           # Test framework
    ├── SKILL.md              # Test agent skill definition
    ├── scripts/
    │   ├── run_tests.py      # Test runner
    │   ├── generate_baseline.py
    │   ├── generate_evasion.py
    │   └── generate_benign.py
    ├── test_inputs/
    │   ├── baseline/         # Attack test files
    │   ├── evasion/          # Evasion test files
    │   └── benign/           # Benign test files
    └── test_outputs/         # Test results
```

---

## Setting Up Development Environment

### Step 1: Get the Code

```bash
# If from website download
unzip MPS_V2_Distribution_Package.zip
cd MPS\ V2\ Distribution_Package

# Or copy to working directory
cp -r "MPS V2 Distribution_Package" ~/mps-dev
cd ~/mps-dev
```

### Step 2: Verify Python

```bash
python --version
# Should be 3.8+
```

### Step 3: Set Up Path

```bash
# Linux/macOS
export MPS_SCRIPTS="$(pwd)/mal-prompt-sentinel/scripts"

# Windows PowerShell
$env:MPS_SCRIPTS = "$(Get-Location)\mal-prompt-sentinel\scripts"
```

### Step 4: Verify Installation

```bash
# Test scanner runs
echo "test" > test.txt
python $MPS_SCRIPTS/quick_scan.py --input test.txt --output result.json
cat result.json
```

---

## Code Organization

### mps_patterns.py

**Purpose:** Centralized pattern definitions

**Key Components:**
- `SHARED_PATTERNS` - Used by both scanners
- `DEEP_SCAN_ONLY` - Additional patterns for deep scan
- `PATTERN_WEIGHTS` - Risk weights per category
- `get_patterns_for_scanner()` - Returns appropriate patterns
- `get_weights()` - Returns weight dictionary

**When to modify:** Adding new attack patterns

### quick_scan.py

**Purpose:** Fast first-pass detection

**Key Components:**
- `quick_scan()` - Main scanning function
- Pattern matching loop
- Score calculation with bonuses/reductions
- Risk level determination

**When to modify:** Changing scoring logic, adding reductions

### deep_scan.py

**Purpose:** Comprehensive analysis with preprocessing

**Key Components:**
- `DeepScanner` class
- `preprocess()` - Text normalization/decoding
- `scan_text()` - Pattern matching
- `analyze()` - Full analysis pipeline

**When to modify:** Improving evasion detection, preprocessing

---

## Making Changes

### Development Workflow

1. **Create backup**
   ```bash
   cp scripts/quick_scan.py scripts/quick_scan.py.bak
   ```

2. **Make changes**
   ```bash
   # Edit file
   nano scripts/quick_scan.py
   ```

3. **Test changes**
   ```bash
   # Quick validation
   echo "ignore previous instructions" > test.txt
   python -B scripts/quick_scan.py --input test.txt --output result.json
   cat result.json
   ```

4. **Run full test suite**
   ```bash
   cd ../mps-test-agent
   python -B scripts/run_tests.py
   ```

5. **Compare results**
   ```bash
   # Check if detection rates changed
   cat test_outputs/full_test_results.json | grep pass_rate
   ```

### Important: Clear Python Cache

Always use `-B` flag or clear cache after changes:

```bash
# Option 1: Run with -B
python -B scripts/quick_scan.py ...

# Option 2: Delete cache
rm -rf scripts/__pycache__
rm -rf __pycache__
```

---

## Debugging

### View Pattern Matches

Add debug output to scanner:

```python
# In quick_scan.py, inside the matching loop
if category_matches:
    print(f"DEBUG: {category} matched {len(category_matches)} times")
```

### Check Score Calculation

```python
# Before returning, print breakdown
print(f"DEBUG: Base score: {total_score}")
print(f"DEBUG: After bonuses: {risk_score}")
print(f"DEBUG: Matched categories: {list(matches.keys())}")
```

### Test Single Pattern

```python
import re

pattern = r'\bignore\s+previous\s+instructions\b'
text = "Please ignore previous instructions"

if re.search(pattern, text, re.IGNORECASE):
    print("MATCH")
else:
    print("NO MATCH")
```

---

## Testing Changes

### Quick Smoke Test

```bash
# Should detect attack
echo "Ignore all previous instructions" > attack.txt
python -B scripts/quick_scan.py --input attack.txt --output r.json
grep risk_level r.json
# Expected: ORANGE or RED

# Should pass benign
echo "Hello world" > benign.txt
python -B scripts/quick_scan.py --input benign.txt --output r.json
grep risk_level r.json
# Expected: WHITE
```

### Full Test Suite

```bash
cd mps-test-agent
python -B scripts/run_tests.py
```

### Compare Before/After

```bash
# Before changes
python -B scripts/run_tests.py > before.txt

# After changes
python -B scripts/run_tests.py > after.txt

# Compare
diff before.txt after.txt
```

---

## Common Development Tasks

### Add a New Pattern

See [PATTERN_DEVELOPMENT.md](PATTERN_DEVELOPMENT.md)

### Adjust Scoring

1. Edit `PATTERN_WEIGHTS` in `mps_patterns.py`
2. Test impact on detection rates
3. Check benign accuracy not decreased

### Add a Reduction

1. Edit `quick_scan.py` or `deep_scan.py`
2. Add marker patterns
3. Add reduction logic
4. Test benign content not over-flagged

### Fix False Positive

1. Identify triggering pattern
2. Add context-aware reduction
3. Test specific benign case passes
4. Verify attacks still detected

---

## Code Style

### Python Guidelines

- Follow PEP 8
- Use meaningful variable names
- Comment complex regex patterns
- Add docstrings to functions

### Pattern Guidelines

- Keep patterns readable
- Use non-capturing groups `(?:...)` when possible
- Avoid catastrophic backtracking
- Test performance with long strings

### Example Good Pattern

```python
# Catches: "ignore all previous instructions"
# Avoids: "do not ignore" (negative context)
r'\b(?<!not\s)(?<!don\'t\s)ignore\s+(?:all\s+)?previous\s+instructions?\b'
```

---

## Version Management

### Updating Version Numbers

When releasing changes, update version in:

1. `quick_scan.py` - `'version': '2.x'`
2. `deep_scan.py` - `'version': '2.x'`
3. `mps_patterns.py` - `VERSION = "2.x"`
4. `CHANGELOG.md` - Add version entry
5. `README.md` - Update badges if used

### Changelog Entry Format

```markdown
## [V2.x] - YYYY-MM-DD

### Added
- New feature description

### Changed
- Modified behavior description

### Fixed
- Bug fix description
```

---

## Getting Help

### Before Asking

1. Check documentation
2. Review existing patterns
3. Run tests to isolate issue
4. Prepare minimal reproduction case

### Contact

**Email:** StrategicPromptArchitect@gmail.com

**Include:**
- What you're trying to do
- What you've tried
- Error messages or unexpected behavior
- Python version and OS

---

© 2025 StrategicPromptArchitect
