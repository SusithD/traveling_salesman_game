"""
Summary screen for the Traveling Salesman Problem game
"""
import logging
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QFrame, QGraphicsDropShadowEffect, QSizePolicy, QSpacerItem,
    QScrollArea
)
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect, QEasingCurve
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
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(20)
        
        # Enable size constraints to work better with scrolling
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        # Create scrollable content
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(20)
        
        # Create container with flexible sizing
        container = QFrame()
        container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
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
        
        summary_icon = QLabel("🎯")
        summary_icon.setStyleSheet("""
            font-size: 36px;
            padding: 10px;
            background-color: #8e44ad;
            color: white;
            border-radius: 10px;
        """)
        header_layout.addWidget(summary_icon)
        
        header_text = QVBoxLayout()
        title = QLabel("Game Summary")
        title.setStyleSheet("""
            color: white;
            font-size: 24px;
            font-weight: bold;
        """)
        header_text.addWidget(title)
        
        subtitle = QLabel("Your traveling salesman adventure")
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
        
        # Player info
        player_frame = QFrame()
        player_frame.setStyleSheet("""
            background-color: #2c3e50;
            border-radius: 10px;
            padding: 15px;
        """)
        player_layout = QHBoxLayout(player_frame)
        
        player_icon = QLabel("👤")
        player_icon.setStyleSheet("font-size: 28px; margin-right: 15px;")
        player_layout.addWidget(player_icon)
        
        player_info = QVBoxLayout()
        player_label = QLabel("Player")
        player_label.setStyleSheet("color: #3498db; font-size: 14px; font-weight: bold;")
        player_info.addWidget(player_label)
        
        self.player_name = QLabel("Player Name")  # Will be populated with actual player name
        self.player_name.setStyleSheet("color: white; font-size: 20px; font-weight: bold;")
        player_info.addWidget(self.player_name)
        
        player_layout.addLayout(player_info)
        player_layout.addStretch()
        
        container_layout.addWidget(player_frame)
        
        # Game statistics - use a scroll area for this section
        stats_scroll_area = QScrollArea()
        stats_scroll_area.setWidgetResizable(True)
        stats_scroll_area.setFrameShape(QScrollArea.NoFrame)
        stats_scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        stats_scroll_area.setStyleSheet("""
            background: transparent;
            border: none;
        """)
        
        stats_frame = QFrame()
        stats_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        stats_frame.setStyleSheet("""
            background-color: #222222;
            border-radius: 10px;
            padding: 20px;
        """)
        stats_layout = QVBoxLayout(stats_frame)
        
        stats_title = QLabel("Journey Statistics")
        stats_title.setStyleSheet("color: white; font-size: 18px; font-weight: bold;")
        stats_layout.addWidget(stats_title)
        
        # Grid for stats
        stats_grid = QHBoxLayout()
        stats_grid.setSpacing(20)
        
        # Home city stat
        home_city_layout = self.create_stat_box("🏠", "Home City", "")
        self.home_city_value = home_city_layout.itemAt(2).widget()
        stats_grid.addLayout(home_city_layout)
        
        # Cities visited stat
        cities_visited_layout = self.create_stat_box("🌆", "Cities Visited", "")
        self.cities_visited_value = cities_visited_layout.itemAt(2).widget()
        stats_grid.addLayout(cities_visited_layout)
        
        # Total distance stat
        distance_layout = self.create_stat_box("📏", "Shortest Distance", "")
        self.distance_value = distance_layout.itemAt(2).widget()
        stats_grid.addLayout(distance_layout)
        
        stats_layout.addLayout(stats_grid)
        
        # Add separator
        stats_separator = QFrame()
        stats_separator.setFrameShape(QFrame.HLine)
        stats_separator.setFrameShadow(QFrame.Sunken)
        stats_separator.setStyleSheet("background-color: #333333; height: 1px; margin: 15px 0;")
        stats_layout.addWidget(stats_separator)
        
        # Algorithm comparison
        algo_title = QLabel("Algorithm Comparison")
        algo_title.setStyleSheet("color: white; font-size: 16px; font-weight: bold; margin-top: 5px;")
        stats_layout.addWidget(algo_title)
        
        # Algorithm stats grid
        algo_grid = QVBoxLayout()
        algo_grid.setSpacing(15)
        
        # Winning algorithm
        self.winner_layout = QHBoxLayout()
        
        winner_label = QLabel("Winning Algorithm")
        winner_label.setStyleSheet("color: #2ecc71; font-size: 14px; font-weight: bold;")
        self.winner_layout.addWidget(winner_label)
        
        self.winner_name = QLabel()
        self.winner_name.setStyleSheet("color: white; font-size: 14px;")
        self.winner_layout.addWidget(self.winner_name)
        
        self.winner_layout.addStretch()
        
        self.winner_distance = QLabel()
        self.winner_distance.setStyleSheet("color: #2ecc71; font-size: 14px; font-weight: bold;")
        self.winner_layout.addWidget(self.winner_distance)
        
        algo_grid.addLayout(self.winner_layout)
        
        # Performance comparison
        algo_comparison = QHBoxLayout()
        
        # Brute Force stats
        bf_layout = QVBoxLayout()
        bf_title = QLabel("Brute Force")
        bf_title.setStyleSheet("color: #e74c3c; font-size: 13px; font-weight: bold;")
        bf_title.setAlignment(Qt.AlignCenter)
        bf_layout.addWidget(bf_title)
        
        self.bf_time = QLabel()
        self.bf_time.setStyleSheet("color: white; font-size: 12px;")
        self.bf_time.setAlignment(Qt.AlignCenter)
        bf_layout.addWidget(self.bf_time)
        
        algo_comparison.addLayout(bf_layout)
        
        # Nearest Neighbor stats
        nn_layout = QVBoxLayout()
        nn_title = QLabel("Nearest Neighbor")
        nn_title.setStyleSheet("color: #3498db; font-size: 13px; font-weight: bold;")
        nn_title.setAlignment(Qt.AlignCenter)
        nn_layout.addWidget(nn_title)
        
        self.nn_time = QLabel()
        self.nn_time.setStyleSheet("color: white; font-size: 12px;")
        self.nn_time.setAlignment(Qt.AlignCenter)
        nn_layout.addWidget(self.nn_time)
        
        algo_comparison.addLayout(nn_layout)
        
        # Dynamic Programming stats
        dp_layout = QVBoxLayout()
        dp_title = QLabel("Dynamic Programming")
        dp_title.setStyleSheet("color: #f39c12; font-size: 13px; font-weight: bold;")
        dp_title.setAlignment(Qt.AlignCenter)
        dp_layout.addWidget(dp_title)
        
        self.dp_time = QLabel()
        self.dp_time.setStyleSheet("color: white; font-size: 12px;")
        self.dp_time.setAlignment(Qt.AlignCenter)
        dp_layout.addWidget(self.dp_time)
        
        algo_comparison.addLayout(dp_layout)
        
        algo_grid.addLayout(algo_comparison)
        
        stats_layout.addLayout(algo_grid)
        
        # Set the stats frame as the scroll area widget
        stats_scroll_area.setWidget(stats_frame)
        container_layout.addWidget(stats_scroll_area)
        
        # Prediction result
        prediction_frame = QFrame()
        prediction_frame.setStyleSheet("""
            border-radius: 10px;
            padding: 15px;
        """)
        prediction_layout = QVBoxLayout(prediction_frame)
        
        prediction_title = QLabel("Your Algorithm Prediction")
        prediction_title.setStyleSheet("color: white; font-size: 16px; font-weight: bold;")
        prediction_layout.addWidget(prediction_title)
        
        prediction_result = QHBoxLayout()
        
        prediction_label = QLabel("You predicted:")
        prediction_label.setStyleSheet("color: #aaaaaa; font-size: 14px;")
        prediction_result.addWidget(prediction_label)
        
        self.prediction_value = QLabel()
        self.prediction_value.setStyleSheet("color: white; font-size: 14px; font-weight: bold;")
        prediction_result.addWidget(self.prediction_value)
        
        prediction_result.addStretch()
        
        self.prediction_outcome = QLabel()
        self.prediction_outcome.setStyleSheet("""
            padding: 5px 10px;
            border-radius: 3px;
        """)
        prediction_result.addWidget(self.prediction_outcome)
        
        prediction_layout.addLayout(prediction_result)
        
        container_layout.addWidget(prediction_frame)
        
        # Learned lesson
        lesson_frame = QFrame()
        lesson_frame.setStyleSheet("""
            background-color: rgba(25, 118, 210, 0.1);
            border: 1px solid #1976D2;
            border-radius: 10px;
            padding: 15px;
        """)
        lesson_layout = QVBoxLayout(lesson_frame)
        
        lesson_title = QLabel("What We Learned")
        lesson_title.setStyleSheet("color: #1976D2; font-size: 16px; font-weight: bold;")
        lesson_layout.addWidget(lesson_title)
        
        self.lesson_text = QLabel()
        self.lesson_text.setWordWrap(True)
        self.lesson_text.setStyleSheet("color: white; font-size: 14px; line-height: 1.4;")
        lesson_layout.addWidget(self.lesson_text)
        
        container_layout.addWidget(lesson_frame)
        
        # Button area
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        play_again_button = QPushButton("Play Again")
        play_again_button.setStyleSheet("""
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
        play_again_button.clicked.connect(self.restart_game)
        button_layout.addWidget(play_again_button)
        
        quit_button = QPushButton("Quit Game")
        quit_button.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        quit_button.clicked.connect(self.quit_game)
        button_layout.addWidget(quit_button)
        
        container_layout.addLayout(button_layout)
        
        # Add container to content layout
        content_layout.addWidget(container)
        
        # Add content to main layout
        main_layout.addWidget(content_widget)
    
    def create_stat_box(self, icon, title, value):
        """Create a statistics box layout"""
        stat_layout = QVBoxLayout()
        stat_layout.setAlignment(Qt.AlignCenter)
        
        icon_label = QLabel(icon)
        icon_label.setStyleSheet("font-size: 24px;")
        icon_label.setAlignment(Qt.AlignCenter)
        stat_layout.addWidget(icon_label)
        
        title_label = QLabel(title)
        title_label.setStyleSheet("color: #aaaaaa; font-size: 12px;")
        title_label.setAlignment(Qt.AlignCenter)
        stat_layout.addWidget(title_label)
        
        value_label = QLabel(value)
        value_label.setStyleSheet("color: white; font-size: 18px; font-weight: bold;")
        value_label.setAlignment(Qt.AlignCenter)
        stat_layout.addWidget(value_label)
        
        return stat_layout
    
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
        shortest_distance = 0  # Default initialization
        
        if results and shortest_algorithm:
            # Update shortest distance
            shortest_distance = results[shortest_algorithm]["length"]
            self.distance_value.setText(f"{shortest_distance:.2f} km")
            
            # Update winner info
            self.winner_name.setText(shortest_algorithm)
            self.winner_distance.setText(f"{shortest_distance:.2f} km")
            
            # Update algorithm times
            if "Brute Force" in results:
                self.bf_time.setText(f"{results['Brute Force']['time']:.6f} sec")
            
            if "Nearest Neighbor" in results:
                self.nn_time.setText(f"{results['Nearest Neighbor']['time']:.6f} sec")
            
            if "Dynamic Programming" in results:
                self.dp_time.setText(f"{results['Dynamic Programming']['time']:.6f} sec")
        
        # Update prediction and outcome
        if hasattr(self.flow_manager.game_state, 'user_prediction'):
            user_prediction = self.flow_manager.game_state.user_prediction
            self.prediction_value.setText(user_prediction)
            
            if user_prediction == shortest_algorithm:
                self.prediction_outcome.setText("CORRECT")
                self.prediction_outcome.setStyleSheet("""
                    background-color: #27ae60;
                    color: white;
                    padding: 5px 10px;
                    border-radius: 3px;
                    font-weight: bold;
                """)
                
                # Set lesson text for correct prediction
                self.lesson_text.setText(
                    f"Great job! You correctly predicted that {shortest_algorithm} would find "
                    f"the shortest route. This algorithm was able to find a path with a total distance "
                    f"of {shortest_distance:.2f} km. Different algorithms have different strengths and "
                    f"weaknesses based on the problem size and structure."
                )
            else:
                self.prediction_outcome.setText("INCORRECT")
                self.prediction_outcome.setStyleSheet("""
                    background-color: #e74c3c;
                    color: white;
                    padding: 5px 10px;
                    border-radius: 3px;
                    font-weight: bold;
                """)
                
                # Set lesson text for incorrect prediction
                self.lesson_text.setText(
                    f"You predicted {user_prediction}, but {shortest_algorithm} found the shortest "
                    f"route with a distance of {shortest_distance:.2f} km. This shows how algorithm "
                    f"performance can vary based on the specific problem. For the Traveling Salesman Problem, "
                    f"the best algorithm depends on factors like number of cities, their distribution, and "
                    f"available computational resources."
                )
    
    def restart_game(self):
        """Restart the game with a new scenario"""
        self.flow_manager.reset_game()
        self.flow_manager.show_welcome_screen()
    
    def quit_game(self):
        """Quit the game"""
        import sys
        sys.exit(0)