"""
Clinical Note Generator - Production-Ready
Automated generation of SOAP notes, discharge summaries, and progress notes

Phase 15: Advanced Medical NLP & Auto-Coding
"""

import json
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict
from datetime import datetime

from medical_nlp_engine import MedicalNLPEngine, MedicalEntity
from autocoding_system import MedicalAutoCodingSystem, CodingResult


@dataclass
class ClinicalNote:
    """Clinical note structure"""
    note_type: str  # SOAP, discharge_summary, progress_note
    patient_context: Dict
    content: str
    icd10_codes: List[str]
    cpt_codes: List[str]
    generated_at: str = None

    def __post_init__(self):
        if self.generated_at is None:
            self.generated_at = datetime.now().isoformat()


class ClinicalNoteGenerator:
    """
    Production-ready clinical note generator
    Generates structured clinical notes from medical data
    """

    def __init__(self):
        self.nlp_engine = MedicalNLPEngine()
        self.autocoding_system = MedicalAutoCodingSystem()

    def generate_soap_note(self, patient_data: Dict) -> ClinicalNote:
        """
        Generate SOAP (Subjective, Objective, Assessment, Plan) note

        Args:
            patient_data: Dictionary with patient information

        Returns:
            ClinicalNote object
        """
        # Extract information
        chief_complaint = patient_data.get('chief_complaint', '')
        history = patient_data.get('history', '')
        vitals = patient_data.get('vitals', {})
        exam_findings = patient_data.get('exam_findings', '')
        labs = patient_data.get('labs', {})
        assessment = patient_data.get('assessment', '')
        plan = patient_data.get('plan', '')

        # Build SOAP note sections
        soap_sections = []

        # SUBJECTIVE
        subjective = self._build_subjective(chief_complaint, history)
        soap_sections.append(f"SUBJECTIVE:\n{subjective}")

        # OBJECTIVE
        objective = self._build_objective(vitals, exam_findings, labs)
        soap_sections.append(f"\nOBJECTIVE:\n{objective}")

        # ASSESSMENT
        assessment_section = self._build_assessment(assessment)
        soap_sections.append(f"\nASSESSMENT:\n{assessment_section}")

        # PLAN
        plan_section = self._build_plan(plan)
        soap_sections.append(f"\nPLAN:\n{plan_section}")

        # Combine all sections
        note_content = "\n".join(soap_sections)

        # Auto-code the note
        coding_report = self.autocoding_system.code_text(note_content)

        return ClinicalNote(
            note_type="SOAP",
            patient_context=patient_data,
            content=note_content,
            icd10_codes=[c.code for c in coding_report.icd10_codes],
            cpt_codes=[c.code for c in coding_report.cpt_codes]
        )

    def generate_discharge_summary(self, patient_data: Dict) -> ClinicalNote:
        """
        Generate discharge summary

        Args:
            patient_data: Dictionary with patient information

        Returns:
            ClinicalNote object
        """
        # Extract information
        admission_date = patient_data.get('admission_date', 'N/A')
        discharge_date = patient_data.get('discharge_date', 'N/A')
        admission_diagnosis = patient_data.get('admission_diagnosis', '')
        hospital_course = patient_data.get('hospital_course', '')
        procedures = patient_data.get('procedures', [])
        discharge_diagnosis = patient_data.get('discharge_diagnosis', '')
        medications = patient_data.get('medications', [])
        follow_up = patient_data.get('follow_up', '')
        discharge_condition = patient_data.get('discharge_condition', 'Stable')

        # Build discharge summary sections
        sections = []

        # Header
        sections.append("DISCHARGE SUMMARY")
        sections.append("=" * 60)

        # Admission/Discharge dates
        sections.append(f"\nADMISSION DATE: {admission_date}")
        sections.append(f"DISCHARGE DATE: {discharge_date}")

        # Chief Complaint / Admission Diagnosis
        sections.append(f"\nADMISSION DIAGNOSIS:")
        sections.append(f"  {admission_diagnosis}")

        # Hospital Course
        sections.append(f"\nHOSPITAL COURSE:")
        sections.append(f"  {hospital_course}")

        # Procedures Performed
        if procedures:
            sections.append(f"\nPROCEDURES PERFORMED:")
            for proc in procedures:
                sections.append(f"  - {proc}")

        # Discharge Diagnosis
        sections.append(f"\nDISCHARGE DIAGNOSIS:")
        sections.append(f"  {discharge_diagnosis}")

        # Discharge Medications
        if medications:
            sections.append(f"\nDISCHARGE MEDICATIONS:")
            for med in medications:
                sections.append(f"  - {med}")

        # Discharge Condition
        sections.append(f"\nDISCHARGE CONDITION: {discharge_condition}")

        # Follow-up
        sections.append(f"\nFOLLOW-UP:")
        sections.append(f"  {follow_up}")

        # Combine all sections
        note_content = "\n".join(sections)

        # Auto-code the note
        coding_report = self.autocoding_system.code_text(note_content)

        return ClinicalNote(
            note_type="discharge_summary",
            patient_context=patient_data,
            content=note_content,
            icd10_codes=[c.code for c in coding_report.icd10_codes],
            cpt_codes=[c.code for c in coding_report.cpt_codes]
        )

    def generate_progress_note(self, patient_data: Dict) -> ClinicalNote:
        """
        Generate progress note

        Args:
            patient_data: Dictionary with patient information

        Returns:
            ClinicalNote object
        """
        # Extract information
        date = patient_data.get('date', datetime.now().strftime('%Y-%m-%d'))
        interval_history = patient_data.get('interval_history', '')
        vitals = patient_data.get('vitals', {})
        exam = patient_data.get('exam', '')
        labs = patient_data.get('labs', {})
        assessment_plan = patient_data.get('assessment_plan', '')

        # Build progress note sections
        sections = []

        # Header
        sections.append(f"PROGRESS NOTE - {date}")
        sections.append("=" * 60)

        # Interval History
        sections.append(f"\nINTERVAL HISTORY:")
        sections.append(f"  {interval_history}")

        # Vital Signs
        if vitals:
            sections.append(f"\nVITAL SIGNS:")
            for vital, value in vitals.items():
                sections.append(f"  {vital}: {value}")

        # Physical Exam
        sections.append(f"\nPHYSICAL EXAMINATION:")
        sections.append(f"  {exam}")

        # Laboratory Data
        if labs:
            sections.append(f"\nLABORATORY DATA:")
            for test, value in labs.items():
                sections.append(f"  {test}: {value}")

        # Assessment and Plan
        sections.append(f"\nASSESSMENT AND PLAN:")
        sections.append(f"  {assessment_plan}")

        # Combine all sections
        note_content = "\n".join(sections)

        # Auto-code the note
        coding_report = self.autocoding_system.code_text(note_content)

        return ClinicalNote(
            note_type="progress_note",
            patient_context=patient_data,
            content=note_content,
            icd10_codes=[c.code for c in coding_report.icd10_codes],
            cpt_codes=[c.code for c in coding_report.cpt_codes]
        )

    def _build_subjective(self, chief_complaint: str, history: str) -> str:
        """Build subjective section"""
        lines = []

        if chief_complaint:
            lines.append(f"Chief Complaint: {chief_complaint}")
            lines.append("")

        if history:
            lines.append(f"History of Present Illness:")
            lines.append(f"  {history}")

        return "\n".join(lines) if lines else "  No subjective findings documented."

    def _build_objective(self, vitals: Dict, exam_findings: str, labs: Dict) -> str:
        """Build objective section"""
        lines = []

        if vitals:
            lines.append("Vital Signs:")
            for vital, value in vitals.items():
                lines.append(f"  {vital}: {value}")
            lines.append("")

        if exam_findings:
            lines.append("Physical Examination:")
            lines.append(f"  {exam_findings}")
            lines.append("")

        if labs:
            lines.append("Laboratory Results:")
            for test, value in labs.items():
                lines.append(f"  {test}: {value}")

        return "\n".join(lines) if lines else "  No objective findings documented."

    def _build_assessment(self, assessment: str) -> str:
        """Build assessment section"""
        if assessment:
            # Parse out individual diagnoses
            diagnoses = [d.strip() for d in assessment.split(';') if d.strip()]

            if len(diagnoses) > 1:
                lines = []
                for i, diag in enumerate(diagnoses, 1):
                    lines.append(f"  {i}. {diag}")
                return "\n".join(lines)
            else:
                return f"  {assessment}"

        return "  No assessment documented."

    def _build_plan(self, plan: str) -> str:
        """Build plan section"""
        if plan:
            # Parse out individual plan items
            plan_items = [p.strip() for p in plan.split(';') if p.strip()]

            if len(plan_items) > 1:
                lines = []
                for i, item in enumerate(plan_items, 1):
                    lines.append(f"  {i}. {item}")
                return "\n".join(lines)
            else:
                return f"  {plan}"

        return "  No plan documented."

    def extract_note_from_text(self, clinical_text: str, note_type: str = "SOAP") -> ClinicalNote:
        """
        Extract structured note from unstructured clinical text

        Args:
            clinical_text: Unstructured clinical text
            note_type: Type of note to generate

        Returns:
            ClinicalNote object
        """
        # Analyze the text with NLP
        nlp_results = self.nlp_engine.analyze_text(clinical_text)

        # Auto-code the text
        coding_report = self.autocoding_system.code_text(clinical_text)

        # Create a basic structured note
        sections = []
        sections.append(f"{note_type.upper()} NOTE")
        sections.append("=" * 60)
        sections.append(f"\nCLINICAL TEXT:")
        sections.append(f"  {clinical_text}")

        if coding_report.icd10_codes:
            sections.append(f"\nDIAGNOSIS CODES:")
            for code in coding_report.icd10_codes:
                sections.append(f"  - {code.code}: {code.description}")

        if coding_report.cpt_codes:
            sections.append(f"\nPROCEDURE CODES:")
            for code in coding_report.cpt_codes:
                sections.append(f"  - {code.code}: {code.description}")

        note_content = "\n".join(sections)

        return ClinicalNote(
            note_type=note_type,
            patient_context={"original_text": clinical_text},
            content=note_content,
            icd10_codes=[c.code for c in coding_report.icd10_codes],
            cpt_codes=[c.code for c in coding_report.cpt_codes]
        )


