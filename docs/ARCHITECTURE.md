# MPS Architecture
Note: This documentation was created with AI assistance and examples are provided for illustration purposes. They have not been fully tested in all environments. Please verify functionality in your specific setup before production use.

**How MalPromptSentinel Works**

---

## Overview

MPS uses a two-tier scanning architecture:

```
Input Text
    │
    ▼
┌─────────────┐
│ Quick Scan  │ ──→ WHITE (safe) ──→ Proceed
│  (~200ms)   │
└─────────────┘
    │
    ▼ (ORANGE/RED)
┌─────────────┐
│ Deep Scan   │ ──→ Final Decision
│  (~150ms)   │
└─────────────┘
```

---

## Component Overview

### 1. Pattern Library (`mps_patterns.py`)

**Purpose:** Centralized pattern definitions

**Structure:**
```python
SHARED_PATTERNS = {
    'category_name': [
        r'regex_pattern_1',
        r'regex_pattern_2',
    ],
}

DEEP_SCAN_ONLY = {
    # Patterns only used by deep scan
}

PATTERN_WEIGHTS = {
    'category_name': 70,  # Risk weight
}
```

**Why Centralized:**
- Single source of truth
- No sync issues between scanners
- Easy to add/modify patterns
- Version controlled

---

### 2. Quick Scan (`quick_scan.py`)

**Purpose:** Fast first-pass detection

**Flow:**
```
Input Text
    │
    ▼
[Pattern Matching]
    │
    ▼
[Calculate Base Score]
    │
    ▼
[Apply Bonuses]
  - Clustering bonus
  - Combo bonus
  - Density bonus
    │
    ▼
[Apply Reductions]
  - Quote context
  - Technical content
  - Educational content
  - Review/documentation
  - Legitimate composition
    │
    ▼
[Determine Risk Level]
    │
    ▼
Output JSON
```

**Key Features:**
- No preprocessing (raw text matching)
- Fast execution (~200ms)
- Optimized for common attacks
- Exit code indicates risk level

---

### 3. Deep Scan (`deep_scan.py`)

**Purpose:** Comprehensive analysis with evasion detection

**Flow:**
```
Input Text
    │
    ▼
[Preprocessing]
  - Base64 decoding
  - Hex decoding
  - URL decoding
  - Unicode normalization
  - Zero-width removal
  - Leetspeak reversal
  - Whitespace normalization
    │
    ▼
[Pattern Matching on ALL versions]
    │
    ▼
[Calculate Base Score]
    │
    ▼
[Apply Context Reductions]
  - Compositional/OTA handling
  - Educational content
  - Technical content
  - Image/multimodal context
  - Session persistence context
    │
    ▼
[Determine Risk Level]
    │
    ▼
Output JSON
```

**Key Features:**
- Multi-layer preprocessing
- Evasion technique detection
- Context-aware scoring
- Higher accuracy, slightly slower

---

## Pattern Matching Logic

### How Patterns are Matched

```python
for category, patterns in PATTERNS.items():
    for pattern in patterns:
        matches = re.finditer(pattern, text, re.IGNORECASE | re.DOTALL)
        for match in matches:
            record_match(category, pattern, match)
```

### Scoring Algorithm

**Base Score:**
```python
for category, matches in matched_patterns.items():
    weight = PATTERN_WEIGHTS[category]
    
    if len(matches) == 1:
        score += weight
    else:
        # Diminishing returns for multiple matches
        score += weight * (1 - 0.5 ** len(matches))
```

**Bonuses:**
```python
# Clustering: Patterns close together = intentional
if patterns_within_50_chars >= 2:
    score *= 1.2  # 20% boost

# Combo: Multiple categories = coordinated attack
if len(matched_categories) >= 2:
    score += 10 * len(matched_categories)

# Density: 3+ matches in same category = focused attack
if any_category_has_3_plus_matches:
    score += 20
```

**Reductions:**
```python
# Quote context: Pattern in quotes = example
if pattern_in_quotes and score >= 40:
    score *= 0.8  # 20% reduction

# Technical content: Code samples
if is_technical and score >= 40:
    score *= 0.85  # 15% reduction

# Educational: Academic/research content
if is_educational and score >= 40:
    score *= 0.75  # 25% reduction
```

---

## Risk Level Determination

