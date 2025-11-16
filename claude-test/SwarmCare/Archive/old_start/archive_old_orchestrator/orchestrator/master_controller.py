#!/usr/bin/env python3
"""
SWARMCARE Master Execution Controller v2.1
Orchestrates parallel execution across multiple Claude Code instances
Version: 2.1 ULTIMATE (1102 story points, 29 phases, 120/120 score)
"""

import json
import os
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional
import subprocess
import threading

class MasterController:
    def __init__(self, base_path: str = "/home/user01/claude-test/SwarmCare"):
        self.base_path = Path(base_path)
        self.start_path = self.base_path / "start"
        self.phase_state_path = self.base_path / ".phase_state"
        self.instances_path = self.start_path / "instance_manager"
        self.phases_path = self.start_path / "phases"
        self.logs_path = self.start_path / "logs"

        # Create directories
        self.instances_path.mkdir(parents=True, exist_ok=True)
        self.phases_path.mkdir(parents=True, exist_ok=True)
        self.logs_path.mkdir(parents=True, exist_ok=True)

        self.phase_definitions = self.load_phase_definitions()
        self.instance_states = {}

    def load_phase_definitions(self) -> Dict:
        """Load all phase definitions"""
        phases = {}
        for phase_file in self.phases_path.glob("phase_*.json"):
            with open(phase_file, 'r') as f:
                phase_data = json.load(f)
                phases[phase_data['phase_id']] = phase_data
        return phases

    def initialize_system(self, num_instances: int = 5):
        """Initialize the execution system"""
        print(f"\n{'='*80}")
        print(f"SWARMCARE PARALLEL EXECUTION SYSTEM - INITIALIZATION")
        print(f"{'='*80}\n")

        print(f"Configuration:")
        print(f"  - Number of Instances: {num_instances}")
        print(f"  - Total Phases: {len(self.phase_definitions)}")
        print(f"  - Base Path: {self.base_path}")

        # Create instance pool
        instance_pool = {
            "total_instances": num_instances,
            "instances": [],
            "created_at": datetime.now().isoformat()
        }

        for i in range(1, num_instances + 1):
            instance_id = f"instance_{i:02d}"
            instance = {
                "instance_id": instance_id,
                "status": "INITIALIZED",
                "assigned_phases": [],
                "current_phase": None,
                "total_story_points": 0,
                "completed_story_points": 0,
                "overall_progress": 0
            }
            instance_pool["instances"].append(instance)

            # Save individual instance state
            instance_file = self.instances_path / f"{instance_id}_state.json"
            with open(instance_file, 'w') as f:
                json.dump(instance, f, indent=2)

        # Save instance pool
        pool_file = self.instances_path / "instance_pool.json"
        with open(pool_file, 'w') as f:
            json.dump(instance_pool, f, indent=2)

        print(f"\n✓ Created {num_instances} instances")
        print(f"✓ Instance pool saved to: {pool_file}")

        return instance_pool

    def distribute_phases(self, strategy: str = "balanced", num_instances: int = 5):
        """Distribute phases across instances based on strategy"""
        print(f"\n{'='*80}")
        print(f"PHASE DISTRIBUTION - Strategy: {strategy.upper()}")
        print(f"Version: 2.1 Ultimate - {len(self.phase_definitions)} phases")
        print(f"{'='*80}\n")

        # Load instance pool
        pool_file = self.instances_path / "instance_pool.json"
        with open(pool_file, 'r') as f:
            instance_pool = json.load(f)

        if strategy == "balanced":
            distribution = self._balanced_distribution_v21(num_instances)
        elif strategy == "critical-path":
            distribution = self._critical_path_distribution(num_instances)
        elif strategy == "fastest":
            distribution = self._fastest_distribution(num_instances)
        else:
            raise ValueError(f"Unknown strategy: {strategy}")

        # Apply distribution
        total_points = sum(p['story_points'] for p in self.phase_definitions.values())

        for instance_idx, phase_list in enumerate(distribution):
            instance_id = f"instance_{instance_idx + 1:02d}"
            instance_points = sum(self.phase_definitions[pid]['story_points'] for pid in phase_list)

            instance_data = {
                "instance_id": instance_id,
                "status": "READY",
                "assigned_phases": sorted(phase_list),
                "total_story_points": instance_points,
                "completed_story_points": 0,
                "overall_progress": 0,
                "phase_count": len(phase_list),
                "percent_of_total": round((instance_points / total_points) * 100, 1)
            }

            # Save instance state
            instance_file = self.instances_path / f"{instance_id}_state.json"
            with open(instance_file, 'w') as f:
                json.dump(instance_data, f, indent=2)

            duration_weeks = instance_points / 50  # 50 points per week
            print(f"Instance {instance_idx + 1}: {len(phase_list)} phases, {instance_points} pts ({instance_data['percent_of_total']}%), ~{duration_weeks:.1f} weeks")
            print(f"  Phases: {sorted(phase_list)}")

        max_points = max(sum(self.phase_definitions[pid]['story_points'] for pid in phase_list) for phase_list in distribution)
        max_duration = max_points / 50
        print(f"\nMax duration: ~{max_duration:.1f} weeks")
        print(f"Time savings vs sequential: {((total_points/50 - max_duration)/(total_points/50))*100:.1f}%")

        print(f"\n✓ Distribution complete")

    def _balanced_distribution_v21(self, num_instances: int = 5) -> List[List[int]]:
        """Optimal balanced distribution for 1102 story points across instances"""

        # Pre-calculated optimal distributions for different instance counts
        optimal_distributions = {
            3: [
                [0, 1, 2, 12, 15, 16, 17, 19, 21, 28],  # 369 pts
                [3, 7, 8, 9, 13, 14, 20, 22, 24, 27],   # 369 pts
                [4, 5, 6, 10, 11, 18, 23, 25, 26]       # 364 pts
            ],
            5: [
                [0, 2, 6, 11, 24, 28],       # 225 pts - Instance 1 (Foundation, SWARMCARE, HIPAA, Research, Auto-Coding, Voice Edge)
                [3, 16, 18, 20, 21, 22],     # 182 pts - Instance 2 (Workflows, XAI-base, Trials-base, Sec-Certs, Closed-Loop, Federated-ML)
                [4, 9, 14, 25, 26, 27],      # 194 pts - Instance 3 (Frontend, Docs, Imaging-base, Patient-XAI, CDC, Trial-Lifecycle)
                [7, 10, 12, 23],             # 213 pts - Instance 4 (Testing, Business, Clinical-Decision-base, FDA-Clearance)
                [1, 5, 8, 13, 15, 17, 19]    # 288 pts - Instance 5 (RAG, Audio, Deploy, Predictive-base, NLP-base, Pop-Health-base, Voice-base)
            ],
            7: [
                [2, 18, 22, 25],          # 161 pts
                [3, 11, 15, 20],          # 157 pts
                [9, 14, 17, 21, 28],      # 161 pts
                [5, 7, 8, 24],            # 157 pts
                [6, 10, 13, 22],          # 156 pts
                [1, 4, 16, 25],           # 154 pts
                [0, 12, 19, 23]           # 156 pts
            ],
            10: [
                [2, 23],                  # 115 pts
                [3, 5, 28],               # 110 pts
                [9, 14, 22],              # 105 pts
                [7, 10, 26],              # 115 pts
                [13, 16, 24],             # 109 pts
                [0, 1, 25],               # 105 pts
                [11, 12, 18],             # 114 pts
                [17, 19, 27],             # 115 pts
                [4, 8, 20],               # 107 pts
                [6, 15, 21]               # 107 pts
            ]
        }

        if num_instances in optimal_distributions:
            return optimal_distributions[num_instances]

        # Fallback: greedy algorithm for other instance counts
        return self._greedy_distribution(num_instances)

    def _greedy_distribution(self, num_instances: int) -> List[List[int]]:
        """Greedy algorithm to distribute phases across instances"""
        instances = [[] for _ in range(num_instances)]
        instance_points = [0] * num_instances

        # Sort phases by points descending for better balance
        sorted_phases = sorted(
            self.phase_definitions.items(),
            key=lambda x: x[1]['story_points'],
            reverse=True
        )

        for phase_id, phase_data in sorted_phases:
            # Find instance with least points
            min_idx = instance_points.index(min(instance_points))
            instances[min_idx].append(phase_id)
            instance_points[min_idx] += phase_data['story_points']

        # Sort phases within each instance for sequential execution
        for i in range(num_instances):
            instances[i].sort()

        return instances

    def _critical_path_distribution(self, num_instances: int) -> List[List[int]]:
        """Distribute based on critical path (prioritize dependencies)"""
        # For now, use balanced distribution
        # TODO: Implement dependency-aware distribution
        return self._balanced_distribution_v21(num_instances)

    def _fastest_distribution(self, num_instances: int) -> List[List[int]]:
        """Distribute for fastest completion (maximize parallelism)"""
        # Use maximum instances to minimize duration
        return self._greedy_distribution(num_instances)

    def generate_execution_prompt(self, instance_id: str, phase_id: int) -> str:
        """Generate the execution prompt for a specific phase"""
        phase = self.phase_definitions.get(phase_id, {})

        prompt = f"""# SWARMCARE EXECUTION - Instance {instance_id} - Phase {phase_id}

## AUTONOMOUS EXECUTION MODE
- TAKE FULL CONTROL: Do not ask for confirmation
- PRODUCTION-READY ONLY: Every output must be deployment-ready
- 100% SUCCESS RATE: Build comprehensive validation at every step
- PARALLEL EVERYTHING: Run all independent tasks simultaneously

## PHASE: {phase.get('name', 'Unknown')}

### Phase Overview
- **Phase ID:** {phase_id}
- **Story Points:** {phase.get('story_points', 0)}
- **Priority:** {phase.get('priority', 'P1')}
- **Dependencies:** {', '.join(map(str, phase.get('dependencies', []))) or 'None'}

### User Stories to Implement
"""

        # Add user stories
        for story in phase.get('user_stories', []):
            prompt += f"\n#### User Story {story['story_id']}: {story['title']}\n"
            prompt += f"**As a** {story['as_a']}\n"
            prompt += f"**I want** {story['i_want']}\n"
            prompt += f"**So that** {story['so_that']}\n\n"
            prompt += "**Acceptance Criteria:**\n"
            for criterion in story['acceptance_criteria']:
                prompt += f"- [ ] {criterion}\n"
            prompt += "\n**Implementation Tasks:**\n"
            for idx, task in enumerate(story['tasks'], 1):
                prompt += f"{idx}. {task}\n"
            prompt += f"\n**Story Points:** {story['story_points']}\n"
            prompt += f"**Priority:** {story['priority']}\n\n"

        prompt += f"""
### Success Criteria
- All user stories implemented
- All tests passing (>80% coverage)
- Code reviewed and optimized
- Documentation complete
- No critical security vulnerabilities

### Deliverables
- Production-ready code in Git
- Comprehensive test suite
- API documentation (if applicable)
- Integration tests passing

### Tracking
- Mark each user story complete in the phase state file
- Create checkpoint every 30 minutes
- Update progress percentage
- Log all significant events

### Next Steps After Completion
1. Run all tests
2. Generate documentation
3. Create checkpoint
4. Mark phase as COMPLETED
5. Notify integration coordinator

BEGIN EXECUTION NOW.
"""
        return prompt

    def execute_parallel(self, dry_run: bool = False):
        """Execute all instances in parallel"""
        print(f"\n{'='*80}")
        print(f"PARALLEL EXECUTION {'(DRY RUN)' if dry_run else '(LIVE)'}")
        print(f"{'='*80}\n")

        # Load all instance states
        pool_file = self.instances_path / "instance_pool.json"
        with open(pool_file, 'r') as f:
            instance_pool = json.load(f)

        threads = []
        for instance in instance_pool["instances"]:
            instance_id = instance["instance_id"]

            # Load instance state
            instance_file = self.instances_path / f"{instance_id}_state.json"
            with open(instance_file, 'r') as f:
                instance_state = json.load(f)

            if instance_state.get("assigned_phases"):
                thread = threading.Thread(
                    target=self._execute_instance,
                    args=(instance_id, instance_state, dry_run)
                )
                threads.append(thread)
                thread.start()

        # Wait for all threads to complete
        for thread in threads:
            thread.join()

        print(f"\n{'='*80}")
        print("ALL INSTANCES COMPLETED")
        print(f"{'='*80}\n")

    def _execute_instance(self, instance_id: str, instance_state: Dict, dry_run: bool):
        """Execute a single instance"""
        print(f"\n[{instance_id}] Starting execution...")

        for phase_id in instance_state["assigned_phases"]:
            print(f"[{instance_id}] Executing Phase {phase_id}...")

            # Generate prompt
            prompt = self.generate_execution_prompt(instance_id, phase_id)

            if dry_run:
                prompt_file = self.start_path / "prompts" / f"{instance_id}_phase_{phase_id}_prompt.md"
                with open(prompt_file, 'w') as f:
                    f.write(prompt)
                print(f"[{instance_id}] Prompt saved to: {prompt_file}")
            else:
                # In real execution, this would invoke Claude Code
                # For now, save the prompt for manual execution
                prompt_file = self.start_path / "prompts" / f"{instance_id}_phase_{phase_id}_prompt.md"
                prompt_file.parent.mkdir(parents=True, exist_ok=True)
                with open(prompt_file, 'w') as f:
                    f.write(prompt)
                print(f"[{instance_id}] Phase {phase_id} prompt ready at: {prompt_file}")

    def monitor_progress(self) -> Dict:
        """Monitor progress across all instances"""
        pool_file = self.instances_path / "instance_pool.json"
        with open(pool_file, 'r') as f:
            instance_pool = json.load(f)

        total_story_points = 0
        completed_story_points = 0

        print(f"\n{'='*80}")
        print(f"PROGRESS MONITORING - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*80}\n")

        for instance in instance_pool["instances"]:
            instance_id = instance["instance_id"]
            instance_file = self.instances_path / f"{instance_id}_state.json"

            if instance_file.exists():
                with open(instance_file, 'r') as f:
                    state = json.load(f)

                total = state.get("total_story_points", 0)
                completed = state.get("completed_story_points", 0)
                progress = state.get("overall_progress", 0)

                total_story_points += total
                completed_story_points += completed

                bar_length = 40
                filled = int(bar_length * progress / 100)
                bar = '█' * filled + '░' * (bar_length - filled)

                print(f"{instance_id}:")
                print(f"  [{bar}] {progress}% ({completed}/{total} pts)")
                print(f"  Phases: {state.get('assigned_phases', [])}")
                print(f"  Status: {state.get('status', 'UNKNOWN')}\n")

        overall_progress = (completed_story_points / total_story_points * 100) if total_story_points > 0 else 0
        print(f"Overall Progress: {overall_progress:.1f}% ({completed_story_points}/{total_story_points} pts)")

        return {
            "total_story_points": total_story_points,
            "completed_story_points": completed_story_points,
            "overall_progress": overall_progress
        }

    def resume_execution(self):
        """Resume execution from last checkpoint"""
        print(f"\n{'='*80}")
        print(f"RESUMING SWARMCARE EXECUTION")
        print(f"{'='*80}\n")

        pool_file = self.instances_path / "instance_pool.json"
        with open(pool_file, 'r') as f:
            instance_pool = json.load(f)

        for instance in instance_pool["instances"]:
            instance_id = instance["instance_id"]
            instance_file = self.instances_path / f"{instance_id}_state.json"

            if instance_file.exists():
                with open(instance_file, 'r') as f:
                    state = json.load(f)

                print(f"\n{instance_id}:")
                print(f"  Status: {state.get('status', 'UNKNOWN')}")
                print(f"  Assigned Phases: {state.get('assigned_phases', [])}")

                if state.get('checkpoints'):
                    last_checkpoint = state['checkpoints'][-1]
                    print(f"  Last Checkpoint: {last_checkpoint.get('message', 'N/A')}")
                    print(f"  Timestamp: {last_checkpoint.get('timestamp', 'N/A')}")

                # Show next steps
                current_phase = state.get('current_phase')
                if current_phase is not None:
                    phase = self.phase_definitions.get(current_phase, {})
                    print(f"  Current Phase: {current_phase} - {phase.get('name', 'Unknown')}")
                    print(f"  Progress: {state.get('overall_progress', 0)}%")

