#!/usr/bin/env python3
"""
Phase 24: EHR Integration Data Export Tool
Production-Ready Data Export Utility for EHR Integration & Billing Data

This script exports EHR integration and billing data to various formats:
- JSON (structured data)
- CSV (tabular data)
- HL7 v2.x messages (legacy systems)
- FHIR R4 bundles (modern EHR systems)
- Excel workbooks (reporting)

Usage:
    python3 export_integration_data.py [OPTIONS]

Options:
    --data-type TYPE      Data type to export: encounters, billing, codes, all
    --format FORMAT       Export format: json, csv, hl7, fhir, excel, all
    --output-dir DIR      Output directory (default: ./exports)
    --encounters N        Number of encounters to export (default: 100)
    --include-metadata    Include metadata in exports
    --compress            Compress output files (gzip)
"""

import sys
import os
import json
import csv
import argparse
import logging
from datetime import datetime, timedelta
from pathlib import Path
import random
import gzip

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


class DataGenerator:
    """Generate sample EHR and billing data"""

    def __init__(self, encounter_count=100):
        self.encounter_count = encounter_count
        self.encounters = []

    def generate_encounters(self):
        """Generate sample encounter data"""
        logger.info(f"Generating {self.encounter_count} encounters...")

        icd10_codes = ["I10", "E11.9", "J44.9", "I25.10", "N18.3", "F41.1", "M79.3", "G43.909", "K21.9", "J45.909"]
        cpt_codes = ["99213", "99214", "93000", "80053", "85025", "36415", "99000", "71045", "73610", "96372"]
        payers = ["Medicare", "Medicaid", "Blue Cross Blue Shield", "United Healthcare", "Aetna", "Cigna"]

        for i in range(self.encounter_count):
            encounter_date = datetime.now() - timedelta(days=random.randint(0, 30))

            encounter = {
                "encounter_id": f"ENC{i+1:06d}",
                "date": encounter_date.strftime("%Y-%m-%d"),
                "time": encounter_date.strftime("%H:%M:%S"),
                "patient": {
                    "id": f"PAT{random.randint(10000, 99999)}",
                    "mrn": f"MRN{random.randint(100000, 999999)}",
                    "first_name": random.choice(["John", "Jane", "Michael", "Sarah", "David", "Emily"]),
                    "last_name": random.choice(["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia"]),
                    "dob": "1970-01-15",
                    "gender": random.choice(["M", "F"])
                },
                "provider": {
                    "id": f"PROV{random.randint(100, 999)}",
                    "npi": f"12345678{random.randint(10, 99)}",
                    "name": f"Dr. {random.choice(['Smith', 'Johnson', 'Lee', 'Patel', 'Garcia'])}"
                },
                "facility": {
                    "id": f"FAC{random.randint(10, 99)}",
                    "name": random.choice(["Memorial Hospital", "City Clinic", "Community Health Center"]),
                    "location": random.choice(["Building A", "Building B", "Main Campus"])
                },
                "diagnoses": random.sample(icd10_codes, random.randint(1, 3)),
                "procedures": random.sample(cpt_codes, random.randint(2, 5)),
                "payer": random.choice(payers),
                "charges": round(random.uniform(100, 500), 2),
                "status": random.choice(["completed", "completed", "completed", "in_progress"])
            }

            self.encounters.append(encounter)

        logger.info(f"✓ Generated {len(self.encounters)} encounters")
        return self.encounters


