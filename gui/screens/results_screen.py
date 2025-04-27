"""
Results screen for the Traveling Salesman Problem game
"""
import logging
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QFrame, QTabWidget, QGraphicsDropShadowEffect, QSizePolicy,
    QScrollArea
)
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect, QEasingCurve, QTimer
from PyQt5.QtGui import QColor, QFont

logger = logging.getLogger("ResultsScreen")

class ResultsScreen(QWidget):
    """
    Screen for displaying algorithm results and route comparisons
    """
    def __init__(self, flow_manager):
        super().__init__()
        self.flow_manager = flow_manager
        self.current_algorithm_index = 0
        self.algorithm_names = []
        
        # Animation timers
        self.reveal_timer = QTimer(self)
        self.reveal_timer.timeout.connect(self.reveal_next_algorithm)
        
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
        
        results_icon = QLabel("🏆")
        results_icon.setStyleSheet("""
            font-size: 36px;
            padding: 10px;
            background-color: #9b59b6;
            color: white;
            border-radius: 10px;
        """)
        header_layout.addWidget(results_icon)
        
        header_text = QVBoxLayout()
        title = QLabel("Results")
        title.setStyleSheet("""
            color: white;
            font-size: 24px;
            font-weight: bold;
        """)
        header_text.addWidget(title)
        
        subtitle = QLabel("Algorithm performance comparison")
        subtitle.setStyleSheet("color: #aaaaaa; font-size: 16px;")
        header_text.addWidget(subtitle)
        
        header_layout.addLayout(header_text)
        header_layout.addStretch()
        
        # Prediction result indicator
        self.prediction_result = QLabel()
        self.prediction_result.setStyleSheet("""
            padding: 8px 15px;
            border-radius: 5px;
            font-weight: bold;
            font-size: 14px;
        """)
        header_layout.addWidget(self.prediction_result)
        
        container_layout.addLayout(header_layout)
        
        # Add separator
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        separator.setStyleSheet("background-color: #333333; height: 1px;")
        container_layout.addWidget(separator)
        
        # Journey summary
        self.journey_summary = QLabel()
        self.journey_summary.setWordWrap(True)
        self.journey_summary.setStyleSheet("""
            color: white;
            font-size: 15px;
            padding: 10px;
            background-color: #2c3e50;
            border-radius: 8px;
        """)
        container_layout.addWidget(self.journey_summary)
        
        # Algorithm results displayed in stages
        self.results_container = QFrame()
        self.results_container.setStyleSheet("""
            background-color: #222222;
            border-radius: 10px;
            padding: 15px;
        """)
        results_layout = QVBoxLayout(self.results_container)
        
        # Algorithm cards container (will be populated dynamically)
        self.algo_cards_layout = QVBoxLayout()
        self.algo_cards_layout.setSpacing(15)
        results_layout.addLayout(self.algo_cards_layout)
        
        container_layout.addWidget(self.results_container)
        
        # Winner section (initially hidden)
        self.winner_frame = QFrame()
        self.winner_frame.setStyleSheet("""
            background-color: #27ae60;
            border-radius: 10px;
            padding: 15px;
        """)
        self.winner_frame.setVisible(False)
        winner_layout = QVBoxLayout(self.winner_frame)
        
        winner_title = QLabel("Winning Algorithm")
        winner_title.setStyleSheet("""
            color: white;
            font-size: 18px;
            font-weight: bold;
        """)
        winner_title.setAlignment(Qt.AlignCenter)
        winner_layout.addWidget(winner_title)
        
        self.winner_label = QLabel()
        self.winner_label.setStyleSheet("""
            color: white;
            font-size: 24px;
            font-weight: bold;
        """)
        self.winner_label.setAlignment(Qt.AlignCenter)
        winner_layout.addWidget(self.winner_label)
        
        self.winner_stats = QLabel()
        self.winner_stats.setStyleSheet("""
            color: rgba(255, 255, 255, 0.8);
            font-size: 14px;
        """)
        self.winner_stats.setAlignment(Qt.AlignCenter)
        winner_layout.addWidget(self.winner_stats)
        
        container_layout.addWidget(self.winner_frame)
        
        # Navigation buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        restart_button = QPushButton("New Game")
        restart_button.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px 15px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        restart_button.clicked.connect(self.restart_game)
        button_layout.addWidget(restart_button)
        
        continue_button = QPushButton("Summary →")
        continue_button.setStyleSheet("""
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
        """)
        continue_button.clicked.connect(self.show_summary)
        button_layout.addWidget(continue_button)
        
        container_layout.addLayout(button_layout)
        
        # Add container to main layout
        main_layout.addWidget(container)
    
    def create_algorithm_card(self, algorithm, result):
        """Create a card showing algorithm results"""
        card = QFrame()
        card.setObjectName(f"{algorithm.lower().replace(' ', '_')}_card")
        
        if self.flow_manager.game_state.shortest_algorithm == algorithm:
            # Highlight the winning algorithm
            card.setStyleSheet("""
                background-color: rgba(39, 174, 96, 0.2);
                border: 2px solid #27ae60;
                border-radius: 10px;
                padding: 15px;
                margin: 5px 0;
            """)
        else:
            card.setStyleSheet("""
                background-color: #1a1a1a;
                border: 1px solid #333333;
                border-radius: 10px;
                padding: 15px;
                margin: 5px 0;
            """)
        
        # Add card shadow effect
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 0, 0, 80))
        shadow.setOffset(0, 3)
        card.setGraphicsEffect(shadow)
        
        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(10)
        
        # Algorithm name and performance
        header_layout = QHBoxLayout()
        
        # Algorithm name with indicator
        name_layout = QVBoxLayout()
        
        name = QLabel(algorithm)
        name.setStyleSheet("""
            color: white;
            font-size: 18px;
            font-weight: bold;
        """)
        name_layout.addWidget(name)
        
        complexity = QLabel(f"Complexity: {result['complexity']}")
        complexity.setStyleSheet("color: #aaaaaa; font-size: 12px;")
        name_layout.addWidget(complexity)
        
        header_layout.addLayout(name_layout)
        header_layout.addStretch()
        
        # Route length and time
        stats_layout = QVBoxLayout()
        stats_layout.setAlignment(Qt.AlignRight)
        
        route_length = QLabel(f"Route Length: {result['length']:.2f} km")
        route_length.setStyleSheet("""
            color: white;
            font-size: 16px;
            font-weight: bold;
        """)
        stats_layout.addWidget(route_length)
        
        time_taken = QLabel(f"Time: {result['time']:.6f} seconds")
        time_taken.setStyleSheet("color: #aaaaaa; font-size: 12px;")
        stats_layout.addWidget(time_taken)
        
        header_layout.addLayout(stats_layout)
        
        card_layout.addLayout(header_layout)
        
        # Add separator
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        separator.setStyleSheet("background-color: #333333; height: 1px;")
        card_layout.addWidget(separator)
        
        # Route visualization
        route_frame = QFrame()
        route_frame.setStyleSheet("background-color: #222222; border-radius: 5px;")
        route_layout = QVBoxLayout(route_frame)
        
        route_title = QLabel("Route")
        route_title.setStyleSheet("color: #bbbbbb; font-size: 14px;")
        route_layout.addWidget(route_title)
        
        route_text = " → ".join(result['route'])
        route_label = QLabel(route_text)
        route_label.setWordWrap(True)
        route_label.setStyleSheet("""
            color: white;
            font-size: 14px;
            padding: 5px;
            background-color: #333333;
            border-radius: 5px;
        """)
        route_layout.addWidget(route_label)
        
        card_layout.addWidget(route_frame)
        
        return card
    
    def reset(self):
        """Reset the results screen state"""
        # Clear algorithm cards
        for i in reversed(range(self.algo_cards_layout.count())):
            widget = self.algo_cards_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)
        
        # Hide winner section
        self.winner_frame.setVisible(False)
        
        # Reset algorithm index
        self.current_algorithm_index = 0
        self.algorithm_names = []
    
    def setup_results(self):
        """Set up the results screen with current game data"""
        # Reset any previous state
        self.reset()
        
        # Get results from game state
        results = self.flow_manager.game_state.algorithm_results
        if not results:
            self.journey_summary.setText("No results available.")
            return
        
        # Set journey summary
        player_name = self.flow_manager.game_state.player_name
        home_city = self.flow_manager.game_state.home_city
        city_count = len(self.flow_manager.game_state.selected_cities)
        
        self.journey_summary.setText(
            f"{player_name}'s journey: Starting from {home_city}, "
            f"visiting {city_count - 1} cities, and returning to {home_city}."
        )
        
        # Store algorithm names for staged reveal
        self.algorithm_names = list(results.keys())
        
        # Set prediction result
        user_prediction = self.flow_manager.game_state.user_prediction
        shortest_algorithm = self.flow_manager.game_state.shortest_algorithm
        
        if user_prediction == shortest_algorithm:
            self.prediction_result.setText("Your prediction was correct!")
            self.prediction_result.setStyleSheet("""
                background-color: #27ae60;
                color: white;
                padding: 8px 15px;
                border-radius: 5px;
                font-weight: bold;
                font-size: 14px;
            """)
        else:
            self.prediction_result.setText("Your prediction was incorrect")
            self.prediction_result.setStyleSheet("""
                background-color: #e74c3c;
                color: white;
                padding: 8px 15px;
                border-radius: 5px;
                font-weight: bold;
                font-size: 14px;
            """)
        
        # Start revealing algorithms one by one for dramatic effect
        self.reveal_timer.start(1000)  # Show one algorithm per second
    
    def reveal_next_algorithm(self):
        """Reveal the next algorithm result"""
        if self.current_algorithm_index < len(self.algorithm_names):
            # Get the algorithm and its results
            algorithm = self.algorithm_names[self.current_algorithm_index]
            result = self.flow_manager.game_state.algorithm_results[algorithm]
            
            # Create and add the algorithm card
            card = self.create_algorithm_card(algorithm, result)
            self.algo_cards_layout.addWidget(card)
            
            # Increment index
            self.current_algorithm_index += 1
        else:
            # Stop the timer once all algorithms are revealed
            self.reveal_timer.stop()
            
            # Show winner section
            self.show_winner()
    
    def show_winner(self):
        """Show the winning algorithm section"""
        shortest_algorithm = self.flow_manager.game_state.shortest_algorithm
        if shortest_algorithm:
            result = self.flow_manager.game_state.algorithm_results[shortest_algorithm]
            
            self.winner_label.setText(shortest_algorithm)
            self.winner_stats.setText(
                f"Route Length: {result['length']:.2f} km | "
                f"Execution Time: {result['time']:.6f} seconds"
            )
            
            # Show winner frame with animation
            self.winner_frame.setVisible(True)
            
            # Apply animation effect
            self.winner_frame.setStyleSheet("""
                background-color: #27ae60;
                border-radius: 10px;
                padding: 15px;
            """)
    
    def restart_game(self):
        """Restart the game with a new scenario"""
        self.flow_manager.reset_game()
        self.flow_manager.show_welcome_screen()
    
    def show_summary(self):
        """Continue to the summary screen"""
        self.flow_manager.show_summary_screen()