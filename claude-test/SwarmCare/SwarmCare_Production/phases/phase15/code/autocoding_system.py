"""
Medical Auto-Coding System - Production-Ready
Automated ICD-10 and CPT coding using NLP and pattern matching

Phase 15: Advanced Medical NLP & Auto-Coding
"""

import json
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
from collections import defaultdict

from medical_code_database import MedicalCodeDatabase, ICD10Code, CPTCode
from medical_nlp_engine import MedicalNLPEngine, MedicalEntity


@dataclass
class CodingResult:
    """Result from auto-coding"""
    code: str
    code_type: str  # ICD10 or CPT
    description: str
    confidence: float
    supporting_evidence: List[str]
    category: str


@dataclass
class AutoCodingReport:
    """Complete auto-coding report"""
    text: str
    icd10_codes: List[CodingResult]
    cpt_codes: List[CodingResult]
    entities_analyzed: int
    total_codes: int
    confidence_score: float
    warnings: List[str]
    timestamp: str = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now().isoformat()


class MedicalAutoCodingSystem:
    """
    Production-ready medical auto-coding system
    Combines NLP entity extraction with medical code databases
    """

    def __init__(self):
        self.code_db = MedicalCodeDatabase()
        self.nlp_engine = MedicalNLPEngine()
        self.min_confidence_threshold = 0.6

    def code_text(self, clinical_text: str) -> AutoCodingReport:
        """
        Auto-code clinical text

        Args:
            clinical_text: Clinical text to code

        Returns:
            AutoCodingReport with ICD-10 and CPT codes
        """
        # Step 1: NLP analysis
        nlp_results = self.nlp_engine.analyze_text(clinical_text)
        entities = [MedicalEntity(**e) for e in nlp_results['entities']]

        # Step 2: Extract ICD-10 codes (diagnosis codes)
        icd10_codes = self._extract_icd10_codes(clinical_text, entities)

        # Step 3: Extract CPT codes (procedure codes)
        cpt_codes = self._extract_cpt_codes(clinical_text, entities)

        # Step 4: Calculate overall confidence
        all_codes = icd10_codes + cpt_codes
        if all_codes:
            confidence_score = sum(c.confidence for c in all_codes) / len(all_codes)
        else:
            confidence_score = 0.0

        # Step 5: Generate warnings
        warnings = self._generate_warnings(clinical_text, icd10_codes, cpt_codes, entities)

        return AutoCodingReport(
            text=clinical_text,
            icd10_codes=icd10_codes,
            cpt_codes=cpt_codes,
            entities_analyzed=len(entities),
            total_codes=len(all_codes),
            confidence_score=confidence_score,
            warnings=warnings
        )

    def _extract_icd10_codes(self, text: str, entities: List[MedicalEntity]) -> List[CodingResult]:
        """Extract ICD-10 diagnosis codes"""
        icd10_codes = []
        text_lower = text.lower()

        # Get disease entities (non-negated)
        diseases = [
            e for e in entities
            if e.entity_type == 'disease' and not e.attributes.get('negated', False)
        ]

        # Code each disease
        for disease in diseases:
            search_results = self.code_db.search_icd10(disease.text, max_results=3)

            for code_str, icd_code, confidence in search_results:
                if confidence >= self.min_confidence_threshold:
                    # Check for complications or specific variants
                    adjusted_confidence, specific_code = self._check_icd10_variants(
                        text_lower, disease, code_str, icd_code
                    )

                    if specific_code:
                        code_str = specific_code
                        icd_code = self.code_db.get_icd10(specific_code)
                        confidence = adjusted_confidence

                    icd10_codes.append(CodingResult(
                        code=code_str,
                        code_type='ICD10',
                        description=icd_code.description,
                        confidence=confidence * disease.confidence,
                        supporting_evidence=[disease.text],
                        category=icd_code.category
                    ))
                    break  # Take best match only

        # Also check for direct ICD-10 mentions in text
        icd10_codes.extend(self._extract_explicit_icd10_codes(text))

        # Remove duplicates
        icd10_codes = self._remove_duplicate_codes(icd10_codes)

        return sorted(icd10_codes, key=lambda x: x.confidence, reverse=True)

    def _check_icd10_variants(self, text: str, disease: MedicalEntity,
                              code: str, icd_code: ICD10Code) -> Tuple[float, Optional[str]]:
        """Check for specific ICD-10 variants based on context"""

        # Diabetes variants
        if "diabetes" in disease.text.lower():
            if "hyperglycemia" in text or "high blood sugar" in text:
                return (0.95, "E11.65")  # with hyperglycemia
            elif "kidney" in text or "nephropathy" in text or "renal" in text:
                return (0.95, "E11.22")  # with kidney disease
            elif "neuropathy" in text or "peripheral nerve" in text:
                return (0.95, "E11.42")  # with neuropathy
            elif "ketoacidosis" in text or "dka" in text:
                return (0.95, "E10.10")  # Type 1 with DKA

        # MI variants
        if "myocardial infarction" in disease.text.lower() or "heart attack" in disease.text.lower():
            if "stemi" in text or "st elevation" in text:
                return (0.95, "I21.0")  # STEMI
            elif "nstemi" in text or "non-st elevation" in text:
                return (0.95, "I21.4")  # NSTEMI

        # Heart failure variants
        if "heart failure" in disease.text.lower():
            if "systolic" in text or "reduced ejection" in text or "hfref" in text:
                return (0.95, "I50.22")  # Systolic HF
            elif "left ventricular" in text or "lv failure" in text:
                return (0.95, "I50.1")  # LV failure

        # Asthma variants
        if "asthma" in disease.text.lower():
            if "exacerbation" in text or "attack" in text or "acute" in text:
                return (0.95, "J45.901")  # with exacerbation

        # COPD variants
        if "copd" in disease.text.lower():
            if "exacerbation" in text or "acute" in text or "flare" in text:
                return (0.95, "J44.1")  # with exacerbation

        # Migraine variants
        if "migraine" in disease.text.lower():
            if "aura" in text or "classic migraine" in text:
                return (0.95, "G43.109")  # with aura

        # GERD variants
        if "gerd" in disease.text.lower() or "reflux" in disease.text.lower():
            if "esophagitis" in text or "erosive" in text:
                return (0.95, "K21.0")  # with esophagitis

        return (1.0, None)  # No specific variant found

    def _extract_explicit_icd10_codes(self, text: str) -> List[CodingResult]:
        """Extract explicitly mentioned ICD-10 codes"""
        import re
        codes = []

        # Pattern for ICD-10 codes (e.g., E11.9, I10, J45.909)
        pattern = r'\b([A-Z]\d{2}(?:\.\d{1,4})?)\b'

        for match in re.finditer(pattern, text):
            code_str = match.group(1)
            icd_code = self.code_db.get_icd10(code_str)

            if icd_code:
                codes.append(CodingResult(
                    code=code_str,
                    code_type='ICD10',
                    description=icd_code.description,
                    confidence=1.0,  # Explicit mention = high confidence
                    supporting_evidence=[f"Explicitly mentioned: {code_str}"],
                    category=icd_code.category
                ))

        return codes

    def _extract_cpt_codes(self, text: str, entities: List[MedicalEntity]) -> List[CodingResult]:
        """Extract CPT procedure codes"""
        cpt_codes = []
        text_lower = text.lower()

        # Get procedure entities
        procedures = [e for e in entities if e.entity_type == 'procedure']

        # Code each procedure
        for procedure in procedures:
            search_results = self.code_db.search_cpt(procedure.text, max_results=3)

            for code_str, cpt_code, confidence in search_results:
                if confidence >= self.min_confidence_threshold:
                    cpt_codes.append(CodingResult(
                        code=code_str,
                        code_type='CPT',
                        description=cpt_code.description,
                        confidence=confidence * procedure.confidence,
                        supporting_evidence=[procedure.text],
                        category=cpt_code.category
                    ))
                    break  # Take best match only

        # Add E&M codes based on visit context
        em_code = self._infer_em_code(text_lower, entities)
        if em_code:
            cpt_codes.append(em_code)

        # Also check for explicit CPT mentions
        cpt_codes.extend(self._extract_explicit_cpt_codes(text))

        # Remove duplicates
        cpt_codes = self._remove_duplicate_codes(cpt_codes)

        return sorted(cpt_codes, key=lambda x: x.confidence, reverse=True)

    def _infer_em_code(self, text: str, entities: List[MedicalEntity]) -> Optional[CodingResult]:
        """Infer E&M code based on context"""

        # Check for admission/hospitalization
        if any(keyword in text for keyword in ['admitted', 'admission', 'hospitalized', 'inpatient']):
            return CodingResult(
                code='99223',
                code_type='CPT',
                description='Initial hospital care, high complexity',
                confidence=0.85,
                supporting_evidence=['Admission context detected'],
                category='E&M'
            )

        # Check for follow-up visit
        if any(keyword in text for keyword in ['follow up', 'office visit', 'outpatient']):
            # Determine complexity based on number of entities
            complexity = len(entities)
            if complexity >= 10:
                code = '99215'
                desc = 'Office visit, established patient, level 5'
            elif complexity >= 5:
                code = '99214'
                desc = 'Office visit, established patient, level 4'
            else:
                code = '99213'
                desc = 'Office visit, established patient, level 3'

            return CodingResult(
                code=code,
                code_type='CPT',
                description=desc,
                confidence=0.75,
                supporting_evidence=[f'Office visit context, {complexity} clinical findings'],
                category='E&M'
            )

        return None

    def _extract_explicit_cpt_codes(self, text: str) -> List[CodingResult]:
        """Extract explicitly mentioned CPT codes"""
        import re
        codes = []

        # Pattern for CPT codes (5-digit)
        pattern = r'\b(\d{5})\b'

        for match in re.finditer(pattern, text):
            code_str = match.group(1)
            cpt_code = self.code_db.get_cpt(code_str)

            if cpt_code:
                codes.append(CodingResult(
                    code=code_str,
                    code_type='CPT',
                    description=cpt_code.description,
                    confidence=1.0,
                    supporting_evidence=[f"Explicitly mentioned: {code_str}"],
                    category=cpt_code.category
                ))

        return codes

    def _remove_duplicate_codes(self, codes: List[CodingResult]) -> List[CodingResult]:
        """Remove duplicate codes, keeping highest confidence"""
        seen_codes = {}

        for code in codes:
            if code.code not in seen_codes or code.confidence > seen_codes[code.code].confidence:
                seen_codes[code.code] = code

        return list(seen_codes.values())

    def _generate_warnings(self, text: str, icd10_codes: List[CodingResult],
                          cpt_codes: List[CodingResult], entities: List[MedicalEntity]) -> List[str]:
        """Generate warnings for coding review"""
        warnings = []

        # Warning: No codes found
        if not icd10_codes and not cpt_codes:
            warnings.append("No medical codes could be extracted. Review text for clinical content.")

        # Warning: Low confidence codes
        low_conf_codes = [c for c in (icd10_codes + cpt_codes) if c.confidence < 0.7]
        if low_conf_codes:
            warnings.append(f"{len(low_conf_codes)} codes have confidence <70%. Manual review recommended.")

        # Warning: Negated entities found
        negated_entities = [e for e in entities if e.attributes.get('negated')]
        if negated_entities:
            warnings.append(f"{len(negated_entities)} negated findings detected. Verify codes exclude these.")

        # Warning: Multiple diseases but no procedures
        diseases = [e for e in entities if e.entity_type == 'disease']
        procedures = [e for e in entities if e.entity_type == 'procedure']
        if len(diseases) > 2 and len(procedures) == 0:
            warnings.append("Multiple diagnoses without documented procedures. Consider adding procedure codes.")

        # Warning: Medications without diseases
        medications = [e for e in entities if e.entity_type == 'medication']
        if medications and not diseases:
            warnings.append("Medications documented without diagnoses. Verify all diagnoses are captured.")

        return warnings


