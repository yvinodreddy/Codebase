#!/usr/bin/env python3
"""
BASIC CLAUDE SKILL: Patient Data Fetcher
Level: Beginner (⭐)
Purpose: Simple skill to fetch patient data from FHIR API
Learning Focus: Understanding basic skill structure
"""

import json
import requests
from datetime import datetime
from typing import Dict, Optional

class PatientFetcherSkill:
    """
    This is your FIRST Claude Skill!
    It demonstrates the basic structure every skill needs.
    """

    def __init__(self):
        """Initialize the skill with basic configuration"""
        # Skill metadata (like an ID card for your skill)
        self.metadata = {
            "name": "Patient Data Fetcher",
            "version": "1.0.0",
            "author": "Healthcare Dev Team",
            "description": "Fetches patient data from FHIR API",
            "complexity": "Basic",
            "learning_time": "10 minutes"
        }

        # API configuration
        self.base_url = "http://localhost:5079"
        self.token = None

        # Skill triggers (words that activate this skill)
        self.triggers = [
            "get patient",
            "fetch patient",
            "show patient",
            "patient data",
            "find patient"
        ]

    def authenticate(self, username: str = "dr.smith", password: str = "Doctor123!") -> bool:
        """
        Step 1: Authenticate with the API
        This is like logging into the system
        """
        print("🔐 Authenticating with FHIR API...")

        try:
            response = requests.post(
                f"{self.base_url}/api/auth/login",
                json={"username": username, "password": password},
                headers={"Content-Type": "application/json"}
            )

            if response.status_code == 200:
                self.token = response.json()["token"]
                print("✅ Authentication successful!")
                return True
            else:
                print(f"❌ Authentication failed: {response.status_code}")
                return False

        except Exception as e:
            print(f"❌ Connection error: {e}")
            return False

    def fetch_patient(self, patient_id: str) -> Optional[Dict]:
        """
        Step 2: Fetch patient data
        This is the main action of our skill
        """
        if not self.token:
            print("⚠️ Not authenticated. Please authenticate first.")
            return None

        print(f"🔍 Fetching data for patient {patient_id}...")

        try:
            response = requests.get(
                f"{self.base_url}/api/fhir/Patient/{patient_id}",
                headers={"Authorization": f"Bearer {self.token}"}
            )

            if response.status_code == 200:
                print("✅ Patient data retrieved successfully!")
                return response.json()
            else:
                print(f"❌ Failed to fetch patient: {response.status_code}")
                return None

        except Exception as e:
            print(f"❌ Error fetching patient: {e}")
            return None

    def format_output(self, patient_data: Dict) -> str:
        """
        Step 3: Format the output for easy reading
        This makes the data human-friendly
        """
        if not patient_data:
            return "No patient data available"

        # Extract key information
        patient_id = patient_data.get('id', 'Unknown')
        names = patient_data.get('name', [{}])[0]
        family_name = names.get('family', 'Unknown')
        given_names = names.get('given', ['Unknown'])
        gender = patient_data.get('gender', 'Unknown')
        birth_date = patient_data.get('birthDate', 'Unknown')

        # Create formatted output
        output = f"""
╔════════════════════════════════════════╗
║         PATIENT INFORMATION            ║
╠════════════════════════════════════════╣
║ ID:        {patient_id:<28} ║
║ Name:      {family_name}, {' '.join(given_names):<20} ║
║ Gender:    {gender:<28} ║
║ Birth:     {birth_date:<28} ║
╚════════════════════════════════════════╝
        """
        return output

    def execute(self, patient_id: str = "1") -> str:
        """
        Main execution method - This runs the entire skill
        This is what happens when someone says "get patient 1"
        """
        print("\n🚀 EXECUTING BASIC CLAUDE SKILL: Patient Fetcher")
        print("="*50)

        # Step 1: Authenticate
        if not self.authenticate():
            return "Failed to authenticate with the API"

        # Step 2: Fetch patient data
        patient_data = self.fetch_patient(patient_id)

        # Step 3: Format and return output
        output = self.format_output(patient_data)

        print(output)
        print("\n✅ Skill execution completed!")
        print("="*50)

        return output

    def explain(self):
        """
        Educational method - Explains how this skill works
        Great for learning!
        """
        explanation = """
        🎓 HOW THIS BASIC SKILL WORKS:

        1. TRIGGER: User says something like "get patient 1"

        2. PARSE: Extract patient ID from the request

        3. AUTHENTICATE: Login to the API to get access token

        4. FETCH: Use token to request patient data

        5. FORMAT: Convert JSON data to readable format

        6. RETURN: Show formatted data to user

        KEY CONCEPTS DEMONSTRATED:
        • API Authentication
        • HTTP Requests (GET/POST)
        • Error Handling
        • Data Formatting
        • Skill Structure

        NEXT STEPS:
        Try modifying this skill to:
        - Fetch multiple patients
        - Add more patient details
        - Include error recovery
        - Cache results for speed
        """
        print(explanation)


# TESTING SECTION - Try the skill yourself!
def test_basic_skill():
    """Test the basic skill with sample data"""
    print("\n" + "🧪 TESTING BASIC CLAUDE SKILL ".center(60, "="))

    # Create skill instance
    skill = PatientFetcherSkill()

    # Show skill metadata
    print(f"\nSkill: {skill.metadata['name']}")
    print(f"Version: {skill.metadata['version']}")
    print(f"Complexity: {skill.metadata['complexity']}")

    # Execute the skill
    result = skill.execute(patient_id="1")

    # Show learning explanation
    print("\n📚 Want to understand how it works?")
    input("Press Enter to see the explanation...")
    skill.explain()


if __name__ == "__main__":
    # Run the test when script is executed directly
    test_basic_skill()

    # Interactive mode
    print("\n🎯 TRY IT YOURSELF!")
    print("Enter a patient ID to fetch (or 'quit' to exit):")

    skill = PatientFetcherSkill()

    while True:
        user_input = input("\nPatient ID: ").strip()

        if user_input.lower() == 'quit':
            print("👋 Goodbye!")
            break

        if user_input:
            skill.execute(patient_id=user_input)