"""
Script to download pre-trained models for age and gender prediction.
"""

import os
import urllib.request
from pathlib import Path


# Model URLs
MODELS = {
    'opencv_face_detector.pbtxt': 'https://raw.githubusercontent.com/opencv/opencv/master/samples/dnn/face_detector/deploy.prototxt',
    'opencv_face_detector_uint8.pb': 'https://github.com/opencv/opencv_3rdparty/raw/dnn_samples_face_detector_20170830/res10_300x300_ssd_iter_140000.caffemodel',
    'age_deploy.prototxt': 'https://raw.githubusercontent.com/GilLevi/AgeGenderDeepLearning/master/age_net_definitions/deploy_age.prototxt',
    'age_net.caffemodel': 'https://github.com/GilLevi/AgeGenderDeepLearning/raw/master/models/age_net.caffemodel',
    'gender_deploy.prototxt': 'https://raw.githubusercontent.com/GilLevi/AgeGenderDeepLearning/master/gender_net_definitions/deploy_gender.prototxt',
    'gender_net.caffemodel': 'https://github.com/GilLevi/AgeGenderDeepLearning/raw/master/models/gender_net.caffemodel'
}


def download_models(model_dir='models'):
    """
    Download all required pre-trained models.
    
    Args:
        model_dir: Directory to save models
    """
    # Create models directory if it doesn't exist
    Path(model_dir).mkdir(parents=True, exist_ok=True)
    
    print("=" * 60)
    print("Downloading Pre-trained Models")
    print("=" * 60)
    print()
    
    for filename, url in MODELS.items():
        filepath = os.path.join(model_dir, filename)
        
        # Skip if file already exists
        if os.path.exists(filepath):
            print(f"[SKIP] {filename} already exists, skipping...")
            continue
        
        print(f"Downloading {filename}...")
        print(f"  URL: {url}")
        
        try:
            # Download with progress
            def progress_hook(block_num, block_size, total_size):
                downloaded = block_num * block_size
                if total_size > 0:
                    percent = min(downloaded * 100 / total_size, 100)
                    print(f"\r  Progress: {percent:.1f}%", end='', flush=True)
            
            urllib.request.urlretrieve(url, filepath, progress_hook)
            print(f"\n[OK] Downloaded successfully!")
            
        except Exception as e:
            print(f"\n✗ Error downloading {filename}: {e}")
            print(f"  Please download manually from: {url}")
        
        print()
    
    print("=" * 60)
    print("Download Complete!")
    print("=" * 60)
    print()
    
    # Verify all files exist
    missing_files = []
    for filename in MODELS.keys():
        filepath = os.path.join(model_dir, filename)
        if not os.path.exists(filepath):
            missing_files.append(filename)
    
    if missing_files:
        print("[WARNING] The following files are missing:")
        for filename in missing_files:
            print(f"  - {filename}")
        print("\nPlease download them manually and place in the 'models' directory.")
    else:
        print("[OK] All model files are ready!")
        print("\nYou can now run the application with: python main.py")


if __name__ == "__main__":
    download_models()
