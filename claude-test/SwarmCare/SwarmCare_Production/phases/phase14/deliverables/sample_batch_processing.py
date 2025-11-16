#!/usr/bin/env python3
"""
Phase 14: Sample Batch Processing Script
Demonstrates batch analysis of multiple medical images
"""

import sys
import os
import time
import json

# Add code directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'code'))

from medical_imaging_core import MedicalImagingPipeline

def main():
    """Demonstrate batch processing"""

    print("\n" + "="*80)
    print("PHASE 14: BATCH PROCESSING DEMONSTRATION")
    print("="*80 + "\n")

    # Initialize pipeline
    print("Initializing Medical Imaging Pipeline...")
    pipeline = MedicalImagingPipeline(use_guardrails=False)
    print("✅ Pipeline initialized\n")

    # Create test images
    print("📸 Creating test images for batch processing...")
    print("   Note: Using synthetic images for demonstration\n")

    test_images = create_test_images(count=10)
    print(f"✅ Created {len(test_images)} test images\n")

    # Batch analysis
    print("="*80)
    print("BATCH ANALYSIS")
    print("="*80 + "\n")

    start_time = time.time()

    # Process images
    print(f"Processing {len(test_images)} images...")
    print("-" * 80)

    results = pipeline.batch_analyze(test_images, modality="XRAY")

    total_time = time.time() - start_time

    # Display results summary
    print("\n" + "="*80)
    print("BATCH PROCESSING RESULTS")
    print("="*80 + "\n")

    print(f"Total Images:       {len(test_images)}")
    print(f"Successful:         {len(results)}")
    print(f"Failed:             {len(test_images) - len(results)}")
    print(f"Total Time:         {total_time:.2f}s")
    print(f"Average Time:       {(total_time/len(results)*1000):.2f}ms per image")
    print(f"Throughput:         {(len(results)/(total_time/60)):.1f} images/minute")

    # Priority distribution
    print("\n" + "-"*80)
    print("CLINICAL PRIORITY DISTRIBUTION")
    print("-"*80)

    priority_counts = {}
    for result in results:
        priority = result.clinical_priority
        priority_counts[priority] = priority_counts.get(priority, 0) + 1

    for priority, count in sorted(priority_counts.items()):
        percentage = (count / len(results)) * 100
        print(f"{priority:15s} {count:3d} ({percentage:5.1f}%)")

    # Abnormality distribution
    print("\n" + "-"*80)
    print("ABNORMALITY DETECTION SUMMARY")
    print("-"*80)

    abnormality_counts = {}
    for result in results:
        for detection in result.detections:
            abn_type = detection.abnormality_type
            abnormality_counts[abn_type] = abnormality_counts.get(abn_type, 0) + 1

    for abn_type, count in sorted(abnormality_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"{abn_type:20s} {count:3d}")

    # Quality scores
    print("\n" + "-"*80)
    print("IMAGE QUALITY STATISTICS")
    print("-"*80)

    quality_scores = [r.quality_score for r in results]
    print(f"Average Quality:    {sum(quality_scores)/len(quality_scores):.2f}/100")
    print(f"Minimum Quality:    {min(quality_scores):.2f}/100")
    print(f"Maximum Quality:    {max(quality_scores):.2f}/100")

    # Performance statistics
    print("\n" + "-"*80)
    print("PERFORMANCE STATISTICS")
    print("-"*80)

    processing_times = [r.processing_time_ms for r in results]
    print(f"Average Processing: {sum(processing_times)/len(processing_times):.2f}ms")
    print(f"Minimum Processing: {min(processing_times):.2f}ms")
    print(f"Maximum Processing: {max(processing_times):.2f}ms")

    # Export summary
    print("\n" + "-"*80)
    print("EXPORT BATCH RESULTS")
    print("-"*80)

    summary = {
        "total_images": len(test_images),
        "successful": len(results),
        "failed": len(test_images) - len(results),
        "total_time_seconds": total_time,
        "average_time_ms": sum(processing_times)/len(processing_times),
        "throughput_images_per_minute": len(results)/(total_time/60),
        "priority_distribution": priority_counts,
        "abnormality_distribution": abnormality_counts,
        "quality_statistics": {
            "average": sum(quality_scores)/len(quality_scores),
            "min": min(quality_scores),
            "max": max(quality_scores)
        }
    }

    output_file = "batch_processing_summary.json"
    with open(output_file, 'w') as f:
        json.dump(summary, f, indent=2)
    print(f"✅ Summary exported to: {output_file}")

    # Export individual results
    for i, result in enumerate(results, 1):
        result_file = f"batch_result_{i:03d}.json"
        with open(result_file, 'w') as f:
            json.dump(result.to_dict(), f, indent=2, default=str)
    print(f"✅ Individual results exported ({len(results)} files)")

    print("\n" + "="*80)
    print("✅ BATCH PROCESSING COMPLETE")
    print("="*80 + "\n")

    return 0


def create_test_images(count=10):
    """Create synthetic test images"""
    import tempfile
    import numpy as np

    temp_dir = tempfile.mkdtemp()
    image_paths = []

    try:
        from PIL import Image
        for i in range(count):
            image_path = os.path.join(temp_dir, f"test_image_{i+1:03d}.png")
            img_data = np.random.randint(60, 200, (512, 512), dtype=np.uint8)
            img = Image.fromarray(img_data)
            img.save(image_path)
            image_paths.append(image_path)
    except ImportError:
        # Fallback if PIL not available
        for i in range(count):
            image_paths.append(f"test_{i+1}.png")

    return image_paths


if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n⚠️  Batch processing interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