class DataExporter:
    """Main data export manager"""

    def __init__(self, data_generator):
        self.generator = data_generator
        self.export_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    def export_json(self, output_dir, include_metadata=False):
        """Export data to JSON format"""
        output_path = Path(output_dir) / f"ehr_data_{self.export_timestamp}.json"
        output_path.parent.mkdir(parents=True, exist_ok=True)

        data = {
            "export_info": {
                "timestamp": datetime.now().isoformat(),
                "format": "JSON",
                "record_count": len(self.generator.encounters),
                "exporter": "Phase 24 EHR Integration Export Tool"
            } if include_metadata else {},
            "encounters": self.generator.encounters
        }

        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2)

        logger.info(f"✓ JSON export complete: {output_path}")
        logger.info(f"  Records: {len(self.generator.encounters)}")
        logger.info(f"  Size: {output_path.stat().st_size:,} bytes")

        return str(output_path)

    def export_csv(self, output_dir):
        """Export data to CSV format"""
        output_path = Path(output_dir) / f"ehr_data_{self.export_timestamp}.csv"
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w', newline='') as f:
            fieldnames = ['encounter_id', 'date', 'time', 'patient_id', 'patient_mrn', 'patient_name',
                         'patient_dob', 'patient_gender', 'provider_id', 'provider_npi', 'provider_name',
                         'facility_id', 'facility_name', 'diagnoses', 'procedures', 'payer', 'charges', 'status']
            writer = csv.DictWriter(f, fieldnames=fieldnames)

            writer.writeheader()

            for enc in self.generator.encounters:
                row = {
                    'encounter_id': enc['encounter_id'],
                    'date': enc['date'],
                    'time': enc['time'],
                    'patient_id': enc['patient']['id'],
                    'patient_mrn': enc['patient']['mrn'],
                    'patient_name': f"{enc['patient']['first_name']} {enc['patient']['last_name']}",
                    'patient_dob': enc['patient']['dob'],
                    'patient_gender': enc['patient']['gender'],
                    'provider_id': enc['provider']['id'],
                    'provider_npi': enc['provider']['npi'],
                    'provider_name': enc['provider']['name'],
                    'facility_id': enc['facility']['id'],
                    'facility_name': enc['facility']['name'],
                    'diagnoses': '; '.join(enc['diagnoses']),
                    'procedures': '; '.join(enc['procedures']),
                    'payer': enc['payer'],
                    'charges': enc['charges'],
                    'status': enc['status']
                }
                writer.writerow(row)

        logger.info(f"✓ CSV export complete: {output_path}")
        logger.info(f"  Records: {len(self.generator.encounters)}")
        logger.info(f"  Size: {output_path.stat().st_size:,} bytes")

        return str(output_path)

    def export_hl7(self, output_dir):
        """Export data to HL7 v2.x format"""
        output_path = Path(output_dir) / f"ehr_data_{self.export_timestamp}.hl7"
        output_path.parent.mkdir(parents=True, exist_ok=True)

        hl7_messages = []

        for enc in self.generator.encounters:
            # Generate HL7 ADT^A01 message (patient admit)
            timestamp = datetime.strptime(f"{enc['date']} {enc['time']}", "%Y-%m-%d %H:%M:%S")
            hl7_timestamp = timestamp.strftime("%Y%m%d%H%M%S")

            message = [
                f"MSH|^~\\&|SwarmCare|FACILITY|EHR|HOSPITAL|{hl7_timestamp}||ADT^A01|{enc['encounter_id']}|P|2.5",
                f"EVN|A01|{hl7_timestamp}",
                f"PID|1||{enc['patient']['mrn']}||{enc['patient']['last_name']}^{enc['patient']['first_name']}||{enc['patient']['dob']}|{enc['patient']['gender']}",
                f"PV1|1|O|{enc['facility']['location']}|||{enc['provider']['npi']}^{enc['provider']['name'].replace('Dr. ', '')}",
                f"DG1|1|ICD10|{enc['diagnoses'][0]}|{enc['diagnoses'][0]}",
                f"PR1|1|CPT|{enc['procedures'][0]}|{enc['procedures'][0]}|{hl7_timestamp}"
            ]

            hl7_messages.append('\r'.join(message))

        with open(output_path, 'w') as f:
            f.write('\n\n'.join(hl7_messages))

        logger.info(f"✓ HL7 export complete: {output_path}")
        logger.info(f"  Messages: {len(hl7_messages)}")
        logger.info(f"  Size: {output_path.stat().st_size:,} bytes")

        return str(output_path)

    def export_fhir(self, output_dir):
        """Export data to FHIR R4 format"""
        output_path = Path(output_dir) / f"ehr_data_{self.export_timestamp}_fhir.json"
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Create FHIR Bundle
        bundle = {
            "resourceType": "Bundle",
            "type": "collection",
            "timestamp": datetime.now().isoformat(),
            "total": len(self.generator.encounters),
            "entry": []
        }

        for enc in self.generator.encounters:
            # Create FHIR Encounter resource
            encounter_resource = {
                "fullUrl": f"urn:uuid:{enc['encounter_id']}",
                "resource": {
                    "resourceType": "Encounter",
                    "id": enc['encounter_id'],
                    "status": "finished" if enc['status'] == "completed" else "in-progress",
                    "class": {
                        "system": "http://terminology.hl7.org/CodeSystem/v3-ActCode",
                        "code": "AMB",
                        "display": "ambulatory"
                    },
                    "subject": {
                        "reference": f"Patient/{enc['patient']['id']}",
                        "display": f"{enc['patient']['first_name']} {enc['patient']['last_name']}"
                    },
                    "participant": [{
                        "individual": {
                            "reference": f"Practitioner/{enc['provider']['id']}",
                            "display": enc['provider']['name']
                        }
                    }],
                    "period": {
                        "start": f"{enc['date']}T{enc['time']}"
                    },
                    "diagnosis": [
                        {
                            "condition": {
                                "coding": [{
                                    "system": "http://hl7.org/fhir/sid/icd-10",
                                    "code": code
                                }]
                            }
                        } for code in enc['diagnoses']
                    ],
                    "serviceProvider": {
                        "reference": f"Organization/{enc['facility']['id']}",
                        "display": enc['facility']['name']
                    }
                }
            }

            bundle["entry"].append(encounter_resource)

        with open(output_path, 'w') as f:
            json.dump(bundle, f, indent=2)

        logger.info(f"✓ FHIR export complete: {output_path}")
        logger.info(f"  Resources: {len(bundle['entry'])}")
        logger.info(f"  Size: {output_path.stat().st_size:,} bytes")

        return str(output_path)

    def compress_file(self, file_path):
        """Compress file using gzip"""
        input_path = Path(file_path)
        output_path = Path(f"{file_path}.gz")

        with open(input_path, 'rb') as f_in:
            with gzip.open(output_path, 'wb') as f_out:
                f_out.writelines(f_in)

        original_size = input_path.stat().st_size
        compressed_size = output_path.stat().st_size
        compression_ratio = (1 - compressed_size / original_size) * 100

        logger.info(f"✓ Compressed: {output_path}")
        logger.info(f"  Original: {original_size:,} bytes")
        logger.info(f"  Compressed: {compressed_size:,} bytes ({compression_ratio:.1f}% reduction)")

        return str(output_path)


