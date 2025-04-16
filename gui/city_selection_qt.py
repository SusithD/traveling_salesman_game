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
        title_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        main_layout.addWidget(title_label)
        
        instruction_label = QLabel("Check the cities you want to visit (must select at least 2):")
        main_layout.addWidget(instruction_label)
        
        # City selection area
        city_group = QGroupBox("Cities")
        city_group.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.city_layout = QGridLayout(city_group)
        main_layout.addWidget(city_group)
        
        # Button area
        button_layout = QHBoxLayout()
        
        self.calculate_button = QPushButton("Calculate Routes")
        self.calculate_button.clicked.connect(self.calculate_routes)
        button_layout.addWidget(self.calculate_button)
        
        self.select_all_button = QPushButton("Select All")
        self.select_all_button.clicked.connect(self.select_all_cities)
        button_layout.addWidget(self.select_all_button)
        
        self.clear_button = QPushButton("Clear Selection")
        self.clear_button.clicked.connect(self.clear_selection)
        button_layout.addWidget(self.clear_button)
        
        button_layout.addStretch(1)
        main_layout.addLayout(button_layout)
        
        # Distance matrix area
        matrix_group = QGroupBox("Distance Matrix")
        matrix_group.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        matrix_layout = QVBoxLayout(matrix_group)
        
        # Create a scroll area for the matrix
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        
        self.matrix_widget = QWidget()
        self.matrix_layout = QGridLayout(self.matrix_widget)
        
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
        
        # Create checkboxes for each city
        cols = 5
        for i, city in enumerate(cities):
            row, col = divmod(i, cols)
            
            if city == home_city:
                # Home city is disabled and marked special
                checkbox = QCheckBox(f"{city} (Home)")
                checkbox.setEnabled(False)
                checkbox.setStyleSheet("color: blue; font-weight: bold;")
            else:
                checkbox = QCheckBox(city)
                checkbox.setChecked(False)
            
            self.city_layout.addWidget(checkbox, row, col)
            self.city_checkboxes[city] = checkbox
        
        # Update the distance matrix display
        self.update_distance_matrix()
        logger.debug("City selection checkboxes updated")
    
    def update_distance_matrix(self):
        """Display the distance matrix in the UI"""
        logger.debug("Updating distance matrix display")
        
        # Clear existing matrix items
        while self.matrix_layout.count():
            item = self.matrix_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        # Get the distance matrix from the game state
        cities = self.game_state.city_map.get_cities()
        distances = self.game_state.city_map.get_distances()
        
        # Create the matrix header row
        self.matrix_layout.addWidget(QLabel(""), 0, 0)
        for i, city in enumerate(cities):
            header_label = QLabel(city)
            header_label.setStyleSheet("font-weight: bold;")
            self.matrix_layout.addWidget(header_label, 0, i + 1)
        
        # Create the matrix with distances
        for i, city1 in enumerate(cities):
            # Row header
            header_label = QLabel(city1)
            header_label.setStyleSheet("font-weight: bold;")
            self.matrix_layout.addWidget(header_label, i + 1, 0)
            
            for j, city2 in enumerate(cities):
                if city1 == city2:
                    self.matrix_layout.addWidget(QLabel("---"), i + 1, j + 1)
                else:
                    distance = distances.get((city1, city2)) or distances.get((city2, city1))
                    self.matrix_layout.addWidget(QLabel(str(distance)), i + 1, j + 1)
        
        logger.debug("Distance matrix display updated")
    
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