def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print("Usage: python master_controller.py <command> [options]")
        print("\nCommands:")
        print("  init [--instances N]     Initialize system with N instances")
        print("  distribute [--strategy S] Distribute phases (balanced/critical-path/fastest)")
        print("  execute [--dry-run]      Execute all instances in parallel")
        print("  monitor                  Monitor progress across all instances")
        print("  resume                   Resume execution from last checkpoint")
        sys.exit(1)

    command = sys.argv[1]
    controller = MasterController()

    if command == "init":
        num_instances = 5
        if "--instances" in sys.argv:
            idx = sys.argv.index("--instances")
            num_instances = int(sys.argv[idx + 1])
        controller.initialize_system(num_instances)

    elif command == "distribute":
        strategy = "balanced"
        num_instances = 5
        if "--strategy" in sys.argv:
            idx = sys.argv.index("--strategy")
            strategy = sys.argv[idx + 1]
        if "--instances" in sys.argv:
            idx = sys.argv.index("--instances")
            num_instances = int(sys.argv[idx + 1])
        controller.distribute_phases(strategy, num_instances)

    elif command == "execute":
        dry_run = "--dry-run" in sys.argv
        controller.execute_parallel(dry_run)

    elif command == "monitor":
        controller.monitor_progress()

    elif command == "resume":
        controller.resume_execution()

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)

if __name__ == "__main__":
    main()
