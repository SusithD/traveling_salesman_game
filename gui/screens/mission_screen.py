"""
Mission briefing screen for the Traveling Salesman Problem game
"""
import logging
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QFrame, QGraphicsDropShadowEffect
)
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect, QEasingCurve, QTimer
from PyQt5.QtGui import QColor, QFont

logger = logging.getLogger("MissionScreen")

class MissionScreen(QWidget):
    """
    Mission briefing screen that introduces the game scenario and home city
    """
    def __init__(self, flow_manager):
        super().__init__()
        self.flow_manager = flow_manager
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the UI components"""
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(20)
        
        # Create container
        container = QFrame()
        container.setStyleSheet("""
            background-color: #111111;
            border: 2px solid #333333;
            border-radius: 15px;
            padding: 20px;
        """)
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(30, 30, 30, 30)
        container_layout.setSpacing(25)
        
        # Header
        header_layout = QHBoxLayout()
        
        mission_icon = QLabel("🧭")
        mission_icon.setStyleSheet("""
            font-size: 36px;
            padding: 10px;
            background-color: #f39c12;
            color: white;
            border-radius: 10px;
        """)
        header_layout.addWidget(mission_icon)
        
        header_text = QVBoxLayout()
        title = QLabel("Mission Briefing")
        title.setStyleSheet("""
            color: white;
            font-size: 24px;
            font-weight: bold;
        """)
        header_text.addWidget(title)
        
        subtitle = QLabel("Your traveling salesman adventure begins here")
        subtitle.setStyleSheet("color: #aaaaaa; font-size: 16px;")
        header_text.addWidget(subtitle)
        
        header_layout.addLayout(header_text)
        header_layout.addStretch()
        
        container_layout.addLayout(header_layout)
        
        # Add separator
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        separator.setStyleSheet("background-color: #333333; height: 1px;")
        container_layout.addWidget(separator)
        
        # Mission briefing content
        mission_frame = QFrame()
        mission_frame.setStyleSheet("""
            background-color: #222222;
            border-radius: 10px;
            padding: 20px;
        """)
        mission_layout = QVBoxLayout(mission_frame)
        mission_layout.setSpacing(20)
        
        # Greeting
        self.greeting_label = QLabel("Hello, Traveler!")
        self.greeting_label.setStyleSheet("""
            color: white;
            font-size: 20px;
            font-weight: bold;
        """)
        mission_layout.addWidget(self.greeting_label)
        
        # Scenario description
        scenario_text = QLabel(
            "You are a traveling salesman who needs to visit several cities and return "
            "home while traveling the shortest possible distance. Your journey begins and "
            "ends at your home city."
        )
        scenario_text.setWordWrap(True)
        scenario_text.setStyleSheet("""
            color: white;
            font-size: 15px;
            line-height: 24px;
        """)
        mission_layout.addWidget(scenario_text)
        
        # Home city announcement with dramatic styling
        home_city_frame = QFrame()
        home_city_frame.setStyleSheet("""
            background-color: #2c3e50;
            border: 1px solid #34495e;
            border-radius: 10px;
            padding: 15px;
        """)
        home_layout = QVBoxLayout(home_city_frame)
        
        home_title = QLabel("Your Home City")
        home_title.setStyleSheet("color: #3498db; font-size: 16px; font-weight: bold;")
        home_title.setAlignment(Qt.AlignCenter)
        home_layout.addWidget(home_title)
        
        self.home_city_label = QLabel("City X")  # Will be updated with actual home city
        self.home_city_label.setStyleSheet("""
            color: white;
            font-size: 30px;
            font-weight: bold;
        """)
        self.home_city_label.setAlignment(Qt.AlignCenter)
        # Add shadow effect to make it pop
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setColor(QColor("#3498db"))
        shadow.setOffset(0, 0)
        self.home_city_label.setGraphicsEffect(shadow)
        home_layout.addWidget(self.home_city_label)
        
        mission_layout.addWidget(home_city_frame)
        
        # Strategy hint
        hint_text = QLabel(
            "Your task is to select which cities to visit, predict which algorithm will find the "
            "shortest route, and then analyze the results to see if your prediction was correct."
        )
        hint_text.setWordWrap(True)
        hint_text.setStyleSheet("""
            color: #f39c12;
            font-size: 15px;
            font-style: italic;
            padding: 10px;
            background-color: rgba(243, 156, 18, 0.1);
            border-radius: 5px;
        """)
        mission_layout.addWidget(hint_text)
        
        # Add algorithms teaser
        algo_intro = QLabel("You'll be working with three different algorithms:")
        algo_intro.setStyleSheet("color: white; font-size: 15px; margin-top: 5px;")
        mission_layout.addWidget(algo_intro)
        
        # Algorithm cards layout
        algo_layout = QHBoxLayout()
        algo_layout.setSpacing(15)
        
        # Brute Force card
        bf_card = self.create_algo_card("Brute Force", "🧮", "#c0392b", "Tries all possible routes")
        algo_layout.addWidget(bf_card)
        
        # Nearest Neighbor card
        nn_card = self.create_algo_card("Nearest Neighbor", "📍", "#2980b9", "Always picks closest next city")
        algo_layout.addWidget(nn_card)
        
        # Dynamic Programming card
        dp_card = self.create_algo_card("Dynamic Programming", "⚙️", "#27ae60", "Uses optimal subproblems")
        algo_layout.addWidget(dp_card)
        
        mission_layout.addLayout(algo_layout)
        
        container_layout.addWidget(mission_frame)
        
        # Button area
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        back_button = QPushButton("← Back")
        back_button.setStyleSheet("""
            QPushButton {
                background-color: #333333;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px 15px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #444444;
            }
        """)
        back_button.clicked.connect(self.go_back)
        button_layout.addWidget(back_button)
        
        continue_button = QPushButton("Select Cities →")
        continue_button.setStyleSheet("""
            QPushButton {
                background-color: #f39c12;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px 20px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #e67e22;
            }
            QPushButton:pressed {
                background-color: #d35400;
            }
        """)
        continue_button.clicked.connect(self.continue_to_selection)
        button_layout.addWidget(continue_button)
        
        container_layout.addLayout(button_layout)
        
        # Add container to main layout
        main_layout.addWidget(container)
    
    def create_algo_card(self, title, icon, color, description):
        """Create a small card for algorithm brief"""
        card = QFrame()
        card.setStyleSheet(f"""
            background-color: #1a1a1a;
            border: 1px solid {color};
            border-radius: 8px;
            padding: 10px;
        """)
        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(5)
        card_layout.setContentsMargins(10, 10, 10, 10)
        
        # Icon with color background
        icon_label = QLabel(icon)
        icon_label.setStyleSheet(f"""
            font-size: 24px;
            padding: 8px;
            background-color: {color};
            color: white;
            border-radius: 5px;
            margin-bottom: 8px;
        """)
        icon_label.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(icon_label)
        
        # Title
        title_label = QLabel(title)
        title_label.setStyleSheet("color: white; font-weight: bold; font-size: 14px;")
        title_label.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(title_label)
        
        # Description
        desc_label = QLabel(description)
        desc_label.setStyleSheet("color: #aaaaaa; font-size: 12px;")
        desc_label.setAlignment(Qt.AlignCenter)
        desc_label.setWordWrap(True)
        card_layout.addWidget(desc_label)
        
        return card
    
    def update_display(self):
        """Update the display with current game state"""
        # Personalize greeting with player name
        if self.flow_manager.game_state.player_name:
            self.greeting_label.setText(f"Hello, {self.flow_manager.game_state.player_name}!")
        
        # Show home city
        if self.flow_manager.game_state.home_city:
            self.home_city_label.setText(self.flow_manager.game_state.home_city)
        else:
            self.home_city_label.setText("City not set")
    
    def go_back(self):
        """Go back to the welcome screen"""
        self.flow_manager.show_welcome_screen()
    
    def continue_to_selection(self):
        """Continue to the city selection screen"""
        self.flow_manager.show_city_selection_screen()