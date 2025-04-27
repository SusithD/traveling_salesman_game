"""
Welcome screen for the Traveling Salesman Problem game
"""
import logging
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QMessageBox, QGridLayout, QSpacerItem, QSizePolicy, QFrame
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QPixmap, QColor, QPalette, QBrush, QLinearGradient

logger = logging.getLogger("WelcomeScreen")

class WelcomeScreen(QWidget):
    """
    Welcome screen for the TSP game, requesting player name and introducing the concept
    """
    
    def __init__(self, game_flow_manager):
        super().__init__()
        
        # Save reference to game flow manager
        self.game_flow_manager = game_flow_manager
        
        # Setup the UI
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the user interface"""
        # Create main layout with center alignment
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(50, 50, 50, 50)
        main_layout.setSpacing(30)
        main_layout.setAlignment(Qt.AlignCenter)
        
        # Create a central container frame
        central_frame = QFrame()
        central_frame.setObjectName("welcomeContainer")
        central_frame.setStyleSheet("""
            #welcomeContainer {
                background-color: rgba(26, 26, 26, 0.7);
                border-radius: 20px;
                border: 1px solid rgba(255, 255, 255, 0.1);
            }
        """)
        
        central_layout = QVBoxLayout(central_frame)
        central_layout.setContentsMargins(40, 40, 40, 40)
        central_layout.setSpacing(25)
        central_layout.setAlignment(Qt.AlignCenter)
        
        # Add logo/icon - creating a placeholder element
        icon_label = QLabel()
        icon_label.setFixedSize(120, 120)
        icon_label.setStyleSheet("""
            background-color: #3D5AFE;
            border-radius: 60px;
            color: white;
            font-size: 50px;
            font-weight: bold;
        """)
        icon_label.setText("TSP")
        icon_label.setAlignment(Qt.AlignCenter)
        central_layout.addWidget(icon_label, 0, Qt.AlignCenter)
        
        # Add title with enhanced styling
        title_label = QLabel("THE TRAVELING SALESMAN")
        title_label.setObjectName("welcomeTitle")
        title_label.setStyleSheet("""
            #welcomeTitle {
                color: white;
                font-size: 28px;
                font-weight: bold;
                letter-spacing: 1px;
            }
        """)
        title_label.setAlignment(Qt.AlignCenter)
        central_layout.addWidget(title_label)
        
        # Add subtitle with modern styling
        subtitle_label = QLabel("ADVENTURE")
        subtitle_label.setObjectName("welcomeSubtitle")
        subtitle_label.setStyleSheet("""
            #welcomeSubtitle {
                color: #3D5AFE;
                font-size: 36px;
                font-weight: bold;
                letter-spacing: 2px;
                margin-bottom: 10px;
            }
        """)
        subtitle_label.setAlignment(Qt.AlignCenter)
        central_layout.addWidget(subtitle_label)
        
        # Stylish separator
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setStyleSheet("""
            background-color: #3D5AFE;
            max-width: 100px;
            height: 3px;
            margin: 10px;
        """)
        central_layout.addWidget(separator, 0, Qt.AlignCenter)
        
        # Description with enhanced styling 
        description_text = (
            "Welcome to The Traveling Salesman Adventure! This interactive game will help you "
            "understand and compare different algorithms for solving the famous Traveling Salesman Problem. "
            "You'll create routes, make predictions, and see algorithms in action!"
        )
        description_label = QLabel(description_text)
        description_label.setObjectName("welcomeDescription")
        description_label.setStyleSheet("""
            #welcomeDescription {
                color: #CCCCCC;
                font-size: 15px;
                line-height: 150%;
                padding: 15px;
            }
        """)
        description_label.setWordWrap(True)
        description_label.setAlignment(Qt.AlignCenter)
        central_layout.addWidget(description_label)
        
        # Add vertical spacer
        central_layout.addSpacing(20)
        
        # Player name input with modern styling
        name_container = QFrame()
        name_container.setObjectName("nameInputContainer")
        name_container.setStyleSheet("""
            #nameInputContainer {
                background-color: rgba(33, 33, 33, 0.7);
                border-radius: 12px;
                padding: 5px;
            }
        """)
        name_layout = QVBoxLayout(name_container)
        name_layout.setContentsMargins(20, 20, 20, 20)
        name_layout.setSpacing(10)
        
        # Input label
        name_label = QLabel("What should we call you?")
        name_label.setStyleSheet("""
            color: #FFFFFF;
            font-size: 14px;
            font-weight: bold;
        """)
        name_label.setAlignment(Qt.AlignCenter)
        name_layout.addWidget(name_label)
        
        # Input field with modern styling
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter your name")
        self.name_input.setMinimumWidth(250)
        self.name_input.setMinimumHeight(40)
        self.name_input.setAlignment(Qt.AlignCenter)
        self.name_input.setStyleSheet("""
            QLineEdit {
                background-color: #212121;
                color: white;
                font-size: 16px;
                padding: 10px 15px;
                border: 1px solid #3D5AFE;
                border-radius: 8px;
            }
            QLineEdit:focus {
                border: 2px solid #536DFE;
                background-color: #262626;
            }
        """)
        name_layout.addWidget(self.name_input)
        
        # Add name container to central layout
        central_layout.addWidget(name_container, 0, Qt.AlignCenter)
        
        # Add vertical spacer
        central_layout.addSpacing(20)
        
        # Start button with modern styling
        start_button = QPushButton("BEGIN ADVENTURE")
        start_button.setObjectName("startButton")
        start_button.setStyleSheet("""
            #startButton {
                background-color: #3D5AFE;
                color: white;
                border: none;
                border-radius: 12px;
                padding: 15px 30px;
                font-size: 16px;
                font-weight: bold;
                letter-spacing: 1px;
                min-width: 250px;
            }
            #startButton:hover {
                background-color: #536DFE;
            }
            #startButton:pressed {
                background-color: #303F9F;
            }
        """)
        start_button.clicked.connect(self.on_start_clicked)
        central_layout.addWidget(start_button, 0, Qt.AlignCenter)
        
        # Add central frame to main layout
        main_layout.addWidget(central_frame, 0, Qt.AlignCenter)
        
    def on_start_clicked(self):
        """Handle the start button click event"""
        player_name = self.name_input.text().strip()
        
        if not player_name:
            QMessageBox.warning(self, "Name Required", "Please enter your name to continue.")
            return
        
        # Set the player name in the game state
        self.game_flow_manager.game_state.set_player_name(player_name)
        
        # Move to the mission screen
        self.game_flow_manager.show_mission_screen()
        
    def update_display(self):
        """Update the display (called when screen is shown)"""
        # Clear the name input field
        self.name_input.clear()
        self.name_input.setFocus()