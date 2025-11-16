#!/usr/bin/env python3
"""
SwarmCare v2.1 - Distribution Config Generator
Generates balanced machine distributions for all 1102 story points across 29 phases
"""

import json
from pathlib import Path

# All 29 phases with their story points (from phase files)
PHASES = [
    {"id": 0, "name": "Foundation & Infrastructure", "points": 37, "priority": "P0", "dependencies": []},
    {"id": 1, "name": "RAG Heat System", "points": 60, "priority": "P0", "dependencies": [0]},
    {"id": 2, "name": "SWARMCARE Agents", "points": 94, "priority": "P0", "dependencies": [0, 1]},
    {"id": 3, "name": "Workflow Orchestration", "points": 76, "priority": "P0", "dependencies": [2]},
    {"id": 4, "name": "Frontend Application", "points": 47, "priority": "P1", "dependencies": [1, 2, 3]},
    {"id": 5, "name": "Audio Generation", "points": 21, "priority": "P1", "dependencies": [3]},
    {"id": 6, "name": "HIPAA Compliance (Base)", "points": 47, "priority": "P0", "dependencies": [0]},
    {"id": 7, "name": "Testing & QA", "points": 68, "priority": "P0", "dependencies": [0, 1, 2, 3, 4, 5, 6]},
    {"id": 8, "name": "Production Deployment", "points": 47, "priority": "P0", "dependencies": [7]},
    {"id": 9, "name": "Documentation", "points": 21, "priority": "P1", "dependencies": [8]},
    {"id": 10, "name": "Business & Partnerships", "points": 26, "priority": "P0", "dependencies": [8]},
    {"id": 11, "name": "Research & Publications", "points": 21, "priority": "P2", "dependencies": [8]},
    {"id": 12, "name": "Real-time Clinical Decision Support (Base)", "points": 55, "priority": "P0", "dependencies": [0, 1, 2]},
    {"id": 13, "name": "Predictive Analytics & ML Models (Base)", "points": 62, "priority": "P0", "dependencies": [0, 1, 12]},
    {"id": 14, "name": "Multi-modal AI - Medical Imaging (Base)", "points": 76, "priority": "P0", "dependencies": [0, 1]},
    {"id": 15, "name": "Advanced Medical NLP & Auto-Coding (Base)", "points": 47, "priority": "P0", "dependencies": [1]},
    {"id": 16, "name": "Explainable AI & Interpretability (Base)", "points": 34, "priority": "P0", "dependencies": [13, 14]},
    {"id": 17, "name": "Population Health Management (Base)", "points": 43, "priority": "P1", "dependencies": [13]},
    {"id": 18, "name": "Clinical Trial Matching & Research (Base)", "points": 38, "priority": "P1", "dependencies": [1, 2]},
    {"id": 19, "name": "Voice AI & Ambient Intelligence (Base)", "points": 51, "priority": "P0", "dependencies": [2, 15]},
    {"id": 20, "name": "Epic 7A: Security Certifications (SOC 2, HITRUST)", "points": 13, "priority": "P0", "dependencies": [6]},
    {"id": 21, "name": "Epic 13A: Closed-Loop Clinical Automation", "points": 13, "priority": "P0", "dependencies": [12]},
    {"id": 22, "name": "Epic 14A: Continuous Learning & Federated ML", "points": 8, "priority": "P0", "dependencies": [13]},
    {"id": 23, "name": "Epic 15A: FDA Clearance & PACS Integration", "points": 21, "priority": "P0", "dependencies": [14]},
    {"id": 24, "name": "Epic 16A: 100% Automated Coding & EHR Integration", "points": 13, "priority": "P0", "dependencies": [15]},
    {"id": 25, "name": "Epic 17A: Validated Patient-Facing XAI", "points": 8, "priority": "P0", "dependencies": [16]},
    {"id": 26, "name": "Epic 18A: Real-time CDC & Public Health Integration", "points": 21, "priority": "P0", "dependencies": [17]},
    {"id": 27, "name": "Epic 19A: Full Trial Lifecycle (EDC, eConsent, AE Reporting)", "points": 21, "priority": "P1", "dependencies": [18]},
    {"id": 28, "name": "Epic 20A: Ultra-fast Offline Voice AI (<500ms, 8 EHRs)", "points": 13, "priority": "P0", "dependencies": [19]},
]

