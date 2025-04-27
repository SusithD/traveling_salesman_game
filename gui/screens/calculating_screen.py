"""
Calculating animation screen for the Traveling Salesman Problem game
"""
import logging
import time
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QFrame, QProgressBar, QGraphicsOpacityEffect
)
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QColor, QFont

from core.route_calculator import RouteCalculator
from utils.timer import Timer

logger = logging.getLogger("CalculatingScreen")

class CalculatingScreen(QWidget):
    """
    Screen that displays an animation while calculating routes
    """
    def __init__(self, flow_manager):
        super().__init__()
        self.flow_manager = flow_manager
        self.route_calculator = RouteCalculator()
        self.timer = Timer()
        
        # For animated progress
        self.progress_phases = [
            "Analyzing city distances...",
            "Initializing algorithms...",
            "Running Brute Force algorithm...",
            "Running Nearest Neighbor algorithm...",
            "Running Dynamic Programming algorithm...",
            "Comparing results...",
            "Finalizing analysis..."
        ]
        self.current_phase = 0
        self.animation_timer = QTimer(self)
        self.animation_timer.timeout.connect(self.update_progress)
        
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
        
        calculating_icon = QLabel("⚙️")
        calculating_icon.setStyleSheet("""
            font-size: 36px;
            padding: 10px;
            background-color: #16a085;
            color: white;
            border-radius: 10px;
        """)
        header_layout.addWidget(calculating_icon)
        
        header_text = QVBoxLayout()
        title = QLabel("Calculating Optimal Routes")
        title.setStyleSheet("""
            color: white;
            font-size: 24px;
            font-weight: bold;
        """)
        header_text.addWidget(title)
        
        subtitle = QLabel("Please wait while the algorithms work their magic...")
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
        
        # Calculation animation area
        animation_frame = QFrame()
        animation_frame.setStyleSheet("""
            background-color: #222222;
            border-radius: 15px;
            padding: 30px;
        """)
        animation_layout = QVBoxLayout(animation_frame)
        animation_layout.setSpacing(30)
        
        # Animated processing status
        self.status_label = QLabel("Initializing...")
        self.status_label.setStyleSheet("""
            color: #2ecc71;
            font-size: 18px;
            font-weight: bold;
        """)
        self.status_label.setAlignment(Qt.AlignCenter)
        animation_layout.addWidget(self.status_label)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setMinimumHeight(15)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: none;
                border-radius: 7px;
                background-color: #2c3e50;
                margin: 10px 0;
            }
            
            QProgressBar::chunk {
                background-color: #2ecc71;
                border-radius: 7px;
            }
        """)
        animation_layout.addWidget(self.progress_bar)
        
        # Processing details
        self.detail_label = QLabel("Preparing to solve the Traveling Salesman Problem...")
        self.detail_label.setWordWrap(True)
        self.detail_label.setStyleSheet("""
            color: #bbb;
            font-size: 14px;
        """)
        self.detail_label.setAlignment(Qt.AlignCenter)
        animation_layout.addWidget(self.detail_label)
        
        # Add some space
        animation_layout.addStretch()
        
        # Algorithms being tested
        algo_title = QLabel("Testing Algorithms:")
        algo_title.setStyleSheet("color: white; font-size: 16px; font-weight: bold;")
        animation_layout.addWidget(algo_title)
        
        # Algorithm indicators
        algo_frame = QFrame()
        algo_frame.setStyleSheet("""
            background-color: #1a1a1a;
            border-radius: 10px;
            padding: 15px;
        """)
        algo_layout = QHBoxLayout(algo_frame)
        
        # Brute Force indicator
        self.bf_indicator = self.create_algo_indicator("Brute Force", "#c0392b", "WAITING")
        algo_layout.addWidget(self.bf_indicator)
        
        # Nearest Neighbor indicator
        self.nn_indicator = self.create_algo_indicator("Nearest Neighbor", "#2980b9", "WAITING")
        algo_layout.addWidget(self.nn_indicator)
        
        # Dynamic Programming indicator
        self.dp_indicator = self.create_algo_indicator("Dynamic Programming", "#27ae60", "WAITING")
        algo_layout.addWidget(self.dp_indicator)
        
        animation_layout.addWidget(algo_frame)
        
        # Your prediction reminder
        self.prediction_label = QLabel()
        self.prediction_label.setStyleSheet("""
            color: #f39c12;
            font-size: 14px;
            font-style: italic;
            padding: 10px;
            background-color: rgba(243, 156, 18, 0.1);
            border-radius: 5px;
            margin-top: 15px;
        """)
        self.prediction_label.setAlignment(Qt.AlignCenter)
        animation_layout.addWidget(self.prediction_label)
        
        # Done button (initially hidden)
        self.done_button = QPushButton("Show Results →")
        self.done_button.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px 20px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2ecc71;
            }
            QPushButton:pressed {
                background-color: #219653;
            }
        """)
        self.done_button.clicked.connect(self.show_results)
        self.done_button.setVisible(False)  # Hide initially
        animation_layout.addWidget(self.done_button, 0, Qt.AlignCenter)
        
        container_layout.addWidget(animation_frame)
        
        # Add container to main layout
        main_layout.addWidget(container)
        
    def create_algo_indicator(self, name, color, status="WAITING"):
        """Create an indicator for algorithm status"""
        indicator = QFrame()
        indicator.setStyleSheet(f"""
            background-color: #222222;
            border: 1px solid {color};
            border-radius: 8px;
            padding: 10px;
        """)
        indicator_layout = QVBoxLayout(indicator)
        indicator_layout.setContentsMargins(10, 10, 10, 10)
        indicator_layout.setSpacing(5)
        
        # Algorithm name
        name_label = QLabel(name)
        name_label.setStyleSheet(f"""
            color: {color};
            font-weight: bold;
            font-size: 14px;
        """)
        name_label.setAlignment(Qt.AlignCenter)
        indicator_layout.addWidget(name_label)
        
        # Status indicator
        status_label = QLabel(status)
        status_label.setStyleSheet("""
            color: #888888;
            font-size: 12px;
            padding: 3px 8px;
            background-color: #333333;
            border-radius: 4px;
        """)
        status_label.setAlignment(Qt.AlignCenter)
        indicator_layout.addWidget(status_label)
        
        # Save reference to status label
        indicator.status_label = status_label
        
        return indicator
    
    def reset(self):
        """Reset the calculating screen state"""
        # Reset progress
        self.progress_bar.setValue(0)
        self.current_phase = 0
        self.status_label.setText("Initializing...")
        self.detail_label.setText("Preparing to solve the Traveling Salesman Problem...")
        
        # Reset algorithm indicators
        self.bf_indicator.status_label.setText("WAITING")
        self.bf_indicator.status_label.setStyleSheet("""
            color: #888888;
            font-size: 12px;
            padding: 3px 8px;
            background-color: #333333;
            border-radius: 4px;
        """)
        
        self.nn_indicator.status_label.setText("WAITING")
        self.nn_indicator.status_label.setStyleSheet("""
            color: #888888;
            font-size: 12px;
            padding: 3px 8px;
            background-color: #333333;
            border-radius: 4px;
        """)
        
        self.dp_indicator.status_label.setText("WAITING")
        self.dp_indicator.status_label.setStyleSheet("""
            color: #888888;
            font-size: 12px;
            padding: 3px 8px;
            background-color: #333333;
            border-radius: 4px;
        """)
        
        # Hide done button
        self.done_button.setVisible(False)
    
    def start_calculation(self):
        """Start the calculation process with animation"""
        # Show user prediction
        prediction = self.flow_manager.game_state.user_prediction
        self.prediction_label.setText(f"You predicted that {prediction} will find the shortest route")
        
        # Start animated progress
        self.animation_timer.start(800)  # Update every 0.8 seconds
        
        # Start actual calculation in the background
        # We'll use a single-shot timer to start the actual calculation
        # after a short delay to let the animation begin
        QTimer.singleShot(400, self.calculate_routes)
    
    def update_progress(self):
        """Update the progress animation"""
        if self.current_phase < len(self.progress_phases):
            # Update progress bar
            progress = (self.current_phase + 1) * 100 // len(self.progress_phases)
            self.progress_bar.setValue(progress)
            
            # Update status text
            self.status_label.setText(self.progress_phases[self.current_phase])
            
            # Update algorithm indicators
            if self.current_phase == 2:  # Running Brute Force
                self.bf_indicator.status_label.setText("RUNNING")
                self.bf_indicator.status_label.setStyleSheet("""
                    color: white;
                    font-size: 12px;
                    padding: 3px 8px;
                    background-color: #c0392b;
                    border-radius: 4px;
                """)
            elif self.current_phase == 3:  # Running Nearest Neighbor
                self.bf_indicator.status_label.setText("DONE")
                self.bf_indicator.status_label.setStyleSheet("""
                    color: white;
                    font-size: 12px;
                    padding: 3px 8px;
                    background-color: #555555;
                    border-radius: 4px;
                """)
                
                self.nn_indicator.status_label.setText("RUNNING")
                self.nn_indicator.status_label.setStyleSheet("""
                    color: white;
                    font-size: 12px;
                    padding: 3px 8px;
                    background-color: #2980b9;
                    border-radius: 4px;
                """)
            elif self.current_phase == 4:  # Running Dynamic Programming
                self.nn_indicator.status_label.setText("DONE")
                self.nn_indicator.status_label.setStyleSheet("""
                    color: white;
                    font-size: 12px;
                    padding: 3px 8px;
                    background-color: #555555;
                    border-radius: 4px;
                """)
                
                self.dp_indicator.status_label.setText("RUNNING")
                self.dp_indicator.status_label.setStyleSheet("""
                    color: white;
                    font-size: 12px;
                    padding: 3px 8px;
                    background-color: #27ae60;
                    border-radius: 4px;
                """)
            elif self.current_phase == 5:  # Comparing results
                self.dp_indicator.status_label.setText("DONE")
                self.dp_indicator.status_label.setStyleSheet("""
                    color: white;
                    font-size: 12px;
                    padding: 3px 8px;
                    background-color: #555555;
                    border-radius: 4px;
                """)
            
            # Update detail label with random facts about algorithms
            if self.current_phase == 0:
                self.detail_label.setText("Analyzing the distances between all selected cities...")
            elif self.current_phase == 1:
                self.detail_label.setText("Preparing to execute multiple algorithmic approaches...")
            elif self.current_phase == 2:
                self.detail_label.setText("The Brute Force algorithm tries every possible route - there are (n-1)! possible routes for n cities.")
            elif self.current_phase == 3:
                self.detail_label.setText("The Nearest Neighbor algorithm is a greedy approach that always visits the closest unvisited city next.")
            elif self.current_phase == 4:
                self.detail_label.setText("Dynamic Programming uses the Bellman-Held-Karp algorithm which runs in O(n²2ⁿ) time.")
            elif self.current_phase == 5:
                self.detail_label.setText("Comparing results from all algorithms to determine the shortest route...")
            elif self.current_phase == 6:
                self.detail_label.setText("All calculations complete! Click to see results.")
                self.done_button.setVisible(True)
            
            self.current_phase += 1
            
            # Stop the animation when we're done
            if self.current_phase >= len(self.progress_phases):
                self.animation_timer.stop()
                self.progress_bar.setValue(100)
                self.status_label.setText("Calculation Complete!")
    
    def calculate_routes(self):
        """Actually calculate the routes using all algorithms"""
        try:
            # Get necessary data
            cities = self.flow_manager.game_state.selected_cities
            distances = self.flow_manager.game_state.city_map.get_distances()
            home_city = self.flow_manager.game_state.home_city
            
            # Dictionary to store results
            results = {}
            
            # Calculate using brute force
            self.timer.start()
            brute_force_route, brute_force_length = self.route_calculator.brute_force(
                cities, distances, home_city)
            brute_force_time = self.timer.stop()
            
            results["Brute Force"] = {
                "route": brute_force_route,
                "length": brute_force_length,
                "time": brute_force_time,
                "complexity": "O(n!)"
            }
            
            # Calculate using nearest neighbor
            self.timer.start()
            nearest_neighbor_route, nearest_neighbor_length = self.route_calculator.nearest_neighbor(
                cities, distances, home_city)
            nearest_neighbor_time = self.timer.stop()
            
            results["Nearest Neighbor"] = {
                "route": nearest_neighbor_route,
                "length": nearest_neighbor_length,
                "time": nearest_neighbor_time,
                "complexity": "O(n²)"
            }
            
            # Calculate using dynamic programming
            self.timer.start()
            dp_route, dp_length = self.route_calculator.dynamic_programming(
                cities, distances, home_city)
            dp_time = self.timer.stop()
            
            results["Dynamic Programming"] = {
                "route": dp_route,
                "length": dp_length,
                "time": dp_time,
                "complexity": "O(n²2ⁿ)"
            }
            
            # Store results in game state
            self.flow_manager.game_state.algorithm_results = results
            
            # Find the algorithm with the shortest route
            min_length = float('inf')
            shortest_algorithm = None
            
            for algo, result in results.items():
                if result["length"] < min_length:
                    min_length = result["length"]
                    shortest_algorithm = algo
            
            self.flow_manager.game_state.shortest_algorithm = shortest_algorithm
            
        except Exception as e:
            logger.error(f"Error calculating routes: {str(e)}")
            self.detail_label.setText(f"Error: {str(e)}")
    
    def show_results(self):
        """Show the results screen"""
        self.flow_manager.show_results_screen()