"""
City selection screen for the Traveling Salesman Problem game
"""
import logging
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QFrame, QScrollArea, QGridLayout, QCheckBox, QSizePolicy
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor

logger = logging.getLogger("CitySelectionScreen")

class CitySelectionScreen(QWidget):
    """
    Screen for selecting cities to visit in the TSP game
    """
    def __init__(self, flow_manager):
        super().__init__()
        self.flow_manager = flow_manager
        self.city_checkboxes = {}
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
        
        # Header with progress indicator
        header_layout = QHBoxLayout()
        
        # Left side - Title
        header_left = QVBoxLayout()
        title = QLabel("City Selection")
        title.setStyleSheet("""
            color: white;
            font-size: 24px;
            font-weight: bold;
        """)
        header_left.addWidget(title)
        
        subtitle = QLabel("Choose which cities you want to visit")
        subtitle.setStyleSheet("color: #aaaaaa; font-size: 16px;")
        header_left.addWidget(subtitle)
        
        header_layout.addLayout(header_left)
        header_layout.addStretch()
        
        # Right side - Progress indicator
        progress_frame = QFrame()
        progress_frame.setStyleSheet("""
            background-color: rgba(255, 255, 255, 0.1);
            border-radius: 10px;
            padding: 5px 15px;
        """)
        progress_layout = QHBoxLayout(progress_frame)
        progress_layout.setContentsMargins(10, 5, 10, 5)
        progress_layout.setSpacing(5)
        
        # Step indicators
        step1 = QLabel("1")
        step1.setStyleSheet("""
            background-color: #3498db;
            color: white;
            border-radius: 10px;
            padding: 5px;
            font-weight: bold;
            min-width: 20px;
            min-height: 20px;
            qproperty-alignment: AlignCenter;
        """)
        progress_layout.addWidget(step1)
        
        progress_layout.addWidget(QLabel("→"))
        
        step2 = QLabel("2")
        step2.setStyleSheet("""
            background-color: #f39c12;
            color: white;
            border-radius: 10px;
            padding: 5px;
            font-weight: bold;
            min-width: 20px;
            min-height: 20px;
            qproperty-alignment: AlignCenter;
        """)
        progress_layout.addWidget(step2)
        
        progress_layout.addWidget(QLabel("→"))
        
        step3 = QLabel("3")
        step3.setStyleSheet("""
            background-color: #333333;
            color: #aaaaaa;
            border-radius: 10px;
            padding: 5px;
            font-weight: bold;
            min-width: 20px;
            min-height: 20px;
            qproperty-alignment: AlignCenter;
        """)
        progress_layout.addWidget(step3)
        
        header_layout.addWidget(progress_frame)
        container_layout.addLayout(header_layout)
        
        # Add separator
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        separator.setStyleSheet("background-color: #333333; height: 1px;")
        container_layout.addWidget(separator)
        
        # Main content area with instructions
        instruction_label = QLabel(
            "Select which cities you want to visit. You must select at least 2 cities besides your home city."
        )
        instruction_label.setStyleSheet("color: white; font-size: 15px;")
        instruction_label.setWordWrap(True)
        container_layout.addWidget(instruction_label)
        
        # Home city indicator
        self.home_city_frame = QFrame()
        self.home_city_frame.setStyleSheet("""
            background-color: #2c3e50;
            border: 1px solid #3498db;
            border-radius: 10px;
            padding: 10px;
            margin-bottom: 20px;
        """)
        home_city_layout = QHBoxLayout(self.home_city_frame)
        
        home_icon = QLabel("🏠")
        home_icon.setStyleSheet("font-size: 24px; margin-right: 10px;")
        home_city_layout.addWidget(home_icon)
        
        home_text = QVBoxLayout()
        home_label = QLabel("Home City")
        home_label.setStyleSheet("color: #3498db; font-size: 14px; font-weight: bold;")
        home_text.addWidget(home_label)
        
        self.home_city_name = QLabel("City X")  # Will be populated with actual home city
        self.home_city_name.setStyleSheet("color: white; font-size: 18px; font-weight: bold;")
        home_text.addWidget(self.home_city_name)
        
        home_city_layout.addLayout(home_text)
        home_city_layout.addStretch()
        
        hint_label = QLabel("Your journey will start and end here")
        hint_label.setStyleSheet("color: #aaaaaa; font-size: 12px; font-style: italic;")
        home_city_layout.addWidget(hint_label)
        
        container_layout.addWidget(self.home_city_frame)
        
        # City selection area
        city_selection_frame = QFrame()
        city_selection_frame.setStyleSheet("""
            background-color: #222222;
            border-radius: 10px;
            padding: 15px;
        """)
        city_selection_layout = QVBoxLayout(city_selection_frame)
        
        # Title and quick selection buttons
        selection_header = QHBoxLayout()
        
        cities_title = QLabel("Available Cities")
        cities_title.setStyleSheet("color: white; font-size: 16px; font-weight: bold;")
        selection_header.addWidget(cities_title)
        
        selection_header.addStretch()
        
        select_all_btn = QPushButton("Select All")
        select_all_btn.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 5px 10px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #2ecc71;
            }
        """)
        select_all_btn.clicked.connect(self.select_all_cities)
        selection_header.addWidget(select_all_btn)
        
        clear_all_btn = QPushButton("Clear All")
        clear_all_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 5px 10px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        clear_all_btn.clicked.connect(self.clear_selection)
        selection_header.addWidget(clear_all_btn)
        
        city_selection_layout.addLayout(selection_header)
        
        # City checkboxes in a scrollable grid
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                border: none;
                background: #333333;
                width: 8px;
                border-radius: 4px;
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
        
        # City grid widget
        city_grid_widget = QWidget()
        city_grid_widget.setStyleSheet("background-color: transparent;")
        self.city_grid = QGridLayout(city_grid_widget)
        self.city_grid.setSpacing(15)
        self.city_grid.setContentsMargins(10, 10, 10, 10)
        
        scroll_area.setWidget(city_grid_widget)
        scroll_area.setMinimumHeight(250)
        city_selection_layout.addWidget(scroll_area)
        
        # Selected cities counter
        self.selection_counter = QLabel("0 cities selected")
        self.selection_counter.setStyleSheet("""
            color: #aaaaaa;
            font-size: 14px;
            padding: 10px 0;
        """)
        self.selection_counter.setAlignment(Qt.AlignCenter)
        city_selection_layout.addWidget(self.selection_counter)
        
        container_layout.addWidget(city_selection_frame)
        
        # City distance preview
        distance_title = QLabel("City Distances Reference")
        distance_title.setStyleSheet("color: white; font-size: 16px; font-weight: bold; margin-top: 10px;")
        container_layout.addWidget(distance_title)
        
        # Distance info in a collapsible/expandable area
        distance_frame = QFrame()
        distance_frame.setStyleSheet("""
            background-color: #1a1a1a;
            border-radius: 8px;
            padding: 15px;
        """)
        distance_layout = QVBoxLayout(distance_frame)
        
        distance_info = QLabel(
            "The distances between cities are shown in kilometers. These distances will be used "
            "when calculating the optimal route."
        )
        distance_info.setWordWrap(True)
        distance_info.setStyleSheet("color: #aaaaaa; font-size: 13px;")
        distance_layout.addWidget(distance_info)
        
        # Scrollable distance matrix area
        distance_scroll = QScrollArea()
        distance_scroll.setWidgetResizable(True)
        distance_scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar {
                border: none;
                background: #333333;
                width: 8px;
                height: 8px;
                border-radius: 4px;
            }
            QScrollBar::handle {
                background: #666666;
                min-height: 20px;
                min-width: 20px;
                border-radius: 4px;
            }
            QScrollBar::add-line, QScrollBar::sub-line {
                height: 0px;
                width: 0px;
            }
        """)
        
        self.distance_matrix_widget = QWidget()
        self.distance_matrix_widget.setStyleSheet("background-color: transparent;")
        self.distance_matrix = QGridLayout(self.distance_matrix_widget)
        self.distance_matrix.setSpacing(1)
        
        distance_scroll.setWidget(self.distance_matrix_widget)
        distance_scroll.setMaximumHeight(200)  # Limit the height
        distance_layout.addWidget(distance_scroll)
        
        container_layout.addWidget(distance_frame)
        
        # Button area
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        back_button = QPushButton("← Back")
        back_button.setStyleSheet("""
            QPushButton {
                background-color: #333333;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px 15px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #444444;
            }
        """)
        back_button.clicked.connect(self.go_back)
        button_layout.addWidget(back_button)
        
        self.continue_button = QPushButton("Make Prediction →")
        self.continue_button.setStyleSheet("""
            QPushButton {
                background-color: #f39c12;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px 20px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #e67e22;
            }
            QPushButton:pressed {
                background-color: #d35400;
            }
            QPushButton:disabled {
                background-color: #555555;
                color: #aaaaaa;
            }
        """)
        self.continue_button.clicked.connect(self.continue_to_prediction)
        self.continue_button.setEnabled(False)  # Disabled initially until enough cities selected
        button_layout.addWidget(self.continue_button)
        
        container_layout.addLayout(button_layout)
        
        # Add container to main layout
        main_layout.addWidget(container)
    
    def update_display(self):
        """Update the display with current game state"""
        # Update home city
        if self.flow_manager.game_state.home_city:
            self.home_city_name.setText(self.flow_manager.game_state.home_city)
        
        # Clear existing city checkboxes
        for checkbox in self.city_checkboxes.values():
            checkbox.setParent(None)
        self.city_checkboxes = {}
        
        # Get cities from the game state
        if self.flow_manager.game_state.city_map:
            cities = self.flow_manager.game_state.city_map.get_cities()
            home_city = self.flow_manager.game_state.home_city
            
            # Create checkboxes in grid layout
            cols = 3
            for i, city in enumerate(cities):
                row, col = divmod(i, cols)
                
                # Create checkbox with styled card appearance
                checkbox_frame = QFrame()
                if city == home_city:
                    # Home city styling - disabled but highlighted
                    checkbox_frame.setStyleSheet("""
                        background-color: rgba(52, 152, 219, 0.2);
                        border: 1px solid #3498db;
                        border-radius: 8px;
                        padding: 10px;
                    """)
                else:
                    # Normal city styling
                    checkbox_frame.setStyleSheet("""
                        background-color: #333333;
                        border: 1px solid #444444;
                        border-radius: 8px;
                        padding: 10px;
                    """)
                
                frame_layout = QVBoxLayout(checkbox_frame)
                frame_layout.setContentsMargins(10, 10, 10, 10)
                frame_layout.setSpacing(5)
                
                # City name and checkbox
                checkbox = QCheckBox(city)
                checkbox.setStyleSheet("""
                    QCheckBox {
                        color: white;
                        font-size: 15px;
                        font-weight: bold;
                    }
                    QCheckBox::indicator {
                        width: 18px;
                        height: 18px;
                        border: 1px solid #666666;
                        border-radius: 3px;
                    }
                    QCheckBox::indicator:checked {
                        background-color: #3498db;
                        border: 1px solid #2980b9;
                    }
                """)
                
                # Disable home city checkbox
                if city == home_city:
                    checkbox.setEnabled(False)
                    home_label = QLabel("(Home)")
                    home_label.setStyleSheet("color: #3498db; font-size: 12px;")
                    frame_layout.addWidget(home_label)
                else:
                    # Track checkbox changes
                    checkbox.stateChanged.connect(self.update_selection_count)
                
                frame_layout.addWidget(checkbox)
                self.city_grid.addWidget(checkbox_frame, row, col)
                self.city_checkboxes[city] = checkbox
            
            # Update distance matrix
            self.update_distance_matrix(cities)
    
    def update_distance_matrix(self, cities):
        """Update the distance matrix display"""
        # Clear existing matrix cells
        for i in reversed(range(self.distance_matrix.count())):
            self.distance_matrix.itemAt(i).widget().deleteLater()
        
        # Get the distances from the game state
        distances = self.flow_manager.game_state.city_map.get_distances()
        
        # Create header row
        header_cell = QLabel("")
        header_cell.setStyleSheet("""
            background-color: #222222;
            color: white;
            padding: 5px;
            border: 1px solid #333333;
        """)
        self.distance_matrix.addWidget(header_cell, 0, 0)
        
        for i, city in enumerate(cities):
            header = QLabel(city)
            header.setStyleSheet("""
                background-color: #2c3e50;
                color: white;
                font-weight: bold;
                padding: 5px;
                border: 1px solid #34495e;
                border-radius: 3px;
            """)
            header.setAlignment(Qt.AlignCenter)
            self.distance_matrix.addWidget(header, 0, i + 1)
            
            # Create row headers
            row_header = QLabel(city)
            row_header.setStyleSheet("""
                background-color: #2c3e50;
                color: white;
                font-weight: bold;
                padding: 5px;
                border: 1px solid #34495e;
                border-radius: 3px;
            """)
            row_header.setAlignment(Qt.AlignCenter)
            self.distance_matrix.addWidget(row_header, i + 1, 0)
        
        # Fill in distances
        for i, city1 in enumerate(cities):
            for j, city2 in enumerate(cities):
                if city1 == city2:
                    cell = QLabel("—")
                    cell.setStyleSheet("""
                        background-color: #222222;
                        color: #555555;
                        padding: 5px;
                        border: 1px solid #333333;
                    """)
                else:
                    distance = distances.get((city1, city2)) or distances.get((city2, city1), 0)
                    cell = QLabel(f"{distance:.1f}")
                    
                    # Style cells with alternating colors
                    if (i + j) % 2 == 0:
                        cell.setStyleSheet("""
                            background-color: #1a1a1a;
                            color: white;
                            padding: 5px;
                            border: 1px solid #333333;
                        """)
                    else:
                        cell.setStyleSheet("""
                            background-color: #222222;
                            color: white;
                            padding: 5px;
                            border: 1px solid #333333;
                        """)
                
                cell.setAlignment(Qt.AlignCenter)
                self.distance_matrix.addWidget(cell, i + 1, j + 1)
    
    def update_selection_count(self):
        """Update the selection counter and continue button state"""
        selected_count = len(self.get_selected_cities())
        self.selection_counter.setText(f"{selected_count} cities selected")
        
        # Enable continue button if at least 2 cities (besides home) are selected
        if selected_count >= 2:
            self.continue_button.setEnabled(True)
            self.selection_counter.setStyleSheet("""
                color: #2ecc71;
                font-size: 14px;
                font-weight: bold;
                padding: 10px 0;
            """)
        else:
            self.continue_button.setEnabled(False)
            self.selection_counter.setStyleSheet("""
                color: #e74c3c;
                font-size: 14px;
                padding: 10px 0;
            """)
    
    def get_selected_cities(self):
        """Get list of selected cities"""
        return [city for city, checkbox in self.city_checkboxes.items() 
                if checkbox.isChecked() and city != self.flow_manager.game_state.home_city]
    
    def select_all_cities(self):
        """Select all available cities"""
        home_city = self.flow_manager.game_state.home_city
        for city, checkbox in self.city_checkboxes.items():
            if city != home_city:
                checkbox.setChecked(True)
                
        self.update_selection_count()
    
    def clear_selection(self):
        """Clear all city selections"""
        for checkbox in self.city_checkboxes.values():
            checkbox.setChecked(False)
            
        self.update_selection_count()
    
    def go_back(self):
        """Go back to the mission briefing screen"""
        self.flow_manager.show_mission_screen()
    
    def continue_to_prediction(self):
        """Continue to the prediction screen"""
        # Get selected cities
        selected_cities = self.get_selected_cities()
        
        # Add home city
        if self.flow_manager.game_state.home_city not in selected_cities:
            selected_cities.append(self.flow_manager.game_state.home_city)
        
        # Update game state
        self.flow_manager.game_state.selected_cities = selected_cities
        
        # Continue to prediction screen
        self.flow_manager.show_prediction_screen()