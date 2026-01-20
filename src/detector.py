"""
Age and Gender Detection Module
Handles face detection and age/gender prediction using pre-trained CNN models.
"""

import cv2
import numpy as np
import os
from typing import List, Tuple, Optional


class AgeGenderDetector:
    """
    Age and Gender detector using pre-trained CNN models.
    """
    
    # Age groups for prediction
    AGE_GROUPS = ['0-2', '4-6', '8-12', '15-20', '25-32', '38-43', '48-53', '60-100']
    
    # Gender labels
    GENDER_LABELS = ['Male', 'Female']
    
    # Model mean values for preprocessing
    MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)
    
    def __init__(self, model_dir: str = 'models'):
        """
        Initialize the detector with pre-trained models.
        
        Args:
            model_dir: Directory containing model files
        """
        self.model_dir = model_dir
        self.face_net = None
        self.age_net = None
        self.gender_net = None
        
        # Model file paths
        # Try Caffe face detector first (more reliable)
        self.face_proto = os.path.join(model_dir, 'deploy.prototxt')
        self.face_model = os.path.join(model_dir, 'res10_300x300_ssd_iter_140000.caffemodel')
        
        # Fallback to TensorFlow face detector if Caffe not available
        if not os.path.exists(self.face_proto) or not os.path.exists(self.face_model):
            self.face_proto = os.path.join(model_dir, 'opencv_face_detector.pbtxt')
            self.face_model = os.path.join(model_dir, 'opencv_face_detector_uint8.pb')
            self.use_tf_face_detector = True
        else:
            self.use_tf_face_detector = False
        
        self.age_proto = os.path.join(model_dir, 'age_deploy.prototxt')
        self.age_model = os.path.join(model_dir, 'age_net.caffemodel')
        self.gender_proto = os.path.join(model_dir, 'gender_deploy.prototxt')
        self.gender_model = os.path.join(model_dir, 'gender_net.caffemodel')
        
        self._load_models()
    
    def _load_models(self) -> None:
        """Load all pre-trained models."""
        try:
            # Check if model files exist
            self._check_model_files()
            
            # Load face detection model
            print("Loading face detection model...")
            if self.use_tf_face_detector:
                print("  Using TensorFlow face detector...")
                self.face_net = cv2.dnn.readNetFromTensorflow(self.face_model, self.face_proto)
            else:
                print("  Using Caffe face detector...")
                self.face_net = cv2.dnn.readNetFromCaffe(self.face_proto, self.face_model)
            
            # Load age prediction model (Caffe)
            print("Loading age prediction model...")
            self.age_net = cv2.dnn.readNetFromCaffe(self.age_proto, self.age_model)
            
            # Load gender prediction model (Caffe)
            print("Loading gender prediction model...")
            self.gender_net = cv2.dnn.readNetFromCaffe(self.gender_proto, self.gender_model)
            
            # Verify models loaded correctly
            if self.face_net is None or self.face_net.empty():
                raise Exception("Face detection network is empty after loading")
            if self.age_net is None or self.age_net.empty():
                raise Exception("Age prediction network is empty after loading")
            if self.gender_net is None or self.gender_net.empty():
                raise Exception("Gender prediction network is empty after loading")
            
            print("All models loaded successfully!")
            
        except Exception as e:
            raise Exception(f"Error loading models: {e}")
    
    def _check_model_files(self) -> None:
        """Check if all required model files exist."""
        required_files = [
            self.face_proto, self.face_model,
            self.age_proto, self.age_model,
            self.gender_proto, self.gender_model
        ]
        
        missing_files = [f for f in required_files if not os.path.exists(f)]
        
        if missing_files:
            print("\nMissing model files:")
            for f in missing_files:
                print(f"  - {f}")
            print("\nPlease download the models using the download_models.py script")
            print("or manually download them as described in README.md")
            raise FileNotFoundError("Required model files are missing")
    
    def detect_faces(self, image: np.ndarray, conf_threshold: float = 0.7) -> List[Tuple[int, int, int, int]]:
        """
        Detect faces in an image.
        
        Args:
            image: Input image (BGR format)
            conf_threshold: Confidence threshold for detection
        
        Returns:
            List of face bounding boxes [(x, y, w, h), ...]
        """
        faces = []
        
        # Validate input
        if image is None or image.size == 0:
            print("Error: Empty or invalid image")
            return faces
        
        # Validate network is loaded
        if self.face_net is None or self.face_net.empty():
            print("Error: Face detection network not loaded")
            return faces
        
        try:
            h, w = image.shape[:2]
            
            # Prepare image for face detection
            blob = cv2.dnn.blobFromImage(
                image, 
                scalefactor=1.0, 
                size=(300, 300), 
                mean=[104.0, 117.0, 123.0], 
                swapRB=False, 
                crop=False
            )
            
            # Validate blob
            if blob is None or blob.size == 0:
                print("Error: Failed to create blob from image")
                return faces
            
            # Set input and run forward pass
            self.face_net.setInput(blob)
            detections = self.face_net.forward()
            
            # Process detections
            for i in range(detections.shape[2]):
                confidence = detections[0, 0, i, 2]
                
                if confidence > conf_threshold:
                    # Get bounding box coordinates
                    x1 = int(detections[0, 0, i, 3] * w)
                    y1 = int(detections[0, 0, i, 4] * h)
                    x2 = int(detections[0, 0, i, 5] * w)
                    y2 = int(detections[0, 0, i, 6] * h)
                    
                    # Ensure coordinates are within image bounds
                    x1 = max(0, x1)
                    y1 = max(0, y1)
                    x2 = min(w, x2)
                    y2 = min(h, y2)
                    
                    # Validate bounding box
                    if x2 > x1 and y2 > y1:
                        # Convert to (x, y, width, height) format
                        face_box = (x1, y1, x2 - x1, y2 - y1)
                        faces.append(face_box)
            
        except Exception as e:
            print(f"Error in face detection: {e}")
            import traceback
            traceback.print_exc()
        
        return faces
    
    def predict_age(self, face_img: np.ndarray) -> Tuple[str, float]:
        """
        Predict age group for a face.
        
        Args:
            face_img: Face image (BGR format)
        
        Returns:
            Tuple of (age_group, confidence)
        """
        # Prepare face image for age prediction
        blob = cv2.dnn.blobFromImage(face_img, 1.0, (227, 227), 
                                     self.MODEL_MEAN_VALUES, swapRB=False)
        
        self.age_net.setInput(blob)
        age_preds = self.age_net.forward()
        
        # Get prediction with highest confidence
        age_idx = age_preds[0].argmax()
        confidence = age_preds[0][age_idx]
        
        return self.AGE_GROUPS[age_idx], float(confidence)
    
    def predict_gender(self, face_img: np.ndarray) -> Tuple[str, float]:
        """
        Predict gender for a face.
        
        Args:
            face_img: Face image (BGR format)
        
        Returns:
            Tuple of (gender, confidence)
        """
        # Prepare face image for gender prediction
        blob = cv2.dnn.blobFromImage(face_img, 1.0, (227, 227), 
                                     self.MODEL_MEAN_VALUES, swapRB=False)
        
        self.gender_net.setInput(blob)
        gender_preds = self.gender_net.forward()
        
        # Get prediction with highest confidence
        gender_idx = gender_preds[0].argmax()
        confidence = gender_preds[0][gender_idx]
        
        return self.GENDER_LABELS[gender_idx], float(confidence)
    
    def predict(self, image: np.ndarray, conf_threshold: float = 0.7) -> dict:
        """
        Detect faces and predict age and gender.
        
        Args:
            image: Input image (BGR format)
            conf_threshold: Confidence threshold for face detection
        
        Returns:
            Dictionary containing:
                - faces: List of face bounding boxes
                - ages: List of predicted age groups
                - genders: List of predicted genders
                - age_confidences: List of age prediction confidences
                - gender_confidences: List of gender prediction confidences
        """
        # Detect faces
        faces = self.detect_faces(image, conf_threshold)
        
        ages = []
        genders = []
        age_confidences = []
        gender_confidences = []
        
        # Predict age and gender for each face
        for (x, y, w, h) in faces:
            # Extract face region with padding
            padding = 20
            y1 = max(0, y - padding)
            y2 = min(image.shape[0], y + h + padding)
            x1 = max(0, x - padding)
            x2 = min(image.shape[1], x + w + padding)
            
            face_img = image[y1:y2, x1:x2]
            
            # Skip if face region is too small
            if face_img.shape[0] < 20 or face_img.shape[1] < 20:
                ages.append("Unknown")
                genders.append("Unknown")
                age_confidences.append(0.0)
                gender_confidences.append(0.0)
                continue
            
            # Predict age and gender
            try:
                age, age_conf = self.predict_age(face_img)
                gender, gender_conf = self.predict_gender(face_img)
                
                ages.append(age)
                genders.append(gender)
                age_confidences.append(age_conf)
                gender_confidences.append(gender_conf)
            except Exception as e:
                print(f"Error predicting for face: {e}")
                ages.append("Unknown")
                genders.append("Unknown")
                age_confidences.append(0.0)
                gender_confidences.append(0.0)
        
        return {
            'faces': faces,
            'ages': ages,
            'genders': genders,
            'age_confidences': age_confidences,
            'gender_confidences': gender_confidences
        }
