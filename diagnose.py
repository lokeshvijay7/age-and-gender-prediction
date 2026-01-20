"""
Quick diagnostic script to test webcam and display functionality.
"""

import cv2
import numpy as np
from PIL import Image, ImageTk
import tkinter as tk


def test_webcam_capture():
    """Test if webcam can capture frames."""
    print("Testing webcam capture...")
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("❌ Failed to open webcam")
        return False
    
    ret, frame = cap.read()
    cap.release()
    
    if not ret:
        print("❌ Failed to read frame from webcam")
        return False
    
    print(f"✓ Webcam capture successful! Frame shape: {frame.shape}")
    return True


def test_image_conversion():
    """Test image conversion to PhotoImage."""
    print("\nTesting image conversion...")
    
    # Create test image
    test_img = np.zeros((480, 640, 3), dtype=np.uint8)
    test_img[:] = (100, 150, 200)  # Fill with color
    
    try:
        # Convert BGR to RGB
        img_rgb = cv2.cvtColor(test_img, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(img_rgb)
        
        # Create Tkinter root (needed for PhotoImage)
        root = tk.Tk()
        root.withdraw()
        
        photo = ImageTk.PhotoImage(img_pil)
        
        print(f"✓ Image conversion successful! PhotoImage size: {photo.width()}x{photo.height()}")
        
        root.destroy()
        return True
        
    except Exception as e:
        print(f"❌ Image conversion failed: {e}")
        return False


def test_canvas_display():
    """Test displaying image on canvas."""
    print("\nTesting canvas display...")
    
    try:
        root = tk.Tk()
        root.title("Canvas Test")
        root.geometry("800x600")
        
        canvas = tk.Canvas(root, bg='black', width=800, height=600)
        canvas.pack(fill=tk.BOTH, expand=True)
        
        # Force canvas to update
        root.update_idletasks()
        
        # Create test image
        test_img = np.zeros((480, 640, 3), dtype=np.uint8)
        test_img[:] = (0, 255, 0)  # Green
        
        # Add text to image
        cv2.putText(test_img, "TEST IMAGE", (200, 240),
                   cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3)
        
        # Convert and display
        img_rgb = cv2.cvtColor(test_img, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(img_rgb)
        photo = ImageTk.PhotoImage(img_pil)
        
        # Store reference
        canvas.image = photo
        
        # Get canvas size
        canvas.update_idletasks()
        canvas_width = max(canvas.winfo_width(), 800)
        canvas_height = max(canvas.winfo_height(), 600)
        
        print(f"Canvas size: {canvas_width}x{canvas_height}")
        
        # Display image
        canvas.create_image(
            canvas_width // 2,
            canvas_height // 2,
            image=photo,
            anchor=tk.CENTER
        )
        
        canvas.update()
        
        print("✓ Canvas display test window opened!")
        print("  You should see a green image with 'TEST IMAGE' text")
        print("  Close the window to continue...")
        
        root.mainloop()
        return True
        
    except Exception as e:
        print(f"❌ Canvas display failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all diagnostic tests."""
    print("=" * 60)
    print("Webcam and Display Diagnostic Tool")
    print("=" * 60)
    print()
    
    results = []
    
    # Test 1: Webcam capture
    results.append(("Webcam Capture", test_webcam_capture()))
    
    # Test 2: Image conversion
    results.append(("Image Conversion", test_image_conversion()))
    
    # Test 3: Canvas display
    print("\nStarting canvas display test...")
    print("This will open a test window. Please check if you can see the image.")
    input("Press Enter to continue...")
    results.append(("Canvas Display", test_canvas_display()))
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "❌ FAIL"
        print(f"{test_name:.<40} {status}")
    
    print()
    
    if all(r[1] for r in results):
        print("✓ All tests passed! The application should work correctly.")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")


if __name__ == "__main__":
    main()
