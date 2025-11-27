#!/usr/bin/env python3
"""Generate markdown test report"""

import json
from pathlib import Path
from datetime import datetime

def generate_report(results_file: Path) -> str:
    """Generate human-readable markdown report from test results"""
    
    if not results_file.exists():
        return f"Error: Results file not found: {results_file}"
    
    with open(results_file) as f:
        data = json.load(f)
    
    if "error" in data:
        return f"Error in test results: {data['error']}"
    
    summary = data["summary"]
    details = data["detailed_results"]
    
    report = f"""# MPS Test Agent - Validation Report

**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

---

## Executive Summary

- **Total Tests:** {summary['total_tests']}
- **Passed:** {summary['passed']} ({summary['pass_rate']}%)
- **Failed:** {summary['failed']}
- **Errors:** {summary['errors']}

### Overall Assessment

"""
    
    if summary['pass_rate'] >= 90:
        report += "✅ **EXCELLENT** - MPS demonstrates strong detection capabilities across all test categories.\n\n"
    elif summary['pass_rate'] >= 75:
        report += "⚠️ **GOOD** - MPS performs well overall with some gaps requiring attention.\n\n"
    elif summary['pass_rate'] >= 60:
        report += "⚠️ **FAIR** - MPS has significant detection gaps that should be addressed.\n\n"
    else:
        report += "❌ **POOR** - MPS requires substantial improvements to be effective.\n\n"
    
    # Category Breakdown
    report += "## Category Performance\n\n"
    report += "| Category | Tests | Passed | Failed | Errors | Pass Rate |\n"
    report += "|----------|-------|--------|--------|--------|-----------|\n"
    
    for cat, stats in summary['category_breakdown'].items():
        pass_rate = round((stats['passed'] / stats['total'] * 100) if stats['total'] > 0 else 0, 1)
        report += f"| {cat.title()} | {stats['total']} | {stats['passed']} | {stats['failed']} | {stats['errors']} | {pass_rate}% |\n"
    
    report += "\n"
    
    # Category Analysis
    report += "## Detailed Category Analysis\n\n"
    
    for cat, stats in summary['category_breakdown'].items():
        pass_rate = round((stats['passed'] / stats['total'] * 100) if stats['total'] > 0 else 0, 1)
        
        report += f"### {cat.title()} Tests\n\n"
        
        if cat == "baseline":
            report += "Tests known attack patterns that MPS should reliably detect.\n\n"
            if pass_rate >= 90:
                report += f"✅ **Strong Performance** ({pass_rate}%) - Core detection working well.\n\n"
            else:
                report += f"⚠️ **Needs Improvement** ({pass_rate}%) - Core patterns being missed.\n\n"
        
        elif cat == "evasion":
            report += "Tests obfuscation and evasion techniques designed to bypass detection.\n\n"
            if pass_rate >= 70:
                report += f"✅ **Good Resilience** ({pass_rate}%) - Preprocessing pipeline effective.\n\n"
            else:
                report += f"⚠️ **Vulnerable** ({pass_rate}%) - Evasion techniques bypassing detection.\n\n"
        
        elif cat == "benign":
            report += "Tests legitimate content that should NOT be flagged (false positive testing).\n\n"
            if pass_rate >= 90:
                report += f"✅ **Low False Positives** ({pass_rate}%) - Good discrimination.\n\n"
            else:
                report += f"⚠️ **High False Positives** ({pass_rate}%) - Flagging legitimate content.\n\n"
    
    # Performance Metrics
    report += "## Performance Benchmarks\n\n"
    
    quick = summary['performance']['quick_scan']
    report += f"""### Quick Scan
- **Tests Run:** {quick['count']}
- **Average Latency:** {quick['avg_ms']} ms
- **Min/Max:** {quick['min_ms']} / {quick['max_ms']} ms
- **Target:** <100ms """
    
    if quick['avg_ms'] < 60:
        report += "(**✅ Excellent** - Well under target)\n\n"
    elif quick['avg_ms'] < 100:
        report += "(**✅ Good** - Meeting target)\n\n"
    else:
        report += "(**❌ Slow** - Exceeding target)\n\n"
    
    deep = summary['performance']['deep_scan']
    if deep['count'] > 0:
        report += f"""### Deep Scan
- **Tests Run:** {deep['count']}
- **Average Latency:** {deep['avg_ms']} ms
- **Min/Max:** {deep['min_ms']} / {deep['max_ms']} ms
- **Target:** <2000ms """
        
        if deep['avg_ms'] < 1000:
            report += "(**✅ Excellent** - Well under target)\n\n"
        elif deep['avg_ms'] < 2000:
            report += "(**✅ Good** - Meeting target)\n\n"
        else:
            report += "(**❌ Slow** - Exceeding target)\n\n"
    else:
        report += "### Deep Scan\n\n*No deep scans were triggered during this test run.*\n\n"
    
    # Failed Tests Detail
    failed_tests = [t for t in details if t["validation"]["status"] == "FAIL"]
    error_tests = [t for t in details if t["validation"]["status"] == "ERROR"]
    
    if failed_tests:
        report += f"## Failed Tests ({len(failed_tests)})\n\n"
        
        for test in failed_tests[:10]:  # Limit to first 10
            val = test["validation"]
            report += f"""### {test['test_id']}

**Category:** {test['category']}  
**File:** `{Path(test['file']).name}`

**Expected:**
- Risk Level: {val.get('expected_risk', 'N/A')}
- Score Threshold: {val.get('threshold_type', 'N/A')} {val.get('threshold_value', 'N/A')}

**Actual:**
- Risk Level: {val.get('actual_risk', 'N/A')}
- Score: {val.get('actual_score', 'N/A')}
- Scan Type: {val.get('scan_type', 'N/A')}

"""
        
        if len(failed_tests) > 10:
            report += f"\n*... and {len(failed_tests) - 10} more failed tests (see full results JSON for complete details)*\n\n"
    
    if error_tests:
        report += f"## Test Errors ({len(error_tests)})\n\n"
        
        for test in error_tests[:5]:  # Limit to first 5
            report += f"""### {test['test_id']}

**Category:** {test['category']}  
**Error:** {test['validation'].get('message', 'Unknown error')}

"""
        
        if len(error_tests) > 5:
            report += f"\n*... and {len(error_tests) - 5} more errors*\n\n"
    
    # Recommendations
    report += "## Recommendations\n\n"
    
    baseline_stats = summary['category_breakdown'].get('baseline', {})
    evasion_stats = summary['category_breakdown'].get('evasion', {})
    benign_stats = summary['category_breakdown'].get('benign', {})
    
    baseline_rate = (baseline_stats.get('passed', 0) / baseline_stats.get('total', 1) * 100) if baseline_stats.get('total', 0) > 0 else 0
    evasion_rate = (evasion_stats.get('passed', 0) / evasion_stats.get('total', 1) * 100) if evasion_stats.get('total', 0) > 0 else 0
    benign_rate = (benign_stats.get('passed', 0) / benign_stats.get('total', 1) * 100) if benign_stats.get('total', 0) > 0 else 0
    
    recommendations = []
    
    if baseline_rate < 90:
        recommendations.append(
            "**1. Improve Baseline Pattern Detection**  \n"
            f"   Current: {baseline_rate:.1f}% | Target: 90%+  \n"
            "   Action: Review failed baseline tests and add missing patterns to quick_scan.py"
        )
    
    if evasion_rate < 70:
        recommendations.append(
            "**2. Enhance Evasion Resistance**  \n"
            f"   Current: {evasion_rate:.1f}% | Target: 70%+  \n"
            "   Action: Improve preprocessing pipeline in deep_scan.py (normalization, decoding)"
        )
    
    if benign_rate < 90:
        recommendations.append(
            "**3. Reduce False Positives**  \n"
            f"   Current: {benign_rate:.1f}% | Target: 90%+  \n"
            "   Action: Add educational context detection and adjust risk scoring thresholds"
        )
    
    if quick['avg_ms'] > 100:
        recommendations.append(
            f"**4. Optimize Quick Scan Performance**  \n"
            f"   Current: {quick['avg_ms']} ms | Target: <100ms  \n"
            "   Action: Profile quick_scan.py and optimize regex patterns"
        )
    
    if deep.get('avg_ms', 0) > 2000:
        recommendations.append(
            f"**5. Optimize Deep Scan Performance**  \n"
            f"   Current: {deep['avg_ms']} ms | Target: <2000ms  \n"
            "   Action: Profile deep_scan.py and optimize preprocessing steps"
        )
    
    if summary['errors'] > 0:
        recommendations.append(
            f"**6. Fix Test Execution Errors**  \n"
            f"   Errors: {summary['errors']}  \n"
            "   Action: Review error tests for script compatibility issues"
        )
    
    if recommendations:
        for rec in recommendations:
            report += rec + "\n\n"
    else:
        report += "✅ **No Critical Issues Detected**\n\n"
        report += "MPS is performing well across all metrics. Continue monitoring:\n"
        report += "- New attack patterns as they emerge\n"
        report += "- Edge cases in production usage\n"
        report += "- Performance under load\n\n"
    
    # Next Steps
    report += "## Next Steps\n\n"
    report += "1. Review failed test details in `full_test_results.json`\n"
    report += "2. Update MPS patterns and preprocessing based on recommendations\n"
    report += "3. Re-run validation suite after changes\n"
    report += "4. Consider adding custom test cases based on production data\n"
    report += "5. Benchmark against real-world attack samples\n\n"
    
    report += "---\n\n"
    report += "*Report generated by MPS Test Agent v1.0*\n"
    
    return report


def main():
    import sys
    
    results_file = Path("test_outputs/full_test_results.json")
    
    if not results_file.exists():
        print("Error: Test results not found. Run tests first with run_tests.py")
        sys.exit(1)
    
    print("Generating validation report...")
    report = generate_report(results_file)
    
    output_file = Path("test_outputs/mps_validation_report.md")
    output_file.write_text(report)
    
    print("\n" + "=" * 70)
    print(report)
    print("=" * 70)
    print(f"\nReport saved to: {output_file}")
    print()


if __name__ == "__main__":
    main()
