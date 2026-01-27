"""
Test script to verify model loading and basic functionality.
"""

import cv2
import numpy as np
from src.detector import AgeGenderDetector


def test_model_loading():
    """Test if models load successfully."""
    print("Testing model loading...")
    try:
        detector = AgeGenderDetector()
        print("[OK] Models loaded successfully!")
        return detector
    except Exception as e:
        print(f"✗ Error loading models: {e}")
        return None


def test_face_detection(detector):
    """Test face detection with a sample image."""
    print("\nTesting face detection...")
    
    # Create a simple test image (black image)
    test_image = np.zeros((480, 640, 3), dtype=np.uint8)
    
    try:
        faces = detector.detect_faces(test_image)
        print(f"[OK] Face detection works! Detected {len(faces)} face(s)")
        return True
    except Exception as e:
        print(f"✗ Error in face detection: {e}")
        return False


def test_prediction(detector):
    """Test full prediction pipeline."""
    print("\nTesting prediction pipeline...")
    
    # Create a simple test image
    test_image = np.zeros((480, 640, 3), dtype=np.uint8)
    
    try:
        results = detector.predict(test_image)
        print(f"[OK] Prediction works!")
        print(f"  Detected faces: {len(results['faces'])}")
        print(f"  Ages: {results['ages']}")
        print(f"  Genders: {results['genders']}")
        return True
    except Exception as e:
        print(f"✗ Error in prediction: {e}")
        return False


def main():
    """Run all tests."""
    print("=" * 60)
    print("Age and Gender Prediction System - Test Suite")
    print("=" * 60)
    print()
    
    # Test model loading
    detector = test_model_loading()
    if detector is None:
        print("\n Please run 'python download_models.py' first to download models.")
        return
    
    # Test face detection
    test_face_detection(detector)
    
    # Test prediction
    test_prediction(detector)
    
    print("\n" + "=" * 60)
    print("Test Suite Complete!")
    print("=" * 60)
    print("\nYou can now run the application with: python main.py")


if __name__ == "__main__":
    main()