TOTAL_POINTS = sum(p["points"] for p in PHASES)


def generate_5_machine_distribution():
    """Generate balanced distribution for 5 machines"""

    # Target: ~220 points per machine (1102 / 5)
    # Machine 01 MUST have Phase 0 (foundation)

    distribution = {
        "distribution_strategy": "balanced_5_machines_v2.1",
        "version": "2.1",
        "total_machines": 5,
        "total_phases": 29,
        "total_story_points": TOTAL_POINTS,
        "machines": [
            {
                "machine_id": "machine_01",
                "developer": "Developer 1",
                "assigned_phases": [0, 1, 11, 24, 28],
                "phase_names": [PHASES[i]["name"] for i in [0, 1, 11, 24, 28]],
                "total_story_points": sum(PHASES[i]["points"] for i in [0, 1, 11, 24, 28]),
                "estimated_duration": "4-6 days",
                "priority": "P0 - Critical Path",
                "notes": "Contains foundation phase - MUST complete Phase 0 first"
            },
            {
                "machine_id": "machine_02",
                "developer": "Developer 2",
                "assigned_phases": [2, 3, 16, 18, 20, 21, 22],
                "phase_names": [PHASES[i]["name"] for i in [2, 3, 16, 18, 20, 21, 22]],
                "total_story_points": sum(PHASES[i]["points"] for i in [2, 3, 16, 18, 20, 21, 22]),
                "estimated_duration": "4-6 days",
                "priority": "P0 - Critical Path",
                "notes": "Core agent system and ML features"
            },
            {
                "machine_id": "machine_03",
                "developer": "Developer 3",
                "assigned_phases": [4, 5, 9, 14, 25, 26, 27],
                "phase_names": [PHASES[i]["name"] for i in [4, 5, 9, 14, 25, 26, 27]],
                "total_story_points": sum(PHASES[i]["points"] for i in [4, 5, 9, 14, 25, 26, 27]),
                "estimated_duration": "4-6 days",
                "priority": "P1",
                "notes": "Frontend, imaging, and patient-facing features"
            },
            {
                "machine_id": "machine_04",
                "developer": "Developer 4",
                "assigned_phases": [6, 7, 10, 12, 23],
                "phase_names": [PHASES[i]["name"] for i in [6, 7, 10, 12, 23]],
                "total_story_points": sum(PHASES[i]["points"] for i in [6, 7, 10, 12, 23]),
                "estimated_duration": "4-6 days",
                "priority": "P0 - Critical Path",
                "notes": "Compliance, testing, and clinical decision support"
            },
            {
                "machine_id": "machine_05",
                "developer": "Developer 5",
                "assigned_phases": [8, 13, 15, 17, 19],
                "phase_names": [PHASES[i]["name"] for i in [8, 13, 15, 17, 19]],
                "total_story_points": sum(PHASES[i]["points"] for i in [8, 13, 15, 17, 19]),
                "estimated_duration": "4-6 days",
                "priority": "P1",
                "notes": "Deployment, ML/AI, and voice features"
            }
        ],
        "execution_order": [
            {
                "step": 1,
                "description": "Machine 01 MUST complete Phase 0 (Foundation) first",
                "machines": ["machine_01"],
                "phases": [0],
                "estimated_time": "4 hours"
            },
            {
                "step": 2,
                "description": "All machines work in parallel after Phase 0",
                "machines": ["machine_01", "machine_02", "machine_03", "machine_04", "machine_05"],
                "phases": "all_remaining",
                "estimated_time": "4-6 days"
            },
            {
                "step": 3,
                "description": "Package and transfer all phase outputs",
                "action": "./DISTRIBUTED_EXECUTOR.sh package",
                "estimated_time": "1.5 hours"
            },
            {
                "step": 4,
                "description": "Collect and integrate all phases",
                "action": "./COLLECT_PHASES.sh && ./INTEGRATE_ALL.sh",
                "estimated_time": "6-8 hours"
            }
        ]
    }

    return distribution


