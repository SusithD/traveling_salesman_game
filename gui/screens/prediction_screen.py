"""
Algorithm prediction screen for the Traveling Salesman Problem game
"""
import logging
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QFrame, QRadioButton, QButtonGroup, QSpacerItem, 
    QSizePolicy, QGraphicsDropShadowEffect
)
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect, QEasingCurve
from PyQt5.QtGui import QColor, QFont

logger = logging.getLogger("PredictionScreen")

class PredictionScreen(QWidget):
    """
    Screen for predicting which algorithm will find the shortest path
    """
    def __init__(self, flow_manager):
        super().__init__()
        self.flow_manager = flow_manager
        self.selected_algorithm = None
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
        
        # Header with info
        header_layout = QHBoxLayout()
        
        prediction_icon = QLabel("🧠")
        prediction_icon.setStyleSheet("""
            font-size: 36px;
            padding: 10px;
            background-color: #8e44ad;
            color: white;
            border-radius: 10px;
        """)
        header_layout.addWidget(prediction_icon)
        
        header_text = QVBoxLayout()
        title = QLabel("Make Your Prediction")
        title.setStyleSheet("""
            color: white;
            font-size: 24px;
            font-weight: bold;
        """)
        header_text.addWidget(title)
        
        subtitle = QLabel("Predict which algorithm will find the shortest route")
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
        
        # Journey summary - tell the player what they're solving
        summary_frame = QFrame()
        summary_frame.setStyleSheet("""
            background-color: #2c3e50;
            border-radius: 10px;
            padding: 15px;
        """)
        summary_layout = QVBoxLayout(summary_frame)
        
        journey_title = QLabel("Your Journey")
        journey_title.setStyleSheet("color: white; font-weight: bold; font-size: 16px;")
        journey_title.setAlignment(Qt.AlignCenter)
        summary_layout.addWidget(journey_title)
        
        self.journey_label = QLabel()
        self.journey_label.setWordWrap(True)
        self.journey_label.setStyleSheet("""
            color: white;
            font-size: 14px;
            line-height: 20px;
            padding: 8px;
        """)
        summary_layout.addWidget(self.journey_label)
        
        container_layout.addWidget(summary_frame)
        
        # Algorithm selection area with cards
        algo_title = QLabel("Select Your Prediction")
        algo_title.setStyleSheet("""
            color: white;
            font-size: 18px;
            font-weight: bold;
            margin-top: 10px;
        """)
        container_layout.addWidget(algo_title)
        
        # Radio button group for algorithm selection
        self.algorithm_group = QButtonGroup()
        self.algorithm_group.buttonClicked.connect(self.algorithm_selected)
        
        # Brute Force card
        bf_card = self.create_algorithm_card(
            "Brute Force", 
            "🧮", 
            "#c0392b",
            "Tries all possible routes (O(n!))",
            "• Guaranteed to find the optimal solution\n• Very slow for large numbers of cities\n• Computational complexity grows factorially",
            "brute_force"
        )
        container_layout.addWidget(bf_card)
        
        # Nearest Neighbor card
        nn_card = self.create_algorithm_card(
            "Nearest Neighbor", 
            "📍", 
            "#2980b9",
            "Always visits closest unvisited city (O(n²))",
            "• Fast and efficient greedy algorithm\n• May not find the optimal solution\n• Makes decisions based on local information",
            "nearest_neighbor"
        )
        container_layout.addWidget(nn_card)
        
        # Dynamic Programming card
        dp_card = self.create_algorithm_card(
            "Dynamic Programming", 
            "⚙️", 
            "#27ae60",
            "Solves subproblems and builds up solution (O(n²2ⁿ))",
            "• Finds the optimal solution\n• Faster than brute force\n• Uses memoization to avoid repeated work",
            "dynamic_programming"
        )
        container_layout.addWidget(dp_card)
        
        # Button area
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        back_button = QPushButton("← Back")
        back_button.setStyleSheet("""
            QPushButton {
                background-color: #333333;
                color: white;
                border: 1px solid #555555;
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
        
        self.calculate_button = QPushButton("Calculate Routes →")
        self.calculate_button.setStyleSheet("""
            QPushButton {
                background-color: #9b59b6;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px 20px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #8e44ad;
            }
            QPushButton:pressed {
                background-color: #6c3483;
            }
            QPushButton:disabled {
                background-color: #95a5a6;
                color: #dddddd;
            }
        """)
        self.calculate_button.clicked.connect(self.start_calculation)
        self.calculate_button.setEnabled(False)  # Initially disabled
        button_layout.addWidget(self.calculate_button)
        
        container_layout.addLayout(button_layout)
        
        # Add container to main layout
        main_layout.addWidget(container)
    
    def create_algorithm_card(self, title, icon, color, subtitle, details, algorithm_id):
        """Create a card for an algorithm selection"""
        card = QFrame()
        card.setObjectName(f"{algorithm_id}_card")
        card.setStyleSheet(f"""
            QFrame {{
                background-color: #222222;
                border: 1px solid #333333;
                border-radius: 10px;
                padding: 10px;
                margin: 5px 0px;
            }}
            QFrame:hover {{
                background-color: #282828;
                border: 1px solid {color};
            }}
        """)
        card_layout = QHBoxLayout(card)
        card_layout.setContentsMargins(15, 15, 15, 15)
        card_layout.setSpacing(15)
        
        # Icon section
        icon_label = QLabel(icon)
        icon_label.setStyleSheet(f"""
            font-size: 36px;
            padding: 15px;
            background-color: {color};
            color: white;
            border-radius: 10px;
            min-width: 30px;
        """)
        icon_label.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(icon_label)
        
        # Content section
        content_layout = QVBoxLayout()
        content_layout.setSpacing(5)
        
        # Algorithm name with radio button
        title_layout = QHBoxLayout()
        
        radio = QRadioButton(title)
        radio.setObjectName(algorithm_id)
        radio.setStyleSheet("""
            QRadioButton {
                color: white;
                font-size: 18px;
                font-weight: bold;
                spacing: 10px;
            }
            QRadioButton::indicator {
                width: 18px;
                height: 18px;
                border-radius: 9px;
                border: 2px solid #555555;
            }
            QRadioButton::indicator:checked {
                background-color: white;
                border: 2px solid white;
                image: none;
            }
            QRadioButton::indicator:unchecked {
                background-color: transparent;
            }
        """)
        self.algorithm_group.addButton(radio)
        title_layout.addWidget(radio)
        title_layout.addStretch()
        
        # Complexity badge
        complexity = QLabel(subtitle)
        complexity.setStyleSheet(f"""
            background-color: {color};
            opacity: 0.7;
            color: white;
            font-size: 12px;
            padding: 4px 8px;
            border-radius: 4px;
        """)
        title_layout.addWidget(complexity)
        
        content_layout.addLayout(title_layout)
        
        # Details
        details_label = QLabel(details)
        details_label.setStyleSheet("""
            color: #bbbbbb;
            font-size: 13px;
            line-height: 18px;
            padding: 5px;
            margin-top: 5px;
        """)
        content_layout.addWidget(details_label)
        
        card_layout.addLayout(content_layout, 1)
        
        return card
    
    def reset(self):
        """Reset the prediction screen state"""
        # Clear algorithm selection
        self.algorithm_group.setExclusive(False)
        for button in self.algorithm_group.buttons():
            button.setChecked(False)
        self.algorithm_group.setExclusive(True)
        
        # Disable calculate button
        self.calculate_button.setEnabled(False)
        self.selected_algorithm = None
    
    def update_display(self):
        """Update the display with current game state"""
        # Show journey summary
        player_name = self.flow_manager.game_state.player_name
        home_city = self.flow_manager.game_state.home_city
        city_count = len(self.flow_manager.game_state.selected_cities)
        
        cities_list = ", ".join(city for city in self.flow_manager.game_state.selected_cities 
                               if city != home_city)
        
        self.journey_label.setText(
            f"{player_name}, you'll be starting from {home_city}, visiting {city_count - 1} cities "
            f"({cities_list}), and returning to {home_city}.\n\n"
            f"Before calculating the routes, which algorithm do you predict will find the shortest path?"
        )
    
    def algorithm_selected(self, button):
        """Handle algorithm selection"""
        self.selected_algorithm = button.objectName()
        self.calculate_button.setEnabled(True)
        
        # Highlight selected card
        for card_name in ["brute_force_card", "nearest_neighbor_card", "dynamic_programming_card"]:
            card = self.findChild(QFrame, card_name)
            if card_name.startswith(self.selected_algorithm):
                # Selected card gets highlighted border
                if self.selected_algorithm == "brute_force":
                    color = "#c0392b"
                elif self.selected_algorithm == "nearest_neighbor":
                    color = "#2980b9"
                else:  # dynamic_programming
                    color = "#27ae60"
                    
                card.setStyleSheet(f"""
                    background-color: #282828;
                    border: 2px solid {color};
                    border-radius: 10px;
                    padding: 10px;
                    margin: 5px 0px;
                """)
                
                # Add glow effect
                shadow = QGraphicsDropShadowEffect()
                shadow.setBlurRadius(15)
                shadow.setColor(QColor(color))
                shadow.setOffset(0, 0)
                card.setGraphicsEffect(shadow)
            else:
                # Reset other cards
                card.setStyleSheet("""
                    background-color: #222222;
                    border: 1px solid #333333;
                    border-radius: 10px;
                    padding: 10px;
                    margin: 5px 0px;
                """)
                card.setGraphicsEffect(None)
    
    def go_back(self):
        """Go back to the city selection screen"""
        self.flow_manager.show_city_selection_screen()
    
    def start_calculation(self):
        """Start the route calculation process"""
        if not self.selected_algorithm:
            return
            
        # Map the selected algorithm ID to the full name
        algorithm_names = {
            "brute_force": "Brute Force",
            "nearest_neighbor": "Nearest Neighbor",
            "dynamic_programming": "Dynamic Programming"
        }
        
        # Store the user's prediction in the game state
        user_prediction = algorithm_names[self.selected_algorithm]
        self.flow_manager.game_state.user_prediction = user_prediction
        
        # Move to the calculation animation screen
        self.flow_manager.show_calculating_screen(user_prediction)