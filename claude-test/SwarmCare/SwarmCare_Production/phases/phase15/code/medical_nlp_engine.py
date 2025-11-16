"""
Medical NLP Engine - Production-Ready
Advanced NLP with Named Entity Recognition, Relationship Extraction, and Temporal Analysis

Phase 15: Advanced Medical NLP & Auto-Coding
"""

import re
import json
from typing import List, Dict, Tuple, Set, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
from collections import defaultdict


@dataclass
class MedicalEntity:
    """Medical named entity"""
    text: str
    entity_type: str  # disease, medication, procedure, symptom, lab_value, etc.
    start_pos: int
    end_pos: int
    confidence: float = 1.0
    attributes: Dict = None

    def __post_init__(self):
        if self.attributes is None:
            self.attributes = {}


@dataclass
class MedicalRelationship:
    """Relationship between medical entities"""
    entity1: MedicalEntity
    relation_type: str  # treats, causes, indicates, requires, etc.
    entity2: MedicalEntity
    confidence: float = 1.0


@dataclass
class TemporalExpression:
    """Temporal expression in medical text"""
    text: str
    temporal_type: str  # duration, frequency, date, time
    normalized_value: str
    start_pos: int
    end_pos: int


class MedicalNLPEngine:
    """
    Production-ready Medical NLP Engine
    Supports NER, relationship extraction, negation detection, and temporal analysis
    """

    def __init__(self):
        self._initialize_medical_dictionaries()
        self._compile_patterns()

    def _initialize_medical_dictionaries(self):
        """Initialize comprehensive medical term dictionaries"""

        # Diseases and conditions
        self.diseases = {
            "diabetes", "diabetes mellitus", "type 2 diabetes", "type 1 diabetes",
            "hypertension", "high blood pressure",
            "pneumonia", "asthma", "copd", "emphysema",
            "stroke", "cva", "cerebral infarction",
            "myocardial infarction", "heart attack", "mi",
            "heart failure", "chf", "congestive heart failure",
            "atrial fibrillation", "afib", "a-fib",
            "migraine", "seizure", "epilepsy",
            "parkinson disease", "parkinson's disease",
            "multiple sclerosis", "ms",
            "cirrhosis", "liver cirrhosis",
            "gerd", "acid reflux",
            "crohn disease", "ulcerative colitis", "ibd",
            "pancreatitis", "acute pancreatitis",
            "peptic ulcer", "gastric ulcer",
            "hypothyroidism", "hyperthyroidism", "graves disease",
            "dka", "diabetic ketoacidosis",
            "hyperlipidemia", "high cholesterol",
            "angina", "unstable angina",
            "pulmonary embolism", "pe",
            "pleural effusion"
        }

        # Medications
        self.medications = {
            "metformin", "insulin", "glipizide", "glyburide",
            "lisinopril", "losartan", "amlodipine", "hydrochlorothiazide", "furosemide",
            "atorvastatin", "simvastatin", "pravastatin",
            "aspirin", "clopidogrel", "warfarin", "rivaroxaban", "apixaban",
            "levothyroxine", "methimazole",
            "albuterol", "ipratropium", "prednisone", "methylprednisolone",
            "amoxicillin", "azithromycin", "ceftriaxone", "doxycycline",
            "omeprazole", "pantoprazole", "esomeprazole",
            "metoprolol", "carvedilol", "propranolol",
            "spironolactone", "eplerenone",
            "levetiracetam", "lamotrigine", "topiramate",
            "carbidopa-levodopa", "levodopa",
            "triptans", "sumatriptan",
            "lactulose", "rifaximin"
        }

        # Procedures
        self.procedures = {
            "ecg", "ekg", "electrocardiogram",
            "echocardiogram", "echo", "cardiac ultrasound",
            "cardiac catheterization", "cardiac cath",
            "pci", "angioplasty", "stent placement",
            "cabg", "bypass surgery",
            "spirometry", "pulmonary function test", "pft",
            "nebulizer treatment", "breathing treatment",
            "chest xray", "chest x-ray", "cxr",
            "ct scan", "mri", "ultrasound",
            "thoracentesis", "chest tap",
            "thrombectomy", "mechanical thrombectomy",
            "tpa", "thrombolysis",
            "endoscopy", "egd", "colonoscopy",
            "biopsy",
            "blood draw", "venipuncture",
            "iv infusion", "injection"
        }

        # Symptoms
        self.symptoms = {
            "chest pain", "shortness of breath", "dyspnea", "sob",
            "cough", "fever", "chills",
            "nausea", "vomiting", "diarrhea",
            "headache", "dizziness", "lightheadedness",
            "fatigue", "weakness",
            "palpitations", "edema", "swelling",
            "pain", "abdominal pain", "back pain",
            "confusion", "altered mental status",
            "seizure", "convulsion"
        }

        # Lab values and measurements
        self.lab_values = {
            "glucose", "blood sugar", "a1c", "hba1c",
            "tsh", "t4", "t3",
            "blood pressure", "bp",
            "heart rate", "pulse",
            "temperature", "temp",
            "spo2", "oxygen saturation",
            "cholesterol", "ldl", "hdl", "triglycerides",
            "creatinine", "bun", "egfr",
            "hemoglobin", "hematocrit", "wbc", "platelets",
            "sodium", "potassium", "chloride", "bicarbonate",
            "alt", "ast", "bilirubin", "albumin",
            "inr", "pt", "ptt"
        }

        # Anatomical locations
        self.anatomy = {
            "heart", "lung", "lungs", "liver", "kidney", "kidneys",
            "brain", "head", "chest", "abdomen", "stomach",
            "pancreas", "thyroid", "esophagus", "colon",
            "left ventricle", "right ventricle", "atrium",
            "coronary artery", "aorta", "vein", "artery"
        }

    def _compile_patterns(self):
        """Compile regex patterns for entity extraction"""

        # Medication dosage patterns
        self.dosage_pattern = re.compile(
            r'\b(\d+(?:\.\d+)?)\s*(mg|mcg|g|ml|units?|iu)\b',
            re.IGNORECASE
        )

        # Medication frequency patterns
        self.frequency_pattern = re.compile(
            r'\b(once|twice|three times|four times|q\d+h|qid|tid|bid|daily|weekly|monthly)\s*(daily|a day|per day)?\b',
            re.IGNORECASE
        )

        # Vital sign patterns
        self.bp_pattern = re.compile(r'\b(\d{2,3})/(\d{2,3})\s*mmHg\b')
        self.temp_pattern = re.compile(r'\b(\d{2,3}(?:\.\d+)?)\s*(?:°F|°C|degrees?)\b')
        self.hr_pattern = re.compile(r'\bheart rate:?\s*(\d{2,3})\s*(?:bpm|beats)?\b', re.IGNORECASE)

        # Lab value patterns
        self.lab_value_pattern = re.compile(
            r'((?:glucose|a1c|tsh|ldl|hdl|creatinine|hemoglobin|sodium|potassium)[:\s]+)(\d+(?:\.\d+)?)\s*(%|mg/dL|mmol/L|mEq/L)?',
            re.IGNORECASE
        )

        # Negation patterns
        self.negation_patterns = [
            r'\bno\s+',
            r'\bnot\s+',
            r'\bdeny(?:ing|ies)?\s+',
            r'\bdenies\s+',
            r'\bwithout\s+',
            r'\babsence\s+of\s+',
            r'\bfree\s+of\s+',
            r'\brule\s+out\s+',
            r'\br/o\s+'
        ]

        # Temporal patterns
        self.temporal_patterns = {
            'duration': re.compile(r'\b(\d+)\s*(day|week|month|year)s?\b', re.IGNORECASE),
            'frequency': re.compile(r'\bevery\s+(\d+)\s*(hour|day|week)s?\b', re.IGNORECASE),
            'date': re.compile(r'\b(\d{1,2})[/-](\d{1,2})[/-](\d{2,4})\b'),
            'time': re.compile(r'\b(\d{1,2}):(\d{2})\s*(am|pm)?\b', re.IGNORECASE)
        }

    def extract_entities(self, text: str) -> List[MedicalEntity]:
        """
        Extract medical named entities from text

        Args:
            text: Medical text to analyze

        Returns:
            List of extracted MedicalEntity objects
        """
        entities = []
        text_lower = text.lower()

        # Extract diseases
        for disease in sorted(self.diseases, key=len, reverse=True):
            pattern = r'\b' + re.escape(disease) + r'\b'
            for match in re.finditer(pattern, text_lower):
                entities.append(MedicalEntity(
                    text=match.group(),
                    entity_type="disease",
                    start_pos=match.start(),
                    end_pos=match.end(),
                    confidence=1.0
                ))

        # Extract medications
        for medication in sorted(self.medications, key=len, reverse=True):
            pattern = r'\b' + re.escape(medication) + r'\b'
            for match in re.finditer(pattern, text_lower):
                # Check for dosage information
                dosage_match = self.dosage_pattern.search(text, match.end(), match.end() + 20)
                freq_match = self.frequency_pattern.search(text, match.end(), match.end() + 30)

                attributes = {}
                if dosage_match:
                    attributes['dosage'] = dosage_match.group()
                if freq_match:
                    attributes['frequency'] = freq_match.group()

                entities.append(MedicalEntity(
                    text=match.group(),
                    entity_type="medication",
                    start_pos=match.start(),
                    end_pos=match.end(),
                    confidence=1.0,
                    attributes=attributes
                ))

        # Extract procedures
        for procedure in sorted(self.procedures, key=len, reverse=True):
            pattern = r'\b' + re.escape(procedure) + r'\b'
            for match in re.finditer(pattern, text_lower):
                entities.append(MedicalEntity(
                    text=match.group(),
                    entity_type="procedure",
                    start_pos=match.start(),
                    end_pos=match.end(),
                    confidence=1.0
                ))

        # Extract symptoms
        for symptom in sorted(self.symptoms, key=len, reverse=True):
            pattern = r'\b' + re.escape(symptom) + r'\b'
            for match in re.finditer(pattern, text_lower):
                entities.append(MedicalEntity(
                    text=match.group(),
                    entity_type="symptom",
                    start_pos=match.start(),
                    end_pos=match.end(),
                    confidence=1.0
                ))

        # Extract lab values with measurements
        for match in self.lab_value_pattern.finditer(text):
            entities.append(MedicalEntity(
                text=match.group(),
                entity_type="lab_value",
                start_pos=match.start(),
                end_pos=match.end(),
                confidence=1.0,
                attributes={
                    'test': match.group(1).strip().rstrip(':'),
                    'value': match.group(2),
                    'unit': match.group(3) if match.group(3) else ''
                }
            ))

        # Extract vital signs
        for match in self.bp_pattern.finditer(text):
            entities.append(MedicalEntity(
                text=match.group(),
                entity_type="vital_sign",
                start_pos=match.start(),
                end_pos=match.end(),
                confidence=1.0,
                attributes={
                    'type': 'blood_pressure',
                    'systolic': match.group(1),
                    'diastolic': match.group(2)
                }
            ))

        # Remove overlapping entities (keep longer ones)
        entities = self._remove_overlapping_entities(entities)

        return entities

    def _remove_overlapping_entities(self, entities: List[MedicalEntity]) -> List[MedicalEntity]:
        """Remove overlapping entities, keeping longer ones"""
        if not entities:
            return []

        # Sort by start position and length (descending)
        sorted_entities = sorted(entities, key=lambda e: (e.start_pos, -(e.end_pos - e.start_pos)))

        non_overlapping = []
        for entity in sorted_entities:
            # Check if this entity overlaps with any already added entity
            overlaps = False
            for added in non_overlapping:
                if (entity.start_pos < added.end_pos and entity.end_pos > added.start_pos):
                    overlaps = True
                    break

            if not overlaps:
                non_overlapping.append(entity)

        return sorted(non_overlapping, key=lambda e: e.start_pos)

    def detect_negation(self, text: str, entities: List[MedicalEntity]) -> List[MedicalEntity]:
        """
        Detect negation for entities

        Args:
            text: Original text
            entities: List of extracted entities

        Returns:
            Updated entities with negation information
        """
        text_lower = text.lower()

        for entity in entities:
            # Check for negation patterns before the entity
            preceding_text = text_lower[max(0, entity.start_pos - 50):entity.start_pos]

            is_negated = False
            for pattern in self.negation_patterns:
                if re.search(pattern, preceding_text):
                    is_negated = True
                    break

            entity.attributes = entity.attributes or {}
            entity.attributes['negated'] = is_negated

        return entities

    def extract_relationships(self, text: str, entities: List[MedicalEntity]) -> List[MedicalRelationship]:
        """
        Extract relationships between entities

        Args:
            text: Original text
            entities: List of extracted entities

        Returns:
            List of MedicalRelationship objects
        """
        relationships = []
        text_lower = text.lower()

        # Common relationship patterns
        relationship_patterns = {
            'treats': [r'treat', r'therapy', r'management', r'for'],
            'causes': [r'cause', r'due to', r'from', r'secondary to'],
            'indicates': [r'show', r'indicate', r'suggest', r'reveal'],
            'requires': [r'require', r'need', r'indicate']
        }

        # Find medication-disease relationships
        medications = [e for e in entities if e.entity_type == 'medication']
        diseases = [e for e in entities if e.entity_type == 'disease']

        for med in medications:
            for disease in diseases:
                # Check if they're close and have relationship pattern between them
                if abs(med.start_pos - disease.start_pos) < 100:
                    between_text = text_lower[
                        min(med.start_pos, disease.start_pos):max(med.end_pos, disease.end_pos)
                    ]

                    for rel_type, patterns in relationship_patterns.items():
                        for pattern in patterns:
                            if re.search(pattern, between_text):
                                relationships.append(MedicalRelationship(
                                    entity1=med if med.start_pos < disease.start_pos else disease,
                                    relation_type=rel_type,
                                    entity2=disease if med.start_pos < disease.start_pos else med,
                                    confidence=0.8
                                ))
                                break

        return relationships

    def extract_temporal_expressions(self, text: str) -> List[TemporalExpression]:
        """
        Extract temporal expressions from text

        Args:
            text: Medical text

        Returns:
            List of TemporalExpression objects
        """
        temporal_expressions = []

        for temp_type, pattern in self.temporal_patterns.items():
            for match in pattern.finditer(text):
                temporal_expressions.append(TemporalExpression(
                    text=match.group(),
                    temporal_type=temp_type,
                    normalized_value=match.group(),
                    start_pos=match.start(),
                    end_pos=match.end()
                ))

        return temporal_expressions

    def analyze_text(self, text: str) -> Dict:
        """
        Complete NLP analysis of medical text

        Args:
            text: Medical text to analyze

        Returns:
            Dictionary with entities, relationships, and temporal expressions
        """
        # Extract entities
        entities = self.extract_entities(text)

        # Detect negation
        entities = self.detect_negation(text, entities)

        # Extract relationships
        relationships = self.extract_relationships(text, entities)

        # Extract temporal expressions
        temporal_expressions = self.extract_temporal_expressions(text)

        return {
            "text": text,
            "entities": [asdict(e) for e in entities],
            "relationships": [
                {
                    "entity1": asdict(r.entity1),
                    "relation_type": r.relation_type,
                    "entity2": asdict(r.entity2),
                    "confidence": r.confidence
                }
                for r in relationships
            ],
            "temporal_expressions": [asdict(t) for t in temporal_expressions],
            "stats": {
                "total_entities": len(entities),
                "entities_by_type": self._count_entities_by_type(entities),
                "total_relationships": len(relationships),
                "total_temporal_expressions": len(temporal_expressions)
            },
            "analyzed_at": datetime.now().isoformat()
        }

    def _count_entities_by_type(self, entities: List[MedicalEntity]) -> Dict[str, int]:
        """Count entities by type"""
        counts = defaultdict(int)
        for entity in entities:
            counts[entity.entity_type] += 1
        return dict(counts)