def generate_10_machine_distribution():
    """Generate maximum parallelization distribution for 10 machines"""

    # Target: ~110 points per machine (1102 / 10)

    distribution = {
        "distribution_strategy": "maximum_parallelization_10_machines_v2.1",
        "version": "2.1",
        "total_machines": 10,
        "total_phases": 29,
        "total_story_points": TOTAL_POINTS,
        "machines": [
            {
                "machine_id": "machine_01",
                "developer": "Developer 1",
                "assigned_phases": [0, 11],
                "phase_names": [PHASES[i]["name"] for i in [0, 11]],
                "total_story_points": sum(PHASES[i]["points"] for i in [0, 11]),
                "estimated_duration": "1 day",
                "priority": "P0 - MUST RUN FIRST",
                "notes": "Foundation phase - all others depend on this"
            },
            {
                "machine_id": "machine_02",
                "developer": "Developer 2",
                "assigned_phases": [1, 15],
                "phase_names": [PHASES[i]["name"] for i in [1, 15]],
                "total_story_points": sum(PHASES[i]["points"] for i in [1, 15]),
                "estimated_duration": "2-3 days",
                "priority": "P0 - Critical Path",
                "notes": "RAG Heat and Medical NLP"
            },
            {
                "machine_id": "machine_03",
                "developer": "Developer 3",
                "assigned_phases": [2, 18],
                "phase_names": [PHASES[i]["name"] for i in [2, 18]],
                "total_story_points": sum(PHASES[i]["points"] for i in [2, 18]),
                "estimated_duration": "2-4 days",
                "priority": "P0 - Critical Path",
                "notes": "Agent system and clinical trials"
            },
            {
                "machine_id": "machine_04",
                "developer": "Developer 4",
                "assigned_phases": [3, 5, 9],
                "phase_names": [PHASES[i]["name"] for i in [3, 5, 9]],
                "total_story_points": sum(PHASES[i]["points"] for i in [3, 5, 9]),
                "estimated_duration": "2-3 days",
                "priority": "P0 - Critical Path",
                "notes": "Workflows, audio, and documentation"
            },
            {
                "machine_id": "machine_05",
                "developer": "Developer 5",
                "assigned_phases": [4, 10, 27],
                "phase_names": [PHASES[i]["name"] for i in [4, 10, 27]],
                "total_story_points": sum(PHASES[i]["points"] for i in [4, 10, 27]),
                "estimated_duration": "2-3 days",
                "priority": "P1",
                "notes": "Frontend, business, and trial lifecycle"
            },
            {
                "machine_id": "machine_06",
                "developer": "Developer 6",
                "assigned_phases": [6, 7],
                "phase_names": [PHASES[i]["name"] for i in [6, 7]],
                "total_story_points": sum(PHASES[i]["points"] for i in [6, 7]),
                "estimated_duration": "2-3 days",
                "priority": "P0 - Critical Path",
                "notes": "HIPAA compliance and testing"
            },
            {
                "machine_id": "machine_07",
                "developer": "Developer 7",
                "assigned_phases": [8, 12, 21],
                "phase_names": [PHASES[i]["name"] for i in [8, 12, 21]],
                "total_story_points": sum(PHASES[i]["points"] for i in [8, 12, 21]),
                "estimated_duration": "2-3 days",
                "priority": "P0 - Critical Path",
                "notes": "Deployment and clinical automation"
            },
            {
                "machine_id": "machine_08",
                "developer": "Developer 8",
                "assigned_phases": [13, 17, 22],
                "phase_names": [PHASES[i]["name"] for i in [13, 17, 22]],
                "total_story_points": sum(PHASES[i]["points"] for i in [13, 17, 22]),
                "estimated_duration": "2-3 days",
                "priority": "P0",
                "notes": "Predictive analytics and ML"
            },
            {
                "machine_id": "machine_09",
                "developer": "Developer 9",
                "assigned_phases": [14, 16, 23, 25],
                "phase_names": [PHASES[i]["name"] for i in [14, 16, 23, 25]],
                "total_story_points": sum(PHASES[i]["points"] for i in [14, 16, 23, 25]),
                "estimated_duration": "2-4 days",
                "priority": "P0",
                "notes": "Medical imaging and explainability"
            },
            {
                "machine_id": "machine_10",
                "developer": "Developer 10",
                "assigned_phases": [19, 20, 24, 26, 28],
                "phase_names": [PHASES[i]["name"] for i in [19, 20, 24, 26, 28]],
                "total_story_points": sum(PHASES[i]["points"] for i in [19, 20, 24, 26, 28]),
                "estimated_duration": "2-3 days",
                "priority": "P0-P1",
                "notes": "Voice AI and epic features"
            }
        ],
        "execution_order": [
            {
                "step": 1,
                "description": "Machine 01 completes Phase 0 (Foundation)",
                "machines": ["machine_01"],
                "phases": [0],
                "estimated_time": "4 hours"
            },
            {
                "step": 2,
                "description": "All other machines start in parallel after Phase 0",
                "machines": [f"machine_{i:02d}" for i in range(2, 11)],
                "phases": "all_remaining",
                "estimated_time": "2-4 days"
            },
            {
                "step": 3,
                "description": "Package all outputs",
                "action": "./DISTRIBUTED_EXECUTOR.sh package",
                "estimated_time": "30 minutes"
            },
            {
                "step": 4,
                "description": "Collect and integrate",
                "action": "./COLLECT_PHASES.sh && ./INTEGRATE_ALL.sh",
                "estimated_time": "4-6 hours"
            }
        ]
    }

    return distribution


