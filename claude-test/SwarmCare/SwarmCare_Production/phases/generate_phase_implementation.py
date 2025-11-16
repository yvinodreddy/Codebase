#!/usr/bin/env python3
"""
Automated Phase Implementation Generator
Generates complete standalone testing structure for any phase (01-28)
based on the proven Phase 00 blueprint.

Usage:
  python3 generate_phase_implementation.py --phase 01
  python3 generate_phase_implementation.py --all  # Generate all phases 01-28
  python3 generate_phase_implementation.py --range 01 05  # Generate phases 01-05

This script:
1. Reads phase README for context
2. Extracts story points and requirements
3. Generates complete directory structure
4. Creates customized app.py with 6 dashboard sections
5. Creates unified_tracker.py
6. Creates comprehensive_test.py
7. Creates all documentation
8. Sets correct ports
9. Initializes .state/phase_state.json
10. Creates startup scripts
"""

import os
import sys
import json
import argparse
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

# Paths
SCRIPT_DIR = Path(__file__).parent
PHASE00_DIR = SCRIPT_DIR / "phase00"
PHASE00_STANDALONE = PHASE00_DIR / "standalone_testing"
PHASE00_DEPLOYMENT = PHASE00_STANDALONE / "deployment"

# Base port for phases (8000 + phase_number)
BASE_PORT = 8000

# Color codes for output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_header(message: str):
    """Print formatted header"""
    print(f"\n{Colors.HEADER}{'='*80}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{message}{Colors.ENDC}")
    print(f"{Colors.HEADER}{'='*80}{Colors.ENDC}\n")


def print_success(message: str):
    """Print success message"""
    print(f"{Colors.OKGREEN}✅ {message}{Colors.ENDC}")


def print_info(message: str):
    """Print info message"""
    print(f"{Colors.OKCYAN}ℹ️  {message}{Colors.ENDC}")


def print_warning(message: str):
    """Print warning message"""
    print(f"{Colors.WARNING}⚠️  {message}{Colors.ENDC}")


def print_error(message: str):
    """Print error message"""
    print(f"{Colors.FAIL}❌ {message}{Colors.ENDC}")


def read_phase_readme(phase_num: str) -> Dict[str, Any]:
    """Read and parse phase README file"""
    phase_dir = SCRIPT_DIR / f"phase{phase_num}"
    readme_path = phase_dir / "README.md"

    if not readme_path.exists():
        print_error(f"README not found for phase {phase_num}")
        return {}

    with open(readme_path) as f:
        content = f.read()

    # Extract information
    info = {
        "phase_num": phase_num,
        "phase_name": "",
        "story_points": 0,
        "description": "",
        "priority": "P0",
        "status": "Not Started"
    }

    # Parse phase name from title
    for line in content.split('\n'):
        if line.startswith('# Phase'):
            info["phase_name"] = line.split(':', 1)[-1].strip()
        elif 'Story Points:' in line:
            try:
                info["story_points"] = int(line.split(':')[1].strip())
            except:
                pass
        elif 'Priority:' in line:
            info["priority"] = line.split(':')[1].strip()
        elif 'Status:' in line:
            info["status"] = line.split(':')[1].strip()
        elif line.startswith('## Description'):
            # Next non-empty line is the description
            lines = content.split('\n')
            idx = lines.index(line)
            for i in range(idx + 1, min(idx + 5, len(lines))):
                if lines[i].strip() and not lines[i].startswith('#'):
                    info["description"] = lines[i].strip()
                    break

    return info


def create_directory_structure(phase_num: str):
    """Create complete directory structure for phase"""
    phase_dir = SCRIPT_DIR / f"phase{phase_num}"
    standalone_dir = phase_dir / "standalone_testing"

    directories = [
        standalone_dir / "deployment",
        standalone_dir / "deployment" / "generated_files",
        standalone_dir / "deployment" / "frontend",
        standalone_dir / "requirements",
        standalone_dir / "test_data" / "seeding_scripts",
        standalone_dir / "standalone_testing_docs",
        standalone_dir / "issues",
        phase_dir / ".state"
    ]

    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
        print_success(f"Created: {directory.relative_to(SCRIPT_DIR)}")