```python
if risk_score >= 80:
    risk_level = "RED"
    recommendation = "BLOCK - High confidence attack detected"

elif risk_score >= 55:
    risk_level = "ORANGE"
    recommendation = "REVIEW - Moderate risk detected"

else:
    risk_level = "WHITE"
    recommendation = "PROCEED - No significant threats"
```

**Thresholds:**
- WHITE: 0-54 (safe)
- ORANGE: 55-79 (suspicious)
- RED: 80-100 (dangerous)

---

## Preprocessing Pipeline (Deep Scan)

### Base64 Decoding

```python
# Find Base64-like strings
b64_pattern = r'[A-Za-z0-9+/]{20,}={0,2}'
matches = re.findall(b64_pattern, text)

# Try multi-layer decoding (up to 3 levels)
for match in matches:
    for layer in range(3):
        decoded = base64.b64decode(match).decode('utf-8')
        if valid(decoded):
            versions['decoded'] = decoded
```

### Leetspeak Reversal

```python
leet_map = {
    '4': 'a', '3': 'e', '1': 'i', '0': 'o',
    '5': 's', '7': 't', '@': 'a', '$': 's'
}

for leet, normal in leet_map.items():
    text = text.replace(leet, normal)
```

### Zero-Width Removal

```python
zero_width = r'[\u200B-\u200D\uFEFF]'
cleaned = re.sub(zero_width, '', text)
```

---

## File Structure

```
mal-prompt-sentinel/
└── scripts/
    ├── mps_patterns.py   # Pattern definitions
    │   ├── SHARED_PATTERNS
    │   ├── DEEP_SCAN_ONLY
    │   ├── PATTERN_WEIGHTS
    │   └── get_patterns_for_scanner()
    │
    ├── quick_scan.py     # Fast scanner
    │   ├── quick_scan()
    │   └── main()
    │
    └── deep_scan.py      # Comprehensive scanner
        ├── DeepScanner class
        │   ├── __init__()
        │   ├── preprocess()
        │   ├── scan_text()
        │   └── analyze()
        └── main()
```

---

## Data Flow

### Input Processing

```
User File → Read UTF-8 → Validate → Scan → Output JSON
```

### Error Handling

```
Read Error → Exit 1, stderr message
Encoding Error → Exit 1, stderr message
Scan Complete → Exit 0/1/2 based on risk level
```

### Output Generation

```python
output = {
    'risk_score': int,        # 0-100
    'risk_level': str,        # WHITE/ORANGE/RED
    'recommendation': str,    # Human-readable action
    'matched_patterns': dict, # Category → matches
    'pattern_count': int,     # Total matches
    'scan_type': str,         # quick/deep
    'version': str            # 2.0
}
```

---

## Extension Points

### Adding New Patterns

**Location:** `mps_patterns.py`

```python
# Add to SHARED_PATTERNS for both scanners
SHARED_PATTERNS['new_category'] = [
    r'pattern_1',
    r'pattern_2',
]

# Add weight
PATTERN_WEIGHTS['new_category'] = 50
```

### Adding New Reductions

**Location:** `quick_scan.py` or `deep_scan.py`

```python
# Add new marker detection
new_markers = [
    r'\bmarker_pattern\b',
]

is_new_context = any(re.search(p, text, re.IGNORECASE) for p in new_markers)

if is_new_context and risk_score >= 40:
    risk_score = int(risk_score * 0.8)  # 20% reduction
```

### Adding New Preprocessing

**Location:** `deep_scan.py` in `preprocess()` method

```python
def preprocess(self, text):
    versions = {'original': text}
    
    # Add new preprocessing
    versions['new_version'] = self.new_decoder(text)
    
    return versions
```

---

## Performance Considerations

### Quick Scan Optimizations

- Compiled regex patterns (Python caches)
- Early exit not implemented (scans all patterns)
- Minimal memory allocation

### Deep Scan Optimizations

- Preprocessing only creates needed versions
- Pattern matching on original first
- Decoded versions only if suspicion

### Memory Usage

- Quick scan: <50MB typical
- Deep scan: <100MB typical
- Large files (>1MB) may use more

---

## Security Considerations

### Regex Safety

- Patterns tested for ReDoS vulnerability
- Limited lookahead/lookbehind
- Timeout recommended for untrusted input

### Input Validation

- UTF-8 encoding required
- File size should be limited
- Binary files not supported

---

## Version History

- V1 (2024): Initial architecture, inline patterns
- V2 (2025): Centralized patterns, improved reductions

---

© 2025 StrategicPromptArchitect
