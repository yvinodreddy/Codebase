#!/usr/bin/env python3
"""
Phase 14: Sample X-ray Analysis Script
Demonstrates how to use the Medical Imaging Pipeline for X-ray analysis
"""

import sys
import os
import json

# Add code directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'code'))

from medical_imaging_core import MedicalImagingPipeline

def main():
    """Demonstrate X-ray analysis"""

    print("\n" + "="*80)
    print("PHASE 14: X-RAY ANALYSIS DEMONSTRATION")
    print("="*80 + "\n")

    # Initialize pipeline
    print("Initializing Medical Imaging Pipeline...")
    pipeline = MedicalImagingPipeline(use_guardrails=False)
    print("✅ Pipeline initialized\n")

    # In production, you would use actual X-ray images
    # For demonstration, we'll create a synthetic image
    print("📸 Note: This demonstration uses a synthetic test image")
    print("   In production, use actual DICOM or medical image files\n")

    # Create a test image
    import tempfile
    import numpy as np
    try:
        from PIL import Image
        temp_dir = tempfile.mkdtemp()
        test_image_path = os.path.join(temp_dir, "test_chest_xray.png")

        # Create synthetic chest X-ray (grayscale)
        img_data = np.random.randint(80, 180, (512, 512), dtype=np.uint8)
        img = Image.fromarray(img_data)
        img.save(test_image_path)
        print(f"Created test image: {test_image_path}\n")
    except ImportError:
        print("⚠️  PIL not available, using fallback\n")
        test_image_path = "test.png"

    # Analyze X-ray
    print("🔍 Analyzing chest X-ray...")
    print("-" * 80)

    result = pipeline.analyze_image(test_image_path, modality="XRAY")

    if not result:
        print("❌ Analysis failed")
        return 1

    # Display results
    print("\n" + "="*80)
    print("ANALYSIS RESULTS")
    print("="*80 + "\n")

    print(f"Image ID:           {result.image_id}")
    print(f"Modality:           {result.modality}")
    print(f"Quality Score:      {result.quality_score}/100")
    print(f"Clinical Priority:  {result.clinical_priority}")
    print(f"Processing Time:    {result.processing_time_ms:.2f}ms")
    print(f"HIPAA Validated:    {'✅' if result.guardrails_validated else '⚠️  Not validated'}")

    print("\n" + "-"*80)
    print("OVERALL ASSESSMENT")
    print("-"*80)
    print(f"{result.overall_assessment}")

    print("\n" + "-"*80)
    print("FINDINGS SUMMARY")
    print("-"*80)
    print(f"{result.findings_summary}")

    print("\n" + "-"*80)
    print(f"DETECTIONS ({len(result.detections)})")
    print("-"*80)
    for i, detection in enumerate(result.detections, 1):
        print(f"\n{i}. {detection.abnormality_type}")
        print(f"   Confidence: {detection.confidence*100:.1f}%")
        print(f"   Severity: {detection.severity}")
        print(f"   Location: {detection.location}")
        print(f"   Description: {detection.description}")
        print(f"   Recommendation: {detection.recommended_action}")
        print(f"   Evidence-based: {'✅' if detection.evidence_based else '❌'}")

    print("\n" + "-"*80)
    print(f"RECOMMENDATIONS ({len(result.recommendations)})")
    print("-"*80)
    for i, rec in enumerate(result.recommendations, 1):
        print(f"{i}. {rec}")

    # HIPAA Compliance
    print("\n" + "-"*80)
    print("HIPAA COMPLIANCE")
    print("-"*80)
    print(f"Patient ID:         {result.metadata.patient_id}")
    print(f"Institution:        {result.metadata.institution}")
    print(f"PHI Removed:        {'✅' if result.metadata.phi_removed else '❌'}")
    print(f"HIPAA Compliant:    {'✅' if result.metadata.hipaa_compliant else '❌'}")
    print(f"Image Hash:         {result.metadata.image_hash[:16]}...")

    # Export results
    print("\n" + "-"*80)
    print("EXPORT OPTIONS")
    print("-"*80)

    # JSON export
    result_dict = result.to_dict()
    output_file = "xray_analysis_result.json"
    with open(output_file, 'w') as f:
        json.dump(result_dict, f, indent=2, default=str)
    print(f"✅ Results exported to: {output_file}")

    print("\n" + "="*80)
    print("✅ X-RAY ANALYSIS COMPLETE")
    print("="*80 + "\n")

    return 0


if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n⚠️  Analysis interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
