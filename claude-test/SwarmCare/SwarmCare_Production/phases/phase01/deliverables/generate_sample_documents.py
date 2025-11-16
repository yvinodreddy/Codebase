#!/usr/bin/env python3
"""
SwarmCare Phase 01: Sample Medical Documents Generator
Generates 100+ realistic medical documents for testing and demonstration
Story Points: 60 | Generated: 2025-10-28
"""

import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict
from rag_system import MedicalDocument


def generate_sample_documents() -> List[MedicalDocument]:
    """Generate 100+ comprehensive medical documents across specialties"""

    print("=" * 80)
    print("📚 GENERATING SAMPLE MEDICAL DOCUMENTS")
    print("=" * 80)
    print()

    documents = []

    # ========================================================================
    # Endocrinology Documents (20)
    # ========================================================================
    print("Generating Endocrinology documents...")
    endo_templates = [
        ("Type 2 Diabetes Management", "First-line therapy for type 2 diabetes includes metformin 500mg twice daily with meals. Lifestyle modifications including diet and exercise are essential. Target HbA1c is <7% for most patients. Monitor fasting glucose and HbA1c every 3 months. Screen for complications including retinopathy, nephropathy, and neuropathy annually."),
        ("Hyperthyroidism Treatment", "Graves disease is the most common cause of hyperthyroidism. Treatment options include antithyroid medications (methimazole preferred), radioactive iodine, or thyroidectomy. Beta blockers control symptoms. Monitor TSH and free T4 every 4-6 weeks during treatment."),
        ("Hypothyroidism Protocol", "Primary hypothyroidism requires levothyroxine replacement. Start with 1.6 mcg/kg/day. Check TSH after 6-8 weeks and adjust dose. Target TSH 0.5-2.5 mIU/L. Lifelong treatment required. Take medication on empty stomach."),
        ("Diabetic Ketoacidosis", "DKA requires aggressive IV fluids, insulin infusion, and electrolyte replacement. Check glucose, ketones, and electrolytes hourly. Close gap between anion gap and bicarb. Treat underlying cause. ICU monitoring recommended."),
        ("Hyperlipidemia Management", "Statin therapy reduces cardiovascular risk. Target LDL <100 mg/dL for most, <70 mg/dL for high risk. Atorvastatin 20-40mg daily. Monitor lipid panel every 3 months initially. Check liver enzymes baseline and periodically."),
    ]

    for i, (title, content) in enumerate(endo_templates * 4, 1):
        documents.append(MedicalDocument(
            document_id=f"endo_{i:03d}",
            title=f"{title} - Case {i}",
            content=content + f" Patient case study {i} demonstrates typical presentation and treatment response.",
            document_type="clinical_guideline",
            source="Endocrinology Department",
            metadata={"specialty": "Endocrinology", "category": "guideline", "version": "2024"}
        ))

    # ========================================================================
    # Cardiology Documents (20)
    # ========================================================================
    print("Generating Cardiology documents...")
    cardio_templates = [
        ("Hypertension Management", "Blood pressure goal <130/80 mmHg. First-line agents: ACE inhibitors, ARBs, calcium channel blockers, thiazides. Lifestyle modifications essential. Monitor BP weekly initially. Check electrolytes and renal function. Combination therapy often needed."),
        ("Acute Myocardial Infarction", "STEMI requires immediate reperfusion - primary PCI preferred within 90 minutes. Aspirin 325mg, clopidogrel loading, heparin. Door-to-balloon time critical. Post-MI management includes dual antiplatelet therapy, beta blocker, statin, ACE inhibitor."),
        ("Heart Failure Treatment", "Chronic HFrEF managed with guideline-directed medical therapy: ACE inhibitor/ARB, beta blocker, aldosterone antagonist. Consider ARNI for persistent symptoms. Loop diuretics for volume management. Device therapy if EF <35%."),
        ("Atrial Fibrillation", "Rate control with beta blocker or calcium channel blocker. Anticoagulation based on CHA2DS2-VASc score. Consider rhythm control in symptomatic patients. Catheter ablation option for medication-refractory cases."),
        ("Acute Coronary Syndrome", "Unstable angina or NSTEMI requires dual antiplatelet therapy, anticoagulation, beta blocker, statin. Risk stratification with TIMI or GRACE score. Early invasive strategy if high risk. Cardiac catheterization within 24-72 hours."),
    ]

    for i, (title, content) in enumerate(cardio_templates * 4, 1):
        documents.append(MedicalDocument(
            document_id=f"cardio_{i:03d}",
            title=f"{title} - Protocol {i}",
            content=content + f" Clinical protocol {i} based on current AHA/ACC guidelines.",
            document_type="clinical_protocol",
            source="Cardiology Department",
            metadata={"specialty": "Cardiology", "category": "protocol", "version": "2024"}
        ))

    # ========================================================================
    # Pulmonology Documents (20)
    # ========================================================================
    print("Generating Pulmonology documents...")
    pulm_templates = [
        ("Community-Acquired Pneumonia", "CAP severity assessment with CURB-65 or PSI. Outpatient: amoxicillin or doxycycline. Inpatient: ceftriaxone + azithromycin. Duration 5-7 days. Chest X-ray for diagnosis. Blood cultures if severe."),
        ("Asthma Exacerbation", "Assess severity with peak flow. Oxygen to maintain SpO2 >90%. Albuterol nebulizer every 20 minutes. Systemic corticosteroids prednisone 40-60mg for 5 days. Consider ipratropium if severe. Admit if poor response."),
        ("COPD Management", "Bronchodilators cornerstone of therapy. LABA/LAMA combination for symptomatic patients. Inhaled corticosteroids if frequent exacerbations. Smoking cessation critical. Pulmonary rehabilitation. Oxygen if chronic hypoxemia."),
        ("Pulmonary Embolism", "Wells score risk stratification. D-dimer if low/intermediate risk. CT angiography for diagnosis. Anticoagulation with DOAC or warfarin. Thrombolysis if massive PE with hemodynamic instability. IVC filter rarely indicated."),
        ("Pleural Effusion", "Diagnostic thoracentesis for new effusions. Light's criteria distinguish transudate vs exudate. Treat underlying cause. Therapeutic thoracentesis for symptomatic relief. Chest tube if empyema or hemothorax."),
    ]

    for i, (title, content) in enumerate(pulm_templates * 4, 1):
        documents.append(MedicalDocument(
            document_id=f"pulm_{i:03d}",
            title=f"{title} - Guideline {i}",
            content=content + f" Evidence-based guideline {i} from thoracic society recommendations.",
            document_type="clinical_guideline",
            source="Pulmonology Department",
            metadata={"specialty": "Pulmonology", "category": "guideline", "version": "2024"}
        ))

    # ========================================================================
    # Neurology Documents (20)
    # ========================================================================
    print("Generating Neurology documents...")
    neuro_templates = [
        ("Acute Ischemic Stroke", "Time is brain - door-to-needle <60 minutes. tPA if within 4.5 hours and eligible. Mechanical thrombectomy for large vessel occlusion within 24 hours. Blood pressure management. Aspirin after thrombolysis. Stroke unit care."),
        ("Migraine Treatment", "Acute: triptans or NSAIDs. Preventive if ≥4 headache days/month. Options: topiramate, propranolol, amitriptyline. CGRP antagonists for refractory cases. Identify and avoid triggers. Lifestyle modifications."),
        ("Seizure Management", "First seizure: evaluate with MRI and EEG. Start antiepileptic if high recurrence risk. Levetiracetam or lamotrigine common first-line. Monotherapy preferred. Titrate slowly. Monitor drug levels. Driving restrictions."),
        ("Parkinson Disease", "Carbidopa-levodopa gold standard. Start when symptoms impact quality of life. Dopamine agonists alternative in younger patients. MAO-B inhibitors adjunct therapy. Physical therapy important. Manage motor fluctuations."),
        ("Multiple Sclerosis", "Disease-modifying therapy reduces relapse rate and progression. High-efficacy DMT for active disease. Corticosteroids for acute relapses. Symptom management: spasticity, fatigue, bladder dysfunction. MRI monitoring annually."),
    ]

    for i, (title, content) in enumerate(neuro_templates * 4, 1):
        documents.append(MedicalDocument(
            document_id=f"neuro_{i:03d}",
            title=f"{title} - Clinical Note {i}",
            content=content + f" Neurology clinical note {i} documenting assessment and treatment plan.",
            document_type="clinical_note",
            source="Neurology Department",
            metadata={"specialty": "Neurology", "category": "clinical_note", "version": "2024"}
        ))

    # ========================================================================
    # Gastroenterology Documents (20)
    # ========================================================================
    print("Generating Gastroenterology documents...")
    gi_templates = [
        ("GERD Management", "Lifestyle modifications first-line. PPI therapy for symptomatic relief. Omeprazole 20mg daily before breakfast. Trial off PPI after 8 weeks if asymptomatic. Step-down to H2 blocker. Endoscopy if alarm features."),
        ("Inflammatory Bowel Disease", "Crohn disease: immunosuppression with biologics (anti-TNF) for moderate-severe. Ulcerative colitis: 5-ASA for mild, immunosuppression for moderate. Monitor inflammatory markers. Colonoscopy surveillance. Nutrition support."),
        ("Cirrhosis Complications", "Screen for varices with endoscopy. Beta blockers for primary prophylaxis. Diuretics for ascites (spironolactone + furosemide). Lactulose for hepatic encephalopathy. Avoid nephrotoxins and NSAIDs. HCC screening with ultrasound q6mo."),
        ("Acute Pancreatitis", "NPO initially, aggressive IV fluids 250-500 mL/hr. Pain control. Nutrition within 24-48 hours if tolerated. Avoid antibiotics unless infected necrosis. CT with contrast if severe or not improving. Identify and treat etiology."),
        ("Peptic Ulcer Disease", "Test and treat H. pylori. Triple therapy: PPI + amoxicillin + clarithromycin for 14 days. Confirm eradication with stool antigen. Stop NSAIDs if possible. PPI for NSAID users. Endoscopy for complicated ulcers."),
    ]

    for i, (title, content) in enumerate(gi_templates * 4, 1):
        documents.append(MedicalDocument(
            document_id=f"gi_{i:03d}",
            title=f"{title} - Treatment Plan {i}",
            content=content + f" Gastroenterology treatment plan {i} with evidence-based approach.",
            document_type="treatment_plan",
            source="Gastroenterology Department",
            metadata={"specialty": "Gastroenterology", "category": "treatment_plan", "version": "2024"}
        ))

    print(f"✅ Generated {len(documents)} medical documents")
    print()

    return documents


