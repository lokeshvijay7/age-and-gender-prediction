# Quick Start Guide

## Age and Gender Prediction System

### 🚀 Getting Started in 3 Steps

#### 1. Install Dependencies
```bash
python -m pip install -r requirements.txt
```

#### 2. Download Models (if not already done)
```bash
python download_models.py
```

#### 3. Run the Application
```bash
python main.py
```

---

## 📖 How to Use

### Image Mode
1. Select **"📷 Image"** mode
2. Click **"📁 Upload Image"**
3. Choose an image file from your computer
4. View predictions with bounding boxes and confidence scores

### Video File Mode
1. Select **"🎥 Video File"** mode
2. Click **"📁 Upload Video"**
3. Choose a video file
4. Watch real-time predictions on each frame

### Live Webcam Mode
1. Select **"📹 Live Webcam"** mode
2. Click **"▶️ Start Webcam"**
3. See real-time age and gender predictions
4. Click **"⏹️ Stop Webcam"** when done

---

## ⚙️ Settings

### Confidence Threshold
- Adjust the slider to change face detection sensitivity
- **Lower values** (30-50%): Detect more faces (may include false positives)
- **Higher values** (70-95%): Only high-confidence detections (may miss some faces)
- **Recommended**: 70% for balanced results

---

## 📊 Understanding Results

### Age Predictions
The system predicts age in **8 groups**:
- 0-2 years (Baby)
- 4-6 years (Toddler)
- 8-12 years (Child)
- 15-20 years (Teenager)
- 25-32 years (Young Adult)
- 38-43 years (Adult)
- 48-53 years (Middle-aged)
- 60-100 years (Senior)

### Gender Predictions
- **Male** or **Female**
- Confidence score indicates prediction certainty

### Confidence Scores
- **90-100%**: Very confident prediction
- **70-89%**: Confident prediction
- **50-69%**: Moderate confidence
- **Below 50%**: Low confidence (take with caution)

---

## 💡 Tips for Best Results

1. **Good Lighting**: Ensure faces are well-lit
2. **Clear Faces**: Frontal or near-frontal faces work best
3. **Image Quality**: Higher resolution images give better results
4. **Multiple Faces**: The system can detect and predict for multiple faces
5. **Webcam Position**: Position yourself facing the camera directly

---

## 🔧 Troubleshooting

### "Models not found" error
- Run `python download_models.py` to download models
- Check that all 6 files exist in the `models/` directory

### Webcam not working
- Check webcam permissions
- Close other applications using the webcam
- Try restarting the application

### Low FPS on webcam
- Close other applications
- Reduce confidence threshold
- Use a better computer/GPU

### No faces detected
- Ensure good lighting
- Face the camera directly
- Lower the confidence threshold
- Check image quality

---

## 📁 Project Structure

```
age-gender/
├── models/                    # Pre-trained model files (6 files)
├── src/
│   ├── detector.py           # Core detection logic
│   ├── gui.py                # GUI interface
│   └── utils.py              # Helper functions
├── test_images/              # Place test images here
├── main.py                   # Run this to start the app
├── download_models.py        # Download models
├── test_system.py            # Test the system
├── requirements.txt          # Python dependencies
└── README.md                 # Full documentation
```

---

## 🎯 Next Steps

1. **Test with your own images**: Place images in `test_images/` folder
2. **Try the webcam**: Test real-time detection
3. **Experiment with settings**: Adjust confidence threshold
4. **Process videos**: Upload video files to analyze

---

## 📞 Need Help?

- Check the full [README.md](README.md) for detailed documentation
- Review model accuracy metrics
- Test with the provided test script: `python test_system.py`

---

**Enjoy using the Age and Gender Prediction System! 🎉**
