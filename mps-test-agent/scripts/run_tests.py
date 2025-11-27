#!/usr/bin/env python3
"""Execute MPS tests and collect results - Updated for MPS v2.0"""

import json
import subprocess
import time
import sys
from pathlib import Path
from typing import Dict, List

class MPSTestRunner:
    def __init__(self, mps_scripts_path: str):
        self.mps_path = Path(mps_scripts_path)
        
        # Check for v2 scanner first, fall back to v1
        self.quick_scan = self.mps_path / "quick_scan.py"
        self.deep_scan = self.mps_path / "deep_scan.py"
        self.results = []
        self.scanner_version = "unknown"
        
        # Verify scripts exist
        if not self.quick_scan.exists():
            raise FileNotFoundError(f"Quick scan script not found: {self.quick_scan}")
        if not self.deep_scan.exists():
            raise FileNotFoundError(f"Deep scan script not found: {self.deep_scan}")
        
        # Detect scanner version
        self.detect_scanner_version()
    
    def detect_scanner_version(self):
        """Detect MPS scanner version from filename or test output"""
        if "v2" in self.quick_scan.name:
            self.scanner_version = "2.0"
        else:
            # Try to detect from a test scan
            try:
                test_file = Path("test_inputs/baseline/direct_override_1.txt")
                if test_file.exists():
                    test_output = Path("test_outputs/_version_check.json")
                    subprocess.run([
                        "python3", str(self.quick_scan),
                        "--input", str(test_file),
                        "--output", str(test_output)
                    ], capture_output=True, timeout=2, check=False)
                    
                    if test_output.exists():
                        with open(test_output) as f:
                            result = json.load(f)
                        if "version" in result:
                            self.scanner_version = result["version"]
                        else:
                            self.scanner_version = "1.0"
                        test_output.unlink()  # Clean up
            except:
                pass
        
        print(f"Scanner Version Detected: MPS v{self.scanner_version}")
        print()
    
    def run_test(self, test_case: Dict) -> Dict:
        """Run MPS scans on a single test case"""
        test_file = Path(test_case["file"])
        test_id = test_case["test_id"]
        
        if not test_file.exists():
            return {
                "test_id": test_id,
                "category": test_case["category"],
                "file": str(test_file),
                "validation": {
                    "status": "ERROR",
                    "message": f"Test file not found: {test_file}"
                }
            }
        
        result = {
            "test_id": test_id,
            "category": test_case["category"],
            "file": str(test_file)
        }
        
        # Quick scan
        quick_output = Path("test_outputs") / f"{test_id}_quick.json"
        start_time = time.time()
        
        try:
            proc = subprocess.run([
                "python3", str(self.quick_scan),
                "--input", str(test_file),
                "--output", str(quick_output)
            ], check=False, capture_output=True, timeout=5, text=True)
            
            quick_time = (time.time() - start_time) * 1000  # Convert to ms
            
            if quick_output.exists():
                with open(quick_output) as f:
                    quick_result = json.load(f)
                
                result["quick_scan"] = {
                    "risk_score": quick_result["risk_score"],
                    "risk_level": quick_result["risk_level"],
                    "latency_ms": round(quick_time, 2),
                    "pattern_count": quick_result["pattern_count"],
                    "exit_code": proc.returncode
                }
                
                # v2.0 specific fields
                if "version" in quick_result:
                    result["quick_scan"]["scanner_version"] = quick_result["version"]
                
                # Check for OTA indicator (v2.0 feature)
                if "matched_patterns" in quick_result and "compositional_attack" in quick_result["matched_patterns"]:
                    result["quick_scan"]["ota_indicator"] = True
                
            else:
                result["quick_scan"] = {
                    "error": "Quick scan produced no output",
                    "stderr": proc.stderr[:500] if proc.stderr else ""
                }
            
        except subprocess.TimeoutExpired:
            result["quick_scan"] = {"error": "Quick scan timeout (>5s)"}
        except Exception as e:
            result["quick_scan"] = {"error": str(e)}
        
        # Deep scan (if quick scan was suspicious or for evasion tests)
        should_deep_scan = (
            result.get("quick_scan", {}).get("risk_score", 0) >= 40 or
            test_case["category"] == "evasion"
        )
        
        if should_deep_scan and "error" not in result.get("quick_scan", {}):
            deep_output = Path("test_outputs") / f"{test_id}_deep.json"
            start_time = time.time()
            
            try:
                proc = subprocess.run([
                    "python3", str(self.deep_scan),
                    "--input", str(test_file),
                    "--output", str(deep_output)
                ], check=False, capture_output=True, timeout=10, text=True)
                
                deep_time = (time.time() - start_time) * 1000
                
                if deep_output.exists():
                    with open(deep_output) as f:
                        deep_result = json.load(f)
                    
                    result["deep_scan"] = {
                        "risk_score": deep_result["risk_score"],
                        "risk_level": deep_result["risk_level"],
                        "latency_ms": round(deep_time, 2),
                        "pattern_count": deep_result["pattern_count"],
                        "evasion_detected": deep_result.get("evasion_detected"),
                        "exit_code": proc.returncode
                    }
                else:
                    result["deep_scan"] = {
                        "error": "Deep scan produced no output",
                        "stderr": proc.stderr[:500] if proc.stderr else ""
                    }
                
            except subprocess.TimeoutExpired:
                result["deep_scan"] = {"error": "Deep scan timeout (>10s)"}
            except Exception as e:
                result["deep_scan"] = {"error": str(e)}
        
        # Validation
        result["validation"] = self.validate_result(result, test_case)
        
        return result
    
    def validate_result(self, result: Dict, expected: Dict) -> Dict:
        """Compare actual results to expected outcomes"""
        validation = {}
        
        # Determine which scan to validate
        if "deep_scan" in result and "error" not in result["deep_scan"]:
            scan_result = result["deep_scan"]
            scan_type = "deep"
        elif "quick_scan" in result and "error" not in result["quick_scan"]:
            scan_result = result["quick_scan"]
            scan_type = "quick"
        else:
            return {
                "status": "ERROR",
                "message": "No valid scan results",
                "scan_type": "none"
            }
        
        expected_risk = expected.get("expected_risk")
        actual_risk = scan_result["risk_level"]
        actual_score = scan_result["risk_score"]
        
        # Check risk level match
        validation["risk_level_match"] = (actual_risk == expected_risk)
        
        # Check score threshold
        if "expected_score_min" in expected:
            validation["score_threshold_met"] = (actual_score >= expected["expected_score_min"])
            validation["threshold_type"] = "minimum"
            validation["threshold_value"] = expected["expected_score_min"]
        elif "expected_score_max" in expected:
            validation["score_threshold_met"] = (actual_score <= expected["expected_score_max"])
            validation["threshold_type"] = "maximum"
            validation["threshold_value"] = expected["expected_score_max"]
        else:
            validation["score_threshold_met"] = None
        
        # Overall pass/fail
        if validation["risk_level_match"] and validation.get("score_threshold_met", True):
            validation["status"] = "PASS"
        else:
            validation["status"] = "FAIL"
            validation["expected_risk"] = expected_risk
            validation["actual_risk"] = actual_risk
            validation["actual_score"] = actual_score
        
        validation["scan_type"] = scan_type
        
        # v2.0 specific validation notes
        if scan_result.get("ota_indicator"):
            validation["ota_detected"] = True
        
        return validation
    
    def run_all_tests(self, manifests: List[Path]) -> Dict:
        """Run all tests from manifest files"""
        all_tests = []
        
        # Load all manifests
        for manifest_path in manifests:
            if not manifest_path.exists():
                print(f"Warning: Manifest not found: {manifest_path}")
                continue
                
            with open(manifest_path) as f:
                tests = json.load(f)
                all_tests.extend(tests)
        
        if not all_tests:
            return {
                "error": "No tests loaded from manifests",
                "manifests_checked": [str(m) for m in manifests]
            }
        
        print(f"Running {len(all_tests)} tests...")
        print()
        
        # Execute tests
        for i, test_case in enumerate(all_tests, 1):
            print(f"[{i}/{len(all_tests)}] Testing: {test_case['test_id']:<45}", end=" ")
            result = self.run_test(test_case)
            
            # Print status
            status = result["validation"]["status"]
            if status == "PASS":
                print("✓ PASS")
            elif status == "FAIL":
                print("✗ FAIL")
            else:
                print("⚠ ERROR")
            
            self.results.append(result)
        
        print()
        
        # Generate summary
        summary = self.generate_summary()
        summary["scanner_version"] = self.scanner_version
        
        return {
            "summary": summary,
            "detailed_results": self.results
        }
    
    def generate_summary(self) -> Dict:
        """Generate summary statistics"""
        total = len(self.results)
        passed = sum(1 for r in self.results if r["validation"]["status"] == "PASS")
        failed = sum(1 for r in self.results if r["validation"]["status"] == "FAIL")
        errors = sum(1 for r in self.results if r["validation"]["status"] == "ERROR")
        
        # Category breakdown
        categories = {}
        for result in self.results:
            cat = result["category"]
            if cat not in categories:
                categories[cat] = {"total": 0, "passed": 0, "failed": 0, "errors": 0}
            
            categories[cat]["total"] += 1
            status = result["validation"]["status"]
            if status == "PASS":
                categories[cat]["passed"] += 1
            elif status == "FAIL":
                categories[cat]["failed"] += 1
            elif status == "ERROR":
                categories[cat]["errors"] += 1
        
        # Performance metrics
        quick_latencies = [
            r["quick_scan"]["latency_ms"]
            for r in self.results
            if "quick_scan" in r and "latency_ms" in r["quick_scan"]
        ]
        
        deep_latencies = [
            r["deep_scan"]["latency_ms"]
            for r in self.results
            if "deep_scan" in r and "latency_ms" in r["deep_scan"]
        ]
        
        # v2.0 specific: OTA detection stats
        ota_detected_count = sum(
            1 for r in self.results
            if r.get("quick_scan", {}).get("ota_indicator", False)
        )
        
        summary = {
            "total_tests": total,
            "passed": passed,
            "failed": failed,
            "errors": errors,
            "pass_rate": round((passed / total * 100) if total > 0 else 0, 2),
            "category_breakdown": categories,
            "performance": {
                "quick_scan": {
                    "count": len(quick_latencies),
                    "avg_ms": round(sum(quick_latencies) / len(quick_latencies), 2) if quick_latencies else 0,
                    "min_ms": round(min(quick_latencies), 2) if quick_latencies else 0,
                    "max_ms": round(max(quick_latencies), 2) if quick_latencies else 0
                },
                "deep_scan": {
                    "count": len(deep_latencies),
                    "avg_ms": round(sum(deep_latencies) / len(deep_latencies), 2) if deep_latencies else 0,
                    "min_ms": round(min(deep_latencies), 2) if deep_latencies else 0,
                    "max_ms": round(max(deep_latencies), 2) if deep_latencies else 0
                }
            }
        }
        
        # Add v2.0 specific stats if detected
        if ota_detected_count > 0:
            summary["v2_features"] = {
                "ota_indicators_detected": ota_detected_count
            }
        
        return summary


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 run_tests.py <mps_scripts_path>")
        print()
        print("Example:")
        print("  python3 run_tests.py /mnt/user-data/uploads")
        print("  python3 run_tests.py ../mal-prompt-sentinel/scripts")
        sys.exit(1)
    
    mps_scripts_path = sys.argv[1]
    
    print("=" * 70)
    print("MPS Test Agent - Validation Suite v2.0")
    print("=" * 70)
    print()
    print(f"MPS Scripts Path: {mps_scripts_path}")
    print()
    
    try:
        runner = MPSTestRunner(mps_scripts_path)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)
    
    manifests = [
        Path("test_inputs/baseline_manifest.json"),
        Path("test_inputs/evasion_manifest.json"),
        Path("test_inputs/benign_manifest.json")
    ]
    
    results = runner.run_all_tests(manifests)
    
    if "error" in results:
        print(f"Error: {results['error']}")
        sys.exit(1)
    
    # Save results
    output_file = Path("test_outputs/full_test_results.json")
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, "w") as f:
        json.dump(results, f, indent=2)
    
    # Print summary
    summary = results['summary']
    
    print("=" * 70)
    print("Test Results Summary")
    print("=" * 70)
    print()
    print(f"Scanner Version: MPS v{summary.get('scanner_version', 'unknown')}")
    print(f"Total Tests:     {summary['total_tests']}")
    print(f"Passed:          {summary['passed']} ({summary['pass_rate']}%)")
    print(f"Failed:          {summary['failed']}")
    print(f"Errors:          {summary['errors']}")
    print()
    
    # v2.0 specific output
    if "v2_features" in summary:
        print("v2.0 Features:")
        print(f"  OTA Indicators Detected: {summary['v2_features']['ota_indicators_detected']}")
        print()
    
    print("Category Breakdown:")
    print("-" * 70)
    for cat, stats in summary['category_breakdown'].items():
        pass_rate = round((stats['passed'] / stats['total'] * 100) if stats['total'] > 0 else 0, 1)
        print(f"  {cat.title():<15} {stats['passed']}/{stats['total']} passed ({pass_rate}%)")
    print()
    
    print("Performance:")
    print("-" * 70)
    quick = summary['performance']['quick_scan']
    deep = summary['performance']['deep_scan']
    print(f"  Quick Scan:  {quick['avg_ms']} ms avg  (min: {quick['min_ms']}, max: {quick['max_ms']})")
    if deep['count'] > 0:
        print(f"  Deep Scan:   {deep['avg_ms']} ms avg  (min: {deep['min_ms']}, max: {deep['max_ms']})")
    else:
        print(f"  Deep Scan:   No deep scans triggered")
    print()
    
    print("=" * 70)
    print(f"Full results saved to: {output_file}")
    print("=" * 70)
    
    # Exit code based on overall success
    if summary['errors'] > 0:
        sys.exit(2)
    elif summary['failed'] > 0:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == '__main__':
    main()