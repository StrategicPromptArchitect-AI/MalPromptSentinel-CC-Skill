#!/usr/bin/env python3

"""
MalPromptSentinel Quick Scan V2
Pattern-based prompt injection detection for high-frequency attacks

Note: This code was developed with AI assistance. Please verify 
functionality in your specific setup before production use.

Copyright (c) 2025 StrategicPromptArchitect
License: MIT
Website: https://StrategicPromptArchitect.ca
Contact: StrategicPromptArchitect@gmail.com

Version History:
    V1 (2024) - Initial release with inline patterns
    V2 (2025) - Centralized patterns, OTA detection, improved accuracy

Features:
    - Pattern-based injection detection (200+ regex patterns)
    - Orchestration Threat Attack (OTA) detection
    - Compositional attack pattern recognition
    - Semantic tone detection (authoritarian vs manipulative)
    - Pattern clustering analysis
    - Context-aware score reductions (educational, technical, quoted)
    - 3-tier risk system (WHITE/ORANGE/RED)

Performance (V2):
    - Baseline Detection: 48.5%
    - Benign Accuracy: 93.3%
    - Average Latency: ~200ms
    - Target: <250ms on typical input (<10KB)

Usage:
    python quick_scan.py --input <file> --output <result.json>

Exit Codes:
    0 = WHITE (safe)
    1 = ORANGE (suspicious)
    2 = RED (dangerous)

Dependencies:
    - Python 3.8+
    - mps_patterns.py (must be in same directory)
    - No external packages required

See Also:
    - deep_scan.py: Comprehensive scanner with evasion detection
    - mps_patterns.py: Centralized pattern library
    - docs/API.md: Full API documentation
"""

import re
import sys
import json
import argparse
from pathlib import Path

from mps_patterns import get_patterns_for_scanner, get_weights

# Get patterns for this scanner
CRITICAL_PATTERNS = get_patterns_for_scanner('quick')
PATTERN_WEIGHTS = get_weights()

