"""
Algorithm prediction screen for the Traveling Salesman Problem game
"""
import logging
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QFrame, QRadioButton, QButtonGroup, QSpacerItem, 
    QSizePolicy, QGraphicsDropShadowEffect, QMessageBox
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
        self.selected_algorithm = None  # Track which algorithm is selected
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the UI components"""
        # Main layout with center alignment
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(20)
        main_layout.setAlignment(Qt.AlignCenter)
        
        # Create central container frame with modern styling
        central_frame = QFrame()
        central_frame.setObjectName("predictionContainer")
        central_frame.setMinimumWidth(1000)
        central_frame.setMaximumWidth(1200)
        central_frame.setStyleSheet("""
            #predictionContainer {
                background-color: rgba(26, 26, 26, 0.7);
                border-radius: 20px;
                border: 1px solid rgba(255, 255, 255, 0.1);
            }
        """)
        
        container_layout = QVBoxLayout(central_frame)
        container_layout.setContentsMargins(40, 40, 40, 40)
        container_layout.setSpacing(25)
        
        # Header with progress indicator
        header_frame = QFrame()
        header_frame.setObjectName("headerFrame")
        header_frame.setStyleSheet("""
            #headerFrame {
                background-color: rgba(243, 156, 18, 0.15);
                border-radius: 15px;
            }
        """)
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(20, 15, 20, 15)
        
        # Left side - Title with icon
        header_left = QHBoxLayout()
        
        # Prediction icon
        prediction_icon = QLabel("🧠")
        prediction_icon.setFixedSize(60, 60)
        prediction_icon.setObjectName("predictionIcon")
        prediction_icon.setStyleSheet("""
            #predictionIcon {
                font-size: 30px;
                background-color: #f39c12;
                color: white;
                border-radius: 30px;
                margin-right: 15px;
            }
        """)
        prediction_icon.setAlignment(Qt.AlignCenter)
        header_left.addWidget(prediction_icon)
        
        # Title and subtitle
        title_layout = QVBoxLayout()
        title_layout.setSpacing(5)
        
        title = QLabel("ALGORITHM PREDICTION")
        title.setObjectName("predictionTitle")
        title.setStyleSheet("""
            #predictionTitle {
                color: white;
                font-size: 22px;
                font-weight: bold;
                letter-spacing: 1px;
            }
        """)
        title_layout.addWidget(title)
        
        subtitle = QLabel("Predict which algorithm will find the shortest route")
        subtitle.setObjectName("predictionSubtitle")
        subtitle.setStyleSheet("""
            #predictionSubtitle {
                color: #BBBBBB;
                font-size: 14px;
            }
        """)
        title_layout.addWidget(subtitle)
        
        header_left.addLayout(title_layout)
        header_layout.addLayout(header_left)
        header_layout.addStretch()
        
        # Right side - Progress indicator
        progress_frame = QFrame()
        progress_frame.setObjectName("progressFrame")
        progress_frame.setStyleSheet("""
            #progressFrame {
                background-color: rgba(255, 255, 255, 0.1);
                border-radius: 10px;
                padding: 5px 15px;
            }
        """)
        progress_layout = QHBoxLayout(progress_frame)
        progress_layout.setContentsMargins(10, 5, 10, 5)
        progress_layout.setSpacing(8)
        
        # Step indicators
        step1 = QLabel("1")
        step1.setObjectName("step1")
        step1.setStyleSheet("""
            #step1 {
                background-color: #3D5AFE;
                color: white;
                border-radius: 12px;
                padding: 5px;
                font-weight: bold;
                min-width: 24px;
                min-height: 24px;
                qproperty-alignment: AlignCenter;
            }
        """)
        progress_layout.addWidget(step1)
        
        arrow1 = QLabel("→")
        arrow1.setStyleSheet("color: white; font-size: 14px;")
        progress_layout.addWidget(arrow1)
        
        step2 = QLabel("2")
        step2.setObjectName("step2")
        step2.setStyleSheet("""
            #step2 {
                background-color: #3D5AFE;
                color: white;
                border-radius: 12px;
                padding: 5px;
                font-weight: bold;
                min-width: 24px;
                min-height: 24px;
                qproperty-alignment: AlignCenter;
            }
        """)
        progress_layout.addWidget(step2)
        
        arrow2 = QLabel("→")
        arrow2.setStyleSheet("color: white; font-size: 14px;")
        progress_layout.addWidget(arrow2)
        
        step3 = QLabel("3")
        step3.setObjectName("step3")
        step3.setStyleSheet("""
            #step3 {
                background-color: #f39c12;
                color: white;
                border-radius: 12px;
                padding: 5px;
                font-weight: bold;
                min-width: 24px;
                min-height: 24px;
                qproperty-alignment: AlignCenter;
            }
        """)
        progress_layout.addWidget(step3)
        
        header_layout.addWidget(progress_frame)
        container_layout.addWidget(header_frame)
        
        # Stylish separator
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setStyleSheet("""
            background-color: #f39c12;
            max-width: 150px;
            height: 3px;
            margin: 5px;
        """)
        container_layout.addWidget(separator, 0, Qt.AlignCenter)
        
        # Journey summary frame with updated styling
        journey_frame = QFrame()
        journey_frame.setObjectName("journeyFrame")
        journey_frame.setStyleSheet("""
            #journeyFrame {
                background-color: rgba(33, 33, 33, 0.7);
                border-radius: 15px;
                padding: 15px;
            }
        """)
        journey_layout = QVBoxLayout(journey_frame)
        journey_layout.setContentsMargins(25, 25, 25, 25)
        journey_layout.setSpacing(15)
        
        journey_title = QLabel("YOUR JOURNEY")
        journey_title.setObjectName("journeyTitle")
        journey_title.setStyleSheet("""
            #journeyTitle {
                color: #f39c12;
                font-size: 16px;
                font-weight: bold;
                letter-spacing: 1px;
            }
        """)
        journey_title.setAlignment(Qt.AlignCenter)
        journey_layout.addWidget(journey_title)
        
        self.journey_label = QLabel()
        self.journey_label.setObjectName("journeyDetails")
        self.journey_label.setWordWrap(True)
        self.journey_label.setStyleSheet("""
            #journeyDetails {
                color: #DDDDDD;
                font-size: 15px;
                line-height: 150%;
                background-color: rgba(243, 156, 18, 0.1);
                border: 1px solid rgba(243, 156, 18, 0.2);
                border-radius: 10px;
                padding: 15px;
            }
        """)
        self.journey_label.setAlignment(Qt.AlignCenter)
        journey_layout.addWidget(self.journey_label)
        
        container_layout.addWidget(journey_frame)
        
        # Algorithm selection section
        algo_title = QLabel("SELECT YOUR PREDICTION")
        algo_title.setObjectName("algoSectionTitle")
        algo_title.setStyleSheet("""
            #algoSectionTitle {
                color: white;
                font-size: 18px;
                font-weight: bold;
                letter-spacing: 1px;
                margin-top: 10px;
            }
        """)
        algo_title.setAlignment(Qt.AlignCenter)
        container_layout.addWidget(algo_title)
        
        # Radio button group for algorithm selection
        self.algorithm_group = QButtonGroup()
        self.algorithm_group.buttonClicked.connect(self.algorithm_selected)
        
        # Algorithm cards container
        algo_cards_layout = QVBoxLayout()
        algo_cards_layout.setSpacing(15)
        
        # Brute Force card with improved styling
        self.bf_card = self.create_algorithm_card(
            "Brute Force", 
            "🧮", 
            "#e74c3c",
            "Tries all possible routes (O(n!))",
            "• Guaranteed to find the optimal solution\n• Very slow for large numbers of cities\n• Computational complexity grows factorially",
            "brute_force"
        )
        algo_cards_layout.addWidget(self.bf_card)
        
        # Nearest Neighbor card with improved styling
        self.nn_card = self.create_algorithm_card(
            "Nearest Neighbor", 
            "📍", 
            "#3498db",
            "Always visits closest unvisited city (O(n²))",
            "• Fast and efficient greedy algorithm\n• May not find the optimal solution\n• Makes decisions based on local information",
            "nearest_neighbor"
        )
        algo_cards_layout.addWidget(self.nn_card)
        
        # Dynamic Programming card with improved styling
        self.dp_card = self.create_algorithm_card(
            "Dynamic Programming", 
            "⚙️", 
            "#2ecc71",
            "Solves subproblems and builds up solution (O(n²2ⁿ))",
            "• Finds the optimal solution\n• Faster than brute force\n• Uses memoization to avoid repeated work",
            "dynamic_programming"
        )
        algo_cards_layout.addWidget(self.dp_card)
        
        container_layout.addLayout(algo_cards_layout)
        
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
        
        # Find the CALCULATE ROUTES button and disable it initially
        self.calculate_button = QPushButton("CALCULATE ROUTES →")
        self.calculate_button.setObjectName("continueButton")
        self.calculate_button.setFixedSize(250, 50)
        self.calculate_button.setStyleSheet("""
            #continueButton {
                background-color: #f39c12;
                color: white;
                border: none;
                border-radius: 12px;
                padding: 12px 25px;
                font-size: 14px;
                font-weight: bold;
                letter-spacing: 1px;
            }
            #continueButton:hover {
                background-color: #e67e22;
            }
            #continueButton:pressed {
                background-color: #d35400;
            }
            #continueButton:disabled {
                background-color: #555555;
                color: #aaaaaa;
            }
        """)
        self.calculate_button.clicked.connect(self.start_calculation)
        self.calculate_button.setEnabled(False)  # Initially disabled
        
        button_layout.addWidget(self.calculate_button)
        
        container_layout.addLayout(button_layout)
        
        # Add container to main layout
        main_layout.addWidget(central_frame, 0, Qt.AlignCenter)
    
    def create_algorithm_card(self, title, icon, color, subtitle, details, algorithm_id):
        """Create a card for an algorithm selection with improved styling"""
        card = QFrame()
        card.setObjectName(f"{algorithm_id}_card")
        card.setStyleSheet(f"""
            #{algorithm_id}_card {{
                background-color: rgba(33, 33, 33, 0.7);
                border: 1px solid #444444;
                border-radius: 15px;
                padding: 0px;
                margin: 5px 0px;
            }}
            #{algorithm_id}_card:hover {{
                background-color: rgba(40, 40, 40, 0.8);
                border: 1px solid {color};
            }}
        """)
        card_layout = QHBoxLayout(card)
        card_layout.setContentsMargins(20, 20, 20, 20)
        card_layout.setSpacing(20)
        
        # Icon section with improved styling
        icon_frame = QFrame()
        icon_frame.setObjectName(f"{algorithm_id}_icon_frame")
        icon_frame.setFixedSize(80, 80)
        icon_frame.setStyleSheet(f"""
            #{algorithm_id}_icon_frame {{
                background-color: {color};
                border-radius: 40px;
                border: none;
            }}
        """)
        icon_layout = QVBoxLayout(icon_frame)
        icon_layout.setContentsMargins(0, 0, 0, 0)
        
        icon_label = QLabel(icon)
        icon_label.setStyleSheet(f"""
            font-size: 36px;
            color: white;
        """)
        icon_label.setAlignment(Qt.AlignCenter)
        icon_layout.addWidget(icon_label)
        
        card_layout.addWidget(icon_frame)
        
        # Content section with improved styling
        content_layout = QVBoxLayout()
        content_layout.setSpacing(10)
        
        # Algorithm name with radio button
        title_layout = QHBoxLayout()
        
        radio = QRadioButton(title)
        radio.setObjectName(algorithm_id)
        # Explicitly set the algorithm_id property
        radio.setProperty("algorithm_id", algorithm_id)
        radio.setStyleSheet(f"""
            QRadioButton {{
                color: white;
                font-size: 18px;
                font-weight: bold;
                spacing: 10px;
            }}
            QRadioButton::indicator {{
                width: 20px;
                height: 20px;
                border-radius: 10px;
                border: 2px solid #666666;
            }}
            QRadioButton::indicator:checked {{
                background-color: {color};
                border: 2px solid {color};
                image: none;
            }}
            QRadioButton::indicator:unchecked {{
                background-color: transparent;
            }}
        """)
        self.algorithm_group.addButton(radio)
        title_layout.addWidget(radio)
        title_layout.addStretch()
        
        # Complexity badge with improved styling
        complexity = QLabel(subtitle)
        complexity.setStyleSheet(f"""
            background-color: {color};
            color: white;
            font-size: 12px;
            font-weight: bold;
            padding: 6px 10px;
            border-radius: 8px;
        """)
        title_layout.addWidget(complexity)
        
        content_layout.addLayout(title_layout)
        
        # Details with improved styling
        details_label = QLabel(details)
        details_label.setObjectName(f"{algorithm_id}_details")
        details_label.setStyleSheet(f"""
            #{algorithm_id}_details {{
                color: #dddddd;
                font-size: 14px;
                line-height: 150%;
                background-color: rgba(40, 40, 40, 0.6);
                border-radius: 8px;
                padding: 10px 15px;
            }}
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
        
        # Remove highlighting from all cards
        for card_name in ["brute_force_card", "nearest_neighbor_card", "dynamic_programming_card"]:
            card = self.findChild(QFrame, card_name)
            if card:
                algorithm_id = card_name.replace("_card", "")
                card.setStyleSheet(f"""
                    #{card_name} {{
                        background-color: rgba(33, 33, 33, 0.7);
                        border: 1px solid #444444;
                        border-radius: 15px;
                        padding: 0px;
                        margin: 5px 0px;
                    }}
                    #{card_name}:hover {{
                        background-color: rgba(40, 40, 40, 0.8);
                        border: 1px solid #666666;
                    }}
                """)
                card.setGraphicsEffect(None)
    
    def update_display(self):
        """Update the display with current game state"""
        # Show journey summary with improved formatting
        player_name = self.flow_manager.game_state.player_name
        home_city = self.flow_manager.game_state.home_city
        city_count = len(self.flow_manager.game_state.selected_cities)
        
        cities_to_visit = [city for city in self.flow_manager.game_state.selected_cities 
                          if city != home_city]
                          
        if len(cities_to_visit) <= 4:
            # For few cities, just list them with commas
            cities_list = ", ".join(cities_to_visit)
            cities_display = f"visiting {city_count - 1} cities ({cities_list})"
        else:
            # For many cities, show count and first few with "and X more"
            sample_cities = ", ".join(cities_to_visit[:3])
            remaining = len(cities_to_visit) - 3
            cities_display = f"visiting {city_count - 1} cities ({sample_cities}, and {remaining} more)"
        
        self.journey_label.setText(
            f"{player_name}, you'll be starting from {home_city}, {cities_display}, "
            f"and returning to {home_city}.\n\n"
            f"Before calculating the routes, which algorithm do you predict will find the shortest path?"
        )
        
        # Reset selection
        self.reset()
    
    def algorithm_selected(self, button):
        """Handle algorithm selection with enhanced visual feedback"""
        algorithm_id = button.property("algorithm_id")
        self.selected_algorithm = algorithm_id
        
        # Log the selection for debugging
        logger.info(f"Algorithm selected: {algorithm_id}")
        
        # Enable the calculate button now that an algorithm is selected
        self.calculate_button.setEnabled(True)
        
        # Apply selected styling to the clicked algorithm's card
        cards = {
            "brute_force": self.bf_card,
            "nearest_neighbor": self.nn_card,
            "dynamic_programming": self.dp_card
        }
        
        # Colors for different algorithm cards
        colors = {
            "brute_force": "#e74c3c",
            "nearest_neighbor": "#3498db",
            "dynamic_programming": "#2ecc71"
        }
        
        # Update all cards
        for card_name, card in cards.items():
            if card_name == algorithm_id:
                # Selected card styling
                card.setStyleSheet(f"""
                    #{card_name} {{
                        background-color: rgba(33, 33, 33, 0.8);
                        border: 2px solid {colors[card_name]};
                        border-radius: 15px;
                        padding: 0px;
                        margin: 5px 0px;
                    }}
                """)
                
                # Add glow effect
                shadow = QGraphicsDropShadowEffect()
                shadow.setBlurRadius(15)
                shadow.setColor(QColor(colors[card_name]))
                shadow.setOffset(0, 0)
                card.setGraphicsEffect(shadow)
            else:
                # Reset other cards
                card.setStyleSheet(f"""
                    #{card_name} {{
                        background-color: rgba(33, 33, 33, 0.7);
                        border: 1px solid #444444;
                        border-radius: 15px;
                        padding: 0px;
                        margin: 5px 0px;
                    }}
                    #{card_name}:hover {{
                        background-color: rgba(40, 40, 40, 0.8);
                        border: 1px solid #555555;
                    }}
                """)
                
                # Remove shadow effect
                card.setGraphicsEffect(None)

    def go_back(self):
        """Go back to the city selection screen"""
        self.flow_manager.show_city_selection_screen()
    
    def start_calculation(self):
        """Start the route calculation process"""
        logger.info(f"Starting calculation with selected algorithm: {self.selected_algorithm}")
        
        if not self.selected_algorithm:
            logger.error("No algorithm selected, showing warning")
            QMessageBox.warning(
                self, 
                "No Algorithm Selected",
                "Please select an algorithm before continuing.",
                QMessageBox.Ok
            )
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
        logger.info(f"User prediction set to: {user_prediction}")
        
        # Move to the calculation animation screen
        self.flow_manager.show_calculating_screen(user_prediction)