def save_documents_to_json(documents: List[MedicalDocument], output_path: Path):
    """Save documents to JSON file"""
    documents_dict = [doc.to_dict() for doc in documents]

    with open(output_path, 'w') as f:
        json.dump(documents_dict, f, indent=2)

    print(f"✅ Saved {len(documents)} documents to {output_path}")


def main():
    """Generate and save sample documents"""
    print("\n" + "=" * 80)
    print("SWARMCARE PHASE 01: SAMPLE DOCUMENTS GENERATION")
    print("=" * 80)
    print()

    # Generate documents
    documents = generate_sample_documents()

    # Save to JSON
    output_path = Path("sample_medical_documents.json")
    save_documents_to_json(documents, output_path)

    # Show statistics
    print("\n📊 DOCUMENT STATISTICS")
    print("-" * 80)
    print(f"Total documents: {len(documents)}")

    by_specialty = {}
    by_type = {}

    for doc in documents:
        specialty = doc.metadata.get("specialty", "Unknown")
        by_specialty[specialty] = by_specialty.get(specialty, 0) + 1
        by_type[doc.document_type] = by_type.get(doc.document_type, 0) + 1

    print("\nBy Specialty:")
    for specialty, count in sorted(by_specialty.items()):
        print(f"  {specialty}: {count}")

    print("\nBy Document Type:")
    for doc_type, count in sorted(by_type.items()):
        print(f"  {doc_type}: {count}")

    print("\n" + "=" * 80)
    print("✅ SAMPLE DOCUMENTS GENERATION COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    main()
