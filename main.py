#!/usr/bin/env python3
"""
Traveling Salesman Problem Game - Main Entry Point (PyQt5 Version)
"""
import sys
import os
import traceback
import logging
from PyQt5.QtWidgets import QApplication, QMessageBox

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("tsp_game.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("Main")

def main():
    logger.info("Starting Traveling Salesman Game")
    try:
        # Create PyQt application
        app = QApplication(sys.argv)
        
        # Import the GUI components
        from gui.game_window_qt import GameWindowQt
        
        # Create and show the application window
        window = GameWindowQt()
        window.show()
        
        logger.info("Application initialized, entering main event loop")
        
        # Enter the Qt main event loop
        return app.exec_()
    except ImportError as e:
        logger.error(f"Import error: {str(e)}")
        error_msg = f"Error importing required modules: {str(e)}\n\n"
        error_msg += "Please make sure you have activated your virtual environment and installed all requirements:\n\n"
        error_msg += "cd \"/Users/susithalwis/Documents/PDSA CW/traveling_salesman_game\"\n"
        error_msg += "source venv_new/bin/activate\n"
        error_msg += "pip install -r requirements.txt"
        
        show_error_message("Import Error", error_msg)
        return 1
    except Exception as e:
        logger.error(f"Unhandled exception: {str(e)}")
        logger.error(traceback.format_exc())
        error_msg = "An unexpected error occurred:\n\n"
        error_msg += str(e)
        error_msg += "\n\nSee tsp_game.log for details."
        
        show_error_message("Error", error_msg) 
        return 1

def show_error_message(title, message):
    """Display an error message to the user"""
    try:
        app = QApplication(sys.argv) if not QApplication.instance() else QApplication.instance()
        QMessageBox.critical(None, title, message)
    except:
        print(f"{title}: {message}")

if __name__ == "__main__":
    sys.exit(main())