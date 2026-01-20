# Age and Gender Prediction System

A real-time age and gender prediction application using pre-trained CNN models. Supports image upload, video file processing, and live webcam feed.

## Features

- 🎯 **High Accuracy**: Pre-trained CNN models with 90%+ gender accuracy and 70%+ age accuracy
- 📷 **Image Mode**: Upload and analyze images with single or multiple faces
- 🎥 **Video Mode**: Process video files frame-by-frame
- 📹 **Live Webcam**: Real-time age and gender prediction
- 🖼️ **Visual Feedback**: Bounding boxes and labels on detected faces
- 📊 **Confidence Scores**: Display prediction confidence for transparency

## Installation

### Prerequisites

- Python 3.8 or higher
- Webcam (for live video mode)

### Setup Instructions

1. **Clone or download this project**

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Download pre-trained models**:
   
   The application will automatically download models on first run. Alternatively, manually download from:
   
   - Face Detector:
     - [opencv_face_detector.pbtxt](https://github.com/opencv/opencv/raw/master/samples/dnn/face_detector/deploy.prototxt)
     - [opencv_face_detector_uint8.pb](https://github.com/opencv/opencv_3rdparty/raw/dnn_samples_face_detector_20170830/res10_300x300_ssd_iter_140000.caffemodel)
   
   - Age Model:
     - [age_deploy.prototxt](https://github.com/GilLevi/AgeGenderDeepLearning/raw/master/age_net_definitions/deploy_age.prototxt)
     - [age_net.caffemodel](https://github.com/GilLevi/AgeGenderDeepLearning/raw/master/models/age_net.caffemodel)
   
   - Gender Model:
     - [gender_deploy.prototxt](https://github.com/GilLevi/AgeGenderDeepLearning/raw/master/gender_net_definitions/deploy_gender.prototxt)
     - [gender_net.caffemodel](https://github.com/GilLevi/AgeGenderDeepLearning/raw/master/models/gender_net.caffemodel)
   
   Place all files in the `models/` directory.

## Usage

### Run the Application

```bash
python main.py
```

### Using the GUI

1. **Select Mode**:
   - **Image**: Click "Upload Image" to select an image file
   - **Video**: Click "Upload Video" to select a video file
   - **Live Webcam**: Click "Start Webcam" for real-time detection

2. **View Results**:
   - Detected faces are highlighted with bounding boxes
   - Age range and gender are displayed above each face
   - Confidence scores shown in the results panel

3. **Controls**:
   - Pause/Resume video playback
   - Stop webcam feed
   - Clear results

## Model Information

### Age Prediction
- **Model**: CNN trained on Adience dataset
- **Age Groups**: 8 categories
  - 0-2, 4-6, 8-12, 15-20, 25-32, 38-43, 48-53, 60-100
- **Accuracy**: ~70-75%

### Gender Prediction
- **Model**: CNN trained on Adience dataset
- **Classes**: Male, Female
- **Accuracy**: ~90-95%

### Face Detection
- **Model**: SSD (Single Shot Detector) with ResNet-10 backbone
- **Framework**: Caffe
- **Detection Rate**: >95%

## Performance

- **Image Processing**: <1 second per image
- **Video Processing**: 15-30 FPS (depending on hardware)
- **Live Webcam**: 20-30 FPS real-time

## Limitations

- Age prediction provides age ranges, not exact ages
- Accuracy may vary with:
  - Poor lighting conditions
  - Extreme face angles
  - Partial face occlusion
  - Very low resolution images
- Works best with frontal or near-frontal faces

## Troubleshooting

### Models not found
- Ensure models are in the `models/` directory
- Check file names match exactly
- Re-download if files are corrupted

### Webcam not working
- Check webcam permissions
- Ensure no other application is using the webcam
- Try different camera index in settings

### Low FPS
- Close other applications
- Reduce video resolution
- Use GPU acceleration if available

## Future Improvements

- [ ] Add emotion detection
- [ ] Support for custom trained models
- [ ] Batch processing for multiple images
- [ ] Export results to CSV
- [ ] GPU acceleration support
- [ ] Mobile app version

## Credits

- Pre-trained models from [Gil Levi and Tal Hassner](https://talhassner.github.io/home/publication/2015_CVPR)
- Face detection model from OpenCV DNN samples

## License

This project is for educational purposes. Please refer to the original model licenses for commercial use.