def generate_app_py(phase_info: Dict[str, Any]) -> str:
    """Generate customized app.py for phase"""
    phase_num = phase_info["phase_num"]
    phase_name = phase_info["phase_name"]
    port = BASE_PORT + int(phase_num)

    # Read Phase 00 app.py as template
    template_path = PHASE00_DEPLOYMENT / "app.py"
    with open(template_path) as f:
        template = f.read()

    # Customize for this phase
    app_content = template.replace('PHASE_NUMBER = "00"', f'PHASE_NUMBER = "{phase_num}"')
    app_content = app_content.replace('PHASE_NAME = "Foundation"', f'PHASE_NAME = "{phase_name}"')
    app_content = app_content.replace('PORT = 8000', f'PORT = {port}')
    app_content = app_content.replace('Phase 0: Foundation', f'Phase {int(phase_num)}: {phase_name}')

    return app_content


def generate_unified_tracker_py(phase_info: Dict[str, Any]) -> str:
    """Generate customized unified_tracker.py for phase"""
    phase_num = phase_info["phase_num"]
    phase_name = phase_info["phase_name"]

    # Read Phase 00 unified_tracker.py as template
    template_path = PHASE00_DEPLOYMENT / "unified_tracker.py"
    with open(template_path) as f:
        template = f.read()

    # Customize for this phase
    tracker_content = template.replace('phase_number: str = "00"', f'phase_number: str = "{phase_num}"')
    tracker_content = tracker_content.replace('phase_name: str = "Foundation"', f'phase_name: str = "{phase_name}"')

    return tracker_content


def generate_comprehensive_test_py(phase_info: Dict[str, Any]) -> str:
    """Generate customized comprehensive_test.py for phase"""
    phase_num = phase_info["phase_num"]
    phase_name = phase_info["phase_name"]
    port = BASE_PORT + int(phase_num)

    # Read Phase 00 comprehensive_test.py as template
    template_path = PHASE00_DEPLOYMENT / "comprehensive_test.py"
    with open(template_path) as f:
        template = f.read()

    # Customize for this phase
    test_content = template.replace('PHASE_NUMBER = "00"', f'PHASE_NUMBER = "{phase_num}"')
    test_content = test_content.replace('PHASE_NAME = "Foundation"', f'PHASE_NAME = "{phase_name}"')
    test_content = test_content.replace('PORT = 8000', f'PORT = {port}')
    test_content = test_content.replace('Phase 0', f'Phase {int(phase_num)}')

    return test_content


def generate_startup_scripts(phase_info: Dict[str, Any], deployment_dir: Path):
    """Generate START_APPLICATION.sh and other scripts"""
    phase_num = phase_info["phase_num"]
    port = BASE_PORT + int(phase_num)

    # START_APPLICATION.sh
    start_script = f"""#!/bin/bash
# Phase {phase_num} - Standalone Testing Application Startup Script
# This script starts the complete testing application with all services

echo "========================================"
echo "Phase {phase_num}: {phase_info['phase_name']}"
echo "Starting Application..."
echo "========================================"
echo ""

# Check Python version
python3 --version || {{
    echo "❌ Python 3 not found!"
    exit 1
}}

# Check dependencies
echo "Checking dependencies..."
python3 -c "import fastapi" 2>/dev/null || {{
    echo "Installing FastAPI..."
    pip3 install fastapi uvicorn python-multipart
}}

python3 -c "import neo4j" 2>/dev/null || {{
    echo "Installing Neo4j driver..."
    pip3 install neo4j
}}

python3 -c "import redis" 2>/dev/null || {{
    echo "Installing Redis..."
    pip3 install redis
}}

echo ""
echo "✅ Dependencies ready"
echo ""

# Start application
echo "Starting FastAPI application on port {port}..."
python3 app.py

# Application will be accessible at:
# http://localhost:{port}
"""

    (deployment_dir / "START_APPLICATION.sh").write_text(start_script)
    (deployment_dir / "START_APPLICATION.sh").chmod(0o755)

    # QUICK_TEST.sh
    quick_test = f"""#!/bin/bash
echo "========================================"
echo "QUICK SERVICE VERIFICATION"
echo "========================================"
echo ""

echo "✅ Testing Port {port} (Phase {phase_num} Application)..."
curl -s -o /dev/null -w "   HTTP Status: %{{http_code}}\\n" http://localhost:{port}/api/health
echo ""

echo "========================================"
echo "OPEN IN BROWSER:"
echo "========================================"
echo "Main Dashboard: http://localhost:{port}"
echo "API Docs:       http://localhost:{port}/docs"
echo "========================================"
"""

    (deployment_dir / "QUICK_TEST.sh").write_text(quick_test)
    (deployment_dir / "QUICK_TEST.sh").chmod(0o755)

    print_success(f"Generated startup scripts")


