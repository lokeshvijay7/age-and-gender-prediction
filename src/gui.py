"""
GUI Module for Age and Gender Prediction System
Provides a Tkinter-based interface for image, video, and webcam processing.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import cv2
import numpy as np
import threading
import time
from typing import Optional

from src.detector import AgeGenderDetector
from src.utils import (
    draw_predictions, validate_image_file, validate_video_file,
    resize_for_display, create_result_text, calculate_fps
)


class AgeGenderGUI:
    """
    Main GUI application for age and gender prediction.
    """
    
    def __init__(self, root: tk.Tk):
        """
        Initialize the GUI.
        
        Args:
            root: Tkinter root window
        """
        self.root = root
        self.root.title("Age and Gender Prediction System")
        self.root.geometry("1200x700")
        self.root.configure(bg='#2b2b2b')
        
        # Initialize detector
        try:
            self.detector = AgeGenderDetector()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load models:\n{e}")
            self.root.destroy()
            return
        
        # State variables
        self.current_mode = tk.StringVar(value="image")
        self.is_webcam_running = False
        self.is_video_running = False
        self.video_capture = None
        self.current_image = None
        self.current_photo = None  # Store PhotoImage reference
        self.video_thread = None
        self.webcam_thread = None
        
        # Create GUI components
        self._create_widgets()
    
    def _create_widgets(self):
        """Create all GUI widgets."""
        # Title
        title_frame = tk.Frame(self.root, bg='#1e1e1e', height=60)
        title_frame.pack(fill=tk.X, padx=10, pady=(10, 5))
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(
            title_frame,
            text="🎯 Age and Gender Prediction System",
            font=('Arial', 20, 'bold'),
            bg='#1e1e1e',
            fg='#00ff88'
        )
        title_label.pack(pady=10)
        
        # Main container
        main_container = tk.Frame(self.root, bg='#2b2b2b')
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Left panel - Controls
        left_panel = tk.Frame(main_container, bg='#1e1e1e', width=250)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 5))
        left_panel.pack_propagate(False)
        
        self._create_control_panel(left_panel)
        
        # Center panel - Display
        center_panel = tk.Frame(main_container, bg='#1e1e1e')
        center_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        self._create_display_panel(center_panel)
        
        # Right panel - Results
        right_panel = tk.Frame(main_container, bg='#1e1e1e', width=300)
        right_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(5, 0))
        right_panel.pack_propagate(False)
        
        self._create_results_panel(right_panel)
        
        # Status bar
        self._create_status_bar()
    
    def _create_control_panel(self, parent):
        """Create control panel with mode selection and buttons."""
        # Mode selection
        mode_label = tk.Label(
            parent,
            text="Select Mode",
            font=('Arial', 12, 'bold'),
            bg='#1e1e1e',
            fg='#ffffff'
        )
        mode_label.pack(pady=(20, 10))
        
        # Radio buttons for mode
        modes = [
            ("📷 Image", "image"),
            ("🎥 Video File", "video"),
            ("📹 Live Webcam", "webcam")
        ]
        
        for text, mode in modes:
            rb = tk.Radiobutton(
                parent,
                text=text,
                variable=self.current_mode,
                value=mode,
                font=('Arial', 11),
                bg='#1e1e1e',
                fg='#ffffff',
                selectcolor='#2b2b2b',
                activebackground='#1e1e1e',
                activeforeground='#00ff88',
                command=self._on_mode_change
            )
            rb.pack(anchor=tk.W, padx=20, pady=5)
        
        # Separator
        ttk.Separator(parent, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=20, padx=10)
        
        # Buttons frame
        btn_frame = tk.Frame(parent, bg='#1e1e1e')
        btn_frame.pack(fill=tk.X, padx=10)
        
        # Upload Image button
        self.upload_image_btn = tk.Button(
            btn_frame,
            text="📁 Upload Image",
            command=self._upload_image,
            font=('Arial', 10, 'bold'),
            bg='#00ff88',
            fg='#000000',
            activebackground='#00cc6a',
            cursor='hand2',
            relief=tk.FLAT,
            padx=10,
            pady=8
        )
        self.upload_image_btn.pack(fill=tk.X, pady=5)
        
        # Upload Video button
        self.upload_video_btn = tk.Button(
            btn_frame,
            text="📁 Upload Video",
            command=self._upload_video,
            font=('Arial', 10, 'bold'),
            bg='#4a4a4a',
            fg='#ffffff',
            activebackground='#5a5a5a',
            cursor='hand2',
            relief=tk.FLAT,
            padx=10,
            pady=8,
            state=tk.DISABLED
        )
        self.upload_video_btn.pack(fill=tk.X, pady=5)
        
        # Start Webcam button
        self.webcam_btn = tk.Button(
            btn_frame,
            text="▶️ Start Webcam",
            command=self._toggle_webcam,
            font=('Arial', 10, 'bold'),
            bg='#4a4a4a',
            fg='#ffffff',
            activebackground='#5a5a5a',
            cursor='hand2',
            relief=tk.FLAT,
            padx=10,
            pady=8,
            state=tk.DISABLED
        )
        self.webcam_btn.pack(fill=tk.X, pady=5)
        
        # Clear button
        self.clear_btn = tk.Button(
            btn_frame,
            text="🗑️ Clear",
            command=self._clear_display,
            font=('Arial', 10, 'bold'),
            bg='#ff4444',
            fg='#ffffff',
            activebackground='#cc3333',
            cursor='hand2',
            relief=tk.FLAT,
            padx=10,
            pady=8
        )
        self.clear_btn.pack(fill=tk.X, pady=5)
        
        # Settings frame
        ttk.Separator(parent, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=20, padx=10)
        
        settings_label = tk.Label(
            parent,
            text="Settings",
            font=('Arial', 12, 'bold'),
            bg='#1e1e1e',
            fg='#ffffff'
        )
        settings_label.pack(pady=(0, 10))
        
        # Confidence threshold
        conf_frame = tk.Frame(parent, bg='#1e1e1e')
        conf_frame.pack(fill=tk.X, padx=20, pady=5)
        
        conf_label = tk.Label(
            conf_frame,
            text="Confidence:",
            font=('Arial', 9),
            bg='#1e1e1e',
            fg='#cccccc'
        )
        conf_label.pack(side=tk.LEFT)
        
        self.conf_var = tk.DoubleVar(value=0.7)
        self.conf_value_label = tk.Label(
            conf_frame,
            text="70%",
            font=('Arial', 9, 'bold'),
            bg='#1e1e1e',
            fg='#00ff88'
        )
        self.conf_value_label.pack(side=tk.RIGHT)
        
        conf_slider = tk.Scale(
            parent,
            from_=0.3,
            to=0.95,
            resolution=0.05,
            orient=tk.HORIZONTAL,
            variable=self.conf_var,
            command=self._update_confidence_label,
            bg='#2b2b2b',
            fg='#ffffff',
            highlightthickness=0,
            troughcolor='#1e1e1e',
            activebackground='#00ff88'
        )
        conf_slider.pack(fill=tk.X, padx=20, pady=(0, 10))
    
    def _create_display_panel(self, parent):
        """Create image/video display panel."""
        display_label = tk.Label(
            parent,
            text="Display",
            font=('Arial', 12, 'bold'),
            bg='#1e1e1e',
            fg='#ffffff'
        )
        display_label.pack(pady=10)
        
        # Canvas for image/video display
        self.canvas = tk.Canvas(
            parent,
            bg='#000000',
            highlightthickness=0
        )
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        # Placeholder text
        self.placeholder_text = self.canvas.create_text(
            400, 300,
            text="Select a mode and upload content\nor start webcam",
            font=('Arial', 14),
            fill='#666666',
            justify=tk.CENTER
        )
    
    def _create_results_panel(self, parent):
        """Create results display panel."""
        results_label = tk.Label(
            parent,
            text="Results",
            font=('Arial', 12, 'bold'),
            bg='#1e1e1e',
            fg='#ffffff'
        )
        results_label.pack(pady=10)
        
        # Results text widget
        self.results_text = tk.Text(
            parent,
            font=('Arial', 10),
            bg='#2b2b2b',
            fg='#ffffff',
            wrap=tk.WORD,
            relief=tk.FLAT,
            padx=10,
            pady=10
        )
        self.results_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        # Initial message
        self.results_text.insert('1.0', "No predictions yet.\n\nUpload an image, video, or start webcam to begin.")
        self.results_text.config(state=tk.DISABLED)
    
    def _create_status_bar(self):
        """Create status bar at bottom."""
        self.status_bar = tk.Label(
            self.root,
            text="Ready",
            font=('Arial', 9),
            bg='#1e1e1e',
            fg='#00ff88',
            anchor=tk.W,
            relief=tk.FLAT,
            padx=10,
            pady=5
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def _on_mode_change(self):
        """Handle mode change."""
        mode = self.current_mode.get()
        
        # Stop any running processes
        self._stop_all_processes()
        
        # Update button states
        if mode == "image":
            self.upload_image_btn.config(state=tk.NORMAL, bg='#00ff88')
            self.upload_video_btn.config(state=tk.DISABLED, bg='#4a4a4a')
            self.webcam_btn.config(state=tk.DISABLED, bg='#4a4a4a')
        elif mode == "video":
            self.upload_image_btn.config(state=tk.DISABLED, bg='#4a4a4a')
            self.upload_video_btn.config(state=tk.NORMAL, bg='#00ff88')
            self.webcam_btn.config(state=tk.DISABLED, bg='#4a4a4a')
        elif mode == "webcam":
            self.upload_image_btn.config(state=tk.DISABLED, bg='#4a4a4a')
            self.upload_video_btn.config(state=tk.DISABLED, bg='#4a4a4a')
            self.webcam_btn.config(state=tk.NORMAL, bg='#00ff88')
        
        self._update_status(f"Mode: {mode.capitalize()}")
    
    def _update_confidence_label(self, value):
        """Update confidence threshold label."""
        self.conf_value_label.config(text=f"{int(float(value) * 100)}%")
    
    def _upload_image(self):
        """Handle image upload."""
        file_path = filedialog.askopenfilename(
            title="Select Image",
            filetypes=[
                ("Image files", "*.jpg *.jpeg *.png *.bmp *.tiff *.webp"),
                ("All files", "*.*")
            ]
        )
        
        if file_path and validate_image_file(file_path):
            self._process_image(file_path)
        elif file_path:
            messagebox.showerror("Error", "Invalid image file")
    
    def _upload_video(self):
        """Handle video upload."""
        file_path = filedialog.askopenfilename(
            title="Select Video",
            filetypes=[
                ("Video files", "*.mp4 *.avi *.mov *.mkv *.flv *.wmv"),
                ("All files", "*.*")
            ]
        )
        
        if file_path and validate_video_file(file_path):
            self._process_video(file_path)
        elif file_path:
            messagebox.showerror("Error", "Invalid video file")
    
    def _toggle_webcam(self):
        """Toggle webcam on/off."""
        if self.is_webcam_running:
            self._stop_webcam()
        else:
            self._start_webcam()
    
    def _process_image(self, file_path: str):
        """Process and display image with predictions."""
        self._update_status("Processing image...")
        
        try:
            # Read image
            image = cv2.imread(file_path)
            if image is None:
                raise ValueError("Failed to load image")
            
            # Get predictions
            results = self.detector.predict(image, self.conf_var.get())
            
            # Draw predictions
            annotated = draw_predictions(
                image,
                results['faces'],
                results['ages'],
                results['genders'],
                results['age_confidences'],
                results['gender_confidences']
            )
            
            # Display image
            self._display_image(annotated)
            
            # Update results
            result_text = create_result_text(
                len(results['faces']),
                results['ages'],
                results['genders'],
                results['age_confidences'],
                results['gender_confidences']
            )
            self._update_results(result_text)
            
            self._update_status(f"Processed: {len(results['faces'])} face(s) detected")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to process image:\n{e}")
            self._update_status("Error processing image")
    
    def _process_video(self, file_path: str):
        """Process video file."""
        self._stop_all_processes()
        
        try:
            self.video_capture = cv2.VideoCapture(file_path)
            if not self.video_capture.isOpened():
                raise ValueError("Failed to open video")
            
            self.is_video_running = True
            self.video_thread = threading.Thread(target=self._video_loop, daemon=True)
            self.video_thread.start()
            
            self._update_status("Processing video...")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to process video:\n{e}")
            self._update_status("Error processing video")
    
    def _start_webcam(self):
        """Start webcam capture."""
        try:
            self.video_capture = cv2.VideoCapture(0)
            if not self.video_capture.isOpened():
                raise ValueError("Failed to open webcam")
            
            self.is_webcam_running = True
            self.webcam_btn.config(text="⏹️ Stop Webcam", bg='#ff4444')
            
            self.webcam_thread = threading.Thread(target=self._webcam_loop, daemon=True)
            self.webcam_thread.start()
            
            self._update_status("Webcam running...")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start webcam:\n{e}")
            self._update_status("Error starting webcam")
    
    def _stop_webcam(self):
        """Stop webcam capture."""
        self.is_webcam_running = False
        if self.video_capture:
            self.video_capture.release()
        self.webcam_btn.config(text="▶️ Start Webcam", bg='#00ff88')
        self._update_status("Webcam stopped")
    
    def _video_loop(self):
        """Video processing loop."""
        while self.is_video_running and self.video_capture.isOpened():
            ret, frame = self.video_capture.read()
            
            if not ret:
                self.is_video_running = False
                break
            
            # Process frame
            results = self.detector.predict(frame, self.conf_var.get())
            
            # Draw predictions
            annotated = draw_predictions(
                frame,
                results['faces'],
                results['ages'],
                results['genders'],
                results['age_confidences'],
                results['gender_confidences']
            )
            
            # Display frame
            self.root.after(0, self._display_image, annotated)
            
            # Small delay
            time.sleep(0.03)
        
        if self.video_capture:
            self.video_capture.release()
        self.root.after(0, self._update_status, "Video processing complete")
    
    def _webcam_loop(self):
        """Webcam processing loop."""
        frame_count = 0
        start_time = time.time()
        
        while self.is_webcam_running and self.video_capture.isOpened():
            ret, frame = self.video_capture.read()
            
            if not ret:
                break
            
            # Process frame
            results = self.detector.predict(frame, self.conf_var.get())
            
            # Draw predictions
            annotated = draw_predictions(
                frame,
                results['faces'],
                results['ages'],
                results['genders'],
                results['age_confidences'],
                results['gender_confidences']
            )
            
            # Calculate and display FPS
            frame_count += 1
            fps = calculate_fps(start_time, frame_count)
            cv2.putText(annotated, f"FPS: {fps:.1f}", (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            # Display frame
            self.root.after(0, self._display_image, annotated)
            
            # Update results
            if frame_count % 30 == 0:  # Update every 30 frames
                result_text = create_result_text(
                    len(results['faces']),
                    results['ages'],
                    results['genders'],
                    results['age_confidences'],
                    results['gender_confidences']
                )
                self.root.after(0, self._update_results, result_text)
    
    def _display_image(self, image: np.ndarray):
        """Display image on canvas."""
        try:
            # Remove placeholder
            if self.placeholder_text:
                self.canvas.delete(self.placeholder_text)
                self.placeholder_text = None
            
            # Update canvas to get actual size
            self.canvas.update_idletasks()
            
            # Get canvas dimensions (use minimum size if not yet rendered)
            canvas_width = max(self.canvas.winfo_width(), 600)
            canvas_height = max(self.canvas.winfo_height(), 400)
            
            # Resize for display
            display_img = resize_for_display(image, 
                                             canvas_width - 20,
                                             canvas_height - 20)
            
            # Convert to PhotoImage
            image_rgb = cv2.cvtColor(display_img, cv2.COLOR_BGR2RGB)
            image_pil = Image.fromarray(image_rgb)
            photo = ImageTk.PhotoImage(image_pil)
            
            # Store reference BEFORE creating image on canvas
            self.current_photo = photo
            
            # Update canvas
            self.canvas.delete("all")
            
            # Get actual canvas size after update
            canvas_width = max(self.canvas.winfo_width(), 600)
            canvas_height = max(self.canvas.winfo_height(), 400)
            
            self.canvas.create_image(
                canvas_width // 2,
                canvas_height // 2,
                image=photo,
                anchor=tk.CENTER
            )
            
            # Force canvas update
            self.canvas.update()
            
        except Exception as e:
            print(f"Error displaying image: {e}")
            import traceback
            traceback.print_exc()
    
    def _update_results(self, text: str):
        """Update results text widget."""
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete('1.0', tk.END)
        self.results_text.insert('1.0', text)
        self.results_text.config(state=tk.DISABLED)
    
    def _update_status(self, text: str):
        """Update status bar."""
        self.status_bar.config(text=text)
    
    def _clear_display(self):
        """Clear display and results."""
        self._stop_all_processes()
        
        self.canvas.delete("all")
        self.placeholder_text = self.canvas.create_text(
            400, 300,
            text="Select a mode and upload content\nor start webcam",
            font=('Arial', 14),
            fill='#666666',
            justify=tk.CENTER
        )
        
        self._update_results("No predictions yet.\n\nUpload an image, video, or start webcam to begin.")
        self._update_status("Ready")
    
    def _stop_all_processes(self):
        """Stop all running video/webcam processes."""
        self.is_video_running = False
        self.is_webcam_running = False
        
        if self.video_capture:
            self.video_capture.release()
            self.video_capture = None
        
        if self.webcam_btn.cget('text') == "⏹️ Stop Webcam":
            self.webcam_btn.config(text="▶️ Start Webcam", bg='#00ff88')
    
    def run(self):
        """Start the GUI main loop."""
        self.root.mainloop()