if __name__ == "__main__":
    # Test the NLP engine
    nlp = MedicalNLPEngine()

    test_texts = [
        "Patient with type 2 diabetes mellitus on metformin 500mg twice daily. HbA1c is 7.2%. No chest pain or shortness of breath.",
        "Acute myocardial infarction treated with aspirin 325mg and clopidogrel. Cardiac catheterization performed. Blood pressure 140/90 mmHg.",
        "Community-acquired pneumonia. Started on ceftriaxone and azithromycin. Chest X-ray shows right lower lobe infiltrate. Patient denies fever."
    ]

    print("=" * 80)
    print("MEDICAL NLP ENGINE - PRODUCTION READY")
    print("=" * 80)

    for i, text in enumerate(test_texts, 1):
        print(f"\n{'='*80}")
        print(f"TEST {i}: {text[:60]}...")
        print("=" * 80)

        result = nlp.analyze_text(text)

        print(f"\nEntities found: {result['stats']['total_entities']}")
        print(json.dumps(result['stats']['entities_by_type'], indent=2))

        print("\nExtracted Entities:")
        for entity in result['entities'][:10]:  # Show first 10
            negated = " [NEGATED]" if entity.get('attributes', {}).get('negated') else ""
            print(f"  - {entity['entity_type'].upper()}: '{entity['text']}'{negated}")

        if result['relationships']:
            print(f"\nRelationships found: {len(result['relationships'])}")
            for rel in result['relationships'][:5]:  # Show first 5
                print(f"  - {rel['entity1']['text']} --{rel['relation_type']}--> {rel['entity2']['text']}")
