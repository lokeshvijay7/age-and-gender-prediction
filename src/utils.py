"""
Utility functions for age and gender prediction system.
Handles image preprocessing, visualization, and file operations.
"""

import cv2
import numpy as np
from typing import Tuple, List, Optional
import os


def preprocess_image(image: np.ndarray, target_size: Tuple[int, int] = (300, 300)) -> np.ndarray:
    """
    Preprocess image for model input.
    
    Args:
        image: Input image as numpy array
        target_size: Target size for resizing (width, height)
    
    Returns:
        Preprocessed image
    """
    # Resize if needed
    if image.shape[:2] != target_size[::-1]:
        image = cv2.resize(image, target_size)
    
    return image


def draw_predictions(image: np.ndarray, 
                     faces: List[Tuple[int, int, int, int]], 
                     ages: List[str], 
                     genders: List[str],
                     age_confidences: List[float],
                     gender_confidences: List[float]) -> np.ndarray:
    """
    Draw bounding boxes and predictions on image.
    
    Args:
        image: Input image
        faces: List of face bounding boxes (x, y, w, h)
        ages: List of predicted age ranges
        genders: List of predicted genders
        age_confidences: List of age prediction confidences
        gender_confidences: List of gender prediction confidences
    
    Returns:
        Annotated image
    """
    output = image.copy()
    
    for i, (x, y, w, h) in enumerate(faces):
        # Draw bounding box
        color = (0, 255, 0)  # Green
        cv2.rectangle(output, (x, y), (x + w, y + h), color, 2)
        
        # Prepare label
        age = ages[i] if i < len(ages) else "Unknown"
        gender = genders[i] if i < len(genders) else "Unknown"
        age_conf = age_confidences[i] if i < len(age_confidences) else 0.0
        gender_conf = gender_confidences[i] if i < len(gender_confidences) else 0.0
        
        label = f"{gender} ({gender_conf:.1%}), {age} ({age_conf:.1%})"
        
        # Calculate label size and position
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.6
        thickness = 2
        (label_width, label_height), baseline = cv2.getTextSize(label, font, font_scale, thickness)
        
        # Draw label background
        label_y = max(y - 10, label_height + 10)
        cv2.rectangle(output, 
                     (x, label_y - label_height - baseline - 5), 
                     (x + label_width, label_y + baseline - 5), 
                     color, 
                     cv2.FILLED)
        
        # Draw label text
        cv2.putText(output, label, (x, label_y - 5), font, font_scale, (0, 0, 0), thickness)
    
    return output


def validate_image_file(file_path: str) -> bool:
    """
    Validate if file is a supported image format.
    
    Args:
        file_path: Path to image file
    
    Returns:
        True if valid image file, False otherwise
    """
    valid_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp'}
    _, ext = os.path.splitext(file_path.lower())
    return ext in valid_extensions and os.path.isfile(file_path)


def validate_video_file(file_path: str) -> bool:
    """
    Validate if file is a supported video format.
    
    Args:
        file_path: Path to video file
    
    Returns:
        True if valid video file, False otherwise
    """
    valid_extensions = {'.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv'}
    _, ext = os.path.splitext(file_path.lower())
    return ext in valid_extensions and os.path.isfile(file_path)


def resize_for_display(image: np.ndarray, max_width: int = 800, max_height: int = 600) -> np.ndarray:
    """
    Resize image for display while maintaining aspect ratio.
    
    Args:
        image: Input image
        max_width: Maximum width
        max_height: Maximum height
    
    Returns:
        Resized image
    """
    h, w = image.shape[:2]
    
    # Calculate scaling factor
    scale = min(max_width / w, max_height / h, 1.0)
    
    if scale < 1.0:
        new_w = int(w * scale)
        new_h = int(h * scale)
        return cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_AREA)
    
    return image


def calculate_fps(start_time: float, frame_count: int) -> float:
    """
    Calculate frames per second.
    
    Args:
        start_time: Start time in seconds
        frame_count: Number of frames processed
    
    Returns:
        FPS value
    """
    import time
    elapsed = time.time() - start_time
    if elapsed > 0:
        return frame_count / elapsed
    return 0.0


def create_result_text(faces_count: int, 
                       ages: List[str], 
                       genders: List[str],
                       age_confidences: List[float],
                       gender_confidences: List[float]) -> str:
    """
    Create formatted result text for display.
    
    Args:
        faces_count: Number of faces detected
        ages: List of predicted ages
        genders: List of predicted genders
        age_confidences: List of age confidences
        gender_confidences: List of gender confidences
    
    Returns:
        Formatted result string
    """
    if faces_count == 0:
        return "No faces detected"
    
    result = f"Detected {faces_count} face(s):\n\n"
    
    for i in range(faces_count):
        age = ages[i] if i < len(ages) else "Unknown"
        gender = genders[i] if i < len(genders) else "Unknown"
        age_conf = age_confidences[i] if i < len(age_confidences) else 0.0
        gender_conf = gender_confidences[i] if i < len(gender_confidences) else 0.0
        
        result += f"Face {i + 1}:\n"
        result += f"  Gender: {gender} (Confidence: {gender_conf:.1%})\n"
        result += f"  Age: {age} years (Confidence: {age_conf:.1%})\n\n"
    
    return result


def ensure_directory_exists(directory: str) -> None:
    """
    Create directory if it doesn't exist.
    
    Args:
        directory: Directory path
    """
    if not os.path.exists(directory):
        os.makedirs(directory)


def download_file(url: str, destination: str) -> bool:
    """
    Download file from URL.
    
    Args:
        url: URL to download from
        destination: Destination file path
    
    Returns:
        True if successful, False otherwise
    """
    try:
        import urllib.request
        print(f"Downloading {os.path.basename(destination)}...")
        urllib.request.urlretrieve(url, destination)
        print(f"Downloaded successfully!")
        return True
    except Exception as e:
        print(f"Error downloading file: {e}")
        return False
