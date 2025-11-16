#!/usr/bin/env python3
"""
Patient Management System API Tester
Usage: python3 test_api.py
"""

import requests
import json
import time
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:3000/api"
HEADERS = {
    "Content-Type": "application/json",
    # "Authorization": "Bearer YOUR_TOKEN_HERE"
}

# ANSI color codes
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

class APITester:
    def __init__(self, base_url):
        self.base_url = base_url
        self.results = []

    def test_endpoint(self, method, endpoint, data=None, description=""):
        """Test a single API endpoint"""
        url = f"{self.base_url}{endpoint}"
        print(f"\n{YELLOW}Testing:{RESET} {description}")
        print(f"Method: {method}")
        print(f"URL: {url}")

        try:
            start_time = time.time()

            if method == "GET":
                response = requests.get(url, headers=HEADERS)
            elif method == "POST":
                response = requests.post(url, json=data, headers=HEADERS)
            elif method == "PUT":
                response = requests.put(url, json=data, headers=HEADERS)
            elif method == "DELETE":
                response = requests.delete(url, headers=HEADERS)
            else:
                print(f"{RED}Unknown method: {method}{RESET}")
                return

            elapsed_time = (time.time() - start_time) * 1000  # Convert to ms

            # Check status
            if 200 <= response.status_code < 300:
                print(f"{GREEN}✓ Success{RESET} (Status: {response.status_code}, Time: {elapsed_time:.2f}ms)")
                status = "PASS"
            else:
                print(f"{RED}✗ Failed{RESET} (Status: {response.status_code}, Time: {elapsed_time:.2f}ms)")
                status = "FAIL"

            # Show response
            if response.text:
                try:
                    json_response = response.json()
                    print(f"Response: {json.dumps(json_response, indent=2)[:200]}...")
                except:
                    print(f"Response: {response.text[:200]}...")

            # Store result
            self.results.append({
                "endpoint": endpoint,
                "method": method,
                "status_code": response.status_code,
                "status": status,
                "time": elapsed_time,
                "description": description
            })

        except requests.exceptions.ConnectionError:
            print(f"{RED}✗ Connection Error - API not reachable{RESET}")
            self.results.append({
                "endpoint": endpoint,
                "method": method,
                "status_code": 0,
                "status": "ERROR",
                "time": 0,
                "description": description
            })
        except Exception as e:
            print(f"{RED}✗ Error: {str(e)}{RESET}")
            self.results.append({
                "endpoint": endpoint,
                "method": method,
                "status_code": 0,
                "status": "ERROR",
                "time": 0,
                "description": description
            })

    def check_api_health(self):
        """Check if API is running"""
        print(f"\n{BLUE}Checking API Health...{RESET}")
        try:
            response = requests.get(f"{self.base_url}/health", timeout=5)
            if response.status_code == 200:
                print(f"{GREEN}✓ API is healthy and running{RESET}")
                return True
            else:
                print(f"{YELLOW}⚠ API responded with status {response.status_code}{RESET}")
                return True
        except:
            print(f"{RED}✗ API is not reachable at {self.base_url}{RESET}")
            return False

    def run_tests(self):
        """Run all API tests"""
        print("=" * 50)
        print("   PATIENT MANAGEMENT API TEST SUITE")
        print("=" * 50)

        # Check health first
        if not self.check_api_health():
            print("\n⚠ Continuing with tests anyway...")

        # Test cases
        tests = [
            # GET tests
            ("GET", "/patients", None, "Get all patients"),
            ("GET", "/patients/1", None, "Get patient by ID"),
            ("GET", "/patients/search?q=John", None, "Search patients by name"),
            ("GET", "/appointments", None, "Get all appointments"),
            ("GET", "/appointments/today", None, "Get today's appointments"),

            # POST tests
            ("POST", "/patients", {
                "firstName": "Test",
                "lastName": f"Patient_{datetime.now().strftime('%H%M%S')}",
                "dateOfBirth": "1990-01-01",
                "gender": "Male",
                "phone": "555-0123",
                "email": f"test_{datetime.now().strftime('%H%M%S')}@example.com",
                "bloodType": "O+",
                "allergies": "None"
            }, "Create new patient"),

            ("POST", "/appointments", {
                "patientId": 1,
                "doctorId": 1,
                "dateTime": "2024-02-01T10:00:00",
                "reason": "Routine checkup"
            }, "Create new appointment"),

            # PUT tests
            ("PUT", "/patients/1", {
                "phone": "555-9999",
                "email": "updated@example.com"
            }, "Update patient information"),

            # DELETE tests
            ("DELETE", "/patients/999", None, "Delete patient (non-existent)"),
            ("DELETE", "/appointments/999", None, "Delete appointment (non-existent)")
        ]

        # Run each test
        for method, endpoint, data, description in tests:
            self.test_endpoint(method, endpoint, data, description)

        # Show summary
        self.show_summary()

    def show_summary(self):
        """Display test results summary"""
        print("\n" + "=" * 50)
        print("   TEST SUMMARY")
        print("=" * 50)

        total = len(self.results)
        passed = sum(1 for r in self.results if r["status"] == "PASS")
        failed = sum(1 for r in self.results if r["status"] == "FAIL")
        errors = sum(1 for r in self.results if r["status"] == "ERROR")

        print(f"\nTotal Tests: {total}")
        print(f"{GREEN}Passed: {passed}{RESET}")
        print(f"{RED}Failed: {failed}{RESET}")
        print(f"{YELLOW}Errors: {errors}{RESET}")

        # Performance stats
        response_times = [r["time"] for r in self.results if r["time"] > 0]
        if response_times:
            avg_time = sum(response_times) / len(response_times)
            max_time = max(response_times)
            min_time = min(response_times)

            print(f"\n{BLUE}Performance Stats:{RESET}")
            print(f"Average Response Time: {avg_time:.2f}ms")
            print(f"Fastest: {min_time:.2f}ms")
            print(f"Slowest: {max_time:.2f}ms")

        # Failed tests details
        if failed > 0 or errors > 0:
            print(f"\n{RED}Failed/Error Tests:{RESET}")
            for r in self.results:
                if r["status"] in ["FAIL", "ERROR"]:
                    print(f"  - {r['method']} {r['endpoint']}: {r['description']}")

if __name__ == "__main__":
    # Create tester instance
    tester = APITester(BASE_URL)

    # Run all tests
    tester.run_tests()

    print("\n✅ Testing complete!")