#!/usr/bin/env python3
"""
Claude Code Release Monitor
Automatically checks for new releases and generates personalized learning recommendations
"""

import json
import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple


class ReleaseMonitor:
    """Monitor Claude Code releases and provide intelligent updates"""

    def __init__(self):
        self.config_dir = Path.home() / ".claude-release-monitor"
        self.config_file = self.config_dir / "config.json"
        self.history_file = self.config_dir / "history.json"
        self.config_dir.mkdir(exist_ok=True)

        self.config = self.load_config()
        self.history = self.load_history()

    def load_config(self) -> Dict:
        """Load configuration"""
        if self.config_file.exists():
            with open(self.config_file) as f:
                return json.load(f)

        # Default configuration
        config = {
            "notification_method": "console",  # console, email, slack
            "check_frequency": "daily",  # startup, daily, weekly
            "skill_level": "intermediate",  # beginner, intermediate, advanced, expert
            "interests": [
                "productivity",
                "debugging",
                "automation",
                "testing"
            ],
            "email": "",
            "slack_webhook": "",
            "last_check": None,
            "last_seen_version": None
        }

        self.save_config(config)
        return config

    def save_config(self, config: Dict):
        """Save configuration"""
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=2)

    def load_history(self) -> Dict:
        """Load release history"""
        if self.history_file.exists():
            with open(self.history_file) as f:
                return json.load(f)
        return {"versions": [], "learned_features": []}

    def save_history(self, history: Dict):
        """Save release history"""
        with open(self.history_file, 'w') as f:
            json.dump(history, f, indent=2)

    def get_current_version(self) -> str:
        """Get currently installed Claude Code version"""
        try:
            result = subprocess.run(
                ["claude", "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )

            # Parse version from output
            version_match = re.search(r'(\d+\.\d+\.\d+)', result.stdout)
            if version_match:
                return version_match.group(1)
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass

        return "unknown"

    def get_release_notes(self) -> str:
        """Get release notes from Claude Code"""
        try:
            # Use subprocess to capture /release-notes output
            # In real implementation, this would parse the actual output
            result = subprocess.run(
                ["claude", "-p", "/release-notes"],
                capture_output=True,
                text=True,
                timeout=10
            )
            return result.stdout
        except Exception:
            return ""

    def parse_releases(self, notes: str) -> List[Dict]:
        """Parse release notes into structured data"""
        releases = []
        current_version = None
        current_features = []

        for line in notes.split('\n'):
            # Match version lines
            version_match = re.match(r'^Version\s+(\d+\.\d+\.\d+):', line)
            if version_match:
                # Save previous version
                if current_version:
                    releases.append({
                        "version": current_version,
                        "features": current_features.copy()
                    })

                current_version = version_match.group(1)
                current_features = []

            # Match feature lines (starts with •)
            elif line.strip().startswith('•'):
                feature = line.strip()[1:].strip()
                if feature:
                    current_features.append(feature)

        # Save last version
        if current_version:
            releases.append({
                "version": current_version,
                "features": current_features
            })

        return releases

    def categorize_feature(self, feature: str) -> List[str]:
        """Categorize feature by type"""
        categories = []

        feature_lower = feature.lower()

        # Category keywords
        category_map = {
            "productivity": ["shortcut", "faster", "quick", "speed", "optimize", "performance"],
            "debugging": ["debug", "fix", "error", "bug", "diagnose", "troubleshoot"],
            "automation": ["hook", "automat", "script", "workflow", "background"],
            "testing": ["test", "coverage", "validation", "verify"],
            "collaboration": ["team", "share", "pr", "commit", "review", "git"],
            "learning": ["docs", "help", "tutorial", "guide", "example"],
            "security": ["security", "permission", "auth", "safe", "vulnerability"],
            "ai": ["thinking", "model", "agent", "reasoning", "plan"],
            "customization": ["custom", "config", "setting", "plugin", "extension"],
            "integration": ["mcp", "ide", "vscode", "integration", "connect"]
        }

        for category, keywords in category_map.items():
            if any(keyword in feature_lower for keyword in keywords):
                categories.append(category)

        return categories if categories else ["general"]

    def get_new_releases(self, releases: List[Dict]) -> List[Dict]:
        """Get releases newer than last seen version"""
        last_version = self.config.get("last_seen_version")

        if not last_version:
            # First time - return recent releases
            return releases[:5]

        new_releases = []
        for release in releases:
            if release["version"] == last_version:
                break
            new_releases.append(release)

        return new_releases

    def generate_learning_recommendations(self, releases: List[Dict]) -> List[Dict]:
        """Generate personalized learning recommendations"""
        recommendations = []

        skill_level = self.config.get("skill_level", "intermediate")
        interests = self.config.get("interests", [])
        learned = set(self.history.get("learned_features", []))

        # Skill level priorities
        skill_priorities = {
            "beginner": ["productivity", "basics", "shortcuts"],
            "intermediate": ["automation", "debugging", "customization"],
            "advanced": ["integration", "hooks", "performance"],
            "expert": ["ai", "architecture", "optimization"]
        }

        priorities = skill_priorities.get(skill_level, [])

        for release in releases:
            for feature in release["features"]:
                # Skip if already learned
                feature_id = f"{release['version']}:{feature}"
                if feature_id in learned:
                    continue

                categories = self.categorize_feature(feature)

                # Calculate relevance score
                score = 0

                # Interest match
                if any(cat in interests for cat in categories):
                    score += 3

                # Skill level match
                if any(cat in priorities for cat in categories):
                    score += 2

                # Recency bonus
                try:
                    version_parts = [int(x) for x in release["version"].split('.')]
                    version_num = version_parts[0] * 1000 + version_parts[1] * 100 + version_parts[2]
                    if version_num >= 2000:  # Recent versions (2.0+)
                        score += 1
                except:
                    pass

                if score > 0:
                    recommendations.append({
                        "version": release["version"],
                        "feature": feature,
                        "categories": categories,
                        "score": score,
                        "feature_id": feature_id
                    })

        # Sort by score
        recommendations.sort(key=lambda x: x["score"], reverse=True)

        return recommendations[:10]  # Top 10

    def format_notification(self, new_releases: List[Dict], recommendations: List[Dict]) -> str:
        """Format notification message"""
        lines = []

        lines.append("=" * 70)
        lines.append("🚀 CLAUDE CODE UPDATES AVAILABLE!")
        lines.append("=" * 70)
        lines.append("")

        if new_releases:
            lines.append(f"📦 {len(new_releases)} new version(s) detected!")
            lines.append("")

            for release in new_releases[:3]:  # Show top 3
                lines.append(f"Version {release['version']}:")
                for feature in release["features"][:5]:  # Show top 5 features
                    lines.append(f"  • {feature}")
                lines.append("")

        if recommendations:
            lines.append("=" * 70)
            lines.append("💡 PERSONALIZED LEARNING RECOMMENDATIONS")
            lines.append("=" * 70)
            lines.append("")
            lines.append(f"Based on your skill level ({self.config['skill_level']}) and interests:")
            lines.append("")

            for i, rec in enumerate(recommendations[:5], 1):
                lines.append(f"{i}. [{rec['version']}] {rec['feature']}")
                lines.append(f"   Categories: {', '.join(rec['categories'])}")
                lines.append(f"   Relevance: {'⭐' * min(rec['score'], 5)}")
                lines.append("")

        lines.append("=" * 70)
        lines.append("📚 NEXT STEPS:")
        lines.append("=" * 70)
        lines.append("1. Review full release notes: /release-notes")
        lines.append("2. Try new features on a test project")
        lines.append("3. Update documentation: python3 monitor_releases.py --update-docs")
        lines.append("4. Mark features as learned: python3 monitor_releases.py --mark-learned")
        lines.append("")
        lines.append("Update your preferences: python3 monitor_releases.py --configure")
        lines.append("")

        return "\n".join(lines)

    def mark_feature_learned(self, feature_id: str):
        """Mark a feature as learned"""
        learned = self.history.get("learned_features", [])
        if feature_id not in learned:
            learned.append(feature_id)
            self.history["learned_features"] = learned
            self.save_history(self.history)

    def check_for_updates(self):
        """Main update check function"""
        print("🔍 Checking for Claude Code updates...\n")

        # Get current version
        current_version = self.get_current_version()
        print(f"Current version: {current_version}")

        # Get release notes (in real implementation)
        # For now, we'll create mock data based on the release notes provided
        notes = self.get_release_notes()

        if not notes:
            print("⚠️  Could not fetch release notes. Using cached data.")
            # In production, would use cached release notes

        # Parse releases
        releases = self.parse_releases(notes) if notes else []

        # Get new releases
        new_releases = self.get_new_releases(releases)

        # Generate recommendations
        recommendations = self.generate_learning_recommendations(new_releases)

        # Format and display notification
        if new_releases or recommendations:
            notification = self.format_notification(new_releases, recommendations)
            print(notification)

            # Update last seen version
            if new_releases:
                self.config["last_seen_version"] = new_releases[0]["version"]
            self.config["last_check"] = datetime.now().isoformat()
            self.save_config(self.config)
        else:
            print("✅ You're up to date! No new features to learn.")

        return len(new_releases), len(recommendations)

    def configure_interactive(self):
        """Interactive configuration"""
        print("=" * 70)
        print("⚙️  CLAUDE CODE RELEASE MONITOR - CONFIGURATION")
        print("=" * 70)
        print()

        # Skill level
        print("1. What's your skill level?")
        print("   1) Beginner - Just started with Claude Code")
        print("   2) Intermediate - Comfortable with basic features")
        print("   3) Advanced - Using custom commands and agents")
        print("   4) Expert - Building complex workflows")
        choice = input("\nYour choice [1-4]: ").strip()

        skill_map = {"1": "beginner", "2": "intermediate", "3": "advanced", "4": "expert"}
        self.config["skill_level"] = skill_map.get(choice, "intermediate")

        # Interests
        print("\n2. What are you interested in? (comma-separated)")
        print("   Options: productivity, debugging, automation, testing,")
        print("           collaboration, learning, security, ai, customization")
        interests_input = input("\nYour interests: ").strip()

        if interests_input:
            self.config["interests"] = [i.strip() for i in interests_input.split(',')]

        # Check frequency
        print("\n3. How often should we check for updates?")
        print("   1) Every time you start Claude Code")
        print("   2) Daily")
        print("   3) Weekly")
        choice = input("\nYour choice [1-3]: ").strip()

        freq_map = {"1": "startup", "2": "daily", "3": "weekly"}
        self.config["check_frequency"] = freq_map.get(choice, "daily")

        self.save_config(self.config)

        print("\n✅ Configuration saved!")
        print(f"📁 Config location: {self.config_file}")
        print()


def main():
    """Main entry point"""
    monitor = ReleaseMonitor()

    # Parse arguments
    args = sys.argv[1:]

    if "--configure" in args or "-c" in args:
        monitor.configure_interactive()
        return

    if "--help" in args or "-h" in args:
        print("""
Claude Code Release Monitor

Usage:
    python3 monitor_releases.py              # Check for updates
    python3 monitor_releases.py --configure  # Configure preferences
    python3 monitor_releases.py --status     # Show current status

Options:
    -c, --configure     Interactive configuration
    -h, --help          Show this help message
    --status            Show monitoring status

Setup as Cron Job:
    # Check daily at 9 AM
    0 9 * * * cd /path/to/scripts && python3 monitor_releases.py

Setup as Startup Script:
    # Add to .bashrc or .zshrc
    python3 /path/to/monitor_releases.py
""")
        return

    if "--status" in args:
        print("=" * 70)
        print("📊 RELEASE MONITOR STATUS")
        print("=" * 70)
        print(f"\nSkill Level: {monitor.config.get('skill_level', 'Not set')}")
        print(f"Interests: {', '.join(monitor.config.get('interests', []))}")
        print(f"Check Frequency: {monitor.config.get('check_frequency', 'Not set')}")
        print(f"Last Check: {monitor.config.get('last_check', 'Never')}")
        print(f"Last Seen Version: {monitor.config.get('last_seen_version', 'None')}")
        print(f"\nLearned Features: {len(monitor.history.get('learned_features', []))}")
        print(f"Config File: {monitor.config_file}")
        print()
        return

    # Default: check for updates
    new_count, rec_count = monitor.check_for_updates()

    # Exit code indicates if updates were found
    sys.exit(0 if new_count == 0 else 1)


if __name__ == "__main__":
    main()
