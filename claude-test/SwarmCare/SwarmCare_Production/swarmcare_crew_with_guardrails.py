"""
SwarmCare Crew with Integrated Guardrails
Production-ready medical AI crew with 7-layer guardrail protection
"""

import os
import logging
from pathlib import Path
from typing import Dict, Any, Optional, List
from dotenv import load_dotenv
import yaml

from crewai import Agent, Task, Crew, LLM
from crewai.project import CrewBase, agent, task, crew

# Import guardrail functions
from guardrails.crewai_guardrails import (
    medical_knowledge_extraction_guardrail,
    clinical_case_synthesis_guardrail,
    medical_dialogue_guardrail,
    compliance_validation_guardrail,
    podcast_script_guardrail,
    quality_assurance_guardrail
)
from guardrails.multi_layer_system import MultiLayerGuardrailSystem
from guardrails.monitoring import get_monitor

load_dotenv()

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize guardrail system and monitor
guardrail_system = MultiLayerGuardrailSystem()
monitor = get_monitor()


class SwarmCareCrew:
    """
    SwarmCare Medical Podcast Generation Crew with Guardrails

    This crew generates high-quality medical educational content with:
    - 7-layer guardrail protection
    - HIPAA compliance validation
    - Medical fact-checking
    - PHI detection and prevention
    - Content safety filtering
    - Professional quality assurance
    """

    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize SwarmCare crew.

        Args:
            config_path: Path to configuration directory (default: ./Agents)
        """
        self.config_path = Path(config_path) if config_path else Path("Agents")

        # Load configurations
        self.agents_config = self._load_yaml(self.config_path / "agents.yaml")
        self.tasks_config = self._load_yaml(self.config_path / "tasks_with_guardrails.yaml")

        # Initialize LLM
        self.llm = self._create_llm()

        logger.info("SwarmCare Crew initialized with guardrails")

    def _load_yaml(self, file_path: Path) -> Dict:
        """Load YAML configuration file."""
        try:
            with open(file_path, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            logger.error(f"Error loading {file_path}: {e}")
            return {}

    def _create_llm(self) -> LLM:
        """Create LLM instance for Azure OpenAI."""
        return LLM(
            model=f"azure/{os.getenv('AZURE_OPENAI_DEPLOYMENT_NAME', 'gpt-4o')}",
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            base_url=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-08-01-preview")
        )

    def create_agents(self, inputs: Dict[str, Any]) -> Dict[str, Agent]:
        """
        Create all SwarmCare agents.

        Args:
            inputs: Configuration inputs for agents

        Returns:
            Dictionary of agent instances
        """
        agents = {}

        # Medical Knowledge Extractor
        agents["medical_knowledge_extractor"] = Agent(
            role=self.agents_config["medical_knowledge_extractor"]["role"],
            goal=self.agents_config["medical_knowledge_extractor"]["goal"].format(**inputs),
            backstory=self.agents_config["medical_knowledge_extractor"]["backstory"],
            llm=self.llm,
            verbose=True,
            allow_delegation=False,
            max_iter=inputs.get("max_iterations_extractor", 15)
        )

        # Patient Case Synthesizer
        agents["patient_case_synthesizer"] = Agent(
            role=self.agents_config["patient_case_synthesizer"]["role"],
            goal=self.agents_config["patient_case_synthesizer"]["goal"].format(**inputs),
            backstory=self.agents_config["patient_case_synthesizer"]["backstory"],
            llm=self.llm,
            verbose=True,
            allow_delegation=True,
            max_iter=inputs.get("max_iterations_synthesizer", 15)
        )

        # Medical Conversation Writer
        agents["medical_conversation_writer"] = Agent(
            role=self.agents_config["medical_conversation_writer"]["role"],
            goal=self.agents_config["medical_conversation_writer"]["goal"].format(**inputs),
            backstory=self.agents_config["medical_conversation_writer"]["backstory"],
            llm=self.llm,
            verbose=True,
            allow_delegation=False,
            max_iter=inputs.get("max_iterations_writer", 15)
        )

        # Compliance Validator
        agents["compliance_validator"] = Agent(
            role=self.agents_config["compliance_validator"]["role"],
            goal=self.agents_config["compliance_validator"]["goal"].format(**inputs),
            backstory=self.agents_config["compliance_validator"]["backstory"],
            llm=self.llm,
            verbose=True,
            allow_delegation=False,
            max_iter=inputs.get("max_iterations_compliance", 10)
        )

        # Podcast Script Generator
        agents["podcast_script_generator"] = Agent(
            role=self.agents_config["podcast_script_generator"]["role"],
            goal=self.agents_config["podcast_script_generator"]["goal"].format(**inputs),
            backstory=self.agents_config["podcast_script_generator"]["backstory"],
            llm=self.llm,
            verbose=True,
            allow_delegation=True,
            max_iter=inputs.get("max_iterations_script", 15)
        )

        # Quality Assurance Reviewer
        agents["quality_assurance_reviewer"] = Agent(
            role=self.agents_config["quality_assurance_reviewer"]["role"],
            goal=self.agents_config["quality_assurance_reviewer"]["goal"].format(**inputs),
            backstory=self.agents_config["quality_assurance_reviewer"]["backstory"],
            llm=self.llm,
            verbose=True,
            allow_delegation=False,
            max_iter=inputs.get("max_iterations_review", 10)
        )

        logger.info(f"Created {len(agents)} agents")
        return agents

    def create_tasks(self, agents: Dict[str, Agent], inputs: Dict[str, Any]) -> List[Task]:
        """
        Create all SwarmCare tasks with guardrails.

        Args:
            agents: Dictionary of agent instances
            inputs: Configuration inputs for tasks

        Returns:
            List of task instances with guardrails
        """
        tasks = []

        # Task 1: Extract Patient Clinical Profile (with guardrails)
        extract_task = Task(
            description=self.tasks_config["extract_patient_clinical_profile"]["description"].format(**inputs),
            expected_output=self.tasks_config["extract_patient_clinical_profile"]["expected_output"],
            agent=agents["medical_knowledge_extractor"],
            guardrail=medical_knowledge_extraction_guardrail,
            guardrail_max_retries=5
        )
        tasks.append(extract_task)

        # Task 2: Synthesize Clinical Case (with guardrails)
        synthesize_task = Task(
            description=self.tasks_config["synthesize_clinical_case_presentation"]["description"].format(**inputs),
            expected_output=self.tasks_config["synthesize_clinical_case_presentation"]["expected_output"],
            agent=agents["patient_case_synthesizer"],
            context=[extract_task],
            guardrail=clinical_case_synthesis_guardrail,
            guardrail_max_retries=5
        )
        tasks.append(synthesize_task)

        # Task 3: Create Doctor-Patient Dialogue (with guardrails)
        dialogue_task = Task(
            description=self.tasks_config["create_doctor_patient_dialogue"]["description"].format(**inputs),
            expected_output=self.tasks_config["create_doctor_patient_dialogue"]["expected_output"],
            agent=agents["medical_conversation_writer"],
            context=[synthesize_task],
            guardrail=medical_dialogue_guardrail,
            guardrail_max_retries=5
        )
        tasks.append(dialogue_task)

        # Task 4: Create Doctor-Doctor Consultation (with guardrails)
        consultation_task = Task(
            description=self.tasks_config["create_doctor_doctor_consultation"]["description"].format(**inputs),
            expected_output=self.tasks_config["create_doctor_doctor_consultation"]["expected_output"],
            agent=agents["medical_conversation_writer"],
            context=[synthesize_task],
            guardrail=medical_dialogue_guardrail,
            guardrail_max_retries=5
        )
        tasks.append(consultation_task)

        # Task 5: Validate Compliance (with guardrails)
        compliance_task = Task(
            description=self.tasks_config["validate_medical_compliance"]["description"].format(**inputs),
            expected_output=self.tasks_config["validate_medical_compliance"]["expected_output"],
            agent=agents["compliance_validator"],
            context=[dialogue_task, consultation_task],
            guardrail=compliance_validation_guardrail,
            guardrail_max_retries=3
        )
        tasks.append(compliance_task)

        # Task 6: Generate Patient Education Podcast Script (with guardrails)
        patient_podcast_task = Task(
            description=self.tasks_config["generate_podcast_script_patient_education"]["description"].format(**inputs),
            expected_output=self.tasks_config["generate_podcast_script_patient_education"]["expected_output"],
            agent=agents["podcast_script_generator"],
            context=[dialogue_task, compliance_task],
            guardrail=podcast_script_guardrail,
            guardrail_max_retries=5
        )
        tasks.append(patient_podcast_task)

        # Task 7: Generate Professional Education Podcast Script (with guardrails)
        professional_podcast_task = Task(
            description=self.tasks_config["generate_podcast_script_professional_education"]["description"].format(**inputs),
            expected_output=self.tasks_config["generate_podcast_script_professional_education"]["expected_output"],
            agent=agents["podcast_script_generator"],
            context=[consultation_task, compliance_task],
            guardrail=podcast_script_guardrail,
            guardrail_max_retries=5
        )
        tasks.append(professional_podcast_task)

        # Task 8: Final Quality Review (with guardrails)
        quality_task = Task(
            description=self.tasks_config["final_quality_review"]["description"].format(**inputs),
            expected_output=self.tasks_config["final_quality_review"]["expected_output"],
            agent=agents["quality_assurance_reviewer"],
            context=[patient_podcast_task, professional_podcast_task],
            guardrail=quality_assurance_guardrail,
            guardrail_max_retries=3
        )
        tasks.append(quality_task)

        logger.info(f"Created {len(tasks)} tasks with guardrails")
        return tasks

    def create_crew(self, inputs: Dict[str, Any]) -> Crew:
        """
        Create complete SwarmCare crew.

        Args:
            inputs: Configuration inputs

        Returns:
            Crew instance ready for execution
        """
        agents_dict = self.create_agents(inputs)
        tasks_list = self.create_tasks(agents_dict, inputs)

        crew = Crew(
            agents=list(agents_dict.values()),
            tasks=tasks_list,
            verbose=True
        )

        logger.info("SwarmCare Crew created successfully with guardrails")
        return crew

    def kickoff(self, inputs: Dict[str, Any]) -> Any:
        """
        Execute the crew with inputs.

        Args:
            inputs: Input parameters for the crew

        Returns:
            Crew execution result
        """
        logger.info("Starting SwarmCare Crew execution with guardrails...")

        try:
            crew = self.create_crew(inputs)
            result = crew.kickoff()

            # Log statistics
            stats = guardrail_system.get_statistics()
            logger.info(f"Guardrail Statistics: {stats}")

            # Generate monitoring report
            report = monitor.generate_report("swarmcare_execution_report.txt")
            logger.info("Monitoring report generated")

            return result

        except Exception as e:
            logger.error(f"Error during crew execution: {e}")
            monitor.log_error("crew_execution", str(e))
            raise


# Example usage
if __name__ == "__main__":
    # Example input configuration
    example_inputs = {
        "patient_identifier": "ANON-001",
        "patient_name": "Anonymous Patient",
        "medical_specialty": "Internal Medicine",
        "medical_domain": "Chronic Disease Management",
        "target_disease_areas": "Diabetes, Hypertension, Cardiovascular Disease",
        "primary_conditions": "Type 2 Diabetes Mellitus, Essential Hypertension",
        "medication_list": "Metformin, Lisinopril, Atorvastatin",
        "device_list": "Continuous Glucose Monitor, Blood Pressure Monitor",
        "care_team_roles": "Primary Care Physician, Endocrinologist, Dietitian",
        "patient_data_source": "Anonymized EHR Knowledge Graph",
        "observation_timeframe": "Last 3 months",
        "care_focus_areas": "Glycemic control, Blood pressure management",
        "genetic_risk_factors": "Family history of diabetes",
        "alert_categories": "Hyperglycemia, Hypertension",
        "data_extraction_method": "FHIR-compliant extraction",
        "knowledge_graph_format": "RDF with medical ontologies",
        "clinical_filtering_criteria": "Evidence-based guidelines",
        "priority_clinical_elements": "Active conditions, medications, vital signs",
        "educational_target": "healthcare provider",
        "provider_type": "Doctor",
        "patient_type": "Patient",
        "communication_type": "clinical consultation",
        "conversation_participants": "physician and patient",
        "clinical_scenario_type": "chronic disease management",
        "regulatory_framework": "HIPAA",
        "healthcare_jurisdiction": "United States",
        "content_purpose": "medical education",
        "podcast_format": "educational medical podcast",
        "target_listener_group": "healthcare professionals and patients",
        "max_iterations_extractor": 15,
        "max_iterations_synthesizer": 15,
        "max_iterations_writer": 15,
        "max_iterations_compliance": 10,
        "max_iterations_script": 15,
        "max_iterations_review": 10,
        "output_format": "structured markdown",
        "content_length_requirement": "comprehensive",
        "clinical_detail_level": "intermediate",
        "file_extension": "md",
        "require_human_validation": False,
        "require_case_review": False,
        "require_dialogue_review": False,
        "require_consultation_review": False,
        "require_compliance_review": False,
        "require_script_review": False,
        "require_professional_review": False,
        "require_final_approval": False
    }

    # Create and run crew
    swarmcare = SwarmCareCrew()
    result = swarmcare.kickoff(example_inputs)

    print("\n" + "=" * 80)
    print("SWARMCARE EXECUTION COMPLETE WITH GUARDRAILS")
    print("=" * 80)
    print(f"\nResult:\n{result}")
    print("\nGuardrail Statistics:")
    print(guardrail_system.get_statistics())
