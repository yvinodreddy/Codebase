"""
Medical Code Database - Production-Ready
Comprehensive ICD-10 and CPT code mappings for auto-coding system

Phase 15: Advanced Medical NLP & Auto-Coding
"""

import re
import json
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class ICD10Code:
    """ICD-10 diagnosis code"""
    code: str
    description: str
    category: str
    keywords: List[str]
    synonyms: List[str] = None

    def __post_init__(self):
        if self.synonyms is None:
            self.synonyms = []


@dataclass
class CPTCode:
    """CPT procedure code"""
    code: str
    description: str
    category: str
    keywords: List[str]
    modifiers: List[str] = None

    def __post_init__(self):
        if self.modifiers is None:
            self.modifiers = []


class MedicalCodeDatabase:
    """
    Production-ready medical code database
    Supports ICD-10 and CPT coding with comprehensive mappings
    """

    def __init__(self):
        self.icd10_codes = self._initialize_icd10_database()
        self.cpt_codes = self._initialize_cpt_database()
        self._build_search_indices()

    def _initialize_icd10_database(self) -> Dict[str, ICD10Code]:
        """Initialize comprehensive ICD-10 code database"""

        codes = [
            # Endocrinology
            ICD10Code("E11.9", "Type 2 diabetes mellitus without complications", "Endocrine",
                     ["type 2 diabetes", "diabetes mellitus", "t2dm", "dm2", "niddm"],
                     ["adult onset diabetes", "non-insulin dependent diabetes"]),
            ICD10Code("E11.65", "Type 2 diabetes mellitus with hyperglycemia", "Endocrine",
                     ["diabetes hyperglycemia", "elevated glucose", "high blood sugar"]),
            ICD10Code("E11.22", "Type 2 diabetes mellitus with diabetic chronic kidney disease", "Endocrine",
                     ["diabetic nephropathy", "diabetic kidney disease"]),
            ICD10Code("E11.36", "Type 2 diabetes mellitus with diabetic cataract", "Endocrine",
                     ["diabetic cataract", "diabetes eye complications"]),
            ICD10Code("E11.42", "Type 2 diabetes mellitus with diabetic polyneuropathy", "Endocrine",
                     ["diabetic neuropathy", "peripheral neuropathy", "diabetic nerve damage"]),

            ICD10Code("E05.00", "Thyrotoxicosis with diffuse goiter without thyrotoxic crisis", "Endocrine",
                     ["graves disease", "hyperthyroidism", "thyrotoxicosis", "overactive thyroid"],
                     ["graves' disease", "toxic diffuse goiter"]),
            ICD10Code("E05.90", "Thyrotoxicosis, unspecified", "Endocrine",
                     ["hyperthyroidism unspecified", "thyroid overactivity"]),

            ICD10Code("E03.9", "Hypothyroidism, unspecified", "Endocrine",
                     ["hypothyroidism", "underactive thyroid", "low thyroid"],
                     ["myxedema", "thyroid deficiency"]),
            ICD10Code("E03.0", "Congenital hypothyroidism with diffuse goiter", "Endocrine",
                     ["congenital hypothyroidism", "cretinism"]),

            ICD10Code("E10.10", "Type 1 diabetes mellitus with ketoacidosis without coma", "Endocrine",
                     ["diabetic ketoacidosis", "dka", "ketoacidosis"],
                     ["diabetic acidosis", "diabetic coma"]),
            ICD10Code("E10.11", "Type 1 diabetes mellitus with ketoacidosis with coma", "Endocrine",
                     ["dka with coma", "diabetic coma"]),

            ICD10Code("E78.5", "Hyperlipidemia, unspecified", "Endocrine",
                     ["hyperlipidemia", "high cholesterol", "dyslipidemia"],
                     ["elevated lipids", "hypercholesterolemia"]),
            ICD10Code("E78.0", "Pure hypercholesterolemia", "Endocrine",
                     ["hypercholesterolemia", "high ldl", "elevated cholesterol"]),

            # Cardiology
            ICD10Code("I10", "Essential (primary) hypertension", "Cardiovascular",
                     ["hypertension", "high blood pressure", "htn", "elevated bp"],
                     ["essential hypertension", "primary hypertension"]),
            ICD10Code("I11.0", "Hypertensive heart disease with heart failure", "Cardiovascular",
                     ["hypertensive heart disease", "htn heart disease"]),

            ICD10Code("I21.9", "Acute myocardial infarction, unspecified", "Cardiovascular",
                     ["myocardial infarction", "heart attack", "mi", "ami"],
                     ["acute mi", "coronary thrombosis"]),
            ICD10Code("I21.0", "ST elevation (STEMI) myocardial infarction", "Cardiovascular",
                     ["stemi", "st elevation mi", "st elevation myocardial infarction"]),
            ICD10Code("I21.4", "Non-ST elevation (NSTEMI) myocardial infarction", "Cardiovascular",
                     ["nstemi", "non-st elevation mi", "non-stemi"]),

            ICD10Code("I50.9", "Heart failure, unspecified", "Cardiovascular",
                     ["heart failure", "hf", "cardiac failure", "congestive heart failure"],
                     ["chf", "pump failure"]),
            ICD10Code("I50.1", "Left ventricular failure", "Cardiovascular",
                     ["left ventricular failure", "lv failure", "lvf"]),
            ICD10Code("I50.22", "Chronic systolic heart failure", "Cardiovascular",
                     ["systolic heart failure", "hfref", "reduced ejection fraction"]),

            ICD10Code("I48.91", "Unspecified atrial fibrillation", "Cardiovascular",
                     ["atrial fibrillation", "afib", "af", "a fib"],
                     ["auricular fibrillation", "atrial arrhythmia"]),
            ICD10Code("I48.0", "Paroxysmal atrial fibrillation", "Cardiovascular",
                     ["paroxysmal afib", "paroxysmal atrial fibrillation"]),

            ICD10Code("I20.9", "Angina pectoris, unspecified", "Cardiovascular",
                     ["angina", "chest pain", "angina pectoris"],
                     ["cardiac chest pain", "ischemic chest pain"]),
            ICD10Code("I20.0", "Unstable angina", "Cardiovascular",
                     ["unstable angina", "acute coronary syndrome", "acs"]),

            # Pulmonology
            ICD10Code("J18.9", "Pneumonia, unspecified organism", "Respiratory",
                     ["pneumonia", "lung infection", "pulmonary infection"],
                     ["community acquired pneumonia", "cap"]),
            ICD10Code("J18.1", "Lobar pneumonia, unspecified organism", "Respiratory",
                     ["lobar pneumonia", "pneumonia lobar"]),

            ICD10Code("J45.909", "Unspecified asthma, uncomplicated", "Respiratory",
                     ["asthma", "bronchial asthma", "reactive airway"],
                     ["asthmatic bronchitis", "bronchospasm"]),
            ICD10Code("J45.901", "Unspecified asthma with (acute) exacerbation", "Respiratory",
                     ["asthma exacerbation", "asthma attack", "acute asthma"]),

            ICD10Code("J44.9", "Chronic obstructive pulmonary disease, unspecified", "Respiratory",
                     ["copd", "chronic obstructive pulmonary disease", "emphysema"],
                     ["chronic bronchitis", "obstructive lung disease"]),
            ICD10Code("J44.1", "Chronic obstructive pulmonary disease with (acute) exacerbation", "Respiratory",
                     ["copd exacerbation", "acute copd", "copd flare"]),

            ICD10Code("I26.99", "Other pulmonary embolism without acute cor pulmonale", "Respiratory",
                     ["pulmonary embolism", "pe", "lung embolism"],
                     ["pulmonary thromboembolism", "lung clot"]),
            ICD10Code("I26.90", "Septic pulmonary embolism without acute cor pulmonale", "Respiratory",
                     ["septic pulmonary embolism", "septic pe"]),

            ICD10Code("J90", "Pleural effusion, not elsewhere classified", "Respiratory",
                     ["pleural effusion", "fluid in lungs", "pleural fluid"],
                     ["hydrothorax", "lung fluid"]),
            ICD10Code("J91.0", "Malignant pleural effusion", "Respiratory",
                     ["malignant effusion", "cancerous pleural effusion"]),

            # Neurology
            ICD10Code("I63.9", "Cerebral infarction, unspecified", "Neurological",
                     ["stroke", "cerebral infarction", "cva", "brain attack"],
                     ["cerebrovascular accident", "ischemic stroke"]),
            ICD10Code("I63.50", "Cerebral infarction due to unspecified occlusion", "Neurological",
                     ["ischemic stroke", "thrombotic stroke"]),

            ICD10Code("G43.909", "Migraine, unspecified, not intractable, without status migrainosus", "Neurological",
                     ["migraine", "migraine headache", "severe headache"],
                     ["vascular headache", "sick headache"]),
            ICD10Code("G43.109", "Migraine with aura, not intractable, without status migrainosus", "Neurological",
                     ["migraine with aura", "classic migraine"]),

            ICD10Code("G40.909", "Epilepsy, unspecified, not intractable, without status epilepticus", "Neurological",
                     ["epilepsy", "seizure disorder", "convulsions"],
                     ["fits", "seizures"]),
            ICD10Code("R56.9", "Unspecified convulsions", "Neurological",
                     ["seizure", "convulsion", "fit"]),

            ICD10Code("G20", "Parkinson's disease", "Neurological",
                     ["parkinson disease", "parkinson's", "parkinsons", "pd"],
                     ["paralysis agitans", "parkinsonism"]),

            ICD10Code("G35", "Multiple sclerosis", "Neurological",
                     ["multiple sclerosis", "ms", "disseminated sclerosis"],
                     ["demyelinating disease"]),

            # Gastroenterology
            ICD10Code("K21.9", "Gastro-esophageal reflux disease without esophagitis", "Digestive",
                     ["gerd", "acid reflux", "reflux", "heartburn"],
                     ["gastroesophageal reflux", "ger"]),
            ICD10Code("K21.0", "Gastro-esophageal reflux disease with esophagitis", "Digestive",
                     ["gerd with esophagitis", "reflux esophagitis"]),

            ICD10Code("K50.90", "Crohn's disease, unspecified, without complications", "Digestive",
                     ["crohn disease", "crohn's disease", "inflammatory bowel disease"],
                     ["regional enteritis", "ibd"]),
            ICD10Code("K51.90", "Ulcerative colitis, unspecified, without complications", "Digestive",
                     ["ulcerative colitis", "uc", "colitis"]),

            ICD10Code("K70.30", "Alcoholic cirrhosis of liver without ascites", "Digestive",
                     ["cirrhosis", "liver cirrhosis", "hepatic cirrhosis"],
                     ["end stage liver disease", "liver fibrosis"]),
            ICD10Code("K70.31", "Alcoholic cirrhosis of liver with ascites", "Digestive",
                     ["cirrhosis with ascites", "decompensated cirrhosis"]),

            ICD10Code("K85.90", "Acute pancreatitis without necrosis or infection, unspecified", "Digestive",
                     ["acute pancreatitis", "pancreatitis", "inflamed pancreas"],
                     ["pancreas inflammation"]),

            ICD10Code("K27.9", "Peptic ulcer, site unspecified, unspecified as acute or chronic", "Digestive",
                     ["peptic ulcer", "stomach ulcer", "duodenal ulcer"],
                     ["gastric ulcer", "pud"]),
        ]

        return {code.code: code for code in codes}

    def _initialize_cpt_database(self) -> Dict[str, CPTCode]:
        """Initialize comprehensive CPT procedure code database"""

        codes = [
            # Evaluation & Management
            CPTCode("99213", "Office visit, established patient, level 3", "E&M",
                   ["office visit", "outpatient visit", "follow up", "established patient"],
                   ["25"]),
            CPTCode("99214", "Office visit, established patient, level 4", "E&M",
                   ["complex office visit", "detailed visit"],
                   ["25"]),
            CPTCode("99215", "Office visit, established patient, level 5", "E&M",
                   ["comprehensive visit", "high complexity visit"],
                   ["25"]),
            CPTCode("99223", "Initial hospital care, high complexity", "E&M",
                   ["hospital admission", "inpatient admission", "admit"],
                   []),
            CPTCode("99232", "Subsequent hospital care, moderate complexity", "E&M",
                   ["hospital follow up", "inpatient rounding"],
                   []),

            # Cardiology Procedures
            CPTCode("93000", "Electrocardiogram (ECG), complete", "Cardiology",
                   ["ecg", "ekg", "electrocardiogram", "12 lead ecg"],
                   []),
            CPTCode("93306", "Echocardiography, complete", "Cardiology",
                   ["echocardiogram", "echo", "cardiac ultrasound", "transthoracic echo"],
                   []),
            CPTCode("93458", "Cardiac catheterization, left heart", "Cardiology",
                   ["cardiac cath", "heart catheterization", "left heart cath"],
                   []),
            CPTCode("92928", "Percutaneous coronary intervention (PCI)", "Cardiology",
                   ["pci", "angioplasty", "stent placement", "coronary stent"],
                   []),
            CPTCode("33533", "Coronary artery bypass graft (CABG)", "Cardiology",
                   ["cabg", "bypass surgery", "coronary bypass"],
                   []),

            # Pulmonology Procedures
            CPTCode("94010", "Spirometry", "Pulmonology",
                   ["spirometry", "pulmonary function test", "pft", "lung function"],
                   []),
            CPTCode("94640", "Nebulizer treatment", "Pulmonology",
                   ["nebulizer", "breathing treatment", "albuterol nebulizer"],
                   []),
            CPTCode("71020", "Chest X-ray, 2 views", "Pulmonology",
                   ["chest xray", "chest radiograph", "cxr"],
                   []),
            CPTCode("71250", "CT chest without contrast", "Pulmonology",
                   ["chest ct", "ct chest", "chest scan"],
                   []),
            CPTCode("32554", "Thoracentesis", "Pulmonology",
                   ["thoracentesis", "pleural tap", "chest tap"],
                   []),

            # Neurology Procedures
            CPTCode("70450", "CT head without contrast", "Neurology",
                   ["head ct", "ct brain", "brain scan"],
                   []),
            CPTCode("70551", "MRI brain without contrast", "Neurology",
                   ["brain mri", "head mri", "mri brain"],
                   []),
            CPTCode("95816", "Electroencephalogram (EEG)", "Neurology",
                   ["eeg", "brain wave test", "electroencephalogram"],
                   []),
            CPTCode("37195", "Mechanical thrombectomy", "Neurology",
                   ["thrombectomy", "clot removal", "mechanical clot removal"],
                   []),

            # Gastroenterology Procedures
            CPTCode("43235", "Esophagogastroduodenoscopy (EGD)", "Gastroenterology",
                   ["egd", "upper endoscopy", "gastroscopy"],
                   []),
            CPTCode("45378", "Colonoscopy, diagnostic", "Gastroenterology",
                   ["colonoscopy", "colon scope", "lower endoscopy"],
                   []),
            CPTCode("43239", "EGD with biopsy", "Gastroenterology",
                   ["egd with biopsy", "upper endoscopy biopsy"],
                   []),
            CPTCode("76700", "Abdominal ultrasound", "Gastroenterology",
                   ["abdominal ultrasound", "abd us", "belly ultrasound"],
                   []),

            # Laboratory
            CPTCode("83036", "Hemoglobin A1C", "Laboratory",
                   ["a1c", "hba1c", "hemoglobin a1c", "glycated hemoglobin"],
                   []),
            CPTCode("84443", "TSH (thyroid stimulating hormone)", "Laboratory",
                   ["tsh", "thyroid test", "thyroid function"],
                   []),
            CPTCode("80053", "Comprehensive metabolic panel", "Laboratory",
                   ["cmp", "metabolic panel", "chemistry panel"],
                   []),
            CPTCode("85025", "Complete blood count (CBC)", "Laboratory",
                   ["cbc", "complete blood count", "blood count"],
                   []),
            CPTCode("80061", "Lipid panel", "Laboratory",
                   ["lipid panel", "cholesterol test", "lipid profile"],
                   []),

            # Medication Administration
            CPTCode("96372", "Therapeutic injection", "Medication",
                   ["injection", "im injection", "subcutaneous injection"],
                   []),
            CPTCode("96365", "IV infusion", "Medication",
                   ["iv infusion", "intravenous therapy", "iv therapy"],
                   []),
        ]

        return {code.code: code for code in codes}

    def _build_search_indices(self):
        """Build search indices for faster lookups"""
        self.icd10_keyword_index = {}
        self.cpt_keyword_index = {}

        # Build ICD-10 keyword index
        for code_str, icd_code in self.icd10_codes.items():
            all_terms = icd_code.keywords + icd_code.synonyms + [icd_code.description.lower()]
            for term in all_terms:
                term_normalized = term.lower().strip()
                if term_normalized not in self.icd10_keyword_index:
                    self.icd10_keyword_index[term_normalized] = []
                self.icd10_keyword_index[term_normalized].append(code_str)

        # Build CPT keyword index
        for code_str, cpt_code in self.cpt_codes.items():
            all_terms = cpt_code.keywords + [cpt_code.description.lower()]
            for term in all_terms:
                term_normalized = term.lower().strip()
                if term_normalized not in self.cpt_keyword_index:
                    self.cpt_keyword_index[term_normalized] = []
                self.cpt_keyword_index[term_normalized].append(code_str)

    def search_icd10(self, query: str, max_results: int = 10) -> List[Tuple[str, ICD10Code, float]]:
        """
        Search ICD-10 codes by query

        Args:
            query: Search query (diagnosis, symptom, condition)
            max_results: Maximum number of results to return

        Returns:
            List of (code_str, ICD10Code, confidence_score) tuples
        """
        query_lower = query.lower().strip()
        results = []

        # Exact keyword match
        if query_lower in self.icd10_keyword_index:
            for code_str in self.icd10_keyword_index[query_lower]:
                results.append((code_str, self.icd10_codes[code_str], 1.0))

        # Partial keyword match
        for keyword, code_list in self.icd10_keyword_index.items():
            if query_lower in keyword or keyword in query_lower:
                for code_str in code_list:
                    if code_str not in [r[0] for r in results]:
                        confidence = len(query_lower) / max(len(keyword), len(query_lower))
                        results.append((code_str, self.icd10_codes[code_str], confidence * 0.8))

        # Sort by confidence and return top results
        results.sort(key=lambda x: x[2], reverse=True)
        return results[:max_results]

    def search_cpt(self, query: str, max_results: int = 10) -> List[Tuple[str, CPTCode, float]]:
        """
        Search CPT codes by query

        Args:
            query: Search query (procedure, test, treatment)
            max_results: Maximum number of results to return

        Returns:
            List of (code_str, CPTCode, confidence_score) tuples
        """
        query_lower = query.lower().strip()
        results = []

        # Exact keyword match
        if query_lower in self.cpt_keyword_index:
            for code_str in self.cpt_keyword_index[query_lower]:
                results.append((code_str, self.cpt_codes[code_str], 1.0))

        # Partial keyword match
        for keyword, code_list in self.cpt_keyword_index.items():
            if query_lower in keyword or keyword in query_lower:
                for code_str in code_list:
                    if code_str not in [r[0] for r in results]:
                        confidence = len(query_lower) / max(len(keyword), len(query_lower))
                        results.append((code_str, self.cpt_codes[code_str], confidence * 0.8))

        # Sort by confidence and return top results
        results.sort(key=lambda x: x[2], reverse=True)
        return results[:max_results]

    def get_icd10(self, code: str) -> Optional[ICD10Code]:
        """Get ICD-10 code by code string"""
        return self.icd10_codes.get(code)

    def get_cpt(self, code: str) -> Optional[CPTCode]:
        """Get CPT code by code string"""
        return self.cpt_codes.get(code)

    def get_stats(self) -> Dict:
        """Get database statistics"""
        return {
            "total_icd10_codes": len(self.icd10_codes),
            "total_cpt_codes": len(self.cpt_codes),
            "icd10_categories": list(set(c.category for c in self.icd10_codes.values())),
            "cpt_categories": list(set(c.category for c in self.cpt_codes.values())),
            "total_icd10_keywords": len(self.icd10_keyword_index),
            "total_cpt_keywords": len(self.cpt_keyword_index)
        }


if __name__ == "__main__":
    # Test the database
    db = MedicalCodeDatabase()

    print("=" * 80)
    print("MEDICAL CODE DATABASE - PRODUCTION READY")
    print("=" * 80)
    print(json.dumps(db.get_stats(), indent=2))

    print("\n" + "=" * 80)
    print("TESTING ICD-10 SEARCH")
    print("=" * 80)

    test_queries = ["diabetes", "heart attack", "pneumonia", "stroke"]
    for query in test_queries:
        results = db.search_icd10(query, max_results=3)
        print(f"\nQuery: '{query}'")
        for code_str, icd_code, confidence in results:
            print(f"  {code_str}: {icd_code.description} (confidence: {confidence:.2f})")

    print("\n" + "=" * 80)
    print("TESTING CPT SEARCH")
    print("=" * 80)

    test_queries = ["ecg", "colonoscopy", "chest xray", "blood count"]
    for query in test_queries:
        results = db.search_cpt(query, max_results=3)
        print(f"\nQuery: '{query}'")
        for code_str, cpt_code, confidence in results:
            print(f"  {code_str}: {cpt_code.description} (confidence: {confidence:.2f})")
