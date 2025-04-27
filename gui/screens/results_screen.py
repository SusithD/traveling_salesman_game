"""
Results screen for the Traveling Salesman Problem game
"""
import logging
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QFrame, QTabWidget, QGraphicsDropShadowEffect, QSizePolicy,
    QScrollArea, QGraphicsOpacityEffect
)
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect, QEasingCurve, QTimer
from PyQt5.QtGui import QColor, QFont
from utils.visualization import PerformanceChart, plot_route_on_map

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
        # Main layout with center alignment
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(20)
        main_layout.setAlignment(Qt.AlignCenter)
        
        # Create central container frame with modern styling
        central_frame = QFrame()
        central_frame.setObjectName("resultsContainer")
        central_frame.setMinimumWidth(1000)
        central_frame.setMaximumWidth(1200)
        central_frame.setStyleSheet("""
            #resultsContainer {
                background-color: rgba(26, 26, 26, 0.7);
                border-radius: 20px;
                border: 1px solid rgba(255, 255, 255, 0.1);
            }
        """)
        
        container_layout = QVBoxLayout(central_frame)
        container_layout.setContentsMargins(40, 40, 40, 40)
        container_layout.setSpacing(25)
        
        # Header with results icon
        header_frame = QFrame()
        header_frame.setObjectName("headerFrame")
        header_frame.setStyleSheet("""
            #headerFrame {
                background-color: rgba(155, 89, 182, 0.15);
                border-radius: 15px;
            }
        """)
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(20, 15, 20, 15)
        
        # Left side - Title with icon
        header_left = QHBoxLayout()
        
        # Results icon
        results_icon = QLabel("🏆")
        results_icon.setFixedSize(60, 60)
        results_icon.setObjectName("resultsIcon")
        results_icon.setStyleSheet("""
            #resultsIcon {
                font-size: 30px;
                background-color: #9b59b6;
                color: white;
                border-radius: 30px;
                margin-right: 15px;
            }
        """)
        results_icon.setAlignment(Qt.AlignCenter)
        header_left.addWidget(results_icon)
        
        # Title and subtitle
        title_layout = QVBoxLayout()
        title_layout.setSpacing(5)
        
        title = QLabel("ALGORITHM RESULTS")
        title.setObjectName("resultsTitle")
        title.setStyleSheet("""
            #resultsTitle {
                color: white;
                font-size: 22px;
                font-weight: bold;
                letter-spacing: 1px;
            }
        """)
        title_layout.addWidget(title)
        
        subtitle = QLabel("See how each algorithm performed in solving your TSP")
        subtitle.setObjectName("resultsSubtitle")
        subtitle.setStyleSheet("""
            #resultsSubtitle {
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
        
        self.prediction_result = QLabel("Waiting for results...")
        self.prediction_result.setObjectName("predictionResult")
        self.prediction_result.setStyleSheet("""
            #predictionResult {
                color: white;
                font-size: 14px;
                font-weight: bold;
            }
        """)
        self.prediction_result.setAlignment(Qt.AlignCenter)
        prediction_layout.addWidget(self.prediction_result)
        
        header_layout.addWidget(prediction_container)
        container_layout.addWidget(header_frame)
        
        # Stylish separator
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setStyleSheet("""
            background-color: #9b59b6;
            max-width: 150px;
            height: 3px;
            margin: 5px;
        """)
        container_layout.addWidget(separator, 0, Qt.AlignCenter)
        
        # Journey summary with improved styling
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
        journey_layout.setContentsMargins(20, 20, 20, 20)
        journey_layout.setSpacing(15)
        
        journey_title = QLabel("YOUR JOURNEY")
        journey_title.setObjectName("journeyTitle")
        journey_title.setStyleSheet("""
            #journeyTitle {
                color: #9b59b6;
                font-size: 16px;
                font-weight: bold;
                letter-spacing: 1px;
            }
        """)
        journey_title.setAlignment(Qt.AlignCenter)
        journey_layout.addWidget(journey_title)
        
        self.journey_summary = QLabel()
        self.journey_summary.setObjectName("journeyDetails")
        self.journey_summary.setWordWrap(True)
        self.journey_summary.setStyleSheet("""
            #journeyDetails {
                color: #DDDDDD;
                font-size: 15px;
                line-height: 150%;
                background-color: rgba(155, 89, 182, 0.1);
                border: 1px solid rgba(155, 89, 182, 0.2);
                border-radius: 10px;
                padding: 15px;
            }
        """)
        self.journey_summary.setAlignment(Qt.AlignCenter)
        journey_layout.addWidget(self.journey_summary)
        
        container_layout.addWidget(journey_frame)
        
        # Algorithm results section with improved styling
        results_frame = QFrame()
        results_frame.setObjectName("resultsFrame")
        results_frame.setMinimumHeight(400)  # Ensure sufficient space for algorithm cards
        results_frame.setStyleSheet("""
            #resultsFrame {
                background-color: rgba(33, 33, 33, 0.7);
                border-radius: 15px;
                padding: 5px;
            }
        """)
        results_layout = QVBoxLayout(results_frame)
        results_layout.setContentsMargins(20, 20, 20, 20)
        results_layout.setSpacing(20)
        
        results_title = QLabel("ALGORITHM PERFORMANCE")
        results_title.setObjectName("algorithmsTitle")
        results_title.setStyleSheet("""
            #algorithmsTitle {
                color: white;
                font-size: 16px;
                font-weight: bold;
                letter-spacing: 1px;
            }
        """)
        results_title.setAlignment(Qt.AlignCenter)
        results_layout.addWidget(results_title)
        
        # Algorithm cards container in a scrollable area
        results_scroll = QScrollArea()
        results_scroll.setObjectName("resultsScroll")
        results_scroll.setWidgetResizable(True)
        results_scroll.setFrameShape(QScrollArea.NoFrame)
        results_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        results_scroll.setStyleSheet("""
            #resultsScroll {
                border: none;
                background: transparent;
            }
            QScrollBar:vertical {
                border: none;
                background: rgba(51, 51, 51, 0.5);
                width: 8px;
                border-radius: 4px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #666666;
                min-height: 20px;
                border-radius: 4px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)
        
        self.results_container = QWidget()
        self.results_container.setObjectName("cardsContainer")
        self.results_container.setStyleSheet("""
            #cardsContainer {
                background-color: transparent;
                padding: 5px;
            }
        """)
        cards_layout = QVBoxLayout(self.results_container)
        cards_layout.setContentsMargins(5, 5, 5, 5)
        cards_layout.setSpacing(15)
        
        # Algorithm cards will be added here dynamically
        self.algo_cards_layout = QVBoxLayout()
        self.algo_cards_layout.setSpacing(15)
        cards_layout.addLayout(self.algo_cards_layout)
        cards_layout.addStretch()
        
        results_scroll.setWidget(self.results_container)
        results_layout.addWidget(results_scroll)
        
        container_layout.addWidget(results_frame, 1)
        
        # Visualization tab widget with modern styling
        self.visualization_frame = QFrame()
        self.visualization_frame.setObjectName("visualizationFrame")
        self.visualization_frame.setMinimumHeight(450)  # Minimum height
        self.visualization_frame.setMaximumHeight(450)  # Maximum height to prevent auto-expansion
        self.visualization_frame.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)  # Fixed vertical size policy
        self.visualization_frame.setStyleSheet("""
            #visualizationFrame {
                background-color: rgba(33, 33, 33, 0.7);
                border-radius: 15px;
                padding: 5px;
            }
        """)
        visualization_layout = QVBoxLayout(self.visualization_frame)
        visualization_layout.setContentsMargins(20, 20, 20, 20)
        visualization_layout.setSpacing(15)
        
        # Tab widget for different visualizations
        self.viz_tabs = QTabWidget()
        self.viz_tabs.setObjectName("vizTabs")
        self.viz_tabs.setStyleSheet("""
            QTabWidget {
                background-color: transparent;
                border: none;
            }
            QTabWidget::pane {
                background-color: rgba(40, 40, 40, 0.7);
                border: 1px solid #444444;
                border-radius: 8px;
                border-top-left-radius: 0px;
            }
            QTabBar::tab {
                background-color: #2d3436;
                color: #bbbbbb;
                padding: 10px 20px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                margin-right: 3px;
            }
            QTabBar::tab:selected {
                background-color: #9b59b6;
                color: white;
                font-weight: bold;
            }
            QTabBar::tab:hover:!selected {
                background-color: #3d4446;
                color: white;
            }
        """)
        
        # Create performance charts with fixed size
        self.route_length_chart = PerformanceChart(width=7, height=4, dpi=80)
        self.execution_time_chart = PerformanceChart(width=7, height=4, dpi=80)
        self.comparison_chart = PerformanceChart(width=10, height=4, dpi=80)
        self.route_map_widget = QWidget()
        
        # Set fixed size policies for all chart widgets
        self.route_length_chart.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.execution_time_chart.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.comparison_chart.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.route_map_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        # Add chart widgets to tabs
        self.viz_tabs.addTab(self.route_length_chart, "Route Length")
        self.viz_tabs.addTab(self.execution_time_chart, "Execution Time")
        self.viz_tabs.addTab(self.comparison_chart, "Comparison")
        self.viz_tabs.addTab(self.route_map_widget, "Route Map")
        
        # Add viz tabs to layout
        visualization_layout.addWidget(self.viz_tabs)
        
        # Add visualization frame after results frame but before winner frame
        container_layout.addWidget(self.visualization_frame)
        
        # Winner section with improved styling
        self.winner_frame = QFrame()
        self.winner_frame.setObjectName("winnerFrame")
        self.winner_frame.setStyleSheet("""
            #winnerFrame {
                background-color: rgba(39, 174, 96, 0.2);
                border: 1px solid rgba(39, 174, 96, 0.3);
                border-radius: 15px;
                padding: 15px;
            }
        """)
        self.winner_frame.setVisible(False)
        winner_layout = QVBoxLayout(self.winner_frame)
        winner_layout.setContentsMargins(20, 20, 20, 20)
        winner_layout.setSpacing(15)
        
        # Trophy icon with crown
        trophy_container = QFrame()
        trophy_container.setFixedSize(80, 80)
        trophy_container.setStyleSheet("""
            background-color: #27ae60;
            border-radius: 40px;
            margin-bottom: 10px;
        """)
        trophy_layout = QVBoxLayout(trophy_container)
        trophy_layout.setContentsMargins(0, 0, 0, 0)
        trophy_layout.setAlignment(Qt.AlignCenter)
        
        trophy_icon = QLabel("👑")
        trophy_icon.setStyleSheet("""
            font-size: 40px;
            color: white;
        """)
        trophy_icon.setAlignment(Qt.AlignCenter)
        trophy_layout.addWidget(trophy_icon)
        
        winner_layout.addWidget(trophy_container, 0, Qt.AlignCenter)
        
        winner_title = QLabel("WINNING ALGORITHM")
        winner_title.setObjectName("winnerTitle")
        winner_title.setStyleSheet("""
            #winnerTitle {
                color: #27ae60;
                font-size: 16px;
                font-weight: bold;
                letter-spacing: 1px;
            }
        """)
        winner_title.setAlignment(Qt.AlignCenter)
        winner_layout.addWidget(winner_title)
        
        self.winner_label = QLabel()
        self.winner_label.setObjectName("winnerName")
        self.winner_label.setStyleSheet("""
            #winnerName {
                color: white;
                font-size: 24px;
                font-weight: bold;
            }
        """)
        self.winner_label.setAlignment(Qt.AlignCenter)
        
        # Add shadow to winner name for emphasis
        winner_shadow = QGraphicsDropShadowEffect()
        winner_shadow.setBlurRadius(15)
        winner_shadow.setColor(QColor("#27ae60"))
        winner_shadow.setOffset(0, 0)
        self.winner_label.setGraphicsEffect(winner_shadow)
        
        winner_layout.addWidget(self.winner_label)
        
        self.winner_stats = QLabel()
        self.winner_stats.setObjectName("winnerStats")
        self.winner_stats.setWordWrap(True)
        self.winner_stats.setStyleSheet("""
            #winnerStats {
                color: #DDDDDD;
                font-size: 14px;
                background-color: rgba(39, 174, 96, 0.1);
                border-radius: 10px;
                padding: 10px;
            }
        """)
        self.winner_stats.setAlignment(Qt.AlignCenter)
        winner_layout.addWidget(self.winner_stats)
        
        container_layout.addWidget(self.winner_frame)
        
        # Button area with updated styling
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)
        button_layout.setAlignment(Qt.AlignCenter)
        
        back_button = QPushButton("← NEW GAME")
        back_button.setObjectName("backButton")
        back_button.setFixedSize(180, 50)
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
        back_button.clicked.connect(self.restart_game)
        button_layout.addWidget(back_button)
        
        continue_button = QPushButton("VIEW SUMMARY →")
        continue_button.setObjectName("continueButton")
        continue_button.setFixedSize(250, 50)
        continue_button.setStyleSheet("""
            #continueButton {
                background-color: #9b59b6;
                color: white;
                border: none;
                border-radius: 12px;
                padding: 12px 25px;
                font-size: 14px;
                font-weight: bold;
                letter-spacing: 1px;
            }
            #continueButton:hover {
                background-color: #8e44ad;
            }
            #continueButton:pressed {
                background-color: #7d3c98;
            }
        """)
        continue_button.clicked.connect(self.show_summary)
        button_layout.addWidget(continue_button)
        
        container_layout.addLayout(button_layout)
        
        # Add container to main layout
        main_layout.addWidget(central_frame, 0, Qt.AlignCenter)
    
    def create_algorithm_card(self, algorithm, result):
        """Create a card showing algorithm results with improved styling"""
        # Determine color and styling based on algorithm
        colors = {
            "Brute Force": "#e74c3c",
            "Nearest Neighbor": "#3498db",
            "Dynamic Programming": "#2ecc71"
        }
        color = colors.get(algorithm, "#9b59b6")  # Default to purple if unknown
        
        # Check if this is the winning algorithm
        is_winner = self.flow_manager.game_state.shortest_algorithm == algorithm
        
        card = QFrame()
        card.setObjectName(f"{algorithm.replace(' ', '')}Card")
        
        # Apply styling based on whether it's the winning algorithm
        if is_winner:
            card.setStyleSheet(f"""
                #{algorithm.replace(' ', '')}Card {{
                    background-color: rgba(39, 174, 96, 0.2);
                    border: 2px solid #27ae60;
                    border-radius: 15px;
                    padding: 0px;
                    margin: 5px 0px;
                }}
            """)
        else:
            card.setStyleSheet(f"""
                #{algorithm.replace(' ', '')}Card {{
                    background-color: rgba(40, 40, 40, 0.7);
                    border: 1px solid {color};
                    border-radius: 15px;
                    padding: 0px;
                    margin: 5px 0px;
                }}
            """)
        
        # Add shadow effect
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 0, 0, 80))
        shadow.setOffset(0, 3)
        card.setGraphicsEffect(shadow)
        
        card_layout = QHBoxLayout(card)
        card_layout.setContentsMargins(20, 20, 20, 20)
        card_layout.setSpacing(20)
        
        # Left side - Icon and algorithm info
        left_layout = QHBoxLayout()
        left_layout.setSpacing(15)
        
        # Icon based on algorithm
        icons = {
            "Brute Force": "🧮",
            "Nearest Neighbor": "📍",
            "Dynamic Programming": "⚙️"
        }
        icon = icons.get(algorithm, "🔍")  # Default icon if unknown
        
        icon_frame = QFrame()
        icon_frame.setObjectName(f"{algorithm.replace(' ', '')}Icon")
        icon_frame.setFixedSize(70, 70)
        icon_frame.setStyleSheet(f"""
            #{algorithm.replace(' ', '')}Icon {{
                background-color: {color};
                border-radius: 35px;
            }}
        """)
        icon_layout = QVBoxLayout(icon_frame)
        icon_layout.setContentsMargins(0, 0, 0, 0)
        
        icon_label = QLabel(icon)
        icon_label.setStyleSheet("""
            font-size: 30px;
            color: white;
        """)
        icon_label.setAlignment(Qt.AlignCenter)
        icon_layout.addWidget(icon_label)
        
        left_layout.addWidget(icon_frame)
        
        # Algorithm details
        algo_details = QVBoxLayout()
        algo_details.setSpacing(5)
        
        algo_name = QLabel(algorithm)
        algo_name.setObjectName(f"{algorithm.replace(' ', '')}Name")
        algo_name.setStyleSheet(f"""
            #{algorithm.replace(' ', '')}Name {{
                color: white;
                font-size: 18px;
                font-weight: bold;
            }}
        """)
        algo_details.addWidget(algo_name)
        
        # Complexity info
        complexity = QLabel(f"Complexity: {result['complexity']}")
        complexity.setStyleSheet("""
            color: #bbbbbb;
            font-size: 14px;
        """)
        algo_details.addWidget(complexity)
        
        # Route summary
        route_summary = QLabel("Route: " + " → ".join([result['route'][0], "...", result['route'][-1]]))
        route_summary.setStyleSheet("""
            color: #aaaaaa;
            font-size: 13px;
        """)
        algo_details.addWidget(route_summary)
        
        left_layout.addLayout(algo_details)
        card_layout.addLayout(left_layout)
        
        # Spacer
        card_layout.addStretch()
        
        # Right side - Performance metrics
        metrics_layout = QVBoxLayout()
        metrics_layout.setSpacing(10)
        metrics_layout.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        
        # Route length with appropriate styling
        length_layout = QVBoxLayout()
        length_layout.setAlignment(Qt.AlignRight)
        
        length_label = QLabel("ROUTE LENGTH")
        length_label.setStyleSheet("""
            color: #aaaaaa;
            font-size: 12px;
            font-weight: bold;
        """)
        length_layout.addWidget(length_label)
        
        length_value = QLabel(f"{result['length']:.2f} km")
        length_value.setObjectName(f"{algorithm.replace(' ', '')}Length")
        length_value.setStyleSheet(f"""
            #{algorithm.replace(' ', '')}Length {{
                color: {color};
                font-size: 22px;
                font-weight: bold;
            }}
        """)
        length_layout.addWidget(length_value)
        
        metrics_layout.addLayout(length_layout)
        
        # Execution time with appropriate styling  
        time_layout = QVBoxLayout()
        time_layout.setAlignment(Qt.AlignRight)
        
        time_label = QLabel("EXECUTION TIME")
        time_label.setStyleSheet("""
            color: #aaaaaa;
            font-size: 12px;
            font-weight: bold;
        """)
        time_layout.addWidget(time_label)
        
        time_value = QLabel(f"{result['time']:.6f} sec")
        time_value.setStyleSheet("""
            color: white;
            font-size: 15px;
        """)
        time_layout.addWidget(time_value)
        
        metrics_layout.addLayout(time_layout)
        
        # Add winner badge if this is the winning algorithm
        if is_winner:
            winner_badge = QLabel("BEST ROUTE")
            winner_badge.setObjectName("winnerBadge")
            winner_badge.setStyleSheet("""
                #winnerBadge {
                    background-color: #27ae60;
                    color: white;
                    font-size: 12px;
                    font-weight: bold;
                    padding: 5px 15px;
                    border-radius: 10px;
                }
            """)
            winner_badge.setAlignment(Qt.AlignCenter)
            metrics_layout.addWidget(winner_badge)
        
        card_layout.addLayout(metrics_layout)
        
        # Click to view full route label
        view_route = QLabel("View full route")
        view_route.setStyleSheet("""
            color: #9b59b6;
            font-size: 12px;
            text-decoration: underline;
            margin-left: 15px;
        """)
        card_layout.addWidget(view_route)
        
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
        
        cities_to_visit = [city for city in self.flow_manager.game_state.selected_cities 
                          if city != home_city]
                          
        if len(cities_to_visit) <= 3:
            # For few cities, just list them with commas
            cities_list = ", ".join(cities_to_visit)
            cities_display = f"visiting {city_count - 1} cities ({cities_list})"
        else:
            # For many cities, show count and first few with "and X more"
            sample_cities = ", ".join(cities_to_visit[:2])
            remaining = len(cities_to_visit) - 2
            cities_display = f"visiting {city_count - 1} cities ({sample_cities}, and {remaining} more)"
        
        self.journey_summary.setText(
            f"{player_name}'s journey: Starting from {home_city}, "
            f"{cities_display}, and returning to {home_city}."
        )
        
        # Store algorithm names for staged reveal
        self.algorithm_names = list(results.keys())
        
        # Set prediction result
        user_prediction = self.flow_manager.game_state.user_prediction
        shortest_algorithm = self.flow_manager.game_state.shortest_algorithm
        
        if user_prediction == shortest_algorithm:
            self.prediction_result.setObjectName("correctPrediction")
            self.prediction_result.setText("CORRECT!")
            self.prediction_result.setStyleSheet("""
                #correctPrediction {
                    color: #2ecc71;
                    font-size: 16px;
                    font-weight: bold;
                }
            """)
        else:
            self.prediction_result.setObjectName("incorrectPrediction")
            self.prediction_result.setText("INCORRECT!")
            self.prediction_result.setStyleSheet("""
                #incorrectPrediction {
                    color: #e74c3c;
                    font-size: 16px;
                    font-weight: bold;
                }
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
        """Show the winning algorithm section and create visualization charts"""
        shortest_algorithm = self.flow_manager.game_state.shortest_algorithm
        if shortest_algorithm:
            result = self.flow_manager.game_state.algorithm_results[shortest_algorithm]
            
            self.winner_label.setText(shortest_algorithm)
            self.winner_stats.setText(
                f"Found the shortest route with a length of {result['length']:.2f} km in just {result['time']:.6f} seconds.\n"
                f"This algorithm provided the optimal solution for your specific set of cities."
            )
            
            # Show winner frame with animation
            self.winner_frame.setVisible(True)
            
            # Apply animation effect - fade in
            effect = QGraphicsOpacityEffect(self.winner_frame)
            self.winner_frame.setGraphicsEffect(effect)
            
            anim = QPropertyAnimation(effect, b"opacity")
            anim.setStartValue(0)
            anim.setEndValue(1)
            anim.setDuration(1000)
            anim.setEasingCurve(QEasingCurve.InOutCubic)
            anim.start()
            
            # Create the visualization charts
            self.create_visualization_charts()

    def create_visualization_charts(self):
        """Create and display visualization charts for algorithm performance"""
        try:
            algorithm_results = self.flow_manager.game_state.algorithm_results
            if not algorithm_results:
                logger.warning("No algorithm results available for visualization")
                return
                
            # Create route length comparison chart
            self.route_length_chart.plot_route_lengths(algorithm_results)
            
            # Create execution time comparison chart
            self.execution_time_chart.plot_execution_times(algorithm_results)
            
            # Create combined performance comparison chart
            self.comparison_chart.plot_performance_comparison(algorithm_results)
            
            # Create route map for winning algorithm
            self.create_route_map()
            
            logger.info("Successfully created algorithm performance visualizations")
        except Exception as e:
            logger.error(f"Error creating visualization charts: {e}")

    def create_route_map(self):
        """Create a visualization of the winning route"""
        try:
            # Get the winning algorithm and its route
            shortest_algorithm = self.flow_manager.game_state.shortest_algorithm
            if not shortest_algorithm:
                return
                
            result = self.flow_manager.game_state.algorithm_results[shortest_algorithm]
            route = result['route']
            
            # Get distances from the city map
            distances = self.flow_manager.game_state.city_map.get_distances()
            
            # Create a route map figure
            route_map_figure = plot_route_on_map(route, distances)
            
            if route_map_figure:
                # Create layout for the route map tab
                route_map_layout = QVBoxLayout(self.route_map_widget)
                route_map_layout.setContentsMargins(0, 0, 0, 0)
                
                # Create a FigureCanvas to display the figure
                from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
                canvas = FigureCanvasQTAgg(route_map_figure)
                route_map_layout.addWidget(canvas)
                
                # Add a label explaining the visualization
                explanation = QLabel(f"Route visualization for {shortest_algorithm} algorithm")
                explanation.setStyleSheet("""
                    color: white;
                    font-size: 14px;
                    padding: 10px;
                """)
                explanation.setAlignment(Qt.AlignCenter)
                route_map_layout.addWidget(explanation)
        except Exception as e:
            logger.error(f"Error creating route map: {e}")
    
    def restart_game(self):
        """Restart the game with a new scenario"""
        self.flow_manager.reset_game()
        self.flow_manager.show_welcome_screen()
    
    def show_summary(self):
        """Continue to the summary screen"""
        self.flow_manager.show_summary_screen()
    
    def update_display(self):
        """Update the display with current game state"""
        # Set up results when the screen is shown
        self.setup_results()