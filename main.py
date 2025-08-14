#!/usr/bin/env python3
"""
Phrase Bridge - Language Translation Desktop Application
Main entry point for the application
"""

import tkinter as tk
from gui import TranslationApp

def main():
    """Main function to start the translation application"""
    # Create the root window
    root = tk.Tk()
    
    # Create and run the application
    app = TranslationApp(root)
    
    # Start the GUI event loop
    root.mainloop()

if __name__ == "__main__":
    main()
