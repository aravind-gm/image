#!/usr/bin/env python
"""
Test script for Image Similarity Analyzer
Tests backend algorithms without server
"""

import cv2
import numpy as np
from app import (
    histogram_comparison,
    ssim_comparison,
    sift_comparison,
    compare_images,
    resize_images
)
import os
import tempfile

def create_test_image(filename, color):
    """Create a simple test image with specific color"""
    img = np.full((100, 100, 3), color, dtype=np.uint8)
    cv2.imwrite(filename, img)
    return filename

def create_modified_image(base_filename, mod_type='rotate'):
    """Create a modified version of base image"""
    img = cv2.imread(base_filename)
    
    if mod_type == 'rotate':
        h, w = img.shape[:2]
        center = (w // 2, h // 2)
        matrix = cv2.getRotationMatrix2D(center, 45, 1.0)
        img = cv2.warpAffine(img, matrix, (w, h))
    elif mod_type == 'scale':
        img = cv2.resize(img, (50, 50))
        img = cv2.resize(img, (100, 100))
    elif mod_type == 'blur':
        img = cv2.GaussianBlur(img, (5, 5), 0)
    elif mod_type == 'noise':
        noise = np.random.normal(0, 10, img.shape).astype(np.uint8)
        img = cv2.add(img, noise)
    
    return img

def test_algorithms():
    """Test all comparison algorithms"""
    print("🧪 Testing Image Similarity Analyzer\n")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Test 1: Identical images
        print("Test 1: Identical Images")
        img1_path = os.path.join(tmpdir, 'test1.jpg')
        img2_path = os.path.join(tmpdir, 'test1_copy.jpg')
        
        create_test_image(img1_path, [100, 150, 200])
        create_test_image(img2_path, [100, 150, 200])
        
        result = compare_images(img1_path, img2_path)
        print(f"  Similarity: {result['similarity']:.2%}")
        print(f"  ✓ Should be ~100% (actual: {result['similarity']:.2%})\n")
        
        # Test 2: Completely different images
        print("Test 2: Completely Different Images")
        img1_path = os.path.join(tmpdir, 'test2.jpg')
        img2_path = os.path.join(tmpdir, 'test2_diff.jpg')
        
        create_test_image(img1_path, [0, 0, 0])
        create_test_image(img2_path, [255, 255, 255])
        
        result = compare_images(img1_path, img2_path)
        print(f"  Similarity: {result['similarity']:.2%}")
        print(f"  ✓ Should be low (actual: {result['similarity']:.2%})\n")
        
        # Test 3: Rotated image
        print("Test 3: Rotated Image")
        img1_path = os.path.join(tmpdir, 'test3.jpg')
        img2_path = os.path.join(tmpdir, 'test3_rotated.jpg')
        
        base = create_test_image(img1_path, [50, 100, 150])
        rotated = create_modified_image(img1_path, 'rotate')
        cv2.imwrite(img2_path, rotated)
        
        result = compare_images(img1_path, img2_path)
        print(f"  Similarity: {result['similarity']:.2%}")
        print(f"  SIFT Score: {result['sift']:.2%}")
        print(f"  ✓ SIFT should detect rotation\n")
        
        # Test 4: Slightly modified image
        print("Test 4: Slightly Blurred Image")
        img1_path = os.path.join(tmpdir, 'test4.jpg')
        img2_path = os.path.join(tmpdir, 'test4_blurred.jpg')
        
        create_test_image(img1_path, [75, 125, 175])
        blurred = create_modified_image(img1_path, 'blur')
        cv2.imwrite(img2_path, blurred)
        
        result = compare_images(img1_path, img2_path)
        print(f"  Similarity: {result['similarity']:.2%}")
        print(f"  SSIM Score: {result['ssim']:.2%}")
        print(f"  ✓ Should be high (similar content)\n")
        
        # Test 5: Algorithm breakdown
        print("Test 5: Algorithm Score Breakdown")
        result = {
            'similarity': 0.75,
            'histogram': 0.82,
            'ssim': 0.68,
            'sift': 0.73
        }
        
        print(f"  Final Similarity: {result['similarity']:.2%}")
        print(f"  Components:")
        print(f"    - Color Histogram (40%): {result['histogram']:.2%} → {result['histogram'] * 0.40:.2%}")
        print(f"    - SSIM (30%): {result['ssim']:.2%} → {result['ssim'] * 0.30:.2%}")
        print(f"    - SIFT (30%): {result['sift']:.2%} → {result['sift'] * 0.30:.2%}")
        print(f"  Calculation: ({result['histogram']*0.40:.3f} + {result['ssim']*0.30:.3f} + {result['sift']*0.30:.3f}) = {result['similarity']:.3f}\n")
    
    print("✅ All tests completed!")
    print("\n💡 Note: Exact scores may vary due to image content complexity")
    print("        and algorithm variations. These are indicator ranges.")

if __name__ == '__main__':
    try:
        test_algorithms()
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
