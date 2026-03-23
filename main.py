"""
Age and Gender Prediction System
Main entry point for the application.
"""

import tkinter as tk
from src.gui import AgeGenderGUI

def main():
    """Main function to run the application."""
    # Create root window
    root = tk.Tk()
    
    # Create and run GUI
    app = AgeGenderGUI(root)
    app.run()


if __name__ == "__main__":
    main()
