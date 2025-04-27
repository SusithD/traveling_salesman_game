"""
Main game window for the Traveling Salesman Problem game
"""
import logging
import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QScrollArea, QSizePolicy
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

from gui.game_flow_manager import GameFlowManager

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='tsp_game.log',
    filemode='a'
)
logger = logging.getLogger("GameWindow")

class GameWindow(QMainWindow):
    """
    Main window for the Traveling Salesman Problem game
    """
    def __init__(self):
        super().__init__()
        
        # Set application properties
        self.setWindowTitle("Traveling Salesman Game")
        self.setMinimumSize(1000, 700)
        
        # Set up the window
        self.setup_ui()
        
        # Center the window on the screen
        self.center_on_screen()
        
        # Show the window
        self.show()
    
    def setup_ui(self):
        """Setup the UI components"""
        # Create central widget
        central_widget = QWidget(self)
        central_widget.setObjectName("centralWidget")
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Create a scroll area to contain the game content
        self.scroll_area = QScrollArea()
        self.scroll_area.setObjectName("mainScrollArea")
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QScrollArea.NoFrame)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        # Create a container widget for the scroll area
        scroll_container = QWidget()
        scroll_container.setObjectName("scrollContainer")
        scroll_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        # Layout for the scroll container
        container_layout = QVBoxLayout(scroll_container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(0)
        
        # Create game flow manager
        self.game_flow_manager = GameFlowManager(self)
        game_widget = self.game_flow_manager.get_widget()
        game_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.MinimumExpanding)
        
        # Add game widget to container layout
        container_layout.addWidget(game_widget)
        
        # Set the container as the scroll area's widget
        self.scroll_area.setWidget(scroll_container)
        
        # Add scroll area to the main layout
        main_layout.addWidget(self.scroll_area)
    
    def center_on_screen(self):
        """Center the window on the screen"""
        frame_geometry = self.frameGeometry()
        screen_center = QApplication.desktop().availableGeometry().center()
        frame_geometry.moveCenter(screen_center)
        self.move(frame_geometry.topLeft())
    
    def run(self):
        """Run the application"""
        return QApplication.exec_()


def run_application():
    """Run the TSP game application"""
    # Create Qt application
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Use Fusion style for consistent look across platforms
    
    # Set application stylesheet for dark theme
    stylesheet = """
    QWidget {
        background-color: #1e1e1e;
        color: #ffffff;
        font-family: 'Segoe UI', Arial, sans-serif;
    }
    
    QLabel {
        color: #ffffff;
    }
    
    QPushButton {
        background-color: #3498db;
        color: white;
        border: none;
        padding: 8px 16px;
        border-radius: 4px;
    }
    
    QPushButton:hover {
        background-color: #2980b9;
    }
    
    QPushButton:pressed {
        background-color: #1c5a85;
    }
    
    QLineEdit, QTextEdit, QPlainTextEdit {
        background-color: #333333;
        color: #ffffff;
        border: 1px solid #555555;
        padding: 5px;
        border-radius: 3px;
    }
    
    QComboBox {
        background-color: #333333;
        color: #ffffff;
        border: 1px solid #555555;
        padding: 5px;
        border-radius: 3px;
    }
    
    QComboBox::drop-down {
        border: none;
        padding-right: 10px;
    }
    
    QComboBox QAbstractItemView {
        background-color: #333333;
        color: #ffffff;
        selection-background-color: #3498db;
        selection-color: #ffffff;
    }
    
    QTableWidget {
        background-color: #333333;
        color: #ffffff;
        gridline-color: #555555;
    }
    
    QHeaderView::section {
        background-color: #2c2c2c;
        color: #ffffff;
        padding: 5px;
        border: 1px solid #555555;
    }
    
    QTabWidget::pane {
        border: 1px solid #555555;
    }
    
    QTabBar::tab {
        background-color: #2c2c2c;
        color: #aaaaaa;
        padding: 8px 12px;
        border: 1px solid #555555;
        border-bottom: none;
        margin-right: 2px;
    }
    
    QTabBar::tab:selected {
        background-color: #3498db;
        color: #ffffff;
    }
    
    QTabBar::tab:hover:!selected {
        background-color: #3c3c3c;
    }
    
    /* Enhanced scrollbar styling for better user experience */
    QScrollArea {
        border: none;
        background-color: transparent;
    }
    
    QScrollBar:vertical {
        background-color: #2c2c2c;
        width: 12px;
        border-radius: 6px;
        margin: 0px;
    }
    
    QScrollBar::handle:vertical {
        background-color: #555555;
        min-height: 30px;
        border-radius: 6px;
    }
    
    QScrollBar::handle:vertical:hover {
        background-color: #666666;
    }
    
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
        height: 0px;
    }
    
    QScrollBar:horizontal {
        background-color: #2c2c2c;
        height: 12px;
        border-radius: 6px;
        margin: 0px;
    }
    
    QScrollBar::handle:horizontal {
        background-color: #555555;
        min-width: 30px;
        border-radius: 6px;
    }
    
    QScrollBar::handle:horizontal:hover {
        background-color: #666666;
    }
    
    QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
        width: 0px;
    }
    
    /* Make nested scroll areas work better together */
    QScrollArea QScrollArea {
        background-color: transparent;
    }
    
    /* Fixed sizing issues with content being cut off */
    #scrollContainer {
        background-color: transparent;
    }
    
    #mainScrollArea {
        background-color: transparent;
    }
    
    /* Ensure content inside scroll areas is properly sized */
    QScrollArea > QWidget > QWidget {
        background-color: transparent;
    }
    
    QProgressBar {
        border: 1px solid #555555;
        border-radius: 3px;
        background: #333333;
        text-align: center;
    }
    
    QProgressBar::chunk {
        background-color: #3498db;
    }
    """
    app.setStyleSheet(stylesheet)
    
    # Create and run the main window
    window = GameWindow()
    return app.exec_()

if __name__ == "__main__":
    sys.exit(run_application())
