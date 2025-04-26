"""
City selection interface for the Traveling Salesman Problem game (PyQt5 Version)
"""
import logging
import traceback
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QGroupBox,
    QLabel, QCheckBox, QPushButton, QFrame, QScrollArea, QMessageBox,
    QSizePolicy
)
from PyQt5.QtCore import Qt

logger = logging.getLogger("CitySelection")

class CitySelectionFrameQt(QWidget):
    def __init__(self, game_state):
        logger.info("Initializing CitySelectionFrameQt")
        try:
            super().__init__()
            self.game_state = game_state
            self.city_checkboxes = {}
            
            # Apply black background and white text styling
            self.setStyleSheet("""
                QWidget {
                    background-color: black;
                    color: white;
                }
                QGroupBox {
                    border: 1px solid #444444;
                    border-radius: 5px;
                    margin-top: 1.5ex;
                    padding: 10px;
                    color: white;
                }
                QGroupBox::title {
                    subcontrol-origin: margin;
                    subcontrol-position: top left;
                    padding: 0 5px;
                    color: white;
                    font-weight: bold;
                }
                QCheckBox {
                    color: white;
                    spacing: 8px;
                    font-size: 14px;
                }
                QCheckBox::indicator {
                    width: 16px;
                    height: 16px;
                    border: 1px solid #666666;
                }
                QCheckBox::indicator:checked {
                    background-color: white;
                }
                QScrollArea {
                    border: 1px solid #444444;
                    border-radius: 4px;
                    background-color: #111111;
                }
            """)
            
            # Setup the layout
            self.create_widgets()
            
            logger.info("CitySelectionFrameQt initialized successfully")
        except Exception as e:
            logger.error(f"Error in CitySelectionFrameQt initialization: {str(e)}")
            logger.error(traceback.format_exc())
            QMessageBox.critical(None, "Initialization Error", f"Error setting up city selection: {str(e)}")
            raise
        
    def create_widgets(self):
        """Create the widgets for city selection"""
        logger.debug("Creating widgets for CitySelectionFrameQt")
        main_layout = QVBoxLayout(self)
        self.setLayout(main_layout)
        
        # Title and instructions
        title_label = QLabel("Select Cities to Visit")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; color: white; margin-bottom: 8px;")
        main_layout.addWidget(title_label)
        
        instruction_label = QLabel("Check the cities you want to visit (must select at least 2):")
        instruction_label.setStyleSheet("color: #cccccc; font-size: 14px; margin-bottom: 12px;")
        main_layout.addWidget(instruction_label)
        
        # City selection area with scroll functionality
        city_group = QGroupBox("Cities")
        city_group.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.MinimumExpanding)
        city_group.setMinimumHeight(250)  # Increased height
        city_group.setStyleSheet("""
            QGroupBox {
                border: 1px solid #444444;
                border-radius: 5px;
                margin-top: 1.5ex;
                padding: 15px;
                background-color: #111111;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 8px;
                color: white;
                font-weight: bold;
                font-size: 15px;
            }
        """)
        
        # Create a scroll area for the city selection
        city_scroll_area = QScrollArea()
        city_scroll_area.setWidgetResizable(True)
        city_scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                border: none;
                background: #222222;
                width: 12px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #555555;
                min-height: 20px;
                border-radius: 6px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)
        
        city_container = QWidget()
        city_container.setStyleSheet("background-color: #111111;")
        self.city_layout = QGridLayout(city_container)
        self.city_layout.setSpacing(15)  # Increased spacing between checkboxes
        
        city_scroll_area.setWidget(city_container)
        
        city_group_layout = QVBoxLayout(city_group)
        city_group_layout.addWidget(city_scroll_area)
        main_layout.addWidget(city_group)
        
        # Button area
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)
        button_layout.setContentsMargins(5, 15, 5, 15)
        
        self.calculate_button = QPushButton("Calculate Routes")
        self.calculate_button.setStyleSheet("""
            QPushButton {
                background-color: #222222;
                color: white;
                border: 1px solid #444444;
                border-radius: 4px;
                padding: 12px 25px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #444444;
            }
            QPushButton:pressed {
                background-color: #666666;
            }
        """)
        self.calculate_button.clicked.connect(self.calculate_routes)
        button_layout.addWidget(self.calculate_button)
        
        self.select_all_button = QPushButton("Select All")
        self.select_all_button.setStyleSheet("""
            QPushButton {
                background-color: #222222;
                color: white;
                border: 1px solid #444444;
                border-radius: 4px;
                padding: 10px 18px;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #444444;
            }
            QPushButton:pressed {
                background-color: #666666;
            }
        """)
        self.select_all_button.clicked.connect(self.select_all_cities)
        button_layout.addWidget(self.select_all_button)
        
        self.clear_button = QPushButton("Clear Selection")
        self.clear_button.setStyleSheet("""
            QPushButton {
                background-color: #222222;
                color: white;
                border: 1px solid #444444;
                border-radius: 4px;
                padding: 10px 18px;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #444444;
            }
            QPushButton:pressed {
                background-color: #666666;
            }
        """)
        self.clear_button.clicked.connect(self.clear_selection)
        button_layout.addWidget(self.clear_button)
        
        button_layout.addStretch(1)
        main_layout.addLayout(button_layout)
        
        # Distance matrix area with better visual clarity
        matrix_group = QGroupBox("Distance Matrix")
        matrix_group.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        matrix_group.setMinimumHeight(300)  # Increased height
        matrix_group.setStyleSheet("""
            QGroupBox {
                border: 1px solid #444444;
                border-radius: 5px;
                margin-top: 1.5ex;
                padding: 15px;
                background-color: #111111;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 8px;
                color: white;
                font-weight: bold;
                font-size: 15px;
            }
        """)
        matrix_layout = QVBoxLayout(matrix_group)
        
        # Create a scroll area for the matrix
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                border: none;
                background: #222222;
                width: 12px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #555555;
                min-height: 20px;
                border-radius: 6px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
            QScrollBar:horizontal {
                border: none;
                background: #222222;
                height: 12px;
                margin: 0px;
            }
            QScrollBar::handle:horizontal {
                background: #555555;
                min-width: 20px;
                border-radius: 6px;
            }
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
                width: 0px;
            }
        """)
        
        self.matrix_widget = QWidget()
        self.matrix_widget.setStyleSheet("""
            background-color: #111111;
            color: white;
        """)
        self.matrix_layout = QGridLayout(self.matrix_widget)
        self.matrix_layout.setSpacing(8)
        
        scroll_area.setWidget(self.matrix_widget)
        matrix_layout.addWidget(scroll_area)
        
        main_layout.addWidget(matrix_group)
        
        logger.debug("Widgets created successfully")
    
    def update_cities_display(self):
        """Update the city selection checkboxes based on game state"""
        logger.debug("Updating city selection checkboxes")
        
        # Clear existing city checkboxes
        for checkbox in self.city_checkboxes.values():
            checkbox.setParent(None)
        self.city_checkboxes = {}
        
        # Get cities from the game state
        cities = self.game_state.city_map.get_cities()
        home_city = self.game_state.home_city
        
        # Create checkboxes for each city with improved visual display
        cols = 4  # Reduced columns for better layout
        for i, city in enumerate(cities):
            row, col = divmod(i, cols)
            
            if city == home_city:
                # Home city is disabled and marked with special styling
                checkbox = QCheckBox(f"{city} (Home)")
                checkbox.setEnabled(False)
                checkbox.setStyleSheet("""
                    color: #4299e1;
                    font-weight: bold;
                    font-size: 15px;
                    background-color: rgba(26, 54, 93, 0.4);
                    border-radius: 5px;
                    padding: 8px;
                    margin: 5px;
                """)
            else:
                checkbox = QCheckBox(city)
                checkbox.setChecked(False)
                checkbox.setStyleSheet("""
                    color: white;
                    font-size: 15px;
                    padding: 8px;
                    margin: 5px;
                    border: 1px solid #333333;
                    border-radius: 5px;
                    background-color: #222222;
                """)
            
            self.city_layout.addWidget(checkbox, row, col)
            self.city_checkboxes[city] = checkbox
        
        # Ensure the grid layout has consistent spacing
        self.city_layout.setRowStretch(row+1, 1)
        
        # Update the distance matrix display
        self.update_distance_matrix()
        logger.debug("City selection checkboxes updated with enhanced visual clarity")
    
    def update_distance_matrix(self):
        """Display the distance matrix in the UI with black background and white text"""
        logger.debug("Updating distance matrix display")
        
        # Clear existing matrix items
        while self.matrix_layout.count():
            item = self.matrix_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        # Get the distance matrix from the game state
        cities = self.game_state.city_map.get_cities()
        distances = self.game_state.city_map.get_distances()
        
        # Create the matrix header row with better styling
        header_cell = QLabel("")
        header_cell.setStyleSheet("""
            background-color: #222222;
            padding: 8px;
            border: 1px solid #333333;
            font-weight: bold;
        """)
        self.matrix_layout.addWidget(header_cell, 0, 0)
        
        for i, city in enumerate(cities):
            header_label = QLabel(city)
            header_label.setStyleSheet("""
                font-weight: bold;
                font-size: 14px;
                color: white;
                background-color: #333333;
                padding: 8px;
                border: 1px solid #444444;
            """)
            header_label.setAlignment(Qt.AlignCenter)
            self.matrix_layout.addWidget(header_label, 0, i + 1)
        
        # Create the matrix with distances - styled cells
        for i, city1 in enumerate(cities):
            # Row header
            header_label = QLabel(city1)
            header_label.setStyleSheet("""
                font-weight: bold;
                font-size: 14px;
                color: white;
                background-color: #333333;
                padding: 8px;
                border: 1px solid #444444;
            """)
            header_label.setAlignment(Qt.AlignCenter)
            self.matrix_layout.addWidget(header_label, i + 1, 0)
            
            for j, city2 in enumerate(cities):
                cell = QFrame()
                cell_layout = QVBoxLayout(cell)
                cell_layout.setContentsMargins(8, 8, 8, 8)
                
                if city1 == city2:
                    # Diagonal cells (same city to same city)
                    label = QLabel("---")
                    cell.setStyleSheet("""
                        background-color: #222222;
                        border: 1px solid #333333;
                    """)
                else:
                    # Regular distance cells
                    distance = distances.get((city1, city2)) or distances.get((city2, city1))
                    label = QLabel(f"{distance:.1f}")
                    
                    # Alternate row coloring for readability
                    if i % 2 == 0:
                        cell.setStyleSheet("""
                            background-color: #111111;
                            border: 1px solid #333333;
                        """)
                    else:
                        cell.setStyleSheet("""
                            background-color: #181818;
                            border: 1px solid #333333;
                        """)
                
                label.setAlignment(Qt.AlignCenter)
                label.setStyleSheet("color: white; font-size: 13px;")
                cell_layout.addWidget(label)
                self.matrix_layout.addWidget(cell, i + 1, j + 1)
        
        # Set column and row stretching for better spacing
        for i in range(len(cities) + 1):
            self.matrix_layout.setColumnStretch(i, 1)
            if i < len(cities):
                self.matrix_layout.setRowStretch(i + 1, 1)
        
        logger.debug("Distance matrix display updated with enhanced styling")
    
    def get_selected_cities(self):
        """Get list of selected cities"""
        return [city for city, checkbox in self.city_checkboxes.items() if checkbox.isChecked()]
    
    def select_all_cities(self):
        """Select all available cities"""
        logger.debug("Selecting all cities")
        home_city = self.game_state.home_city
        for city, checkbox in self.city_checkboxes.items():
            if city != home_city:
                checkbox.setChecked(True)
        logger.debug("All cities selected")
    
    def clear_selection(self):
        """Clear all city selections"""
        logger.debug("Clearing all city selections")
        for checkbox in self.city_checkboxes.values():
            checkbox.setChecked(False)
        logger.debug("All city selections cleared")
    
    def calculate_routes(self):
        """Start the route calculation process"""
        logger.info("Starting route calculation process")
        
        # Get the selected cities
        selected_cities = self.get_selected_cities()
        
        # Add the home city
        if self.game_state.home_city not in selected_cities:
            selected_cities.append(self.game_state.home_city)
        
        # Check if enough cities are selected
        if len(selected_cities) < 3:  # Home + at least 2 more
            logger.error("Not enough cities selected for route calculation")
            QMessageBox.critical(self, "Error", "Please select at least 2 cities to visit!")
            return
        
        # Set the selected cities in the game state
        self.game_state.selected_cities = selected_cities
        
        # Find the parent window
        parent = self
        while parent.parent():
            parent = parent.parent()
        
        # Start the calculation in the parent window
        parent.results_display.calculate_and_display_routes()
        logger.info("Route calculation process started")