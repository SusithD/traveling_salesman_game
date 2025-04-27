#!/usr/bin/env python3
"""
Traveling Salesman Problem Game
Educational tool that gamifies learning about TSP algorithms
"""
import sys
import logging
from PyQt5.QtWidgets import QApplication
from gui.game_window_qt import GameWindow

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='tsp_game.log',
    filemode='a'
)
logger = logging.getLogger(__name__)

def main():
    """Main function to start the application"""
    logger.info("Starting Traveling Salesman Game")
    
    # Create Qt application
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Use Fusion style for consistent look across platforms
    
    # Create and show the main window
    window = GameWindow()
    
    # Start the application event loop
    exit_code = app.exec_()
    
    # Log application exit
    logger.info(f"Application exited with code {exit_code}")
    return exit_code

if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        logger.exception("Unhandled exception")
        print(f"Error: {str(e)}")
        sys.exit(1)