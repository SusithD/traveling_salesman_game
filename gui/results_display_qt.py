"""
Results display for the Traveling Salesman Problem game (PyQt5 Version)
"""
import logging
import traceback
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTabWidget, QLabel,
    QTextEdit, QComboBox, QPushButton, QMessageBox, QTableWidget,
    QTableWidgetItem, QSizePolicy, QFrame, QDialog
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor

from core.route_calculator import RouteCalculator
from utils.timer import Timer

# Try importing matplotlib, but handle it gracefully if it fails
try:
    import matplotlib.pyplot as plt
    from matplotlib.figure import Figure
    from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
    MATPLOTLIB_AVAILABLE = True
    logger = logging.getLogger("ResultsDisplay")
    logger.info("Matplotlib successfully imported")
except ImportError as e:
    MATPLOTLIB_AVAILABLE = False
    logger = logging.getLogger("ResultsDisplay")
    logger.warning(f"Matplotlib import failed: {e}. Visualizations will be disabled.")
    print("Warning: Matplotlib not available. Visualizations will be disabled.")

class MatplotlibCanvas(FigureCanvasQTAgg):
    """Canvas for matplotlib figures"""
    def __init__(self, width=5, height=4, dpi=100):
        if not MATPLOTLIB_AVAILABLE:
            raise ImportError("Matplotlib is not available")
        
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        super().__init__(self.fig)

