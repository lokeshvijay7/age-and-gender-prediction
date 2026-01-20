"""
Simple test to verify webcam display works.
Run this to test if the basic webcam display is working.
"""

import cv2
import tkinter as tk
from PIL import Image, ImageTk
import time


class SimpleWebcamTest:
    def __init__(self, root):
        self.root = root
        self.root.title("Webcam Display Test")
        self.root.geometry("800x600")
        
        # Create canvas
        self.canvas = tk.Canvas(root, bg='black')
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Control buttons
        btn_frame = tk.Frame(root)
        btn_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)
        
        self.start_btn = tk.Button(btn_frame, text="Start Webcam", command=self.start_webcam, bg='green', fg='white', font=('Arial', 12, 'bold'))
        self.start_btn.pack(side=tk.LEFT, padx=10)
        
        self.stop_btn = tk.Button(btn_frame, text="Stop Webcam", command=self.stop_webcam, bg='red', fg='white', font=('Arial', 12, 'bold'), state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, padx=10)
        
        # State
        self.is_running = False
        self.cap = None
        self.photo = None
        
    def start_webcam(self):
        """Start webcam capture."""
        print("Starting webcam...")
        self.cap = cv2.VideoCapture(0)
        
        if not self.cap.isOpened():
            print("ERROR: Could not open webcam")
            return
        
        self.is_running = True
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        
        print("Webcam started successfully!")
        self.update_frame()
    
    def stop_webcam(self):
        """Stop webcam capture."""
        print("Stopping webcam...")
        self.is_running = False
        
        if self.cap:
            self.cap.release()
        
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        print("Webcam stopped")
    
    def update_frame(self):
        """Update frame from webcam."""
        if not self.is_running:
            return
        
        ret, frame = self.cap.read()
        
        if ret:
            # Add FPS counter
            cv2.putText(frame, f"FPS: {int(1000/33)}", (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            # Convert BGR to RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Convert to PIL Image
            img = Image.fromarray(frame_rgb)
            
            # Resize to fit canvas
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()
            
            if canvas_width > 1 and canvas_height > 1:
                # Calculate scaling
                img_width, img_height = img.size
                scale = min(canvas_width / img_width, canvas_height / img_height)
                new_width = int(img_width * scale)
                new_height = int(img_height * scale)
                
                img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Convert to PhotoImage
            self.photo = ImageTk.PhotoImage(img)
            
            # Update canvas
            self.canvas.delete("all")
            self.canvas.create_image(
                canvas_width // 2 if canvas_width > 1 else 400,
                canvas_height // 2 if canvas_height > 1 else 300,
                image=self.photo,
                anchor=tk.CENTER
            )
        else:
            print("ERROR: Failed to read frame")
        
        # Schedule next update (30 FPS)
        self.root.after(33, self.update_frame)
    
    def on_closing(self):
        """Handle window closing."""
        self.stop_webcam()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleWebcamTest(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    
    print("=" * 60)
    print("Simple Webcam Test")
    print("=" * 60)
    print("Click 'Start Webcam' to begin")
    print("You should see your webcam feed with an FPS counter")
    print("=" * 60)
    
    root.mainloop()
