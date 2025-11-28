"""
Main entry point for the Logical Expression Analyzer
"""
import tkinter as tk
from gui import LogicalAnalyzerApp

def main():
    """Initialize and run the application"""
    root = tk.Tk()
    app = LogicalAnalyzerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()