if __name__ == "__main__":
    # Test the auto-coding system
    system = MedicalAutoCodingSystem()

    test_cases = [
        {
            "name": "Type 2 Diabetes Case",
            "text": "Patient with type 2 diabetes mellitus on metformin 500mg twice daily. HbA1c is 7.2%. No complications. Office visit for diabetes management."
        },
        {
            "name": "Acute MI Case",
            "text": "STEMI myocardial infarction. Patient admitted to CCU. Cardiac catheterization with PCI and stent placement to LAD. Started on aspirin, clopidogrel, atorvastatin, and metoprolol."
        },
        {
            "name": "Pneumonia Case",
            "text": "Community-acquired pneumonia confirmed with chest X-ray showing right lower lobe infiltrate. Started on ceftriaxone and azithromycin. CBC and CMP ordered."
        },
        {
            "name": "Multiple Conditions",
            "text": "Patient with hypertension, type 2 diabetes with diabetic neuropathy, and hyperlipidemia. Blood pressure 145/92. A1C 8.1%. LDL 145. Adjusted lisinopril and atorvastatin. Office visit level 4."
        }
    ]

    print("=" * 80)
    print("MEDICAL AUTO-CODING SYSTEM - PRODUCTION READY")
    print("=" * 80)

    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{'='*80}")
        print(f"TEST CASE {i}: {test_case['name']}")
        print("=" * 80)
        print(f"Text: {test_case['text']}")
        print()

        report = system.code_text(test_case['text'])

        print(f"RESULTS:")
        print(f"  Entities Analyzed: {report.entities_analyzed}")
        print(f"  Total Codes: {report.total_codes}")
        print(f"  Overall Confidence: {report.confidence_score:.1%}")

        if report.icd10_codes:
            print(f"\n  ICD-10 CODES ({len(report.icd10_codes)}):")
            for code in report.icd10_codes:
                print(f"    {code.code}: {code.description}")
                print(f"             Confidence: {code.confidence:.1%} | Evidence: {', '.join(code.supporting_evidence)}")

        if report.cpt_codes:
            print(f"\n  CPT CODES ({len(report.cpt_codes)}):")
            for code in report.cpt_codes:
                print(f"    {code.code}: {code.description}")
                print(f"             Confidence: {code.confidence:.1%} | Evidence: {', '.join(code.supporting_evidence)}")

        if report.warnings:
            print(f"\n  WARNINGS ({len(report.warnings)}):")
            for warning in report.warnings:
                print(f"    ⚠️  {warning}")

    print("\n" + "=" * 80)
    print("AUTO-CODING COMPLETE")
    print("=" * 80)