if __name__ == "__main__":
    # Test the clinical note generator
    generator = ClinicalNoteGenerator()

    print("=" * 80)
    print("CLINICAL NOTE GENERATOR - PRODUCTION READY")
    print("=" * 80)

    # Test Case 1: SOAP Note
    print("\n" + "=" * 80)
    print("TEST 1: SOAP NOTE GENERATION")
    print("=" * 80)

    soap_data = {
        "chief_complaint": "Chest pain",
        "history": "68-year-old male with sudden onset chest pain radiating to left arm, associated with diaphoresis. Pain started 2 hours ago. History of hypertension and hyperlipidemia.",
        "vitals": {
            "BP": "145/92 mmHg",
            "HR": "95 bpm",
            "Temp": "98.6°F",
            "SpO2": "97% on room air"
        },
        "exam_findings": "Anxious appearing. Cardiovascular: Regular rate and rhythm, no murmurs. Lungs: Clear to auscultation bilaterally. No peripheral edema.",
        "labs": {
            "Troponin": "0.5 ng/mL (elevated)",
            "ECG": "ST elevations in leads II, III, aVF"
        },
        "assessment": "Acute ST-elevation myocardial infarction (STEMI), inferior wall; Hypertension; Hyperlipidemia",
        "plan": "Activate cath lab for emergent PCI; Aspirin 325mg, Clopidogrel 600mg load; Heparin IV; Serial troponins; Admit to CCU; Cardiology consult"
    }

    soap_note = generator.generate_soap_note(soap_data)
    print(soap_note.content)
    print(f"\nICD-10 Codes: {', '.join(soap_note.icd10_codes)}")
    print(f"CPT Codes: {', '.join(soap_note.cpt_codes)}")

    # Test Case 2: Discharge Summary
    print("\n" + "=" * 80)
    print("TEST 2: DISCHARGE SUMMARY GENERATION")
    print("=" * 80)

    discharge_data = {
        "admission_date": "2025-10-28",
        "discharge_date": "2025-10-31",
        "admission_diagnosis": "Community-acquired pneumonia",
        "hospital_course": "Patient admitted with fever, cough, and shortness of breath. Chest X-ray confirmed right lower lobe pneumonia. Treated with IV ceftriaxone and azithromycin. Patient improved with antibiotics, fever resolved, oxygen saturation normalized.",
        "procedures": [
            "Chest X-ray",
            "Blood cultures",
            "Sputum culture"
        ],
        "discharge_diagnosis": "Community-acquired pneumonia, resolved",
        "medications": [
            "Amoxicillin 500mg PO TID x 5 days",
            "Albuterol inhaler 2 puffs q4-6h PRN"
        ],
        "discharge_condition": "Stable, afebrile, oxygen saturation 95% on room air",
        "follow_up": "Follow up with primary care physician in 1 week. Repeat chest X-ray in 6 weeks to confirm resolution."
    }

    discharge_note = generator.generate_discharge_summary(discharge_data)
    print(discharge_note.content)
    print(f"\nICD-10 Codes: {', '.join(discharge_note.icd10_codes)}")
    print(f"CPT Codes: {', '.join(discharge_note.cpt_codes)}")

    # Test Case 3: Progress Note
    print("\n" + "=" * 80)
    print("TEST 3: PROGRESS NOTE GENERATION")
    print("=" * 80)

    progress_data = {
        "date": "2025-10-31",
        "interval_history": "Patient continues on insulin drip. Blood sugars improving. Patient reports decreased nausea, taking oral fluids.",
        "vitals": {
            "BP": "128/76 mmHg",
            "HR": "82 bpm",
            "Temp": "98.2°F"
        },
        "exam": "Alert and oriented. No acute distress. Cardiovascular and pulmonary exam normal.",
        "labs": {
            "Glucose": "145 mg/dL",
            "Anion gap": "12 (normalized)",
            "Ketones": "Small (improved)"
        },
        "assessment_plan": "Diabetic ketoacidosis resolving. Continue insulin drip. Transition to subcutaneous insulin when anion gap normalizes and patient tolerating PO. Diabetes education prior to discharge."
    }

    progress_note = generator.generate_progress_note(progress_data)
    print(progress_note.content)
    print(f"\nICD-10 Codes: {', '.join(progress_note.icd10_codes)}")
    print(f"CPT Codes: {', '.join(progress_note.cpt_codes)}")

    # Test Case 4: Extract from unstructured text
    print("\n" + "=" * 80)
    print("TEST 4: EXTRACT NOTE FROM UNSTRUCTURED TEXT")
    print("=" * 80)

    unstructured_text = "Patient with type 2 diabetes and hypertension presents for routine follow-up. Blood pressure today 132/84. A1C is 7.1%, improved from 8.2% three months ago. Continue metformin and lisinopril. Increase atorvastatin to 40mg for LDL of 145. Return in 3 months."

    extracted_note = generator.extract_note_from_text(unstructured_text, "SOAP")
    print(extracted_note.content)
    print(f"\nICD-10 Codes: {', '.join(extracted_note.icd10_codes)}")
    print(f"CPT Codes: {', '.join(extracted_note.cpt_codes)}")

    print("\n" + "=" * 80)
    print("CLINICAL NOTE GENERATION COMPLETE")
    print("=" * 80)