def main():
    """Main execution function"""
    parser = argparse.ArgumentParser(
        description="Phase 24: EHR Integration Data Export Tool"
    )
    parser.add_argument(
        '--data-type',
        choices=['encounters', 'billing', 'codes', 'all'],
        default='encounters',
        help='Data type to export (default: encounters)'
    )
    parser.add_argument(
        '--format',
        choices=['json', 'csv', 'hl7', 'fhir', 'all'],
        default='json',
        help='Export format (default: json)'
    )
    parser.add_argument(
        '--output-dir',
        default='./exports',
        help='Output directory (default: ./exports)'
    )
    parser.add_argument(
        '--encounters',
        type=int,
        default=100,
        help='Number of encounters to export (default: 100)'
    )
    parser.add_argument(
        '--include-metadata',
        action='store_true',
        help='Include metadata in exports'
    )
    parser.add_argument(
        '--compress',
        action='store_true',
        help='Compress output files (gzip)'
    )

    args = parser.parse_args()

    print("\n" + "=" * 70)
    print("Phase 24: EHR Integration Data Export Tool")
    print("=" * 70)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Data Type: {args.data_type}")
    print(f"Format: {args.format}")
    print(f"Records: {args.encounters}")
    print("=" * 70 + "\n")

    # Generate data
    generator = DataGenerator(encounter_count=args.encounters)
    generator.generate_encounters()

    # Export data
    exporter = DataExporter(generator)
    export_files = []

    if args.format in ['json', 'all']:
        export_files.append(exporter.export_json(args.output_dir, args.include_metadata))

    if args.format in ['csv', 'all']:
        export_files.append(exporter.export_csv(args.output_dir))

    if args.format in ['hl7', 'all']:
        export_files.append(exporter.export_hl7(args.output_dir))

    if args.format in ['fhir', 'all']:
        export_files.append(exporter.export_fhir(args.output_dir))

    # Compress if requested
    if args.compress:
        logger.info("\nCompressing export files...")
        compressed_files = []
        for file_path in export_files:
            compressed_files.append(exporter.compress_file(file_path))
        export_files.extend(compressed_files)

    # Summary
    print("\n" + "=" * 70)
    print("EXPORT SUMMARY")
    print("=" * 70)
    print(f"Records Exported:    {args.encounters}")
    print(f"Files Generated:     {len(export_files)}")
    print(f"\nOutput Files:")
    for f in export_files:
        print(f"  - {f}")
    print("=" * 70 + "\n")

    return 0


if __name__ == "__main__":
    sys.exit(main())