def generate_user_stories_json(phase_info: Dict[str, Any]) -> Dict[str, Any]:
    """Generate user_stories.json for phase"""
    return {
        "phase": f"phase{phase_info['phase_num']}",
        "phase_name": phase_info["phase_name"],
        "total_story_points": phase_info["story_points"],
        "priority": phase_info["priority"],
        "status": phase_info["status"],
        "stories": [
            # Placeholder - to be filled with actual stories
            {
                "id": f"US-{phase_info['phase_num']}-001",
                "title": f"{phase_info['phase_name']} - Story 1",
                "description": f"As a developer, I want to implement {phase_info['phase_name']} functionality",
                "story_points": 5,
                "priority": phase_info["priority"],
                "status": "pending",
                "acceptance_criteria": [
                    "Implementation complete",
                    "Tests passing",
                    "Documentation updated"
                ],
                "implementation_notes": "To be implemented",
                "test_scenarios": [],
                "dependencies": [],
                "tags": [phase_info["phase_name"].lower().replace(' ', '-')]
            }
        ],
        "metrics": {
            "planned_story_points": phase_info["story_points"],
            "completed_story_points": 0,
            "completion_percentage": 0,
            "test_coverage_percentage": 0,
            "acceptance_criteria_met": "0%"
        }
    }


def generate_phase_state_json(phase_info: Dict[str, Any]) -> Dict[str, Any]:
    """Generate .state/phase_state.json"""
    return {
        "last_sync": datetime.now().isoformat(),
        "phase": phase_info["phase_num"],
        "status": "active",
        "metrics": {
            "total_stories": 1,  # Placeholder
            "total_story_points": phase_info["story_points"],
            "completed_story_points": 0,
            "completion_percentage": 0,
            "test_pass_rate": 0,
            "documentation_updated": False
        },
        "last_documentation_sync": datetime.now().isoformat(),
        "changes": [],
        "total_changes": 0
    }


def generate_documentation(phase_info: Dict[str, Any], standalone_dir: Path):
    """Generate all documentation files"""

    # ACCESS_GUIDE.md
    access_guide = f"""# How to Access Phase {phase_info['phase_num']} Application

**Phase:** {phase_info['phase_name']}
**Port:** {BASE_PORT + int(phase_info['phase_num'])}
**Status:** Development

## Access URLs

### Main Dashboard
```
http://localhost:{BASE_PORT + int(phase_info['phase_num'])}
```

### API Documentation
```
http://localhost:{BASE_PORT + int(phase_info['phase_num'])}/docs
```

## Quick Start

```bash
cd standalone_testing/deployment
./START_APPLICATION.sh
```

Then open your browser to http://localhost:{BASE_PORT + int(phase_info['phase_num'])}

## Available Sections

1. **Services Status** - Check service health
2. **Testing** - Run and view tests
3. **Requirements** - View user stories
4. **Metrics** - Track progress
5. **Generated Files** - View generated code
6. **Execution Log** - See activity log

---

**Generated:** {datetime.now().strftime('%Y-%m-%d')}
"""

    (standalone_dir / "deployment" / "ACCESS_GUIDE.md").write_text(access_guide)

    # ARCHITECTURE.md
    architecture = f"""# Phase {phase_info['phase_num']} - Technical Architecture

## Overview

Phase: {phase_info['phase_name']}
Story Points: {phase_info['story_points']}

## Components

- FastAPI Application (Port {BASE_PORT + int(phase_info['phase_num'])})
- Unified Tracker System
- Comprehensive Test Suite
- Documentation Auto-Sync

## Technology Stack

- Python 3.x
- FastAPI
- Neo4j (if applicable)
- Redis (if applicable)

---

**Generated:** {datetime.now().strftime('%Y-%m-%d')}
"""

    (standalone_dir / "standalone_testing_docs" / "ARCHITECTURE.md").write_text(architecture)

    print_success("Generated documentation files")