class ResultsDisplayFrameQt(QWidget):
    def __init__(self, game_state, db_manager):
        logger.info("Initializing ResultsDisplayFrameQt")
        try:
            super().__init__()
            self.game_state = game_state
            self.db_manager = db_manager
            self.route_calculator = RouteCalculator()
            self.timer = Timer()
            self.user_prediction = None  # Store user's predicted shortest algorithm
            
            self.create_widgets()
            logger.info("ResultsDisplayFrameQt initialized successfully")
        except Exception as e:
            logger.error(f"Error in ResultsDisplayFrameQt initialization: {str(e)}")
            logger.error(traceback.format_exc())
            QMessageBox.critical(None, "Initialization Error", f"Error setting up results display: {str(e)}")
            raise
    
    def create_widgets(self):
        """Create the widgets for results display"""
        main_layout = QVBoxLayout(self)
        
        # Title
        title_label = QLabel("Route Calculation Results")
        title_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        main_layout.addWidget(title_label)
        
        # Create a tab widget for algorithm results
        self.tab_widget = QTabWidget()
        
        # Create tabs for each algorithm
        self.brute_force_tab = QWidget()
        self.nearest_neighbor_tab = QWidget()
        self.dynamic_programming_tab = QWidget()
        self.comparison_tab = QWidget()
        
        self.tab_widget.addTab(self.brute_force_tab, "Brute Force")
        self.tab_widget.addTab(self.nearest_neighbor_tab, "Nearest Neighbor")
        self.tab_widget.addTab(self.dynamic_programming_tab, "Dynamic Programming")
        self.tab_widget.addTab(self.comparison_tab, "Comparison")
        
        # Initialize tabs
        self.setup_algorithm_tab(self.brute_force_tab, "Brute Force")
        self.setup_algorithm_tab(self.nearest_neighbor_tab, "Nearest Neighbor")
        self.setup_algorithm_tab(self.dynamic_programming_tab, "Dynamic Programming")
        self.setup_comparison_tab()
        
        main_layout.addWidget(self.tab_widget)
        
        # User interaction area
        interaction_layout = QHBoxLayout()
        
        # Label for user choice
        user_choice_label = QLabel("Select what you think is the shortest route:")
        interaction_layout.addWidget(user_choice_label)
        
        # Combo box for algorithm selection
        self.user_choice_combo = QComboBox()
        self.user_choice_combo.addItems(["Brute Force", "Nearest Neighbor", "Dynamic Programming"])
        self.user_choice_combo.setCurrentIndex(-1)  # No selection initially
        interaction_layout.addWidget(self.user_choice_combo)
        
        # Submit button
        submit_button = QPushButton("Submit Answer")
        submit_button.clicked.connect(self.check_answer)
        interaction_layout.addWidget(submit_button)
        
        # Add stretch to push everything to the left
        interaction_layout.addStretch(1)
        main_layout.addLayout(interaction_layout)
    
    def setup_algorithm_tab(self, tab, algorithm_name):
        """Set up a tab for an algorithm"""
        layout = QVBoxLayout(tab)
        
        # Results text area
        result_text = QTextEdit()
        result_text.setReadOnly(True)
        layout.addWidget(result_text)
        
        # Store the reference
        if algorithm_name == "Brute Force":
            self.brute_force_text = result_text
        elif algorithm_name == "Nearest Neighbor":
            self.nearest_neighbor_text = result_text
        else:  # Dynamic Programming
            self.dynamic_programming_text = result_text
        
        # Only create visualization if matplotlib is available
        if MATPLOTLIB_AVAILABLE:
            try:
                # Create a frame for the visualization
                viz_frame = QFrame()
                viz_frame.setFrameShape(QFrame.StyledPanel)
                viz_frame.setFrameShadow(QFrame.Raised)
                viz_layout = QVBoxLayout(viz_frame)
                
                # Create a canvas for the plot
                canvas = MatplotlibCanvas(width=5, height=4, dpi=100)
                viz_layout.addWidget(canvas)
                
                # Store references
                if algorithm_name == "Brute Force":
                    self.brute_force_canvas = canvas
                elif algorithm_name == "Nearest Neighbor":
                    self.nearest_neighbor_canvas = canvas
                else:  # Dynamic Programming
                    self.dynamic_programming_canvas = canvas
                
                layout.addWidget(viz_frame)
                
            except Exception as e:
                logger.error(f"Error creating matplotlib visualization: {e}")
                error_label = QLabel("Visualization unavailable. Error initializing matplotlib.")
                error_label.setStyleSheet("color: red;")
                layout.addWidget(error_label)
        else:
            # Display message if matplotlib is not available
            info_label = QLabel("Matplotlib is not available. Install it to see route visualizations.")
            info_label.setStyleSheet("color: red;")
            layout.addWidget(info_label)
    
    def setup_comparison_tab(self):
        """Set up the comparison tab"""
        layout = QVBoxLayout(self.comparison_tab)
        
        # Create a table for comparison
        self.comparison_table = QTableWidget(0, 4)  # Rows will be added dynamically
        self.comparison_table.setHorizontalHeaderLabels(["Algorithm", "Route Length", "Time (ms)", "Complexity"])
        
        # Set column widths
        header = self.comparison_table.horizontalHeader()
        header.setSectionResizeMode(0, header.Stretch)
        header.setSectionResizeMode(1, header.Stretch)
        header.setSectionResizeMode(2, header.Stretch)
        header.setSectionResizeMode(3, header.Stretch)
        
        layout.addWidget(self.comparison_table)
        
        # Only create visualization if matplotlib is available
        if MATPLOTLIB_AVAILABLE:
            try:
                # Create a frame for the visualization
                viz_frame = QFrame()
                viz_frame.setFrameShape(QFrame.StyledPanel)
                viz_frame.setFrameShadow(QFrame.Raised)
                viz_layout = QVBoxLayout(viz_frame)
                
                # Create a canvas for the plot
                self.comparison_canvas = MatplotlibCanvas(width=5, height=4, dpi=100)
                viz_layout.addWidget(self.comparison_canvas)
                
                layout.addWidget(viz_frame)
                
            except Exception as e:
                logger.error(f"Error creating comparison chart: {e}")
                error_label = QLabel("Chart visualization unavailable. Error initializing matplotlib.")
                error_label.setStyleSheet("color: red;")
                layout.addWidget(error_label)
        else:
            # Display message if matplotlib is not available
            info_label = QLabel("Matplotlib is not available. Install it to see algorithm performance comparisons graphically.")
            info_label.setStyleSheet("color: red;")
            layout.addWidget(info_label)
    
    def clear_results(self):
        """Clear all result displays"""
        # Reset user prediction
        self.user_prediction = None
        
        # Clear text areas
        if hasattr(self, 'brute_force_text'):
            self.brute_force_text.clear()
            self.nearest_neighbor_text.clear()
            self.dynamic_programming_text.clear()
        
        # Clear figures only if matplotlib is available
        if MATPLOTLIB_AVAILABLE:
            try:
                if hasattr(self, 'brute_force_canvas'):
                    self.brute_force_canvas.axes.clear()
                    self.nearest_neighbor_canvas.axes.clear()
                    self.dynamic_programming_canvas.axes.clear()
                    self.comparison_canvas.axes.clear()
                    
                    self.brute_force_canvas.draw()
                    self.nearest_neighbor_canvas.draw()
                    self.dynamic_programming_canvas.draw()
                    self.comparison_canvas.draw()
            except Exception as e:
                logger.error(f"Error clearing matplotlib figures: {e}")
        
        # Clear comparison table
        if hasattr(self, 'comparison_table'):
            self.comparison_table.setRowCount(0)
        
        # Reset user choice combo box
        if hasattr(self, 'user_choice_combo'):
            self.user_choice_combo.setCurrentIndex(-1)
    
    def calculate_and_display_routes(self):
        """Calculate and display routes using all algorithms"""
        if not self.game_state.selected_cities:
            QMessageBox.critical(self, "Error", "No cities selected!")
            return
            
        # First, get the user's prediction for which algorithm will be fastest
        if not self.get_user_prediction():
            return  # User canceled or didn't make a prediction
            
        # Get necessary data
        cities = self.game_state.selected_cities
        distances = self.game_state.city_map.get_distances()
        home_city = self.game_state.home_city
        
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
        self.game_state.algorithm_results = results
        
        # Find the algorithm with the shortest route
        min_length = float('inf')
        self.shortest_algorithm = None
        
        for algo, result in results.items():
            if result["length"] < min_length:
                min_length = result["length"]
                self.shortest_algorithm = algo
        
        # Display results
        self.display_algorithm_results("Brute Force", results["Brute Force"])
        self.display_algorithm_results("Nearest Neighbor", results["Nearest Neighbor"])
        self.display_algorithm_results("Dynamic Programming", results["Dynamic Programming"])
        self.display_comparison(results)
        
        # Show result of user prediction
        if self.user_prediction == self.shortest_algorithm:
            QMessageBox.information(self, "Correct Prediction!", 
                f"Congratulations! You correctly predicted that {self.user_prediction} would find the shortest route.")
        else:
            QMessageBox.information(self, "Prediction Result", 
                f"You predicted {self.user_prediction}, but {self.shortest_algorithm} found the shortest route.")
        
        # Switch to the tab with the user's prediction first, then to comparison
        if self.user_prediction == "Brute Force":
            self.tab_widget.setCurrentIndex(0)
        elif self.user_prediction == "Nearest Neighbor":
            self.tab_widget.setCurrentIndex(1)
        elif self.user_prediction == "Dynamic Programming":
            self.tab_widget.setCurrentIndex(2)
        else:
            self.tab_widget.setCurrentIndex(3)  # Index 3 is the comparison tab
    
    def display_algorithm_results(self, algorithm_name, result):
        """Display results for a specific algorithm"""
        # Get the appropriate text widget
        if algorithm_name == "Brute Force":
            text_widget = self.brute_force_text
            if MATPLOTLIB_AVAILABLE:
                canvas = self.brute_force_canvas
        elif algorithm_name == "Nearest Neighbor":
            text_widget = self.nearest_neighbor_text
            if MATPLOTLIB_AVAILABLE:
                canvas = self.nearest_neighbor_canvas
        else:  # Dynamic Programming
            text_widget = self.dynamic_programming_text
            if MATPLOTLIB_AVAILABLE:
                canvas = self.dynamic_programming_canvas
        
        # Clear previous content
        text_widget.clear()
        
        # Create formatted HTML for better display
        html_content = f"<h3>Algorithm: {algorithm_name}</h3>"
        html_content += f"<p><b>Route:</b> {' → '.join(result['route'])}</p>"
        html_content += f"<p><b>Total Distance:</b> {result['length']:.2f} km</p>"
        html_content += f"<p><b>Calculation Time:</b> {result['time']:.4f} ms</p>"
        html_content += f"<p><b>Time Complexity:</b> {result['complexity']}</p>"
        
        # Highlight user's prediction
        if self.user_prediction and algorithm_name == self.user_prediction:
            html_content += "<p style='color:blue; font-weight:bold; background-color:#e6f2ff; padding:5px; border-left:4px solid blue;'>YOUR PREDICTION</p>"
        
        # Highlight if this is the shortest route
        if algorithm_name == self.shortest_algorithm:
            html_content += "<p style='color:green; font-weight:bold; background-color:#f0ffe0; padding:5px; border-left:4px solid green;'>THIS IS THE SHORTEST ROUTE!</p>"
        
        text_widget.setHtml(html_content)
        
        # Visualize the route only if matplotlib is available
        if MATPLOTLIB_AVAILABLE:
            try:
                canvas.axes.clear()
                self.visualize_route(canvas.axes, result['route'], self.game_state.city_map.get_city_positions())
                canvas.draw()
            except Exception as e:
                logger.error(f"Error visualizing route: {e}")
    
    def visualize_route(self, axes, route, city_positions):
        """Visualize the route on matplotlib axes"""
        # Plot city positions
        x_coords = [city_positions[city][0] for city in route]
        y_coords = [city_positions[city][1] for city in route]
        
        # Create a complete loop by adding the first city at the end
        x_coords.append(x_coords[0])
        y_coords.append(y_coords[0])
        
        # Plot cities
        axes.scatter(x_coords[:-1], y_coords[:-1], color='blue')
        
        # Mark home city
        home_index = route.index(self.game_state.home_city)
        axes.scatter(x_coords[home_index], y_coords[home_index], color='red', s=100, marker='*')
        
        # Plot route
        axes.plot(x_coords, y_coords, 'k-')
        
        # Add city labels
        for i, city in enumerate(route):
            axes.annotate(city, (x_coords[i], y_coords[i]), 
                          textcoords="offset points", xytext=(0, 5), 
                          ha='center')
        
        axes.set_title("Route Visualization")
        axes.set_xlabel("X Coordinate")
        axes.set_ylabel("Y Coordinate")
        axes.grid(True)
    
    def display_comparison(self, results):
        """Display comparison of all algorithms"""
        # Clear previous data in table
        self.comparison_table.setRowCount(0)
        
        # Add data to table
        for i, (algo, result) in enumerate(results.items()):
            row_position = self.comparison_table.rowCount()
            self.comparison_table.insertRow(row_position)
            
            # Add items to the row
            self.comparison_table.setItem(row_position, 0, QTableWidgetItem(algo))
            self.comparison_table.setItem(row_position, 1, QTableWidgetItem(f"{result['length']:.2f} km"))
            self.comparison_table.setItem(row_position, 2, QTableWidgetItem(f"{result['time']:.4f} ms"))
            self.comparison_table.setItem(row_position, 3, QTableWidgetItem(result['complexity']))
            
            # Highlight shortest route
            if algo == self.shortest_algorithm:
                for col in range(4):
                    item = self.comparison_table.item(row_position, col)
                    item.setBackground(QColor(144, 238, 144))  # Light green
        
        # Create bar chart comparison only if matplotlib is available
        if MATPLOTLIB_AVAILABLE and hasattr(self, 'comparison_canvas'):
            try:
                self.comparison_canvas.axes.clear()
                
                algorithms = list(results.keys())
                lengths = [results[algo]["length"] for algo in algorithms]
                times = [results[algo]["time"] for algo in algorithms]
                
                # Create two separate y-axes for different scales
                ax = self.comparison_canvas.axes
                width = 0.35
                x = range(len(algorithms))
                
                # Plot route lengths
                bars1 = ax.bar(x, lengths, width, label='Route Length (km)')
                ax.set_ylabel('Route Length (km)')
                ax.set_xlabel('Algorithm')
                ax.set_xticks(x)
                ax.set_xticklabels(algorithms)
                
                # Twin axis for time
                ax2 = ax.twinx()
                bars2 = ax2.bar([i + width for i in x], times, width, color='orange', label='Time (ms)')
                ax2.set_ylabel('Time (ms)')
                
                # Add legend
                lines1, labels1 = ax.get_legend_handles_labels()
                lines2, labels2 = ax2.get_legend_handles_labels()
                ax.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
                
                self.comparison_canvas.fig.tight_layout()
                self.comparison_canvas.draw()
            except Exception as e:
                logger.error(f"Error creating comparison chart: {e}")
    
    def check_answer(self):
        """Check the user's answer and record in database if correct"""
        user_choice = self.user_choice_combo.currentText()
        
        if not user_choice:
            QMessageBox.critical(self, "Error", "Please select an algorithm first!")
            return
        
        if not hasattr(self, 'shortest_algorithm'):
            QMessageBox.critical(self, "Error", "No routes have been calculated yet!")
            return
        
        if user_choice == self.shortest_algorithm:
            QMessageBox.information(self, "Correct!", 
                f"Congratulations! {user_choice} is indeed the algorithm that found the shortest route.")
            
            # Save the result in the database
            self.save_result_to_database(user_choice)
        else:
            QMessageBox.information(self, "Incorrect", 
                f"Sorry, that's not correct. The {self.shortest_algorithm} algorithm found the shortest route.")
    
    def save_result_to_database(self, algorithm):
        """Save the successful game result to the database"""
        player_name = self.game_state.player_name
        home_city = self.game_state.home_city
        cities_visited = len(self.game_state.selected_cities)
        route = self.game_state.algorithm_results[algorithm]["route"]
        route_length = self.game_state.algorithm_results[algorithm]["length"]
        time_taken = self.game_state.algorithm_results[algorithm]["time"]
        
        self.db_manager.save_game_result(
            player_name=player_name,
            home_city=home_city,
            cities_visited=cities_visited,
            route=route,
            route_length=route_length,
            algorithm=algorithm,
            execution_time=time_taken
        )
        
        QMessageBox.information(self, "Saved", "Your result has been saved to the high scores!")
    
    def get_user_prediction(self):
        """Prompt user to predict which algorithm will find the shortest route"""
        if not self.game_state.selected_cities:
            QMessageBox.critical(self, "Error", "No cities selected!")
            return False
            
        prediction_dialog = QDialog(self)
        prediction_dialog.setWindowTitle("Make Your Prediction")
        prediction_dialog.setMinimumWidth(400)
        
        layout = QVBoxLayout(prediction_dialog)
        
        # Information label
        info_label = QLabel(
            f"<p>You have selected {len(self.game_state.selected_cities)} cities to visit.</p>"
            f"<p>Before calculating the routes, predict which algorithm will find the shortest path:</p>"
        )
        info_label.setWordWrap(True)
        layout.addWidget(info_label)
        
        # Algorithm description
        algo_info = QLabel(
            "<p><b>Brute Force</b>: Tries all possible routes (O(n!))</p>"
            "<p><b>Nearest Neighbor</b>: Always visits closest unvisited city (O(n²))</p>"
            "<p><b>Dynamic Programming</b>: Uses optimal subproblems (O(n²2ⁿ))</p>"
        )
        algo_info.setStyleSheet("background-color: #f0f0f0; padding: 10px; border-radius: 5px;")
        algo_info.setWordWrap(True)
        layout.addWidget(algo_info)
        
        # Prediction combo box
        prediction_combo = QComboBox()
        prediction_combo.addItems(["Brute Force", "Nearest Neighbor", "Dynamic Programming"])
        prediction_combo.setCurrentIndex(-1)  # No selection initially
        layout.addWidget(prediction_combo)
        
        # Buttons
        button_layout = QHBoxLayout()
        cancel_button = QPushButton("Cancel")
        submit_button = QPushButton("Submit Prediction")
        submit_button.setDefault(True)
        submit_button.setEnabled(False)  # Disabled until a selection is made
        
        # Enable submit button when a selection is made
        prediction_combo.currentIndexChanged.connect(
            lambda idx: submit_button.setEnabled(idx != -1)
        )
        
        button_layout.addWidget(cancel_button)
        button_layout.addWidget(submit_button)
        layout.addLayout(button_layout)
        
        # Connect button signals
        cancel_button.clicked.connect(prediction_dialog.reject)
        submit_button.clicked.connect(prediction_dialog.accept)
        
        # Show dialog and get result
        if prediction_dialog.exec_() == QDialog.Accepted and prediction_combo.currentText():
            self.user_prediction = prediction_combo.currentText()
            return True
        else:
            return False