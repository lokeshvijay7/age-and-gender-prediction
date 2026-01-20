"""
Test if the detector works with a simple image.
"""

import cv2
import numpy as np
from src.detector import AgeGenderDetector


# Create a simple test image
test_img = np.zeros((480, 640, 3), dtype=np.uint8)
test_img[:] = (200, 200, 200)  # Gray background

print("Creating detector...")
detector = AgeGenderDetector()

print("\nTesting with blank image...")
results = detector.predict(test_img)
print(f"Faces detected: {len(results['faces'])}")

print("\nNow testing with a real image...")
print("Please upload an image when prompted in the GUI.")
print("If you see an error, check the terminal output for details.")
