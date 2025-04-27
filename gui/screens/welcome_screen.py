"""
Welcome screen for the Traveling Salesman Problem game
"""
import logging
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QMessageBox, QGridLayout, QSpacerItem, QSizePolicy
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QPixmap

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
        # Create main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(50, 50, 50, 50)
        main_layout.setSpacing(30)
        
        # Add title
        title_label = QLabel("THE TRAVELING SALESMAN ADVENTURE")
        title_font = QFont("Arial", 24, QFont.Bold)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)
        
        # Add subtitle
        subtitle_label = QLabel("An Algorithm Learning Experience")
        subtitle_font = QFont("Arial", 16)
        subtitle_label.setFont(subtitle_font)
        subtitle_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(subtitle_label)
        
        # Description 
        description_text = (
            "Welcome to The Traveling Salesman Adventure! This interactive game will help you "
            "understand and compare different algorithms for solving the famous Traveling Salesman Problem. "
            "You'll create routes, make predictions, and see algorithms in action!"
        )
        description_label = QLabel(description_text)
        description_label.setWordWrap(True)
        description_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(description_label)
        
        # Add vertical spacer
        main_layout.addStretch(1)
        
        # Player name input
        name_layout = QHBoxLayout()
        name_label = QLabel("Enter your name:")
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Your name here")
        self.name_input.setMinimumWidth(200)
        
        name_layout.addStretch(1)
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.name_input)
        name_layout.addStretch(1)
        
        main_layout.addLayout(name_layout)
        
        # Add vertical spacer
        main_layout.addStretch(1)
        
        # Start button
        start_button = QPushButton("Begin Adventure")
        start_button.setMinimumSize(QSize(200, 50))
        start_button.setFont(QFont("Arial", 14))
        start_button.clicked.connect(self.on_start_clicked)
        
        button_layout = QHBoxLayout()
        button_layout.addStretch(1)
        button_layout.addWidget(start_button)
        button_layout.addStretch(1)
        
        main_layout.addLayout(button_layout)
        
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