def save_distributions():
    """Generate and save both distribution configs"""
    base_path = Path("/home/user01/claude-test/SwarmCare/start/machine_configs")
    base_path.mkdir(parents=True, exist_ok=True)

    # Generate 5-machine distribution
    dist_5 = generate_5_machine_distribution()
    with open(base_path / "5_machine_distribution.json", "w") as f:
        json.dump(dist_5, f, indent=2)

    print("✓ 5-Machine Distribution:")
    print(f"  Total points distributed: {sum(m['total_story_points'] for m in dist_5['machines'])}")
    for machine in dist_5["machines"]:
        print(f"  {machine['machine_id']}: {machine['total_story_points']} points ({len(machine['assigned_phases'])} phases)")

    # Generate 10-machine distribution
    dist_10 = generate_10_machine_distribution()
    with open(base_path / "10_machine_distribution.json", "w") as f:
        json.dump(dist_10, f, indent=2)

    print("\n✓ 10-Machine Distribution:")
    print(f"  Total points distributed: {sum(m['total_story_points'] for m in dist_10['machines'])}")
    for machine in dist_10["machines"]:
        print(f"  {machine['machine_id']}: {machine['total_story_points']} points ({len(machine['assigned_phases'])} phases)")

    print(f"\n✓ Generated both distribution configs with total {TOTAL_POINTS} story points")


if __name__ == "__main__":
    print("=" * 80)
    print("SWARMCARE V2.1 - DISTRIBUTION CONFIG GENERATOR")
    print(f"Total Story Points: {TOTAL_POINTS}")
    print(f"Total Phases: {len(PHASES)}")
    print("=" * 80)
    print()
    save_distributions()
    print("=" * 80)
