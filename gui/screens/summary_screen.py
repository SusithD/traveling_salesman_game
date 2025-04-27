"""
Summary screen for the Traveling Salesman Problem game
"""
import logging
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QFrame, QGraphicsDropShadowEffect, QSizePolicy, QSpacerItem,
    QScrollArea
)
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect, QEasingCurve, QSize
from PyQt5.QtGui import QColor, QFont

logger = logging.getLogger("SummaryScreen")

class SummaryScreen(QWidget):
    """
    Final summary screen showing player score and game results
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
        
        # Create central container frame with modern styling
        central_frame = QFrame()
        central_frame.setObjectName("summaryContainer")
        central_frame.setMinimumWidth(1000)
        central_frame.setMaximumWidth(1200)
        central_frame.setStyleSheet("""
            #summaryContainer {
                background-color: rgba(26, 26, 26, 0.7);
                border-radius: 20px;
                border: 1px solid rgba(255, 255, 255, 0.1);
            }
        """)
        
        container_layout = QVBoxLayout(central_frame)
        container_layout.setContentsMargins(40, 40, 40, 40)
        container_layout.setSpacing(25)
        
        # Header with summary icon
        header_frame = QFrame()
        header_frame.setObjectName("headerFrame")
        header_frame.setStyleSheet("""
            #headerFrame {
                background-color: rgba(230, 126, 34, 0.15);
                border-radius: 15px;
            }
        """)
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(20, 15, 20, 15)
        
        # Left side - Title with icon
        header_left = QHBoxLayout()
        
        # Summary icon with graduation cap
        summary_icon = QLabel("🎓")
        summary_icon.setFixedSize(60, 60)
        summary_icon.setObjectName("summaryIcon")
        summary_icon.setStyleSheet("""
            #summaryIcon {
                font-size: 30px;
                background-color: #e67e22;
                color: white;
                border-radius: 30px;
                margin-right: 15px;
            }
        """)
        summary_icon.setAlignment(Qt.AlignCenter)
        header_left.addWidget(summary_icon)
        
        # Title and subtitle
        title_layout = QVBoxLayout()
        title_layout.setSpacing(5)
        
        title = QLabel("JOURNEY COMPLETE")
        title.setObjectName("summaryTitle")
        title.setStyleSheet("""
            #summaryTitle {
                color: white;
                font-size: 22px;
                font-weight: bold;
                letter-spacing: 1px;
            }
        """)
        title_layout.addWidget(title)
        
        subtitle = QLabel("Your TSP learning experience summary")
        subtitle.setObjectName("summarySubtitle")
        subtitle.setStyleSheet("""
            #summarySubtitle {
                color: #BBBBBB;
                font-size: 14px;
            }
        """)
        title_layout.addWidget(subtitle)
        
        header_left.addLayout(title_layout)
        header_layout.addLayout(header_left)
        header_layout.addStretch()
        
        # Prediction result indicator on right side of header
        prediction_container = QFrame()
        prediction_container.setObjectName("predictionContainer")
        prediction_container.setStyleSheet("""
            #predictionContainer {
                background-color: rgba(255, 255, 255, 0.1);
                border-radius: 10px;
                padding: 5px 15px;
            }
        """)
        prediction_layout = QVBoxLayout(prediction_container)
        prediction_layout.setContentsMargins(10, 10, 10, 10)
        prediction_layout.setSpacing(5)
        
        prediction_title = QLabel("YOUR PREDICTION")
        prediction_title.setStyleSheet("""
            color: rgba(255, 255, 255, 0.7);
            font-size: 12px;
            font-weight: bold;
        """)
        prediction_title.setAlignment(Qt.AlignCenter)
        prediction_layout.addWidget(prediction_title)
        
        self.prediction_outcome = QLabel("Waiting...")
        self.prediction_outcome.setObjectName("predictionOutcome")
        self.prediction_outcome.setStyleSheet("""
            #predictionOutcome {
                color: white;
                font-size: 14px;
                font-weight: bold;
            }
        """)
        self.prediction_outcome.setAlignment(Qt.AlignCenter)
        prediction_layout.addWidget(self.prediction_outcome)
        
        header_layout.addWidget(prediction_container)
        container_layout.addWidget(header_frame)
        
        # Stylish separator
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setStyleSheet("""
            background-color: #e67e22;
            max-width: 150px;
            height: 3px;
            margin: 5px;
        """)
        container_layout.addWidget(separator, 0, Qt.AlignCenter)
        
        # Player info section
        player_frame = QFrame()
        player_frame.setObjectName("playerFrame")
        player_frame.setStyleSheet("""
            #playerFrame {
                background-color: rgba(33, 33, 33, 0.7);
                border-radius: 15px;
            }
        """)
        player_layout = QHBoxLayout(player_frame)
        player_layout.setContentsMargins(25, 20, 25, 20)
        player_layout.setSpacing(20)
        
        # Player icon
        player_icon = QLabel("👤")
        player_icon.setFixedSize(50, 50)
        player_icon.setObjectName("playerIcon")
        player_icon.setStyleSheet("""
            #playerIcon {
                font-size: 24px;
                background-color: rgba(52, 152, 219, 0.7);
                border-radius: 25px;
                color: white;
            }
        """)
        player_icon.setAlignment(Qt.AlignCenter)
        player_layout.addWidget(player_icon)
        
        # Player name and journey info
        player_info = QVBoxLayout()
        player_info.setSpacing(5)
        
        player_label = QLabel("EXPLORER")
        player_label.setStyleSheet("""
            color: #3498db;
            font-size: 12px;
            font-weight: bold;
            letter-spacing: 1px;
        """)
        player_info.addWidget(player_label)
        
        self.player_name = QLabel("Player Name")
        self.player_name.setStyleSheet("""
            color: white;
            font-size: 20px;
            font-weight: bold;
        """)
        player_info.addWidget(self.player_name)
        
        player_layout.addLayout(player_info)
        player_layout.addStretch()
        
        # Journey quick stats
        journey_stats = QHBoxLayout()
        journey_stats.setSpacing(30)
        
        # Home city stat with icon
        home_stat = QVBoxLayout()
        home_stat.setSpacing(5)
        
        home_label = QLabel("HOME CITY")
        home_label.setStyleSheet("""
            color: #aaaaaa;
            font-size: 10px;
            font-weight: bold;
        """)
        home_stat.addWidget(home_label)
        
        home_layout = QHBoxLayout()
        home_icon = QLabel("🏠")
        home_icon.setStyleSheet("font-size: 16px; margin-right: 5px;")
        home_layout.addWidget(home_icon)
        
        self.home_city_value = QLabel("City")
        self.home_city_value.setStyleSheet("color: white; font-size: 16px;")
        home_layout.addWidget(self.home_city_value)
        
        home_stat.addLayout(home_layout)
        journey_stats.addLayout(home_stat)
        
        # Cities visited stat with icon
        cities_stat = QVBoxLayout()
        cities_stat.setSpacing(5)
        
        cities_label = QLabel("CITIES VISITED")
        cities_label.setStyleSheet("""
            color: #aaaaaa;
            font-size: 10px;
            font-weight: bold;
        """)
        cities_stat.addWidget(cities_label)
        
        cities_layout = QHBoxLayout()
        cities_icon = QLabel("🌆")
        cities_icon.setStyleSheet("font-size: 16px; margin-right: 5px;")
        cities_layout.addWidget(cities_icon)
        
        self.cities_visited_value = QLabel("0")
        self.cities_visited_value.setStyleSheet("color: white; font-size: 16px;")
        cities_layout.addWidget(self.cities_visited_value)
        
        cities_stat.addLayout(cities_layout)
        journey_stats.addLayout(cities_stat)
        
        # Best distance stat with icon
        distance_stat = QVBoxLayout()
        distance_stat.setSpacing(5)
        
        distance_label = QLabel("BEST DISTANCE")
        distance_label.setStyleSheet("""
            color: #aaaaaa;
            font-size: 10px;
            font-weight: bold;
        """)
        distance_stat.addWidget(distance_label)
        
        distance_layout = QHBoxLayout()
        distance_icon = QLabel("📏")
        distance_icon.setStyleSheet("font-size: 16px; margin-right: 5px;")
        distance_layout.addWidget(distance_icon)
        
        self.distance_value = QLabel("0 km")
        self.distance_value.setStyleSheet("color: white; font-size: 16px;")
        distance_layout.addWidget(self.distance_value)
        
        distance_stat.addLayout(distance_layout)
        journey_stats.addLayout(distance_stat)
        
        player_layout.addLayout(journey_stats)
        
        container_layout.addWidget(player_frame)
        
        # Algorithm comparison section
        algo_frame = QFrame()
        algo_frame.setObjectName("algoFrame")
        algo_frame.setStyleSheet("""
            #algoFrame {
                background-color: rgba(33, 33, 33, 0.7);
                border-radius: 15px;
            }
        """)
        algo_layout = QVBoxLayout(algo_frame)
        algo_layout.setContentsMargins(25, 25, 25, 25)
        algo_layout.setSpacing(20)
        
        # Title for algorithm section
        algo_title_layout = QHBoxLayout()
        
        algo_section_title = QLabel("ALGORITHM PERFORMANCE")
        algo_section_title.setStyleSheet("""
            color: white;
            font-size: 16px;
            font-weight: bold;
            letter-spacing: 0.5px;
        """)
        algo_title_layout.addWidget(algo_section_title)
        
        algo_title_layout.addStretch()
        
        # Add winning algorithm badge
        self.winner_badge = QFrame()
        self.winner_badge.setObjectName("winnerBadge")
        self.winner_badge.setFixedHeight(28)
        self.winner_badge.setStyleSheet("""
            #winnerBadge {
                background-color: #27ae60;
                border-radius: 14px;
                padding: 0px 15px;
            }
        """)
        winner_badge_layout = QHBoxLayout(self.winner_badge)
        winner_badge_layout.setContentsMargins(10, 0, 10, 0)
        winner_badge_layout.setSpacing(5)
        
        crown_icon = QLabel("👑")
        crown_icon.setStyleSheet("font-size: 14px;")
        winner_badge_layout.addWidget(crown_icon)
        
        self.winner_name = QLabel("Winning Algorithm")
        self.winner_name.setStyleSheet("""
            color: white;
            font-size: 12px;
            font-weight: bold;
        """)
        winner_badge_layout.addWidget(self.winner_name)
        
        algo_title_layout.addWidget(self.winner_badge)
        
        algo_layout.addLayout(algo_title_layout)
        
        # Algorithm cards container
        algo_cards_layout = QVBoxLayout()
        algo_cards_layout.setSpacing(15)
        
        # Create algorithm comparison cards
        self.bf_card = self.create_algo_card("Brute Force", "🧮", "#e74c3c")
        algo_cards_layout.addWidget(self.bf_card)
        
        self.nn_card = self.create_algo_card("Nearest Neighbor", "📍", "#3498db")
        algo_cards_layout.addWidget(self.nn_card)
        
        self.dp_card = self.create_algo_card("Dynamic Programming", "⚙️", "#2ecc71")
        algo_cards_layout.addWidget(self.dp_card)
        
        algo_layout.addLayout(algo_cards_layout)
        
        container_layout.addWidget(algo_frame)
        
        # Prediction and learning section
        learning_frame = QFrame()
        learning_frame.setObjectName("learningFrame")
        learning_frame.setStyleSheet("""
            #learningFrame {
                background-color: rgba(33, 33, 33, 0.7);
                border-radius: 15px;
            }
        """)
        learning_layout = QVBoxLayout(learning_frame)
        learning_layout.setContentsMargins(25, 25, 25, 25)
        learning_layout.setSpacing(20)
        
        # Prediction detail section
        prediction_detail_layout = QVBoxLayout()
        
        prediction_detail_title = QLabel("YOUR PREDICTION")
        prediction_detail_title.setStyleSheet("""
            color: #e67e22;
            font-size: 16px;
            font-weight: bold;
            letter-spacing: 0.5px;
        """)
        prediction_detail_layout.addWidget(prediction_detail_title)
        
        prediction_box = QFrame()
        prediction_box.setObjectName("predictionBox")
        prediction_box.setStyleSheet("""
            #predictionBox {
                background-color: rgba(230, 126, 34, 0.1);
                border: 1px solid rgba(230, 126, 34, 0.3);
                border-radius: 10px;
            }
        """)
        prediction_box_layout = QHBoxLayout(prediction_box)
        
        self.prediction_icon = QLabel("🤔")
        self.prediction_icon.setStyleSheet("font-size: 24px; margin-right: 10px;")
        prediction_box_layout.addWidget(self.prediction_icon)
        
        prediction_text = QVBoxLayout()
        prediction_text.setSpacing(5)
        
        prediction_intro = QLabel("You predicted that:")
        prediction_intro.setStyleSheet("color: #aaaaaa; font-size: 12px;")
        prediction_text.addWidget(prediction_intro)
        
        self.prediction_value = QLabel("Algorithm Name")
        self.prediction_value.setStyleSheet("""
            color: white;
            font-size: 16px;
            font-weight: bold;
        """)
        prediction_text.addWidget(self.prediction_value)
        
        self.prediction_result_text = QLabel("Would find the shortest route")
        self.prediction_result_text.setStyleSheet("color: #aaaaaa; font-size: 12px;")
        prediction_text.addWidget(self.prediction_result_text)
        
        prediction_box_layout.addLayout(prediction_text)
        prediction_box_layout.addStretch()
        
        prediction_detail_layout.addWidget(prediction_box)
        
        learning_layout.addLayout(prediction_detail_layout)
        
        # Learning section
        learning_title = QLabel("WHAT YOU'VE LEARNED")
        learning_title.setStyleSheet("""
            color: #3498db;
            font-size: 16px;
            font-weight: bold;
            letter-spacing: 0.5px;
            margin-top: 10px;
        """)
        learning_layout.addWidget(learning_title)
        
        learning_box = QFrame()
        learning_box.setObjectName("learningBox")
        learning_box.setStyleSheet("""
            #learningBox {
                background-color: rgba(52, 152, 219, 0.1);
                border: 1px solid rgba(52, 152, 219, 0.3);
                border-radius: 10px;
                padding: 15px;
            }
        """)
        learning_box_layout = QVBoxLayout(learning_box)
        
        self.lesson_text = QLabel()
        self.lesson_text.setWordWrap(True)
        self.lesson_text.setStyleSheet("""
            color: #dddddd;
            font-size: 14px;
            line-height: 150%;
        """)
        learning_box_layout.addWidget(self.lesson_text)
        
        learning_layout.addWidget(learning_box)
        
        container_layout.addWidget(learning_frame)
        
        # Button area with updated styling
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)
        button_layout.setAlignment(Qt.AlignCenter)
        
        play_again_button = QPushButton("← NEW GAME")
        play_again_button.setObjectName("playAgainButton")
        play_again_button.setFixedSize(180, 50)
        play_again_button.setStyleSheet("""
            #playAgainButton {
                background-color: rgba(45, 45, 45, 0.7);
                color: white;
                border: none;
                border-radius: 12px;
                padding: 12px 20px;
                font-size: 14px;
                font-weight: bold;
                letter-spacing: 1px;
            }
            #playAgainButton:hover {
                background-color: rgba(60, 60, 60, 0.8);
            }
            #playAgainButton:pressed {
                background-color: rgba(35, 35, 35, 0.9);
            }
        """)
        play_again_button.clicked.connect(self.restart_game)
        button_layout.addWidget(play_again_button)
        
        quit_button = QPushButton("EXIT GAME →")
        quit_button.setObjectName("quitButton")
        quit_button.setFixedSize(180, 50)
        quit_button.setStyleSheet("""
            #quitButton {
                background-color: #e67e22;
                color: white;
                border: none;
                border-radius: 12px;
                padding: 12px 25px;
                font-size: 14px;
                font-weight: bold;
                letter-spacing: 1px;
            }
            #quitButton:hover {
                background-color: #d35400;
            }
            #quitButton:pressed {
                background-color: #a04000;
            }
        """)
        quit_button.clicked.connect(self.quit_game)
        button_layout.addWidget(quit_button)
        
        container_layout.addLayout(button_layout)
        
        # Add container to main layout
        main_layout.addWidget(central_frame, 0, Qt.AlignCenter)
    
    def create_algo_card(self, name, icon, color):
        """Create an algorithm comparison card with modern styling"""
        card = QFrame()
        card.setObjectName(f"{name.replace(' ', '')}Card")
        card.setStyleSheet(f"""
            #{name.replace(' ', '')}Card {{
                background-color: rgba(40, 40, 40, 0.7);
                border: 1px solid {color};
                border-radius: 12px;
            }}
        """)
        
        # Add shadow effect to card
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 0, 0, 80))
        shadow.setOffset(0, 3)
        card.setGraphicsEffect(shadow)
        
        card_layout = QHBoxLayout(card)
        card_layout.setContentsMargins(20, 15, 20, 15)
        card_layout.setSpacing(15)
        
        # Algorithm icon
        algo_icon = QLabel(icon)
        algo_icon.setFixedSize(40, 40)
        algo_icon.setObjectName(f"{name.replace(' ', '')}Icon")
        algo_icon.setStyleSheet(f"""
            #{name.replace(' ', '')}Icon {{
                font-size: 20px;
                background-color: {color};
                color: white;
                border-radius: 20px;
            }}
        """)
        algo_icon.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(algo_icon)
        
        # Algorithm name and complexity
        algo_info = QVBoxLayout()
        algo_info.setSpacing(5)
        
        algo_name = QLabel(name)
        algo_name.setStyleSheet(f"""
            color: {color};
            font-size: 16px;
            font-weight: bold;
        """)
        algo_info.addWidget(algo_name)
        
        if name == "Brute Force":
            complexity = QLabel("Complexity: O(n!)")
            algo_id = "bf"
        elif name == "Nearest Neighbor":
            complexity = QLabel("Complexity: O(n²)")
            algo_id = "nn"
        else:  # Dynamic Programming
            complexity = QLabel("Complexity: O(n²2ⁿ)")
            algo_id = "dp"
        
        complexity.setStyleSheet("""
            color: #aaaaaa;
            font-size: 12px;
        """)
        algo_info.addWidget(complexity)
        
        card_layout.addLayout(algo_info)
        card_layout.addStretch()
        
        # Algorithm metrics
        metrics_layout = QHBoxLayout()
        metrics_layout.setSpacing(30)
        
        # Route length
        length_layout = QVBoxLayout()
        length_layout.setSpacing(3)
        length_layout.setAlignment(Qt.AlignCenter)
        
        length_label = QLabel("ROUTE LENGTH")
        length_label.setStyleSheet("""
            color: #aaaaaa;
            font-size: 10px;
            font-weight: bold;
        """)
        length_layout.addWidget(length_label)
        
        # Store the length label with appropriate algorithm identifier (bf, nn, dp)
        length_value = QLabel("-")
        self.__setattr__(f"{algo_id}_length", length_value)
        length_value.setObjectName(f"{name.replace(' ', '')}Length")
        length_value.setStyleSheet(f"""
            #{name.replace(' ', '')}Length {{
                color: {color};
                font-size: 16px;
                font-weight: bold;
            }}
        """)
        length_layout.addWidget(length_value)
        
        metrics_layout.addLayout(length_layout)
        
        # Execution time
        time_layout = QVBoxLayout()
        time_layout.setSpacing(3)
        time_layout.setAlignment(Qt.AlignCenter)
        
        time_label = QLabel("EXECUTION TIME")
        time_label.setStyleSheet("""
            color: #aaaaaa;
            font-size: 10px;
            font-weight: bold;
        """)
        time_layout.addWidget(time_label)
        
        # Store the time label with appropriate algorithm identifier (bf, nn, dp)
        time_value = QLabel("-")
        self.__setattr__(f"{algo_id}_time", time_value)
        time_value.setObjectName(f"{name.replace(' ', '')}Time")
        time_value.setStyleSheet(f"""
            #{name.replace(' ', '')}Time {{
                color: white;
                font-size: 14px;
            }}
        """)
        time_layout.addWidget(time_value)
        
        metrics_layout.addLayout(time_layout)
        
        # Winner badge (hidden by default, will be shown for winner)
        badge_layout = QVBoxLayout()
        badge_layout.setAlignment(Qt.AlignCenter)
        
        winner_label = QLabel("BEST ROUTE")
        self.__setattr__(f"{algo_id}_winner_label", winner_label)
        winner_label.setObjectName(f"{name.replace(' ', '')}Badge")
        winner_label.setStyleSheet(f"""
            #{name.replace(' ', '')}Badge {{
                background-color: #27ae60;
                color: white;
                font-size: 11px;
                font-weight: bold;
                padding: 5px 10px;
                border-radius: 10px;
            }}
        """)
        winner_label.setVisible(False)
        badge_layout.addWidget(winner_label)
        
        metrics_layout.addLayout(badge_layout)
        
        card_layout.addLayout(metrics_layout)
        
        return card
    
    def update_display(self):
        """Update the display with current game state"""
        # Update player name
        if self.flow_manager.game_state.player_name:
            self.player_name.setText(self.flow_manager.game_state.player_name)
        
        # Update home city
        if self.flow_manager.game_state.home_city:
            self.home_city_value.setText(self.flow_manager.game_state.home_city)
        
        # Update cities visited
        if self.flow_manager.game_state.selected_cities:
            city_count = len(self.flow_manager.game_state.selected_cities) - 1  # Exclude home city
            self.cities_visited_value.setText(str(city_count))
        
        # Update algorithm results
        results = self.flow_manager.game_state.algorithm_results
        shortest_algorithm = self.flow_manager.game_state.shortest_algorithm
        user_prediction = self.flow_manager.game_state.user_prediction
        shortest_distance = 0  # Default initialization
        
        if results and shortest_algorithm:
            # Update shortest distance
            shortest_distance = results[shortest_algorithm]["length"]
            self.distance_value.setText(f"{shortest_distance:.2f} km")
            
            # Update winner info
            self.winner_name.setText(shortest_algorithm)
            
            # Update algorithm cards
            for algo_name in ["Brute Force", "Nearest Neighbor", "Dynamic Programming"]:
                # Create consistent attribute names based on how the cards were created
                if algo_name == "Brute Force":
                    algo_id = "bf"
                elif algo_name == "Nearest Neighbor":
                    algo_id = "nn"
                elif algo_name == "Dynamic Programming":
                    algo_id = "dp"
                else:
                    # This line shouldn't be reached, but just in case
                    algo_id = algo_name.lower().replace(" ", "_")
                
                if algo_name in results:
                    try:
                        # Update length
                        length_label = self.__getattribute__(f"{algo_id}_length")
                        length_label.setText(f"{results[algo_name]['length']:.2f} km")
                        
                        # Update time
                        time_label = self.__getattribute__(f"{algo_id}_time")
                        time_label.setText(f"{results[algo_name]['time']:.6f} sec")
                        
                        # Set winner badge
                        if algo_name == shortest_algorithm:
                            winner_badge = self.__getattribute__(f"{algo_id}_winner_label")
                            winner_badge.setVisible(True)
                            
                            # Highlight the winner card
                            card = self.__getattribute__(f"{algo_id}_card")
                            card.setStyleSheet(f"""
                                #{algo_name.replace(' ', '')}Card {{
                                    background-color: rgba(39, 174, 96, 0.1);
                                    border: 2px solid #27ae60;
                                    border-radius: 12px;
                                }}
                            """)
                    except AttributeError as e:
                        logger.error(f"Failed to update {algo_id} algorithm card: {str(e)}")
                        # Continue with other algorithms even if one fails
                        continue
            
            # Update prediction outcome
            self.prediction_value.setText(user_prediction)
            
            if user_prediction == shortest_algorithm:
                # Correct prediction
                self.prediction_outcome.setObjectName("correctPrediction")
                self.prediction_outcome.setText("CORRECT!")
                self.prediction_outcome.setStyleSheet("""
                    #correctPrediction {
                        color: #2ecc71;
                        font-size: 16px;
                        font-weight: bold;
                    }
                """)
                
                self.prediction_icon.setText("🎯") # bullseye icon for correct
                self.prediction_result_text.setText("Nice work! Your prediction was spot on!")
                self.prediction_result_text.setStyleSheet("color: #2ecc71; font-size: 12px;")
                
                # Set lesson text for correct prediction
                self.lesson_text.setText(
                    f"<b>Great job!</b> You correctly predicted that <b>{shortest_algorithm}</b> would find "
                    f"the shortest route. This algorithm was able to find a path with a total distance "
                    f"of <b>{shortest_distance:.2f} km</b>.\n\n"
                    f"The TSP is an NP-hard problem, meaning there's no known algorithm that can solve it "
                    f"efficiently for all cases. Different algorithms have different strengths "
                    f"and weaknesses based on the problem size and structure:\n\n"
                    f"• <b>Brute Force</b> guarantees the optimal solution but scales poorly (O(n!)).\n"
                    f"• <b>Nearest Neighbor</b> is fast but may not find the optimal path.\n"
                    f"• <b>Dynamic Programming</b> finds the optimal solution more efficiently than "
                    f"brute force but still has exponential complexity."
                )
            else:
                # Incorrect prediction
                self.prediction_outcome.setObjectName("incorrectPrediction")
                self.prediction_outcome.setText("INCORRECT!")
                self.prediction_outcome.setStyleSheet("""
                    #incorrectPrediction {
                        color: #e74c3c;
                        font-size: 16px;
                        font-weight: bold;
                    }
                """)
                
                self.prediction_icon.setText("❌") # x icon for incorrect
                self.prediction_result_text.setText(f"Actually, {shortest_algorithm} found the shortest route")
                self.prediction_result_text.setStyleSheet("color: #e74c3c; font-size: 12px;")
                
                # Set lesson text for incorrect prediction
                self.lesson_text.setText(
                    f"You predicted <b>{user_prediction}</b>, but <b>{shortest_algorithm}</b> found the shortest "
                    f"route with a distance of <b>{shortest_distance:.2f} km</b>.\n\n"
                    f"This demonstrates an important concept in algorithm analysis: <b>no single algorithm is "
                    f"always the best</b> for every instance of a problem. The TSP is an NP-hard problem, and "
                    f"algorithm performance depends on multiple factors:\n\n"
                    f"• <b>Problem size</b>: With {len(self.flow_manager.game_state.selected_cities)} cities, "
                    f"certain algorithms may perform better than others.\n"
                    f"• <b>Data distribution</b>: The specific arrangement of cities affects performance.\n"
                    f"• <b>Time-space tradeoff</b>: Some algorithms use more memory to achieve faster execution.\n\n"
                    f"Understanding these tradeoffs is crucial for solving computational problems efficiently."
                )
    
    def restart_game(self):
        """Restart the game with a new scenario"""
        self.flow_manager.reset_game()
        self.flow_manager.show_welcome_screen()
    
    def quit_game(self):
        """Quit the game"""
        import sys
        sys.exit(0)