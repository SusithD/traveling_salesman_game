"""
City selection screen for the Traveling Salesman Problem game
"""
import logging
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QFrame, QScrollArea, QGridLayout, QCheckBox, QSizePolicy,
    QGraphicsDropShadowEffect
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
        # Main layout with center alignment
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(20)
        main_layout.setAlignment(Qt.AlignCenter)
        
        # Create central container frame with modern styling - INCREASED WIDTH
        central_frame = QFrame()
        central_frame.setObjectName("selectionContainer")
        central_frame.setMinimumWidth(1000)  # Increased minimum width
        central_frame.setMaximumWidth(1200)  # Increased maximum width
        central_frame.setStyleSheet("""
            #selectionContainer {
                background-color: rgba(26, 26, 26, 0.7);
                border-radius: 20px;
                border: 1px solid rgba(255, 255, 255, 0.1);
            }
        """)
        
        container_layout = QVBoxLayout(central_frame)
        container_layout.setContentsMargins(40, 40, 40, 40)
        container_layout.setSpacing(25)
        
        # Header with progress indicator
        header_frame = QFrame()
        header_frame.setObjectName("headerFrame")
        header_frame.setStyleSheet("""
            #headerFrame {
                background-color: rgba(61, 90, 254, 0.15);
                border-radius: 15px;
            }
        """)
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(20, 15, 20, 15)
        
        # Left side - Title with icon
        header_left = QHBoxLayout()
        
        # Selection icon
        selection_icon = QLabel("🗺️")
        selection_icon.setFixedSize(60, 60)
        selection_icon.setObjectName("selectionIcon")
        selection_icon.setStyleSheet("""
            #selectionIcon {
                font-size: 30px;
                background-color: #3D5AFE;
                color: white;
                border-radius: 30px;
                margin-right: 15px;
            }
        """)
        selection_icon.setAlignment(Qt.AlignCenter)
        header_left.addWidget(selection_icon)
        
        # Title and subtitle
        title_layout = QVBoxLayout()
        title_layout.setSpacing(5)
        
        title = QLabel("CITY SELECTION")
        title.setObjectName("selectionTitle")
        title.setStyleSheet("""
            #selectionTitle {
                color: white;
                font-size: 22px;
                font-weight: bold;
                letter-spacing: 1px;
            }
        """)
        title_layout.addWidget(title)
        
        subtitle = QLabel("Choose which cities you want to visit")
        subtitle.setObjectName("selectionSubtitle")
        subtitle.setStyleSheet("""
            #selectionSubtitle {
                color: #BBBBBB;
                font-size: 14px;
            }
        """)
        title_layout.addWidget(subtitle)
        
        header_left.addLayout(title_layout)
        header_layout.addLayout(header_left)
        header_layout.addStretch()
        
        # Right side - Progress indicator
        progress_frame = QFrame()
        progress_frame.setObjectName("progressFrame")
        progress_frame.setStyleSheet("""
            #progressFrame {
                background-color: rgba(255, 255, 255, 0.1);
                border-radius: 10px;
                padding: 5px 15px;
            }
        """)
        progress_layout = QHBoxLayout(progress_frame)
        progress_layout.setContentsMargins(10, 5, 10, 5)
        progress_layout.setSpacing(8)
        
        # Step indicators
        step1 = QLabel("1")
        step1.setObjectName("step1")
        step1.setStyleSheet("""
            #step1 {
                background-color: #3D5AFE;
                color: white;
                border-radius: 12px;
                padding: 5px;
                font-weight: bold;
                min-width: 24px;
                min-height: 24px;
                qproperty-alignment: AlignCenter;
            }
        """)
        progress_layout.addWidget(step1)
        
        arrow1 = QLabel("→")
        arrow1.setStyleSheet("color: white; font-size: 14px;")
        progress_layout.addWidget(arrow1)
        
        step2 = QLabel("2")
        step2.setObjectName("step2")
        step2.setStyleSheet("""
            #step2 {
                background-color: #f39c12;
                color: white;
                border-radius: 12px;
                padding: 5px;
                font-weight: bold;
                min-width: 24px;
                min-height: 24px;
                qproperty-alignment: AlignCenter;
            }
        """)
        progress_layout.addWidget(step2)
        
        arrow2 = QLabel("→")
        arrow2.setStyleSheet("color: white; font-size: 14px;")
        progress_layout.addWidget(arrow2)
        
        step3 = QLabel("3")
        step3.setObjectName("step3")
        step3.setStyleSheet("""
            #step3 {
                background-color: #333333;
                color: #aaaaaa;
                border-radius: 12px;
                padding: 5px;
                font-weight: bold;
                min-width: 24px;
                min-height: 24px;
                qproperty-alignment: AlignCenter;
            }
        """)
        progress_layout.addWidget(step3)
        
        header_layout.addWidget(progress_frame)
        container_layout.addWidget(header_frame)
        
        # Stylish separator
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setStyleSheet("""
            background-color: #3D5AFE;
            max-width: 150px;
            height: 3px;
            margin: 5px;
        """)
        container_layout.addWidget(separator, 0, Qt.AlignCenter)
        
        # Main content area with instructions
        instruction_label = QLabel(
            "Select which cities you want to visit. You must select at least 2 cities besides your home city."
        )
        instruction_label.setObjectName("instructionLabel")
        instruction_label.setStyleSheet("""
            #instructionLabel {
                color: #DDDDDD;
                font-size: 15px;
                line-height: 150%;
                padding: 5px;
            }
        """)
        instruction_label.setWordWrap(True)
        instruction_label.setAlignment(Qt.AlignCenter)
        container_layout.addWidget(instruction_label)
        
        # Home city indicator with updated styling
        self.home_city_frame = QFrame()
        self.home_city_frame.setObjectName("homeCityFrame")
        self.home_city_frame.setStyleSheet("""
            #homeCityFrame {
                background-color: rgba(61, 90, 254, 0.15);
                border: 1px solid rgba(61, 90, 254, 0.3);
                border-radius: 15px;
            }
        """)
        home_city_layout = QHBoxLayout(self.home_city_frame)
        home_city_layout.setContentsMargins(20, 20, 20, 20)
        
        home_icon = QLabel("🏠")
        home_icon.setObjectName("homeIcon")
        home_icon.setStyleSheet("""
            #homeIcon {
                font-size: 24px;
                margin-right: 10px;
            }
        """)
        home_city_layout.addWidget(home_icon)
        
        home_text = QVBoxLayout()
        home_text.setSpacing(5)
        
        home_label = QLabel("HOME CITY")
        home_label.setObjectName("homeCityLabel")
        home_label.setStyleSheet("""
            #homeCityLabel {
                color: #3D5AFE;
                font-size: 14px;
                font-weight: bold;
                letter-spacing: 1px;
            }
        """)
        home_text.addWidget(home_label)
        
        self.home_city_name = QLabel("City X")  # Will be populated with actual home city
        self.home_city_name.setObjectName("homeCityName")
        self.home_city_name.setStyleSheet("""
            #homeCityName {
                color: white;
                font-size: 18px;
                font-weight: bold;
            }
        """)
        home_text.addWidget(self.home_city_name)
        
        home_city_layout.addLayout(home_text)
        home_city_layout.addStretch()
        
        hint_label = QLabel("Your journey will start and end here")
        hint_label.setStyleSheet("color: #aaaaaa; font-size: 12px; font-style: italic;")
        home_city_layout.addWidget(hint_label)
        
        container_layout.addWidget(self.home_city_frame)
        
        # City selection area with updated styling
        city_selection_frame = QFrame()
        city_selection_frame.setObjectName("citySelectionFrame")
        city_selection_frame.setStyleSheet("""
            #citySelectionFrame {
                background-color: rgba(33, 33, 33, 0.7);
                border-radius: 15px;
                padding: 15px;
            }
        """)
        city_selection_layout = QVBoxLayout(city_selection_frame)
        city_selection_layout.setContentsMargins(20, 20, 20, 20)
        city_selection_layout.setSpacing(15)
        
        # Title and quick selection buttons
        selection_header = QHBoxLayout()
        
        cities_title = QLabel("AVAILABLE CITIES")
        cities_title.setObjectName("citiesTitle")
        cities_title.setStyleSheet("""
            #citiesTitle {
                color: white;
                font-size: 16px;
                font-weight: bold;
                letter-spacing: 1px;
            }
        """)
        selection_header.addWidget(cities_title)
        
        selection_header.addStretch()
        
        select_all_btn = QPushButton("Select All")
        select_all_btn.setObjectName("selectAllBtn")
        select_all_btn.setStyleSheet("""
            #selectAllBtn {
                background-color: #27ae60;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 8px 15px;
                font-size: 13px;
                font-weight: bold;
            }
            #selectAllBtn:hover {
                background-color: #2ecc71;
            }
        """)
        select_all_btn.clicked.connect(self.select_all_cities)
        selection_header.addWidget(select_all_btn)
        
        clear_all_btn = QPushButton("Clear All")
        clear_all_btn.setObjectName("clearAllBtn")
        clear_all_btn.setStyleSheet("""
            #clearAllBtn {
                background-color: #e74c3c;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 8px 15px;
                font-size: 13px;
                font-weight: bold;
            }
            #clearAllBtn:hover {
                background-color: #c0392b;
            }
        """)
        clear_all_btn.clicked.connect(self.clear_selection)
        selection_header.addWidget(clear_all_btn)
        
        city_selection_layout.addLayout(selection_header)
        
        # City checkboxes in a scrollable grid with updated styling
        scroll_area = QScrollArea()
        scroll_area.setObjectName("cityScrollArea")
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            #cityScrollArea {
                border: none;
                background-color: transparent;
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
        
        # City grid widget - INCREASED COLUMNS
        city_grid_widget = QWidget()
        city_grid_widget.setStyleSheet("background-color: transparent;")
        self.city_grid = QGridLayout(city_grid_widget)
        self.city_grid.setSpacing(15)
        self.city_grid.setContentsMargins(10, 10, 10, 10)
        
        scroll_area.setWidget(city_grid_widget)
        scroll_area.setMinimumHeight(280)  # Increased height
        city_selection_layout.addWidget(scroll_area)
        
        # Selected cities counter with updated styling
        self.selection_counter = QLabel("0 cities selected")
        self.selection_counter.setObjectName("selectionCounter")
        self.selection_counter.setStyleSheet("""
            #selectionCounter {
                color: #aaaaaa;
                font-size: 14px;
                padding: 8px 15px;
                background-color: rgba(51, 51, 51, 0.5);
                border-radius: 10px;
                font-weight: bold;
            }
        """)
        self.selection_counter.setAlignment(Qt.AlignCenter)
        city_selection_layout.addWidget(self.selection_counter, 0, Qt.AlignCenter)
        
        container_layout.addWidget(city_selection_frame)
        
        # City distance preview with updated styling
        distance_title = QLabel("CITY DISTANCES REFERENCE")
        distance_title.setObjectName("distanceTitle")
        distance_title.setStyleSheet("""
            #distanceTitle {
                color: white; 
                font-size: 16px; 
                font-weight: bold;
                letter-spacing: 1px;
                margin-top: 10px;
            }
        """)
        distance_title.setAlignment(Qt.AlignCenter)
        container_layout.addWidget(distance_title)
        
        # Distance info in collapsible/expandable area with updated styling
        distance_frame = QFrame()
        distance_frame.setObjectName("distanceFrame")
        distance_frame.setStyleSheet("""
            #distanceFrame {
                background-color: rgba(33, 33, 33, 0.7);
                border-radius: 15px;
                padding: 15px;
            }
        """)
        distance_layout = QVBoxLayout(distance_frame)
        distance_layout.setContentsMargins(20, 20, 20, 20)
        distance_layout.setSpacing(15)
        
        distance_info = QLabel(
            "The distances between cities are shown in kilometers. These distances will be used "
            "when calculating the optimal route."
        )
        distance_info.setObjectName("distanceInfo")
        distance_info.setWordWrap(True)
        distance_info.setStyleSheet("""
            #distanceInfo {
                color: #BBBBBB; 
                font-size: 13px;
                line-height: 150%;
            }
        """)
        distance_info.setAlignment(Qt.AlignCenter)
        distance_layout.addWidget(distance_info)
        
        # Scrollable distance matrix area with updated styling - IMPROVED SCROLLING
        distance_scroll = QScrollArea()
        distance_scroll.setObjectName("distanceScroll")
        distance_scroll.setWidgetResizable(True)
        distance_scroll.setStyleSheet("""
            #distanceScroll {
                border: none;
                background-color: transparent;
            }
            QScrollBar {
                border: none;
                background: rgba(51, 51, 51, 0.5);
                width: 8px;
                height: 8px;
                border-radius: 4px;
                margin: 0px;
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
        self.distance_matrix.setSpacing(2)
        
        distance_scroll.setWidget(self.distance_matrix_widget)
        distance_scroll.setMinimumHeight(250)  # Increased minimum height
        distance_scroll.setMaximumHeight(300)  # Increased maximum height
        distance_layout.addWidget(distance_scroll)
        
        container_layout.addWidget(distance_frame)
        
        # Button area with updated styling
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)
        button_layout.setAlignment(Qt.AlignCenter)
        
        back_button = QPushButton("← BACK")
        back_button.setObjectName("backButton")
        back_button.setFixedSize(150, 50)
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
        back_button.clicked.connect(self.go_back)
        button_layout.addWidget(back_button)
        
        self.continue_button = QPushButton("MAKE PREDICTION →")
        self.continue_button.setObjectName("continueButton")
        self.continue_button.setFixedSize(250, 50)
        self.continue_button.setStyleSheet("""
            #continueButton {
                background-color: #f39c12;
                color: white;
                border: none;
                border-radius: 12px;
                padding: 12px 25px;
                font-size: 14px;
                font-weight: bold;
                letter-spacing: 1px;
            }
            #continueButton:hover {
                background-color: #e67e22;
            }
            #continueButton:pressed {
                background-color: #d35400;
            }
            #continueButton:disabled {
                background-color: #555555;
                color: #aaaaaa;
            }
        """)
        self.continue_button.clicked.connect(self.continue_to_prediction)
        self.continue_button.setEnabled(False)  # Disabled initially until enough cities selected
        button_layout.addWidget(self.continue_button)
        
        container_layout.addLayout(button_layout)
        
        # Add container to main layout
        main_layout.addWidget(central_frame, 0, Qt.AlignCenter)
    
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
            
            # Create checkboxes in grid layout - INCREASED COLUMNS
            cols = 4  # Increased from 3 to 4 columns
            for i, city in enumerate(cities):
                row, col = divmod(i, cols)
                
                # Create checkbox with styled card appearance
                checkbox_frame = QFrame()
                checkbox_frame.setObjectName(f"cityCard_{i}")
                checkbox_frame.setMinimumWidth(200)  # Set minimum width for city cards
                
                if city == home_city:
                    # Home city styling - disabled but highlighted
                    checkbox_frame.setStyleSheet(f"""
                        #cityCard_{i} {{
                            background-color: rgba(61, 90, 254, 0.2);
                            border: 1px solid #3D5AFE;
                            border-radius: 10px;
                            padding: 10px;
                        }}
                    """)
                else:
                    # Normal city styling
                    checkbox_frame.setStyleSheet(f"""
                        #cityCard_{i} {{
                            background-color: #2a2a2a;
                            border: 1px solid #444444;
                            border-radius: 10px;
                            padding: 10px;
                        }}
                        #cityCard_{i}:hover {{
                            background-color: #333333;
                            border: 1px solid #555555;
                        }}
                    """)
                
                frame_layout = QVBoxLayout(checkbox_frame)
                frame_layout.setContentsMargins(12, 12, 12, 12)
                frame_layout.setSpacing(8)
                
                # City name and checkbox
                checkbox = QCheckBox(city)
                checkbox.setObjectName(f"cityCheckbox_{i}")
                checkbox.setStyleSheet(f"""
                    #cityCheckbox_{i} {{
                        color: white;
                        font-size: 15px;
                        font-weight: bold;
                    }}
                    #cityCheckbox_{i}::indicator {{
                        width: 20px;
                        height: 20px;
                        border: 1px solid #666666;
                        border-radius: 4px;
                    }}
                    #cityCheckbox_{i}::indicator:checked {{
                        background-color: #3D5AFE;
                        border: 1px solid #2980b9;
                    }}
                """)
                
                # Disable home city checkbox
                if city == home_city:
                    checkbox.setEnabled(False)
                    home_label = QLabel("(Home)")
                    home_label.setStyleSheet("color: #3D5AFE; font-size: 12px; font-style: italic;")
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
            widget = self.distance_matrix.itemAt(i).widget()
            if widget:
                widget.deleteLater()
        
        # Get the distances from the game state
        distances = self.flow_manager.game_state.city_map.get_distances()
        
        # Create header row
        header_cell = QLabel("")
        header_cell.setStyleSheet("""
            background-color: #222222;
            color: white;
            padding: 5px;
            border: 1px solid #333333;
            border-radius: 3px;
        """)
        self.distance_matrix.addWidget(header_cell, 0, 0)
        
        # Set fixed column width for better readability
        for i, city in enumerate(cities):
            header = QLabel(city)
            header.setObjectName(f"colHeader_{i}")
            header.setStyleSheet(f"""
                #colHeader_{i} {{
                    background-color: #3D5AFE;
                    color: white;
                    font-weight: bold;
                    padding: 6px;
                    border: none;
                    border-radius: 4px;
                }}
            """)
            header.setAlignment(Qt.AlignCenter)
            header.setMinimumWidth(70)  # Set minimum width
            self.distance_matrix.addWidget(header, 0, i + 1)
            
            # Create row headers
            row_header = QLabel(city)
            row_header.setObjectName(f"rowHeader_{i}")
            row_header.setStyleSheet(f"""
                #rowHeader_{i} {{
                    background-color: #3D5AFE;
                    color: white;
                    font-weight: bold;
                    padding: 6px;
                    border: none;
                    border-radius: 4px;
                }}
            """)
            row_header.setAlignment(Qt.AlignCenter)
            row_header.setMinimumWidth(70)  # Set minimum width
            self.distance_matrix.addWidget(row_header, i + 1, 0)
        
        # Fill in distances
        for i, city1 in enumerate(cities):
            for j, city2 in enumerate(cities):
                if city1 == city2:
                    cell = QLabel("—")
                    cell.setObjectName(f"distCell_{i}_{j}")
                    cell.setStyleSheet(f"""
                        #distCell_{i}_{j} {{
                            background-color: #222222;
                            color: #555555;
                            padding: 6px;
                            border: 1px solid #333333;
                            border-radius: 2px;
                        }}
                    """)
                else:
                    distance = distances.get((city1, city2)) or distances.get((city2, city1), 0)
                    cell = QLabel(f"{distance:.1f}")
                    cell.setObjectName(f"distCell_{i}_{j}")
                    
                    # Style cells with alternating colors
                    if (i + j) % 2 == 0:
                        cell.setStyleSheet(f"""
                            #distCell_{i}_{j} {{
                                background-color: #1a1a1a;
                                color: white;
                                padding: 6px;
                                border: 1px solid #333333;
                                border-radius: 2px;
                            }}
                        """)
                    else:
                        cell.setStyleSheet(f"""
                            #distCell_{i}_{j} {{
                                background-color: #222222;
                                color: white;
                                padding: 6px;
                                border: 1px solid #333333;
                                border-radius: 2px;
                            }}
                        """)
                
                cell.setAlignment(Qt.AlignCenter)
                cell.setMinimumWidth(70)  # Set minimum width for all cells
                cell.setMinimumHeight(30)  # Set minimum height for all cells
                self.distance_matrix.addWidget(cell, i + 1, j + 1)
        
        # Set column and row stretch factors to ensure even distribution
        for i in range(len(cities) + 1):
            self.distance_matrix.setColumnStretch(i, 1)
            self.distance_matrix.setRowStretch(i, 1)
    
    def update_selection_count(self):
        """Update the selection counter and continue button state"""
        selected_count = len(self.get_selected_cities())
        self.selection_counter.setText(f"{selected_count} cities selected")
        
        # Enable continue button if at least 2 cities (besides home) are selected
        if selected_count >= 2:
            self.continue_button.setEnabled(True)
            self.selection_counter.setStyleSheet("""
                color: white;
                font-size: 14px;
                font-weight: bold;
                padding: 8px 15px;
                background-color: rgba(46, 204, 113, 0.3);
                border: 1px solid #2ecc71;
                border-radius: 10px;
            """)
        else:
            self.continue_button.setEnabled(False)
            self.selection_counter.setStyleSheet("""
                color: white;
                font-size: 14px;
                font-weight: bold;
                padding: 8px 15px;
                background-color: rgba(231, 76, 60, 0.3);
                border: 1px solid #e74c3c;
                border-radius: 10px;
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