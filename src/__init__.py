"""
Age and Gender Prediction System
Source package initialization.
"""

from src.detector import AgeGenderDetector
from src.gui import AgeGenderGUI
from src.utils import (
    draw_predictions,
    validate_image_file,
    validate_video_file,
    resize_for_display,
    create_result_text
)

__all__ = [
    'AgeGenderDetector',
    'AgeGenderGUI',
    'draw_predictions',
    'validate_image_file',
    'validate_video_file',
    'resize_for_display',
    'create_result_text'
]
