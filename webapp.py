import os
import cv2
import numpy as np
import base64
from flask import Flask, render_template, request, jsonify, url_for, redirect
from src.detector import AgeGenderDetector
from src.ad_manager import AdManager

app = Flask(__name__)
# Max upload size 16MB
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# Initialize core components
print("Initializing Detector Models...")
detector = AgeGenderDetector()
ad_manager = AdManager()

# Demographic Mapping
def map_age_to_category(age_range):
    if age_range in ['0-2', '4-6', '8-12']:
        return 'Child'
    elif age_range in ['15-20']:
        return 'Teen'
    elif age_range in ['25-32', '38-43']:
        return 'Adult'
    elif age_range in ['48-53', '60-100']:
        return 'Senior'
    return 'Adult' # Default fallback

@app.route('/')
def index():
    """Main page with webcam feed and dynamic ad display."""
    return render_template('index.html')

@app.route('/admin')
def admin():
    """Admin panel to upload and manage ads."""
    ads = ad_manager.get_all_ads()
    return render_template('admin.html', ads=ads)

@app.route('/upload_ad', methods=['POST'])
def upload_ad():
    """Handle ad uploads from the admin panel."""
    if 'ad_image' not in request.files:
        return redirect(url_for('admin'))
    
    file = request.files['ad_image']
    target_age = request.form.get('target_age', 'Any')
    target_gender = request.form.get('target_gender', 'Any')
    
    success, msg = ad_manager.add_ad(file, target_age, target_gender)
    return redirect(url_for('admin'))

@app.route('/delete_ad/<ad_id>', methods=['POST'])
def delete_ad(ad_id):
    """Handle ad deletions from the admin panel."""
    ad_manager.delete_ad(ad_id)
    return redirect(url_for('admin'))

@app.route('/edit_ad/<ad_id>', methods=['POST'])
def edit_ad(ad_id):
    """Handle ad edits from the admin panel."""
    target_age = request.form.get('target_age')
    target_gender = request.form.get('target_gender')
    if target_age and target_gender:
        ad_manager.edit_ad(ad_id, target_age, target_gender)
    return redirect(url_for('admin'))

@app.route('/predict', methods=['POST'])
def predict():
    """Receive a base64 frame from the frontend, run prediction, and return the relevant ad."""
    from src.utils import draw_predictions
    data = request.json
    if not data or 'image' not in data:
        return jsonify({'error': 'No image provided'}), 400
        
    try:
        # Decode base64 image
        img_data = data['image'].split(',')[1]
        nparr = np.frombuffer(base64.b64decode(img_data), np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if frame is None:
             return jsonify({'error': 'Invalid image format'}), 400

        # Run detection
        results = detector.predict(frame, conf_threshold=0.6)
        
        # Annotate the frame with bounding boxes
        annotated_frame = draw_predictions(
            frame,
            results['faces'],
            results['ages'],
            results['genders'],
            results['age_confidences'],
            results['gender_confidences']
        )
        
        # Encode annotated frame back to base64
        _, buffer = cv2.imencode('.jpg', annotated_frame)
        annotated_b64 = "data:image/jpeg;base64," + base64.b64encode(buffer).decode('utf-8')

        faces = results['faces']
        if len(faces) == 0:
            return jsonify({
                'detected': False, 
                'message': 'No face detected',
                'annotated_image': annotated_b64
            })
            
        # Get the first face's raw predictions
        raw_age = results['ages'][0]
        raw_gender = results['genders'][0]
        
        # Map to demographic category
        age_category = map_age_to_category(raw_age)
        
        # Get the most relevant ad
        ad = ad_manager.get_relevant_ad(age_category, raw_gender)
        
        ad_url = ad['url'] if ad else None
        
        return jsonify({
            'detected': True,
            'raw_age': raw_age,
            'age_category': age_category,
            'gender': raw_gender,
            'ad_url': ad_url,
            'annotated_image': annotated_b64
        })

    except Exception as e:
        print(f"Error in prediction: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Ensure templates and static folders exist
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static/ads', exist_ok=True)
    app.run(host='0.0.0.0', port=5000, debug=True)
