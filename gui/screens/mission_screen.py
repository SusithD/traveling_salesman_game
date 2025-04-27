"""
Mission briefing screen for the Traveling Salesman Problem game
"""
import logging
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QFrame, QGraphicsDropShadowEffect, QSpacerItem, QSizePolicy
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
        # Main layout with center alignment
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(20)
        main_layout.setAlignment(Qt.AlignCenter)
        
        # Create a central container frame with modern styling
        central_frame = QFrame()
        central_frame.setObjectName("missionContainer")
        central_frame.setMaximumWidth(800)  # Limit width for better readability
        central_frame.setStyleSheet("""
            #missionContainer {
                background-color: rgba(26, 26, 26, 0.7);
                border-radius: 20px;
                border: 1px solid rgba(255, 255, 255, 0.1);
            }
        """)
        
        container_layout = QVBoxLayout(central_frame)
        container_layout.setContentsMargins(40, 40, 40, 40)
        container_layout.setSpacing(30)
        container_layout.setAlignment(Qt.AlignCenter)
        
        # Header with modernized design
        header_frame = QFrame()
        header_frame.setObjectName("headerFrame")
        header_frame.setStyleSheet("""
            #headerFrame {
                background-color: rgba(61, 90, 254, 0.15);
                border-radius: 15px;
            }
        """)
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(20, 15, 20, 15)
        
        # Mission icon with updated styling
        mission_icon = QLabel("🧭")
        mission_icon.setFixedSize(60, 60)
        mission_icon.setObjectName("missionIcon")
        mission_icon.setStyleSheet("""
            #missionIcon {
                font-size: 30px;
                background-color: #3D5AFE;
                color: white;
                border-radius: 30px;
                margin-right: 15px;
            }
        """)
        mission_icon.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(mission_icon)
        
        # Header text with updated styling
        header_text = QVBoxLayout()
        header_text.setSpacing(5)
        
        title = QLabel("MISSION BRIEFING")
        title.setObjectName("missionTitle")
        title.setStyleSheet("""
            #missionTitle {
                color: white;
                font-size: 22px;
                font-weight: bold;
                letter-spacing: 1px;
            }
        """)
        header_text.addWidget(title)
        
        subtitle = QLabel("Your traveling salesman adventure begins here")
        subtitle.setObjectName("missionSubtitle")
        subtitle.setStyleSheet("""
            #missionSubtitle {
                color: #BBBBBB;
                font-size: 14px;
            }
        """)
        header_text.addWidget(subtitle)
        
        header_layout.addLayout(header_text)
        header_layout.addStretch()
        
        container_layout.addWidget(header_frame)
        
        # Stylish separator
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setStyleSheet("""
            background-color: #3D5AFE;
            max-width: 150px;
            height: 3px;
            margin: 5px;
        """)
        container_layout.addWidget(separator, 0, Qt.AlignCenter)
        
        # Mission briefing content in a modernized frame
        mission_frame = QFrame()
        mission_frame.setObjectName("contentFrame")
        mission_frame.setStyleSheet("""
            #contentFrame {
                background-color: rgba(33, 33, 33, 0.5);
                border-radius: 15px;
            }
        """)
        mission_layout = QVBoxLayout(mission_frame)
        mission_layout.setContentsMargins(25, 25, 25, 25)
        mission_layout.setSpacing(25)
        mission_layout.setAlignment(Qt.AlignCenter)
        
        # Greeting with updated styling
        self.greeting_label = QLabel("Hello, Traveler!")
        self.greeting_label.setObjectName("greetingLabel")
        self.greeting_label.setStyleSheet("""
            #greetingLabel {
                color: white;
                font-size: 22px;
                font-weight: bold;
            }
        """)
        self.greeting_label.setAlignment(Qt.AlignCenter)
        mission_layout.addWidget(self.greeting_label)
        
        # Scenario description with updated styling
        scenario_text = QLabel(
            "You are a traveling salesman who needs to visit several cities and return "
            "home while traveling the shortest possible distance. Your journey begins and "
            "ends at your home city."
        )
        scenario_text.setObjectName("scenarioText")
        scenario_text.setWordWrap(True)
        scenario_text.setStyleSheet("""
            #scenarioText {
                color: #DDDDDD;
                font-size: 15px;
                line-height: 150%;
                padding: 5px;
            }
        """)
        scenario_text.setAlignment(Qt.AlignCenter)
        mission_layout.addWidget(scenario_text)
        
        # Home city announcement with enhanced styling
        home_city_frame = QFrame()
        home_city_frame.setObjectName("homeCityFrame")
        home_city_frame.setStyleSheet("""
            #homeCityFrame {
                background-color: rgba(61, 90, 254, 0.15);
                border: 1px solid rgba(61, 90, 254, 0.3);
                border-radius: 15px;
            }
        """)
        home_layout = QVBoxLayout(home_city_frame)
        home_layout.setContentsMargins(20, 25, 20, 25)
        home_layout.setAlignment(Qt.AlignCenter)
        
        home_title = QLabel("YOUR HOME CITY")
        home_title.setObjectName("homeCityTitle")
        home_title.setStyleSheet("""
            #homeCityTitle {
                color: #3D5AFE;
                font-size: 14px;
                font-weight: bold;
                letter-spacing: 1px;
            }
        """)
        home_title.setAlignment(Qt.AlignCenter)
        home_layout.addWidget(home_title)
        
        self.home_city_label = QLabel("City X")  # Will be updated with actual home city
        self.home_city_label.setObjectName("homeCityName")
        self.home_city_label.setStyleSheet("""
            #homeCityName {
                color: white;
                font-size: 36px;
                font-weight: bold;
                letter-spacing: 1px;
                padding: 10px;
            }
        """)
        self.home_city_label.setAlignment(Qt.AlignCenter)
        
        # Add shadow effect to make it pop
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor("#3D5AFE"))
        shadow.setOffset(0, 0)
        self.home_city_label.setGraphicsEffect(shadow)
        home_layout.addWidget(self.home_city_label)
        
        mission_layout.addWidget(home_city_frame)
        
        # Strategy hint with updated styling
        hint_text = QLabel(
            "Your task is to select which cities to visit, predict which algorithm will find the "
            "shortest route, and then analyze the results to see if your prediction was correct."
        )
        hint_text.setObjectName("hintText")
        hint_text.setWordWrap(True)
        hint_text.setStyleSheet("""
            #hintText {
                color: #DDDDDD;
                font-size: 15px;
                background-color: rgba(83, 109, 254, 0.1);
                border-radius: 10px;
                padding: 15px;
                line-height: 150%;
            }
        """)
        hint_text.setAlignment(Qt.AlignCenter)
        mission_layout.addWidget(hint_text)
        
        # Add algorithms section title with updated styling
        algo_intro = QLabel("YOU'LL BE WORKING WITH THREE ALGORITHMS")
        algo_intro.setObjectName("algoIntro")
        algo_intro.setStyleSheet("""
            #algoIntro {
                color: white;
                font-size: 14px;
                font-weight: bold;
                letter-spacing: 1px;
                margin-top: 10px;
            }
        """)
        algo_intro.setAlignment(Qt.AlignCenter)
        mission_layout.addWidget(algo_intro)
        
        # Algorithm cards layout with updated styling
        algo_layout = QHBoxLayout()
        algo_layout.setSpacing(15)
        algo_layout.setAlignment(Qt.AlignCenter)
        
        # Updated algorithm cards
        bf_card = self.create_algo_card("Brute Force", "🧮", "#536DFE", "Tries all possible routes")
        algo_layout.addWidget(bf_card)
        
        nn_card = self.create_algo_card("Nearest Neighbor", "📍", "#536DFE", "Always picks closest next city")
        algo_layout.addWidget(nn_card)
        
        dp_card = self.create_algo_card("Dynamic Programming", "⚙️", "#536DFE", "Uses optimal subproblems")
        algo_layout.addWidget(dp_card)
        
        mission_layout.addLayout(algo_layout)
        
        container_layout.addWidget(mission_frame)
        
        # Button area with updated styling
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)
        button_layout.setAlignment(Qt.AlignCenter)
        
        back_button = QPushButton("← BACK")
        back_button.setObjectName("backButton")
        back_button.setFixedSize(150, 50)
        back_button.setStyleSheet("""
            #backButton {
                background-color: rgba(45, 45, 45, 0.7);
                color: white;
                border: none;
                border-radius: 12px;
                padding: 12px 20px;
                font-size: 14px;
                font-weight: bold;
                letter-spacing: 1px;
            }
            #backButton:hover {
                background-color: rgba(60, 60, 60, 0.8);
            }
            #backButton:pressed {
                background-color: rgba(35, 35, 35, 0.9);
            }
        """)
        back_button.clicked.connect(self.go_back)
        button_layout.addWidget(back_button)
        
        continue_button = QPushButton("SELECT CITIES →")
        continue_button.setObjectName("continueButton")
        continue_button.setFixedSize(250, 50)
        continue_button.setStyleSheet("""
            #continueButton {
                background-color: #3D5AFE;
                color: white;
                border: none;
                border-radius: 12px;
                padding: 12px 25px;
                font-size: 14px;
                font-weight: bold;
                letter-spacing: 1px;
            }
            #continueButton:hover {
                background-color: #536DFE;
            }
            #continueButton:pressed {
                background-color: #303F9F;
            }
        """)
        continue_button.clicked.connect(self.continue_to_selection)
        button_layout.addWidget(continue_button)
        
        container_layout.addLayout(button_layout)
        
        # Add container to main layout
        main_layout.addWidget(central_frame, 0, Qt.AlignCenter)
    
    def create_algo_card(self, title, icon, color, description):
        """Create a small card for algorithm brief with updated styling"""
        card = QFrame()
        card.setObjectName(f"{title.replace(' ', '')}Card")
        card.setFixedWidth(180)  # Fixed width for consistent appearance
        card.setStyleSheet(f"""
            #{title.replace(' ', '')}Card {{
                background-color: rgba(33, 33, 33, 0.7);
                border: 1px solid {color};
                border-radius: 12px;
                padding: 5px;
            }}
        """)
        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(8)
        card_layout.setContentsMargins(10, 15, 10, 15)
        card_layout.setAlignment(Qt.AlignCenter)
        
        # Icon with color background
        icon_label = QLabel(icon)
        icon_label.setFixedSize(50, 50)
        icon_label.setStyleSheet(f"""
            font-size: 24px;
            background-color: {color};
            color: white;
            border-radius: 25px;
            margin-bottom: 8px;
        """)
        icon_label.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(icon_label, 0, Qt.AlignCenter)
        
        # Title with updated styling
        title_label = QLabel(title)
        title_label.setStyleSheet("color: white; font-weight: bold; font-size: 14px; margin-top: 5px;")
        title_label.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(title_label)
        
        # Description with updated styling
        desc_label = QLabel(description)
        desc_label.setStyleSheet("color: #BBBBBB; font-size: 12px;")
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