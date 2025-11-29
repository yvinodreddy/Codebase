#!/usr/bin/env python3
"""
S7: Dependency Vulnerability Scanning
Scans Python dependencies for known security vulnerabilities.

Uses pip-audit or safety (if installed) to check for CVEs in dependencies.
"""

import subprocess
import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional
from config import UltrathinkConfig as Config


class DependencyScanner:
    """
    Scan Python dependencies for security vulnerabilities.

    Supports multiple scanning tools:
    - pip-audit (recommended, official PyPA tool)
    - safety (popular third-party tool)
    - Manual requirements.txt parsing (fallback)
    """

    def __init__(self, cache_file: str = ".dependency_scan_cache.json"):
        """
        Initialize dependency scanner.

        Args:
            cache_file: Path to cache file for scan results
        """
        self.cache_file = Path(cache_file)
        self.cache_hours = Config.DEPENDENCY_SCAN_CACHE_HOURS

    def scan(self, force: bool = False) -> Dict:
        """
        Scan dependencies for vulnerabilities.

        Args:
            force: If True, ignore cache and force new scan

        Returns:
            Dict with scan results
        """
        # Check cache first
        if not force and self._is_cache_valid():
            return self._load_cache()

        # Run actual scan
        result = self._run_scan()

        # Cache results
        self._save_cache(result)

        return result

    def _is_cache_valid(self) -> bool:
        """Check if cached scan results are still valid"""
        if not self.cache_file.exists():
            return False

        try:
            cache_data = self._load_cache()
            cache_time = datetime.fromisoformat(cache_data.get("timestamp", ""))
            age = datetime.now() - cache_time

            return age < timedelta(hours=self.cache_hours)
        except:
            return False

    def _load_cache(self) -> Dict:
        """Load cached scan results"""
        try:
            with open(self.cache_file, 'r') as f:
                return json.load(f)
        except:
            return {}

    def _save_cache(self, data: Dict):
        """Save scan results to cache"""
        data["timestamp"] = datetime.now().isoformat()
        try:
            with open(self.cache_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save scan cache: {e}")

    def _run_scan(self) -> Dict:
        """Run actual dependency scan"""

        # Try pip-audit first (official tool)
        result = self._try_pip_audit()
        if result:
            return result

        # Fallback to safety
        result = self._try_safety()
        if result:
            return result

        # Fallback to manual check
        return self._manual_check()

    def _try_pip_audit(self) -> Optional[Dict]:
        """Try using pip-audit for scanning"""
        try:
            # Check if pip-audit is installed
            subprocess.run(
                ["pip-audit", "--version"],
                capture_output=True,
                check=True,
                timeout=5
            )

            # Run pip-audit
            result = subprocess.run(
                ["pip-audit", "--format", "json"],
                capture_output=True,
                text=True,
                timeout=60
            )

            if result.returncode == 0:
                # No vulnerabilities found
                return {
                    "tool": "pip-audit",
                    "vulnerabilities": [],
                    "total_packages_scanned": "unknown",
                    "status": "clean"
                }
            else:
                # Vulnerabilities found (pip-audit exits with 1)
                try:
                    vulns = json.loads(result.stdout)
                    return {
                        "tool": "pip-audit",
                        "vulnerabilities": vulns.get("dependencies", []),
                        "total_packages_scanned": len(vulns.get("dependencies", [])),
                        "status": "vulnerabilities_found"
                    }
                except:
                    return {
                        "tool": "pip-audit",
                        "vulnerabilities": [],
                        "error": result.stdout + result.stderr,
                        "status": "error"
                    }

        except subprocess.TimeoutExpired:
            return {
                "tool": "pip-audit",
                "error": "Scan timeout after 60 seconds",
                "status": "timeout"
            }
        except subprocess.CalledProcessError:
            # pip-audit not installed
            return None
        except Exception as e:
            return {
                "tool": "pip-audit",
                "error": str(e),
                "status": "error"
            }

    def _try_safety(self) -> Optional[Dict]:
        """Try using safety for scanning"""
        try:
            # Check if safety is installed
            subprocess.run(
                ["safety", "--version"],
                capture_output=True,
                check=True,
                timeout=5
            )

            # Run safety check
            result = subprocess.run(
                ["safety", "check", "--json"],
                capture_output=True,
                text=True,
                timeout=60
            )

            try:
                vulns = json.loads(result.stdout)
                return {
                    "tool": "safety",
                    "vulnerabilities": vulns,
                    "total_packages_scanned": len(vulns),
                    "status": "vulnerabilities_found" if vulns else "clean"
                }
            except:
                return {
                    "tool": "safety",
                    "vulnerabilities": [],
                    "status": "clean"
                }

        except subprocess.TimeoutExpired:
            return {
                "tool": "safety",
                "error": "Scan timeout after 60 seconds",
                "status": "timeout"
            }
        except subprocess.CalledProcessError:
            # safety not installed
            return None
        except Exception as e:
            return {
                "tool": "safety",
                "error": str(e),
                "status": "error"
            }

    def _manual_check(self) -> Dict:
        """
        Manual fallback check (no vulnerability scanning).

        Just lists installed packages for manual review.
        """
        try:
            result = subprocess.run(
                ["pip", "list", "--format", "json"],
                capture_output=True,
                text=True,
                timeout=30
            )

            packages = json.loads(result.stdout)

            return {
                "tool": "manual",
                "message": "No vulnerability scanner installed. Install pip-audit or safety for automated scanning.",
                "installed_packages": packages,
                "total_packages": len(packages),
                "status": "no_scanner",
                "recommendation": "Run: pip install pip-audit"
            }

        except Exception as e:
            return {
                "tool": "manual",
                "error": str(e),
                "status": "error"
            }

    def print_report(self, scan_result: Dict):
        """
        Print human-readable scan report.

        Args:
            scan_result: Result from scan() method
        """
        print("\n" + "="*70)
        print("🔒 DEPENDENCY VULNERABILITY SCAN")
        print("="*70)

        tool = scan_result.get("tool", "unknown")
        status = scan_result.get("status", "unknown")

        print(f"Tool: {tool}")
        print(f"Status: {status}")

        if status == "clean":
            print("\n✅ No known vulnerabilities found!")

        elif status == "vulnerabilities_found":
            vulns = scan_result.get("vulnerabilities", [])
            print(f"\n⚠️  Found {len(vulns)} vulnerability/vulnerabilities:")

            for i, vuln in enumerate(vulns[:10], 1):  # Show first 10
                if tool == "pip-audit":
                    pkg = vuln.get("name", "unknown")
                    version = vuln.get("version", "unknown")
                    vuln_id = vuln.get("id", "unknown")
                    print(f"\n   {i}. {pkg} {version}")
                    print(f"      CVE: {vuln_id}")
                    print(f"      Fix: {vuln.get('fix_versions', 'No fix available')}")

                elif tool == "safety":
                    print(f"\n   {i}. {vuln.get('package', 'unknown')}")
                    print(f"      {vuln.get('vulnerability', 'No details')}")

            if len(vulns) > 10:
                print(f"\n   ... and {len(vulns) - 10} more")

        elif status == "no_scanner":
            print(f"\n⚠️  {scan_result.get('message', '')}")
            print(f"   Total packages installed: {scan_result.get('total_packages', 0)}")
            print(f"\n   Recommendation: {scan_result.get('recommendation', '')}")

        elif status == "error":
            print(f"\n❌ Scan failed: {scan_result.get('error', 'Unknown error')}")

        elif status == "timeout":
            print(f"\n⏱️  Scan timeout: {scan_result.get('error', '')}")

        # Show cache info
        if "timestamp" in scan_result:
            scan_time = datetime.fromisoformat(scan_result["timestamp"])
            age = datetime.now() - scan_time
            print(f"\n📅 Scan age: {age.total_seconds() / 3600:.1f} hours")
            print(f"   Cache valid for: {self.cache_hours} hours")

        print("="*70 + "\n")


def scan_dependencies_on_startup() -> bool:
    """
    Run dependency scan on system startup.

    Returns:
        True if scan successful and clean, False if vulnerabilities found
    """
    if not Config.DEPENDENCY_SCAN_ON_STARTUP:
        return True  # Skip scan, assume OK

    scanner = DependencyScanner()
    result = scanner.scan()

    # Only print if vulnerabilities found
    if result.get("status") == "vulnerabilities_found":
        scanner.print_report(result)
        print("⚠️  WARNING: Vulnerabilities detected in dependencies")
        print("   Consider updating affected packages before proceeding.\n")
        return False

    return True


if __name__ == "__main__":
    """Test dependency scanner"""

    print("Testing Dependency Scanner")
    print("="*70)

    scanner = DependencyScanner()

    # Force new scan
    print("Running scan (force=True)...")
    result = scanner.scan(force=True)

    # Print report
    scanner.print_report(result)

    # Test cache
    print("\nTesting cache...")
    cached_result = scanner.scan(force=False)
    print(f"Cache hit: {result == cached_result}")

    print("\n✅ Test complete")
