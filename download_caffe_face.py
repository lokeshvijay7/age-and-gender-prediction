"""
Download Caffe-based face detection model (more reliable than TensorFlow version)

"""

import os
import urllib.request
from pathlib import Path

# Caffe face detection model URLs
CAFFE_FACE_MODELS = {
    'deploy.prototxt': 'https://raw.githubusercontent.com/opencv/opencv/master/samples/dnn/face_detector/deploy.prototxt',
    'res10_300x300_ssd_iter_140000_fp16.caffemodel': 'https://github.com/opencv/opencv_3rdparty/raw/dnn_samples_face_detector_20170830/res10_300x300_ssd_iter_140000_fp16.caffemodel'
}

def download_caffe_face_model(model_dir='models'):
    """Download Caffe-based face detection model."""
    Path(model_dir).mkdir(parents=True, exist_ok=True)
    
    print("=" * 60)
    print("Downloading Caffe Face Detection Model")
    print("=" * 60)
    print()
    
    for filename, url in CAFFE_FACE_MODELS.items():
        filepath = os.path.join(model_dir, filename)
        
        if os.path.exists(filepath):
            print(f"[SKIP] {filename} already exists")
            continue
        
        print(f"Downloading {filename}...")
        try:
            urllib.request.urlretrieve(url, filepath)
            print(f"[OK] Downloaded successfully!")
        except Exception as e:
            print(f"✗ Error: {e}")
        print()
    
    print("=" * 60)
    print("Download Complete!")
    print("=" * 60)

if __name__ == "__main__":
    download_caffe_face_model()
