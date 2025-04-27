"""
Calculating animation screen for the Traveling Salesman Problem game
"""
import logging
import time
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QFrame, QProgressBar, QGraphicsOpacityEffect, QGraphicsDropShadowEffect
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
        # Main layout with center alignment
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(20)
        main_layout.setAlignment(Qt.AlignCenter)
        
        # Create central container frame with modern styling
        central_frame = QFrame()
        central_frame.setObjectName("calculatingContainer")
        central_frame.setMinimumWidth(1000)
        central_frame.setMaximumWidth(1200)
        central_frame.setStyleSheet("""
            #calculatingContainer {
                background-color: rgba(26, 26, 26, 0.7);
                border-radius: 20px;
                border: 1px solid rgba(255, 255, 255, 0.1);
            }
        """)
        
        container_layout = QVBoxLayout(central_frame)
        container_layout.setContentsMargins(40, 40, 40, 40)
        container_layout.setSpacing(25)
        
        # Header with calculation icon
        header_frame = QFrame()
        header_frame.setObjectName("headerFrame")
        header_frame.setStyleSheet("""
            #headerFrame {
                background-color: rgba(46, 204, 113, 0.15);
                border-radius: 15px;
            }
        """)
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(20, 15, 20, 15)
        
        # Left side - Title with icon
        header_left = QHBoxLayout()
        
        # Calculation icon
        calculating_icon = QLabel("⚙️")
        calculating_icon.setFixedSize(60, 60)
        calculating_icon.setObjectName("calculatingIcon")
        calculating_icon.setStyleSheet("""
            #calculatingIcon {
                font-size: 30px;
                background-color: #2ecc71;
                color: white;
                border-radius: 30px;
                margin-right: 15px;
            }
        """)
        calculating_icon.setAlignment(Qt.AlignCenter)
        header_left.addWidget(calculating_icon)
        
        # Title and subtitle
        title_layout = QVBoxLayout()
        title_layout.setSpacing(5)
        
        title = QLabel("CALCULATING ROUTES")
        title.setObjectName("calculatingTitle")
        title.setStyleSheet("""
            #calculatingTitle {
                color: white;
                font-size: 22px;
                font-weight: bold;
                letter-spacing: 1px;
            }
        """)
        title_layout.addWidget(title)
        
        subtitle = QLabel("Our algorithms are finding the optimal routes")
        subtitle.setObjectName("calculatingSubtitle")
        subtitle.setStyleSheet("""
            #calculatingSubtitle {
                color: #BBBBBB;
                font-size: 14px;
            }
        """)
        title_layout.addWidget(subtitle)
        
        header_left.addLayout(title_layout)
        header_layout.addLayout(header_left)
        header_layout.addStretch()
        
        container_layout.addWidget(header_frame)
        
        # Stylish separator
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setStyleSheet("""
            background-color: #2ecc71;
            max-width: 150px;
            height: 3px;
            margin: 5px;
        """)
        container_layout.addWidget(separator, 0, Qt.AlignCenter)
        
        # User prediction reminder with updated styling
        prediction_frame = QFrame()
        prediction_frame.setObjectName("predictionFrame")
        prediction_frame.setStyleSheet("""
            #predictionFrame {
                background-color: rgba(243, 156, 18, 0.15);
                border: 1px solid rgba(243, 156, 18, 0.3);
                border-radius: 12px;
            }
        """)
        prediction_layout = QVBoxLayout(prediction_frame)
        prediction_layout.setContentsMargins(20, 15, 20, 15)
        
        prediction_title = QLabel("YOUR PREDICTION")
        prediction_title.setObjectName("predictionTitle")
        prediction_title.setStyleSheet("""
            #predictionTitle {
                color: #f39c12;
                font-size: 14px;
                font-weight: bold;
                letter-spacing: 1px;
            }
        """)
        prediction_title.setAlignment(Qt.AlignCenter)
        prediction_layout.addWidget(prediction_title)
        
        self.prediction_label = QLabel("You predicted that Brute Force will find the shortest route")
        self.prediction_label.setObjectName("predictionLabel")
        self.prediction_label.setStyleSheet("""
            #predictionLabel {
                color: white;
                font-size: 16px;
                font-weight: bold;
            }
        """)
        self.prediction_label.setAlignment(Qt.AlignCenter)
        prediction_layout.addWidget(self.prediction_label)
        
        container_layout.addWidget(prediction_frame)
        
        # Status and progress indicators with improved styling
        progress_frame = QFrame()
        progress_frame.setObjectName("progressFrame")
        progress_frame.setStyleSheet("""
            #progressFrame {
                background-color: rgba(33, 33, 33, 0.7);
                border-radius: 15px;
                padding: 5px;
            }
        """)
        progress_layout = QVBoxLayout(progress_frame)
        progress_layout.setContentsMargins(25, 25, 25, 25)
        progress_layout.setSpacing(20)
        
        # Status section
        status_layout = QVBoxLayout()
        
        self.status_label = QLabel("Initializing...")
        self.status_label.setObjectName("statusLabel")
        self.status_label.setStyleSheet("""
            #statusLabel {
                color: #2ecc71;
                font-size: 18px;
                font-weight: bold;
                letter-spacing: 0.5px;
            }
        """)
        self.status_label.setAlignment(Qt.AlignCenter)
        status_layout.addWidget(self.status_label)
        
        # Detail label
        self.detail_label = QLabel("Preparing to solve the Traveling Salesman Problem...")
        self.detail_label.setObjectName("detailLabel")
        self.detail_label.setWordWrap(True)
        self.detail_label.setStyleSheet("""
            #detailLabel {
                color: #bbb;
                font-size: 14px;
                font-style: italic;
                background-color: rgba(46, 204, 113, 0.1);
                border-radius: 8px;
                padding: 10px;
            }
        """)
        self.detail_label.setAlignment(Qt.AlignCenter)
        status_layout.addWidget(self.detail_label)
        
        progress_layout.addLayout(status_layout)
        
        # Modern progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setObjectName("progressBar")
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setMinimumHeight(10)
        self.progress_bar.setStyleSheet("""
            #progressBar {
                border: none;
                border-radius: 5px;
                background-color: rgba(46, 204, 113, 0.1);
                margin: 5px 0;
            }
            
            #progressBar::chunk {
                background-color: #2ecc71;
                border-radius: 5px;
            }
        """)
        progress_layout.addWidget(self.progress_bar)
        
        # Algorithm status cards in HBoxLayout
        algo_layout = QHBoxLayout()
        algo_layout.setSpacing(20)
        algo_layout.setAlignment(Qt.AlignCenter)
        
        # Brute Force card with improved styling
        self.bf_indicator = self.create_algo_indicator(
            "Brute Force", "#e74c3c", "WAITING", "🧮", "Tries all possible permutations"
        )
        algo_layout.addWidget(self.bf_indicator)
        
        # Nearest Neighbor card with improved styling
        self.nn_indicator = self.create_algo_indicator(
            "Nearest Neighbor", "#3498db", "WAITING", "📍", "Always picks closest unvisited city"
        )
        algo_layout.addWidget(self.nn_indicator)
        
        # Dynamic Programming card with improved styling
        self.dp_indicator = self.create_algo_indicator(
            "Dynamic Programming", "#2ecc71", "WAITING", "⚙️", "Uses optimal subproblems"
        )
        algo_layout.addWidget(self.dp_indicator)
        
        progress_layout.addLayout(algo_layout)
        
        # Add progress frame to container
        container_layout.addWidget(progress_frame)
        
        # Done button with updated styling
        self.done_button = QPushButton("SHOW RESULTS →")
        self.done_button.setObjectName("doneButton")
        self.done_button.setFixedSize(250, 50)
        self.done_button.setStyleSheet("""
            #doneButton {
                background-color: #2ecc71;
                color: white;
                border: none;
                border-radius: 12px;
                padding: 12px 25px;
                font-size: 14px;
                font-weight: bold;
                letter-spacing: 1px;
                margin-top: 20px;
            }
            #doneButton:hover {
                background-color: #27ae60;
            }
            #doneButton:pressed {
                background-color: #219653;
            }
        """)
        self.done_button.clicked.connect(self.show_results)
        self.done_button.setVisible(False)  # Hide initially
        container_layout.addWidget(self.done_button, 0, Qt.AlignCenter)
        
        # Add container to main layout
        main_layout.addWidget(central_frame, 0, Qt.AlignCenter)
    
    def create_algo_indicator(self, name, color, status="WAITING", icon="⚙️", description=""):
        """Create an improved algorithm indicator card"""
        indicator = QFrame()
        indicator.setObjectName(f"{name.replace(' ', '')}Card")
        indicator.setFixedWidth(270)
        indicator.setStyleSheet(f"""
            #{name.replace(' ', '')}Card {{
                background-color: rgba(40, 40, 40, 0.7);
                border: 1px solid {color};
                border-radius: 12px;
                padding: 0px;
            }}
        """)
        indicator_layout = QVBoxLayout(indicator)
        indicator_layout.setContentsMargins(15, 15, 15, 15)
        indicator_layout.setSpacing(10)
        
        # Header with icon and name
        header_layout = QHBoxLayout()
        
        # Icon container
        icon_frame = QFrame()
        icon_frame.setObjectName(f"{name.replace(' ', '')}Icon")
        icon_frame.setFixedSize(36, 36)
        icon_frame.setStyleSheet(f"""
            #{name.replace(' ', '')}Icon {{
                background-color: {color};
                border-radius: 18px;
                margin-right: 10px;
            }}
        """)
        icon_layout = QVBoxLayout(icon_frame)
        icon_layout.setContentsMargins(0, 0, 0, 0)
        
        icon_label = QLabel(icon)
        icon_label.setStyleSheet(f"""
            font-size: 18px;
            color: white;
            padding: 0px;
        """)
        icon_label.setAlignment(Qt.AlignCenter)
        icon_layout.addWidget(icon_label)
        
        header_layout.addWidget(icon_frame)
        
        # Algorithm name
        name_label = QLabel(name)
        name_label.setStyleSheet(f"""
            color: {color};
            font-weight: bold;
            font-size: 14px;
        """)
        header_layout.addWidget(name_label)
        header_layout.addStretch()
        
        # Status pill
        status_label = QLabel(status)
        status_label.setObjectName(f"{name.replace(' ', '')}Status")
        status_label.setStyleSheet(f"""
            #{name.replace(' ', '')}Status {{
                color: #888888;
                font-size: 12px;
                font-weight: bold;
                padding: 4px 10px;
                background-color: #333333;
                border-radius: 10px;
            }}
        """)
        status_label.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(status_label)
        
        indicator_layout.addLayout(header_layout)
        
        # Add description
        desc_label = QLabel(description)
        desc_label.setStyleSheet("""
            color: #aaaaaa;
            font-size: 12px;
            font-style: italic;
        """)
        desc_label.setWordWrap(True)
        desc_label.setAlignment(Qt.AlignCenter)
        indicator_layout.addWidget(desc_label)
        
        # Progress indicator (initially empty)
        progress_frame = QFrame()
        progress_frame.setObjectName(f"{name.replace(' ', '')}Progress")
        progress_frame.setFixedHeight(8)
        progress_frame.setStyleSheet(f"""
            #{name.replace(' ', '')}Progress {{
                background-color: rgba({int(color[1:3], 16)}, {int(color[3:5], 16)}, {int(color[5:7], 16)}, 0.1);
                border-radius: 4px;
            }}
        """)
        indicator_layout.addWidget(progress_frame)
        
        # Save reference to status label
        indicator.status_label = status_label
        indicator.progress_frame = progress_frame
        
        return indicator
    
    def reset(self):
        """Reset the calculating screen state"""
        # Reset progress
        self.progress_bar.setValue(0)
        self.current_phase = 0
        self.status_label.setText("Initializing...")
        self.detail_label.setText("Preparing to solve the Traveling Salesman Problem...")
        
        # Reset algorithm indicators
        for name, indicator in [("Brute Force", self.bf_indicator), 
                               ("Nearest Neighbor", self.nn_indicator),
                               ("Dynamic Programming", self.dp_indicator)]:
            algoid = name.replace(" ", "")
            indicator.status_label.setText("WAITING")
            indicator.status_label.setObjectName(f"{algoid}Status")
            indicator.status_label.setStyleSheet(f"""
                #{algoid}Status {{
                    color: #888888;
                    font-size: 12px;
                    font-weight: bold;
                    padding: 4px 10px;
                    background-color: #333333;
                    border-radius: 10px;
                }}
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
                self.bf_indicator.status_label.setObjectName("BruteForceStatus")
                self.bf_indicator.status_label.setText("RUNNING")
                self.bf_indicator.status_label.setStyleSheet("""
                    #BruteForceStatus {
                        color: white;
                        font-size: 12px;
                        font-weight: bold;
                        padding: 4px 10px;
                        background-color: #e74c3c;
                        border-radius: 10px;
                    }
                """)
                # Add progress animation
                self.bf_indicator.progress_frame.setStyleSheet("""
                    #BruteForceProgress {
                        background-color: rgba(231, 76, 60, 0.3);
                        border-radius: 4px;
                    }
                """)
            elif self.current_phase == 3:  # Running Nearest Neighbor
                self.bf_indicator.status_label.setObjectName("BruteForceStatus")
                self.bf_indicator.status_label.setText("DONE")
                self.bf_indicator.status_label.setStyleSheet("""
                    #BruteForceStatus {
                        color: white;
                        font-size: 12px;
                        font-weight: bold;
                        padding: 4px 10px;
                        background-color: #555555;
                        border-radius: 10px;
                    }
                """)
                
                self.nn_indicator.status_label.setObjectName("NearestNeighborStatus")
                self.nn_indicator.status_label.setText("RUNNING")
                self.nn_indicator.status_label.setStyleSheet("""
                    #NearestNeighborStatus {
                        color: white;
                        font-size: 12px;
                        font-weight: bold;
                        padding: 4px 10px;
                        background-color: #3498db;
                        border-radius: 10px;
                    }
                """)
                # Add progress animation
                self.nn_indicator.progress_frame.setStyleSheet("""
                    #NearestNeighborProgress {
                        background-color: rgba(52, 152, 219, 0.3);
                        border-radius: 4px;
                    }
                """)
            elif self.current_phase == 4:  # Running Dynamic Programming
                self.nn_indicator.status_label.setObjectName("NearestNeighborStatus")
                self.nn_indicator.status_label.setText("DONE")
                self.nn_indicator.status_label.setStyleSheet("""
                    #NearestNeighborStatus {
                        color: white;
                        font-size: 12px;
                        font-weight: bold;
                        padding: 4px 10px;
                        background-color: #555555;
                        border-radius: 10px;
                    }
                """)
                
                self.dp_indicator.status_label.setObjectName("DynamicProgrammingStatus")
                self.dp_indicator.status_label.setText("RUNNING")
                self.dp_indicator.status_label.setStyleSheet("""
                    #DynamicProgrammingStatus {
                        color: white;
                        font-size: 12px;
                        font-weight: bold;
                        padding: 4px 10px;
                        background-color: #2ecc71;
                        border-radius: 10px;
                    }
                """)
                # Add progress animation
                self.dp_indicator.progress_frame.setStyleSheet("""
                    #DynamicProgrammingProgress {
                        background-color: rgba(46, 204, 113, 0.3);
                        border-radius: 4px;
                    }
                """)
            elif self.current_phase == 5:  # Comparing results
                self.dp_indicator.status_label.setObjectName("DynamicProgrammingStatus")
                self.dp_indicator.status_label.setText("DONE")
                self.dp_indicator.status_label.setStyleSheet("""
                    #DynamicProgrammingStatus {
                        color: white;
                        font-size: 12px;
                        font-weight: bold;
                        padding: 4px 10px;
                        background-color: #555555;
                        border-radius: 10px;
                    }
                """)
            
            # Update detail label with facts about algorithms
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
                self.detail_label.setText("All calculations complete! Click the button below to see which algorithm performed best.")
                self.done_button.setVisible(True)
                
                # Add completion effect to the done button
                shadow = QGraphicsDropShadowEffect()
                shadow.setBlurRadius(20)
                shadow.setColor(QColor("#2ecc71"))
                shadow.setOffset(0, 0)
                self.done_button.setGraphicsEffect(shadow)
            
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
    
    def update_display(self):
        """Update the display with current game state"""
        # Show user prediction
        prediction = self.flow_manager.game_state.user_prediction
        if prediction:
            self.prediction_label.setText(f"You predicted that {prediction} will find the shortest route")
        else:
            self.prediction_label.setText("")
            
        # Reset the screen for a new calculation
        self.reset()