def implement_phase(phase_num: str, force: bool = False):
    """
    Implement complete standalone testing structure for a phase

    Args:
        phase_num: Phase number (e.g., "01", "02")
        force: If True, overwrite existing files
    """
    print_header(f"IMPLEMENTING PHASE {phase_num}")

    # Read phase information
    print_info(f"Reading phase {phase_num} README...")
    phase_info = read_phase_readme(phase_num)

    if not phase_info:
        print_error(f"Failed to read phase {phase_num} information")
        return False

    print_success(f"Phase Name: {phase_info['phase_name']}")
    print_success(f"Story Points: {phase_info['story_points']}")
    print_success(f"Port: {BASE_PORT + int(phase_num)}")

    # Create directory structure
    print_info("Creating directory structure...")
    create_directory_structure(phase_num)

    # Generate files
    phase_dir = SCRIPT_DIR / f"phase{phase_num}"
    standalone_dir = phase_dir / "standalone_testing"
    deployment_dir = standalone_dir / "deployment"

    print_info("Generating app.py...")
    app_content = generate_app_py(phase_info)
    (deployment_dir / "app.py").write_text(app_content)
    print_success(f"Generated app.py ({len(app_content)} chars)")

    print_info("Generating unified_tracker.py...")
    tracker_content = generate_unified_tracker_py(phase_info)
    (deployment_dir / "unified_tracker.py").write_text(tracker_content)
    print_success(f"Generated unified_tracker.py ({len(tracker_content)} chars)")

    print_info("Generating comprehensive_test.py...")
    test_content = generate_comprehensive_test_py(phase_info)
    (deployment_dir / "comprehensive_test.py").write_text(test_content)
    print_success(f"Generated comprehensive_test.py ({len(test_content)} chars)")

    print_info("Generating startup scripts...")
    generate_startup_scripts(phase_info, deployment_dir)

    print_info("Generating user_stories.json...")
    user_stories = generate_user_stories_json(phase_info)
    (standalone_dir / "requirements" / "user_stories.json").write_text(
        json.dumps(user_stories, indent=4)
    )
    print_success("Generated user_stories.json")

    print_info("Generating phase_state.json...")
    phase_state = generate_phase_state_json(phase_info)
    (phase_dir / ".state" / "phase_state.json").write_text(
        json.dumps(phase_state, indent=2)
    )
    print_success("Generated phase_state.json")

    print_info("Generating documentation...")
    generate_documentation(phase_info, standalone_dir)

    print_header(f"PHASE {phase_num} IMPLEMENTATION COMPLETE ✅")
    print_success(f"Phase {phase_num}: {phase_info['phase_name']}")
    print_success(f"Port: {BASE_PORT + int(phase_num)}")
    print_success(f"Start with: cd phase{phase_num}/standalone_testing/deployment && ./START_APPLICATION.sh")
    print_success(f"Access at: http://localhost:{BASE_PORT + int(phase_num)}")

    return True


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Generate complete standalone testing structure for SwarmCare phases'
    )
    parser.add_argument(
        '--phase',
        type=str,
        help='Phase number to generate (e.g., 01, 02)'
    )
    parser.add_argument(
        '--all',
        action='store_true',
        help='Generate all phases 01-28'
    )
    parser.add_argument(
        '--range',
        nargs=2,
        metavar=('START', 'END'),
        help='Generate range of phases (e.g., --range 01 05)'
    )
    parser.add_argument(
        '--force',
        action='store_true',
        help='Overwrite existing files'
    )

    args = parser.parse_args()

    if args.all:
        print_header("GENERATING ALL PHASES 01-28")
        for i in range(1, 29):
            phase_num = f"{i:02d}"
            implement_phase(phase_num, args.force)
    elif args.range:
        start, end = int(args.range[0]), int(args.range[1])
        print_header(f"GENERATING PHASES {start:02d}-{end:02d}")
        for i in range(start, end + 1):
            phase_num = f"{i:02d}"
            implement_phase(phase_num, args.force)
    elif args.phase:
        implement_phase(args.phase, args.force)
    else:
        parser.print_help()
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