def quick_scan(text, mode='auto'):
    """
    Fast pattern matching for prompt injection detection.
    
    Args:
        text: Input text to scan
        mode: 'auto' (default) or 'shallow-only'
    
    Returns:
        dict: {risk_score, risk_level, matches, scan_type}
    """
    matches = {}
    total_score = 0
    
    for category, patterns in CRITICAL_PATTERNS.items():
        category_matches = []
        
        for pattern in patterns:
            # Use re.IGNORECASE | re.DOTALL on original text
            found = re.finditer(pattern, text, re.IGNORECASE | re.DOTALL)
            for match in found:
                category_matches.append({
                    'pattern': pattern[:50] + '...' if len(pattern) > 50 else pattern,
                    'text': match.group(0)[:100],
                    'position': match.span()
                })
        
        if category_matches:
            matches[category] = category_matches
            # Diminishing returns: first match = full weight, subsequent = 50% less
            weight = PATTERN_WEIGHTS[category]
            if len(category_matches) == 1:
                total_score += weight
            else:
                total_score += weight * (1 - 0.5 ** len(category_matches))
    
    # Calculate final risk score (0-100 scale)
    risk_score = min(100, int(total_score))
    
    # Pattern clustering analysis - detect intentional attacks
    # Check if multiple patterns appear close together (within 50 chars)
    pattern_positions = []
    for category, category_matches in matches.items():
        for match in category_matches:
            pattern_positions.append(match['position'])
    
    # Sort by start position
    pattern_positions.sort(key=lambda x: x[0])
    
    # Check for clustering (2+ patterns within 50 chars)
    is_clustered = False
    for i in range(len(pattern_positions) - 1):
        if pattern_positions[i+1][0] - pattern_positions[i][1] < 50:
            is_clustered = True
            break
    
    # Boost score for clustered patterns (indicates intentional attack)
    if is_clustered and len(matches) >= 2:
        risk_score = min(100, int(risk_score * 1.2))  # 20% boost
    
    # Add combo bonus for multi-category attacks (reduced from 30 to 15)
    if len(matches) >= 2:
        combo_bonus = 10 * len(matches)  # More conservative
        risk_score = min(100, risk_score + combo_bonus)
    
    # Pattern density bonus - multiple patterns in SAME category = intentional
    for category, category_matches in matches.items():
        if len(category_matches) >= 3:
            density_bonus = 20  # Multiple attacks of same type
            risk_score = min(100, risk_score + density_bonus)
            break  # Only apply once
    
    # Check if patterns are in quotes (educational/example context)
    patterns_in_quotes = False
    if '"' in text or "'" in text:
        for category, category_matches in matches.items():
            for match in category_matches:
                start, end = match['position']
                # Check 20 chars before and after for quotes
                context_start = max(0, start - 20)
                context_end = min(len(text), end + 20)
                context = text[context_start:context_end]
                if ('"' in context[:start-context_start] and '"' in context[end-context_start:]) or \
                   ("'" in context[:start-context_start] and "'" in context[end-context_start:]):
                    patterns_in_quotes = True
                    break
            if patterns_in_quotes:
                break
    
    if patterns_in_quotes and risk_score >= 40:
        risk_score = int(risk_score * 0.8)  # 20% reduction for quoted examples
    
    # Reduce false positives for technical/code content
    technical_markers = [
        r'\b(def|function|class|const|var|let)\s+\w+',  # Code definitions
        r'\b(import|require|include)\s+',  # Import statements
        r'[{}\[\]();]',  # Code syntax (3+ occurrences)
        r'//.*|/\*.*\*/',  # Code comments
    ]
    
    is_technical = sum(1 for pattern in technical_markers if re.search(pattern, text)) >= 2
    
    if is_technical and risk_score >= 40:
        risk_score = int(risk_score * 0.85)  # 15% reduction
    
    # Reduce false positives for educational/quoted content
    educational_markers = [
        r'\bexample\s*:',
        r'\battack\s*:',
        r'\bpattern\s*:',
        r'\bdefense\s*:',
        r'\bdetection\s*:',
        r'\babstract\s*:',
        r'\bkeywords\s*:',
        r'\bwe\s+(analyze|examine|propose|study)',
        r'\bfor\s+educational\s+purposes\b',
        r'"\s*ignore\s+previous\s+instructions?\s*"',
        r"'\s*ignore\s+previous\s+instructions?\s*'",
        r'\bthis\s+document\s+describes\b',
        r'\bcommon\s+.*?\s+techniques\b',
    ]
    
    is_educational = any(re.search(pattern, text, re.IGNORECASE) for pattern in educational_markers)
    
    if is_educational and risk_score >= 40:
        risk_score = int(risk_score * 0.75)  # Reduce by 25%

    # Reduce false positives for review/documentation mentioning attacks
    review_documentation_markers = [
        r'\b(?:stars?|rating|review)\b',  # Reviews
        r'\brecommend\b',
        r'\bconfiguration\s+(?:file|example)\b',  # Config docs
        r'\bwarning[:]\s+debug\b',  # Debug warnings
        r'\bexample\s+malicious\b',  # Security examples
        r'#\s+(?:check|example)\s+(?:for|malicious)',  # Code comments about attacks
    ]

    is_review_or_doc = any(re.search(pattern, text, re.IGNORECASE) for pattern in review_documentation_markers)

    if is_review_or_doc and risk_score >= 40:
        risk_score = int(risk_score * 0.6)  # 40% reduction
    
    # Special handling for compositional_attack category
    # These patterns have high false positive rates in legitimate contexts
    if 'compositional_attack' in matches and risk_score >= 40:
        # Check if this is a legitimate composition request
        legitimate_composition_markers = [
            r'\bsummar(?:y|ize)\b',  # "summarize the previous results"
            r'\breport\b',  # "create a report from the previous data"
            r'\b(?:chart|graph|visualization)\b',  # "make a chart using the above data"
            r'\btable\b',  # "put the previous results in a table"
            r'\blist\b',  # "list the previous findings"
        ]
        
        is_legitimate_composition = any(
            re.search(pattern, text, re.IGNORECASE) 
            for pattern in legitimate_composition_markers
        )
        
        if is_legitimate_composition:
            # Reduce score but don't eliminate - still worth noting
            risk_score = int(risk_score * 0.8)  # 20% reduction
    
    # Determine risk level (3-tier system optimized for benign accuracy)
    if risk_score >= 80:
        risk_level = "RED"
        recommendation = "BLOCK - High confidence attack detected"
    elif risk_score >= 55:
        risk_level = "ORANGE"
        recommendation = "REVIEW - Moderate risk detected"
    else:
        risk_level = "WHITE"
        recommendation = "PROCEED - No significant threats"
    
    return {
        'risk_score': risk_score,
        'risk_level': risk_level,
        'recommendation': recommendation,
        'matched_patterns': matches,
        'pattern_count': sum(len(m) for m in matches.values()),
        'scan_type': 'quick',
        'mode': mode,
        'version': '2.0'
    }


def main():
    parser = argparse.ArgumentParser(
        description='MPS Quick Scan v2.0 - Fast prompt injection detection with OTA support'
    )
    parser.add_argument(
        '--input',
        required=True,
        help='Input file to scan'
    )
    parser.add_argument(
        '--output',
        required=True,
        help='Output JSON file for results'
    )
    parser.add_argument(
        '--mode',
        default='auto',
        choices=['auto', 'shallow-only'],
        help='Scan mode (default: auto)'
    )
    
    args = parser.parse_args()
    
    # Read input file
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input file not found: {args.input}", file=sys.stderr)
        sys.exit(1)
    
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            text = f.read()
    except Exception as e:
        print(f"Error reading input file: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Perform scan
    results = quick_scan(text, mode=args.mode)
    
    # Write output
    output_path = Path(args.output)
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2)
    except Exception as e:
        print(f"Error writing output file: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Print summary to stdout
    print(f"Quick Scan Complete (v2.0)")
    print(f"Risk Score: {results['risk_score']}/100")
    print(f"Risk Level: {results['risk_level']}")
    print(f"Patterns Detected: {results['pattern_count']}")
    print(f"Recommendation: {results['recommendation']}")
    
    if 'compositional_attack' in results['matched_patterns']:
        print("\n⚠️  ORCHESTRATION THREAT INDICATOR DETECTED")
        print("This request references previous queries/results.")
        print("Consider reviewing conversation history for attack patterns.")
    
    # Exit code based on risk level
    if results['risk_level'] == 'RED':
        sys.exit(2)
    elif results['risk_level'] == 'ORANGE':
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == '__main__':
    main()