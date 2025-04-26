"""
Results display for the Traveling Salesman Problem game (PyQt5 Version)
"""
import logging
import traceback
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTabWidget, QLabel,
    QTextEdit, QComboBox, QPushButton, QMessageBox, QTableWidget,
    QTableWidgetItem, QSizePolicy, QFrame, QDialog, QScrollArea
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
    def __init__(self, width=8, height=6, dpi=100):  # Increased default height
        if not MATPLOTLIB_AVAILABLE:
            raise ImportError("Matplotlib is not available")
        
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        super().__init__(self.fig)
        # Set minimum height to avoid flattened graphs
        self.setMinimumHeight(300)  # Ensure minimum height for the canvas
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

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
            
            # Apply black background and white text styling
            self.setStyleSheet("""
                QWidget {
                    background-color: black;
                    color: white;
                }
                QLabel {
                    color: white;
                }
                QTabWidget::pane {
                    border: 1px solid #444444;
                    background-color: black;
                }
                QTabBar::tab {
                    background-color: #222222;
                    color: white;
                    padding: 8px 15px;
                    margin-right: 2px;
                    border-top-left-radius: 4px;
                    border-top-right-radius: 4px;
                }
                QTabBar::tab:selected {
                    background-color: black;
                    border-bottom: 2px solid white;
                }
                QComboBox {
                    background-color: #222222;
                    color: white;
                    border: 1px solid #444444;
                    border-radius: 4px;
                    padding: 5px;
                    min-width: 6em;
                }
                QComboBox::drop-down {
                    subcontrol-origin: padding;
                    subcontrol-position: top right;
                    width: 20px;
                    border-left: 1px solid #444444;
                }
                QComboBox QAbstractItemView {
                    background-color: #222222;
                    color: white;
                    selection-background-color: #444444;
                }
                QTableWidget {
                    background-color: #111111;
                    color: white;
                    gridline-color: #333333;
                    border: none;
                }
                QTableWidget::item {
                    border-bottom: 1px solid #333333;
                    padding: 5px;
                }
                QHeaderView::section {
                    background-color: #222222;
                    color: white;
                    padding: 5px;
                    border: 1px solid #444444;
                }
                /* Remove ALL scrollbars in this widget to integrate with main scroll area */
                QScrollBar {
                    width: 0px;
                    height: 0px;
                    background: transparent;
                    border: none;
                }
                QScrollBar::handle {
                    background: transparent;
                    border: none;
                }
                QScrollBar::add-line, QScrollBar::sub-line {
                    border: none;
                    background: none;
                }
            """)
            
            # Create a direct layout for this widget - NO scroll area
            self.main_layout = QVBoxLayout(self)
            self.main_layout.setSpacing(15)  # Increase spacing between elements
            self.main_layout.setContentsMargins(20, 20, 20, 20)  # Add padding around content
            
            # Create the widgets
            self.create_widgets()
            
            logger.info("ResultsDisplayFrameQt initialized successfully")
        except Exception as e:
            logger.error(f"Error in ResultsDisplayFrameQt initialization: {str(e)}")
            logger.error(traceback.format_exc())
            QMessageBox.critical(None, "Initialization Error", f"Error setting up results display: {str(e)}")
            raise
    
    def create_widgets(self):
        """Create the widgets for results display"""
        # Title
        title_label = QLabel("Route Calculation Results")
        title_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        self.main_layout.addWidget(title_label)
        
        # Create a tab widget for algorithm results
        self.tab_widget = QTabWidget()
        # Set the tab widget to expand properly
        self.tab_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.MinimumExpanding)
        self.tab_widget.setMinimumHeight(800)  # Ensure minimum height for content
        
        # Disable nested scrolling in tab widget but allow main scroll
        self.tab_widget.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #444444;
                background-color: black;
            }
            QTabWidget QScrollBar, QTabWidget QTableView QScrollBar {
                width: 0px;
                height: 0px;
                background: transparent;
                border: none;
            }
            QTabWidget QWidget {
                background-color: black;
            }
        """)
        
        # Create tabs for each algorithm
        self.brute_force_tab = QWidget()
        self.nearest_neighbor_tab = QWidget()
        self.dynamic_programming_tab = QWidget()
        self.comparison_tab = QWidget()
        
        # Ensure each tab displays its full content without scrolling
        for tab in [self.brute_force_tab, self.nearest_neighbor_tab, 
                    self.dynamic_programming_tab, self.comparison_tab]:
            tab.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            tab.setStyleSheet("""
                QScrollBar {
                    width: 0px;
                    height: 0px;
                    background: transparent;
                    border: none;
                }
            """)
        
        self.tab_widget.addTab(self.brute_force_tab, "Brute Force")
        self.tab_widget.addTab(self.nearest_neighbor_tab, "Nearest Neighbor")
        self.tab_widget.addTab(self.dynamic_programming_tab, "Dynamic Programming")
        self.tab_widget.addTab(self.comparison_tab, "Comparison")
        
        # Initialize tabs
        self.setup_algorithm_tab(self.brute_force_tab, "Brute Force")
        self.setup_algorithm_tab(self.nearest_neighbor_tab, "Nearest Neighbor")
        self.setup_algorithm_tab(self.dynamic_programming_tab, "Dynamic Programming")
        self.setup_comparison_tab()
        
        # Add the tab widget to the main layout
        self.main_layout.addWidget(self.tab_widget)
        
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
        self.main_layout.addLayout(interaction_layout)
        
        # Add a final stretch to ensure proper scrolling behavior
        self.main_layout.addStretch(1)
    
    def setup_algorithm_tab(self, tab, algorithm_name):
        """Set up a tab for an algorithm with enhanced visual styling"""
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(15)
        
        # Create a card-style container for the algorithm results
        result_card = QFrame()
        result_card.setFrameShape(QFrame.StyledPanel)
        result_card.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        result_card.setStyleSheet("""
            QFrame {
                background-color: #111111;
                border: 1px solid #333333;
                border-radius: 8px;
                padding: 5px;
            }
        """)
        card_layout = QVBoxLayout(result_card)
        card_layout.setSpacing(15)
        
        # Algorithm header with icon styling
        header_container = QFrame()
        header_container.setStyleSheet("""
            QFrame {
                background-color: #222222;
                border-radius: 6px;
                padding: 2px;
                margin-bottom: 10px;
            }
        """)
        header_layout = QHBoxLayout(header_container)
        
        # Add algorithm-specific styling
        if algorithm_name == "Brute Force":
            header_color = "#e74c3c"  # Red
            icon_text = "🧮"  # Calculator emoji for brute force
        elif algorithm_name == "Nearest Neighbor":
            header_color = "#3498db"  # Blue
            icon_text = "📍"  # Pin emoji for nearest neighbor
        else:  # Dynamic Programming
            header_color = "#2ecc71"  # Green
            icon_text = "⚙️"  # Gear emoji for dynamic programming
            
        # Icon label
        icon_label = QLabel(icon_text)
        icon_label.setStyleSheet(f"""
            font-size: 24px;
            padding: 5px;
            background-color: {header_color};
            color: white;
            border-radius: 4px;
            min-width: 40px;
            min-height: 40px;
            qproperty-alignment: AlignCenter;
        """)
        header_layout.addWidget(icon_label)
        
        # Algorithm title
        algo_title = QLabel(algorithm_name)
        algo_title.setStyleSheet(f"""
            color: white;
            font-size: 18px;
            font-weight: bold;
            border-bottom: 2px solid {header_color};
            padding-bottom: 3px;
        """)
        header_layout.addWidget(algo_title)
        header_layout.addStretch(1)
        
        # Complexity badge
        complexity_text = ""
        if algorithm_name == "Brute Force":
            complexity_text = "O(n!)"
        elif algorithm_name == "Nearest Neighbor":
            complexity_text = "O(n²)"
        else:  # Dynamic Programming
            complexity_text = "O(n²2ⁿ)"
            
        complexity_label = QLabel(complexity_text)
        complexity_label.setStyleSheet(f"""
            background-color: #333333;
            color: white;
            border-radius: 4px;
            padding: 5px 8px;
            font-family: monospace;
            font-weight: bold;
        """)
        header_layout.addWidget(complexity_label)
        
        card_layout.addWidget(header_container)
        
        # Results content container
        content_container = QFrame()
        content_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        content_container.setStyleSheet("""
            QFrame {
                background-color: #181818;
                border-radius: 6px;
                padding: 10px;
            }
        """)
        content_layout = QVBoxLayout(content_container)
        content_layout.setSpacing(10)
        content_layout.setContentsMargins(10, 10, 10, 10)
        
        # Results text area with modern styling - use QLabel instead of QTextEdit to avoid scroll issues
        result_text = QTextEdit()
        result_text.setReadOnly(True)
        result_text.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        result_text.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        result_text.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        result_text.setStyleSheet("""
            QTextEdit {
                background-color: #1a1a1a;
                color: white;
                border: 1px solid #333333;
                border-radius: 4px;
                padding: 12px;
                selection-background-color: #444444;
                font-size: 14px;
            }
        """)
        content_layout.addWidget(result_text)
        
        # Store the reference
        if algorithm_name == "Brute Force":
            self.brute_force_text = result_text
        elif algorithm_name == "Nearest Neighbor":
            self.nearest_neighbor_text = result_text
        else:  # Dynamic Programming
            self.dynamic_programming_text = result_text
        
        card_layout.addWidget(content_container)
        
        # Only create visualization if matplotlib is available
        if MATPLOTLIB_AVAILABLE:
            try:
                # Create a frame for the visualization
                viz_frame = QFrame()
                viz_frame.setFrameShape(QFrame.StyledPanel)
                viz_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
                viz_frame.setStyleSheet("""
                    QFrame {
                        background-color: #1a1a1a;
                        border: 1px solid #333333;
                        border-radius: 6px;
                        margin-top: 15px;
                        padding: 10px;
                    }
                """)
                viz_layout = QVBoxLayout(viz_frame)
                viz_layout.setSpacing(10)
                
                # Visualization title
                viz_title = QLabel("Route Visualization")
                viz_title.setStyleSheet("""
                    color: white;
                    font-size: 16px;
                    font-weight: bold;
                    margin-bottom: 5px;
                    border-bottom: 1px solid #444444;
                    padding-bottom: 5px;
                """)
                viz_layout.addWidget(viz_title)
                
                # Create a canvas for the plot with dark theme
                # Use fixed height but don't constrain width
                canvas = MatplotlibCanvas(width=5, height=4, dpi=100)
                canvas.setMinimumHeight(350)  # Minimum height for visibility
                canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
                
                # Set the background of the figure to black
                canvas.fig.patch.set_facecolor('#1a1a1a')
                canvas.axes.set_facecolor('#1a1a1a')
                # Set the text color to white
                canvas.axes.xaxis.label.set_color('white')
                canvas.axes.yaxis.label.set_color('white')
                canvas.axes.title.set_color('white')
                canvas.axes.tick_params(colors='white')
                for spine in canvas.axes.spines.values():
                    spine.set_edgecolor('#444444')
                
                viz_layout.addWidget(canvas)
                
                # Store references
                if algorithm_name == "Brute Force":
                    self.brute_force_canvas = canvas
                elif algorithm_name == "Nearest Neighbor":
                    self.nearest_neighbor_canvas = canvas
                else:  # Dynamic Programming
                    self.dynamic_programming_canvas = canvas
                
                card_layout.addWidget(viz_frame)
                
            except Exception as e:
                logger.error(f"Error creating matplotlib visualization: {e}")
                error_label = QLabel("Visualization unavailable. Error initializing matplotlib.")
                error_label.setStyleSheet("color: #ff6b6b; padding: 10px;")
                card_layout.addWidget(error_label)
        else:
            # Display message if matplotlib is not available
            info_label = QLabel("Matplotlib is not available. Install it to see route visualizations.")
            info_label.setStyleSheet("color: #ff6b6b; padding: 10px; background-color: #2c1617; border-radius: 4px;")
            card_layout.addWidget(info_label)
        
        layout.addWidget(result_card)
        # Don't add stretch at the end - allow content to expand naturally

    def setup_comparison_tab(self):
        """Set up the comparison tab with enhanced visual styling"""
        layout = QVBoxLayout(self.comparison_tab)
        
        # Create header
        header_label = QLabel("Algorithm Performance Comparison")
        header_label.setStyleSheet("""
            font-size: 18px; 
            font-weight: bold; 
            color: white; 
            padding: 10px;
            background-color: #222222;
            border-radius: 6px;
            margin-bottom: 15px;
        """)
        header_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(header_label)
        
        # Create a modern table for comparison
        table_container = QFrame()
        table_container.setStyleSheet("""
            background-color: #111111;
            border-radius: 8px;
            border: 1px solid #333333;
            padding: 5px;
        """)
        table_layout = QVBoxLayout(table_container)
        
        self.comparison_table = QTableWidget(0, 4)  # Rows will be added dynamically
        self.comparison_table.setHorizontalHeaderLabels(["Algorithm", "Route Length", "Time (ms)", "Complexity"])
        self.comparison_table.setMinimumHeight(150)
        self.comparison_table.verticalHeader().setVisible(False)  # Hide vertical headers
        self.comparison_table.setShowGrid(True)
        # Disable scrollbars in the table and let the main scroll area handle scrolling
        self.comparison_table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.comparison_table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.comparison_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.comparison_table.setStyleSheet("""
            QTableWidget {
                background-color: #111111;
                color: white;
                gridline-color: #333333;
                border: none;
                font-size: 14px;
            }
            QTableWidget::item {
                border-bottom: 1px solid #333333;
                padding: 8px;
                margin: 2px;
            }
            QTableWidget::item:selected {
                background-color: #2a3f5f;
            }
            QHeaderView::section {
                background-color: #222222;
                color: white;
                padding: 8px;
                border: 1px solid #444444;
                font-weight: bold;
                border-radius: 0px;
                font-size: 14px;
            }
            QHeaderView::section:first {
                border-top-left-radius: 5px;
            }
            QHeaderView::section:last {
                border-top-right-radius: 5px;
            }
        """)
        
        # Set column widths
        header = self.comparison_table.horizontalHeader()
        header.setSectionResizeMode(0, header.Stretch)
        header.setSectionResizeMode(1, header.Stretch)
        header.setSectionResizeMode(2, header.Stretch)
        header.setSectionResizeMode(3, header.Stretch)
        
        table_layout.addWidget(self.comparison_table)
        layout.addWidget(table_container)
        
        # Legend for the table
        legend_container = QFrame()
        legend_container.setStyleSheet("""
            background-color: #1a1a1a;
            border-radius: 6px;
            padding: 10px;
            margin-top: 10px;
            margin-bottom: 15px;
        """)
        legend_layout = QHBoxLayout(legend_container)
        
        # Create legend items
        legend_items = [
            ("Your Prediction", "#1a365d"),
            ("Shortest Route", "#1c382e"),
            ("Correct Prediction", "#2c532f")
        ]
        
        for text, color in legend_items:
            item_container = QFrame()
            item_layout = QHBoxLayout(item_container)
            item_layout.setContentsMargins(0, 0, 0, 0)
            item_layout.setSpacing(8)
            
            color_box = QFrame()
            color_box.setFixedSize(16, 16)
            color_box.setStyleSheet(f"background-color: {color}; border-radius: 2px;")
            item_layout.addWidget(color_box)
            
            label = QLabel(text)
            label.setStyleSheet("color: white;")
            item_layout.addWidget(label)
            
            legend_layout.addWidget(item_container)
            
        legend_layout.addStretch(1)
        layout.addWidget(legend_container)
        
        # Only create visualization if matplotlib is available
        if MATPLOTLIB_AVAILABLE:
            try:
                # Create a frame for the visualization
                viz_frame = QFrame()
                viz_frame.setFrameShape(QFrame.StyledPanel)
                viz_frame.setStyleSheet("""
                    QFrame {
                        background-color: #111111;
                        border: 1px solid #333333;
                        border-radius: 8px;
                        margin-top: 10px;
                        padding: 15px;
                    }
                """)
                viz_layout = QVBoxLayout(viz_frame)
                
                # Visualization title
                viz_title = QLabel("Performance Comparison Chart")
                viz_title.setStyleSheet("""
                    color: white;
                    font-size: 16px;
                    font-weight: bold;
                    padding-bottom: 5px;
                    border-bottom: 1px solid #444444;
                    margin-bottom: 10px;
                """)
                viz_title.setAlignment(Qt.AlignCenter)
                viz_layout.addWidget(viz_title)
                
                # Create a canvas for the plot with dark theme - with fixed size
                self.comparison_canvas = MatplotlibCanvas(width=5, height=5, dpi=100)
                self.comparison_canvas.setFixedHeight(400)  # Fixed height for main scroll area compatibility
                
                # Set dark theme for the comparison chart
                self.comparison_canvas.fig.patch.set_facecolor('#111111')
                self.comparison_canvas.axes.set_facecolor('#111111')
                # Set the text color to white
                self.comparison_canvas.axes.xaxis.label.set_color('white')
                self.comparison_canvas.axes.yaxis.label.set_color('white')
                self.comparison_canvas.axes.title.set_color('white')
                self.comparison_canvas.axes.tick_params(colors='white')
                for spine in self.comparison_canvas.axes.spines.values():
                    spine.set_edgecolor('#444444')
                
                viz_layout.addWidget(self.comparison_canvas)
                layout.addWidget(viz_frame)
                
            except Exception as e:
                logger.error(f"Error creating comparison chart: {e}")
                error_label = QLabel("Chart visualization unavailable. Error initializing matplotlib.")
                error_label.setStyleSheet("color: #ff6b6b; padding: 10px;")
                layout.addWidget(error_label)
        else:
            # Display message if matplotlib is not available
            info_label = QLabel("Matplotlib is not available. Install it to see algorithm performance comparisons graphically.")
            info_label.setStyleSheet("color: #ff6b6b; padding: 15px; background-color: #2c1617; border-radius: 6px;")
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
        """Display results for a specific algorithm with enhanced visual styling"""
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
        
        # Determine status styling
        status_style = ""
        status_message = ""
        
        if self.user_prediction and algorithm_name == self.user_prediction and algorithm_name == self.shortest_algorithm:
            # Correct prediction and shortest
            status_style = """
                color: #2ecc71; 
                font-weight: bold; 
                background-color: #2c532f; 
                padding: 12px; 
                border-radius: 6px;
                border-left: 4px solid #27ae60;
                margin: 10px 0;
            """
            status_message = "✓ YOUR PREDICTION ✓ SHORTEST ROUTE"
        elif algorithm_name == self.shortest_algorithm:
            # Shortest route
            status_style = """
                color: #2ecc71; 
                font-weight: bold; 
                background-color: #1c382e; 
                padding: 12px; 
                border-radius: 6px;
                border-left: 4px solid #2ecc71;
                margin: 10px 0;
            """
            status_message = "✓ SHORTEST ROUTE"
        elif self.user_prediction and algorithm_name == self.user_prediction:
            # User prediction
            status_style = """
                color: #3498db; 
                font-weight: bold; 
                background-color: #1a365d; 
                padding: 12px; 
                border-radius: 6px;
                border-left: 4px solid #3498db;
                margin: 10px 0;
            """
            status_message = "YOUR PREDICTION"
        
        # Create formatted HTML for better display with dark theme colors and enhanced styling
        html_content = """
        <div style='font-family: Arial, sans-serif;'>
            <div style='margin: 5px 0 15px 0;'>
                <div style='display: flex; align-items: center;'>
                    <div style='font-size: 16px; color: white;'><b>Route Details</b></div>
                </div>
                
                <div style='background-color: #222222; border-radius: 6px; padding: 15px; margin-top: 10px;'>
                    <div style='border-bottom: 1px solid #444444; padding-bottom: 10px; margin-bottom: 10px;'>
                        <span style='color: #aaaaaa; font-size: 13px;'>SELECTED PATH</span>
                        <div style='color: white; font-size: 15px; padding: 5px 0; word-wrap: break-word;'>
                            %s
                        </div>
                    </div>
                    
                    <table style='width: 100%%; border-collapse: collapse; margin-top: 10px;'>
                        <tr>
                            <td style='padding: 8px 5px; width: 50%%; color: #aaaaaa; font-size: 13px;'>TOTAL DISTANCE</td>
                            <td style='padding: 8px 5px; width: 50%%; color: #aaaaaa; font-size: 13px;'>CALCULATION TIME</td>
                        </tr>
                        <tr>
                            <td style='padding: 5px; color: white; font-size: 18px; font-weight: bold;'>%.2f km</td>
                            <td style='padding: 5px; color: white; font-size: 18px; font-weight: bold;'>%.4f ms</td>
                        </tr>
                    </table>
                </div>
            </div>
        """ % (' → '.join(result['route']), result['length'], result['time'])
        
        # Add status message if applicable
        if status_message:
            html_content += """
            <div style='%s'>
                %s
            </div>
            """ % (status_style, status_message)
        
        html_content += "</div>"  # Close main div
        
        # Set the HTML content
        text_widget.setHtml(html_content)
        
        # Disable scrollbars again - sometimes they can appear after setting HTML
        text_widget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        text_widget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        # Important: Make the document size tracking more reliable
        text_widget.document().adjustSize()
        
        # Get accurate document size AFTER rendering the HTML
        document_size = text_widget.document().size().toSize()
        
        # Add extra padding to ensure all content is visible
        text_widget.setMinimumHeight(document_size.height() + 40)
        
        # Dynamically adjust the text widget height based on content
        # Instead of setting fixed height which can cause content to be cut off
        text_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        
        # Visualize the route only if matplotlib is available
        if MATPLOTLIB_AVAILABLE:
            try:
                canvas.axes.clear()
                self.visualize_route(canvas.axes, result['route'], self.game_state.city_map.get_city_positions())
                canvas.draw()
            except Exception as e:
                logger.error(f"Error visualizing route: {e}")

    def visualize_route(self, axes, route, city_positions):
        """Visualize the route on matplotlib axes with enhanced styling"""
        # Plot city positions
        x_coords = [city_positions[city][0] for city in route]
        y_coords = [city_positions[city][1] for city in route]
        
        # Create a complete loop by adding the first city at the end
        x_coords.append(x_coords[0])
        y_coords.append(y_coords[0])
        
        # Plot route line with gradient color for better visualization
        for i in range(len(x_coords) - 1):
            # Create a gradient of colors from start to end
            alpha = (i + 1) / len(x_coords)
            axes.plot([x_coords[i], x_coords[i+1]], [y_coords[i], y_coords[i+1]], 
                     color=f'C0', linewidth=2, alpha=0.7 + 0.3*alpha,
                     solid_capstyle='round')
            
            # Add direction arrows
            if i < len(x_coords) - 1:
                midx = (x_coords[i] + x_coords[i+1]) / 2
                midy = (y_coords[i] + y_coords[i+1]) / 2
                dx = x_coords[i+1] - x_coords[i]
                dy = y_coords[i+1] - y_coords[i]
                # Normalize the direction vector and scale it
                dist = (dx**2 + dy**2)**0.5
                if dist > 0:  # Avoid division by zero
                    dx, dy = dx/dist, dy/dist
                    axes.arrow(midx - dx*0.05, midy - dy*0.05, dx*0.1, dy*0.1,
                              head_width=0.05, head_length=0.08, fc='white', ec='white', alpha=0.7)
        
        # Plot cities with different markers for better visibility
        axes.scatter(x_coords[:-1], y_coords[:-1], color='#3498db', s=120, 
                    edgecolor='white', linewidth=1.5, zorder=10)
        
        # Mark home city with a special symbol
        home_index = route.index(self.game_state.home_city)
        axes.scatter(x_coords[home_index], y_coords[home_index], 
                    color='#e74c3c', s=200, marker='*', 
                    edgecolor='white', linewidth=1.5, zorder=11)
        
        # Add city labels with improved styling
        for i, city in enumerate(route):
            # Use different style for home city
            if city == self.game_state.home_city:
                bbox_props = dict(boxstyle="round,pad=0.3", fc='#c0392b', ec='white', alpha=0.9)
                axes.annotate(city, (x_coords[i], y_coords[i]), 
                          textcoords="offset points", xytext=(0, 8), 
                          ha='center', va='bottom', fontsize=10, color='white',
                          bbox=bbox_props, fontweight='bold', zorder=12)
            else:
                bbox_props = dict(boxstyle="round,pad=0.2", fc='#2c3e50', ec='#7f8c8d', alpha=0.7)
                axes.annotate(city, (x_coords[i], y_coords[i]), 
                          textcoords="offset points", xytext=(0, 8), 
                          ha='center', va='bottom', fontsize=9, color='white',
                          bbox=bbox_props, zorder=12)
        
        # Add sequence numbers to show the order of cities
        for i in range(len(route)):
            axes.annotate(f"{i+1}", (x_coords[i], y_coords[i]), 
                      textcoords="offset points", xytext=(0, -15), 
                      ha='center', va='top', fontsize=8, color='white',
                      bbox=dict(boxstyle="circle,pad=0.2", fc='#34495e', ec='white', alpha=0.8),
                      zorder=12)
        
        # Enhance the plot with a title and labels
        axes.set_title("Route Path Visualization", fontsize=14, color='white', fontweight='bold')
        axes.set_xlabel("X Coordinate", fontsize=10, color='white')
        axes.set_ylabel("Y Coordinate", fontsize=10, color='white')
        
        # Add a legend for the home city
        from matplotlib.lines import Line2D
        legend_elements = [
            Line2D([0], [0], marker='*', color='w', markerfacecolor='#e74c3c', 
                  markersize=10, label=f'Home City: {self.game_state.home_city}'),
            Line2D([0], [0], marker='o', color='w', markerfacecolor='#3498db', 
                  markersize=8, label='Cities to Visit')
        ]
        axes.legend(handles=legend_elements, loc='upper right', framealpha=0.7)
        
        # Set equal aspect ratio to avoid distortion
        axes.set_aspect('equal', adjustable='box')
        
        # Add grid for better readability but make it subtle
        axes.grid(True, linestyle='--', alpha=0.3)
        
        # Add padding around the plot
        axes.margins(0.15)

    def display_comparison(self, results):
        """Display comparison of all algorithms with enhanced visualization"""
        # Clear previous data in table
        self.comparison_table.setRowCount(0)
        
        # Add data to table with better styling
        for i, (algo, result) in enumerate(results.items()):
            row_position = self.comparison_table.rowCount()
            self.comparison_table.insertRow(row_position)
            
            # Add items to the row
            algo_item = QTableWidgetItem(algo)
            length_item = QTableWidgetItem(f"{result['length']:.2f} km")
            time_item = QTableWidgetItem(f"{result['time']:.4f} ms")
            complexity_item = QTableWidgetItem(result['complexity'])
            
            # Apply styling based on algorithm
            if algo == "Brute Force":
                algo_item.setForeground(QColor("#e74c3c"))  # Red
            elif algo == "Nearest Neighbor":
                algo_item.setForeground(QColor("#3498db"))  # Blue
            else:  # Dynamic Programming
                algo_item.setForeground(QColor("#2ecc71"))  # Green
                
            # Make all text bold for better readability
            font = algo_item.font()
            font.setBold(True)
            algo_item.setFont(font)
            length_item.setFont(font)
            time_item.setFont(font)
            complexity_item.setFont(font)
                
            self.comparison_table.setItem(row_position, 0, algo_item)
            self.comparison_table.setItem(row_position, 1, length_item)
            self.comparison_table.setItem(row_position, 2, time_item)
            self.comparison_table.setItem(row_position, 3, complexity_item)
            
            # Highlight user's prediction with dark-theme friendly background
            if algo == self.user_prediction:
                for col in range(4):
                    item = self.comparison_table.item(row_position, col)
                    item.setBackground(QColor(26, 54, 93))  # Dark blue background
                    item.setForeground(QColor(255, 255, 255))  # White text
                    if col == 0:  # Add "Your Prediction" to the algorithm name
                        item.setText(f"{algo} (Your Prediction)")
            
            # Highlight shortest route
            if algo == self.shortest_algorithm:
                for col in range(4):
                    item = self.comparison_table.item(row_position, col)
                    if algo != self.user_prediction:
                        item.setBackground(QColor(28, 56, 46))  # Dark green background
                        item.setForeground(QColor(255, 255, 255))  # White text
                    if col == 0 and algo != self.user_prediction:  # Add "Shortest Route" to the algorithm name
                        item.setText(f"{algo} (Shortest Route)")
                    elif col == 0 and algo == self.user_prediction:  # Both prediction and shortest
                        item.setText(f"{algo} (Your Prediction ✓ Shortest Route)")
                        # Special highlight for correct prediction
                        item.setBackground(QColor(44, 83, 47))  # Better dark green for correct
                        item.setForeground(QColor(255, 255, 255))  # White text
        
        # Create enhanced bar chart comparison only if matplotlib is available
        if MATPLOTLIB_AVAILABLE and hasattr(self, 'comparison_canvas'):
            try:
                self.comparison_canvas.axes.clear()
                
                algorithms = list(results.keys())
                lengths = [results[algo]["length"] for algo in algorithms]
                times = [results[algo]["time"] for algo in algorithms]
                
                # Set colors based on algorithm type and prediction status
                bar_colors = []
                time_colors = []
                
                for algo in algorithms:
                    if algo == self.shortest_algorithm and algo == self.user_prediction:
                        bar_colors.append('#27ae60')  # Dark green for correct prediction
                    elif algo == self.shortest_algorithm:
                        bar_colors.append('#2ecc71')  # Green for shortest route
                    elif algo == self.user_prediction:
                        bar_colors.append('#3498db')  # Blue for prediction
                    else:
                        bar_colors.append('#95a5a6')  # Gray for others
                    
                    # Time bar colors use lighter versions
                    if algo == self.user_prediction:
                        time_colors.append('#5dade2')  # Lighter blue
                    else:
                        time_colors.append('#f39c12')  # Orange for times
                
                # Create two separate y-axes for different scales
                ax = self.comparison_canvas.axes
                width = 0.35
                x = range(len(algorithms))
                
                # Plot route lengths with custom colors
                bars1 = ax.bar(x, lengths, width, label='Route Length (km)', color=bar_colors)
                ax.set_ylabel('Route Length (km)', fontweight='bold')
                ax.set_xlabel('Algorithm', fontweight='bold')
                ax.set_xticks(x)
                ax.set_xticklabels(algorithms)
                
                # Add data labels on bars
                for bar in bars1:
                    height = bar.get_height()
                    ax.annotate(f'{height:.2f}',
                                xy=(bar.get_x() + bar.get_width() / 2, height),
                                xytext=(0, 3),  # 3 points vertical offset
                                textcoords="offset points",
                                ha='center', va='bottom',
                                fontsize=9,
                                color='white',  # Make labels white
                                weight='bold')  # Make labels bold for better visibility
                
                # Twin axis for time
                ax2 = ax.twinx()
                bars2 = ax2.bar([i + width for i in x], times, width, color=time_colors, label='Time (ms)')
                ax2.set_ylabel('Time (ms)', fontweight='bold')
                
                # Add data labels on bars
                for bar in bars2:
                    height = bar.get_height()
                    ax2.annotate(f'{height:.2f}',
                                xy=(bar.get_x() + bar.get_width() / 2, height),
                                xytext=(0, 3),  # 3 points vertical offset
                                textcoords="offset points",
                                ha='center', va='bottom',
                                fontsize=9,
                                color='white',  # Make labels white
                                weight='bold')  # Make labels bold for better visibility
                
                # Add enhanced legend
                lines1, labels1 = ax.get_legend_handles_labels()
                lines2, labels2 = ax2.get_legend_handles_labels()
                
                # Add custom legend entries for prediction and shortest
                from matplotlib.patches import Patch
                legend_elements = [
                    lines1[0], lines2[0]  # Route length and time
                ]
                legend_labels = [labels1[0], labels2[0]]
                
                # Add only if we have a prediction
                if self.user_prediction:
                    legend_elements.append(Patch(facecolor='#3498db', label='Your Prediction'))
                    legend_labels.append('Your Prediction')
                    
                # Add shortest route to legend
                if self.shortest_algorithm:
                    legend_elements.append(Patch(facecolor='#2ecc71', label='Shortest Route'))
                    legend_labels.append('Shortest Route')
                
                # If prediction matches shortest, add special entry
                if self.user_prediction and self.user_prediction == self.shortest_algorithm:
                    legend_elements.append(Patch(facecolor='#27ae60', label='Correct Prediction'))
                    legend_labels.append('Correct Prediction')
                
                ax.legend(legend_elements, legend_labels, loc='upper left', frameon=True, 
                          fancybox=True, shadow=True, fontsize='small')
                
                # Add a title
                ax.set_title('Algorithm Performance Comparison', fontweight='bold', fontsize=14)
                
                # Add grid for better readability
                ax.grid(True, linestyle='--', alpha=0.7)
                
                # Add background grid for better readability
                ax.set_axisbelow(True)
                
                # Add some padding between bars and axes
                ax.margins(y=0.2)
                ax2.margins(y=0.2)
                
                self.comparison_canvas.fig.tight_layout()
                self.comparison_canvas.draw()
            except Exception as e:
                logger.error(f"Error creating enhanced comparison chart: {e}")
                logger.error(traceback.format_exc())
    
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
        prediction_dialog.setStyleSheet("""
            QDialog {
                background-color: black;
                color: white;
            }
            QLabel {
                color: white;
            }
            QPushButton {
                background-color: #222222;
                color: white;
                border: 1px solid #444444;
                border-radius: 4px;
                padding: 6px 12px;
            }
            QPushButton:hover {
                background-color: #333333;
            }
            QPushButton:pressed {
                background-color: #444444;
            }
            QPushButton:disabled {
                background-color: #222222;
                color: #666666;
            }
            QComboBox {
                background-color: #222222;
                color: white;
                border: 1px solid #444444;
                border-radius: 4px;
                padding: 5px;
                min-width: 6em;
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 20px;
                border-left: 1px solid #444444;
            }
            QComboBox QAbstractItemView {
                background-color: #222222;
                color: white;
                selection-background-color: #444444;
            }
        """)
        
        layout = QVBoxLayout(prediction_dialog)
        
        # Information label
        info_label = QLabel(
            f"<p style='color: white;'>You have selected {len(self.game_state.selected_cities)} cities to visit.</p>"
            f"<p style='color: white;'>Before calculating the routes, predict which algorithm will find the shortest path:</p>"
        )
        info_label.setWordWrap(True)
        layout.addWidget(info_label)
        
        # Algorithm description
        algo_info = QLabel(
            "<p style='color: white;'><b>Brute Force</b>: Tries all possible routes (O(n!))</p>"
            "<p style='color: white;'><b>Nearest Neighbor</b>: Always visits closest unvisited city (O(n²))</p>"
            "<p style='color: white;'><b>Dynamic Programming</b>: Uses optimal subproblems (O(n²2ⁿ))</p>"
        )
        algo_info.setStyleSheet("""
            background-color: #111111;
            color: white;
            padding: 10px;
            border-radius: 5px;
            border: 1px solid #333333;
        """)
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