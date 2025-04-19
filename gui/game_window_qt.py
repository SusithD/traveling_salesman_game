"""
Main game window for the Traveling Salesman Problem game (PyQt5 Version)
"""
import logging
import traceback
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTabWidget,
    QLabel, QLineEdit, QPushButton, QMessageBox, QMenu, QMenuBar,
    QAction, QDialog, QTextBrowser, QScrollArea, QFrame
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

from core.game_state import GameState
from core.city_map import CityMap
from database.db_manager import DatabaseManager
from gui.city_selection_qt import CitySelectionFrameQt
from gui.results_display_qt import ResultsDisplayFrameQt

# Configure logging
logger = logging.getLogger("GameWindow")

class StyledFrame(QFrame):
    """Custom frame with black and white styling for containers"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            background-color: white;
            border: 1px solid black;
            border-radius: 8px;
            padding: 10px;
            margin: 5px;
        """)
        self.setFrameShape(QFrame.StyledPanel)

class GameWindowQt(QMainWindow):
    def __init__(self):
        logger.info("Initializing GameWindowQt")
        try:
            super().__init__()
            
            # Set up the main window
            self.setWindowTitle("Traveling Salesman Problem Game")
            self.resize(1000, 700)
            
            self.db_manager = DatabaseManager()
            self.game_state = GameState()
            self.city_map = CityMap()
            
            # Initialize the city map with cities and distances
            logger.debug("Generating cities and distances")
            self.city_map.generate_cities_and_distances()
            
            logger.debug("Setting city map in game state")
            self.game_state.set_city_map(self.city_map)
            
            logger.debug("Selecting home city")
            self.game_state.home_city = self.city_map.select_random_home_city()
            logger.info(f"Home city selected: {self.game_state.home_city}")
            
            # Create the menu
            self.create_menu()
            
            # Set up the central widget and layout
            self.central_widget = QWidget()
            self.setCentralWidget(self.central_widget)
            self.main_layout = QVBoxLayout(self.central_widget)
            
            # Player info section
            self.create_player_info_section()
            
            # Create frames
            self.create_frames()
            
            # Initialize game display
            self.initialize_game_display()
            
            logger.info("GameWindowQt initialization complete")
        except Exception as e:
            logger.error(f"Error in GameWindowQt initialization: {str(e)}")
            logger.error(traceback.format_exc())
            QMessageBox.critical(None, "Initialization Error", f"An error occurred during initialization: {str(e)}")
            raise

    def create_menu(self):
        """Create the main menu"""
        logger.debug("Creating menu")
        menubar = self.menuBar()
        
        # Game menu
        game_menu = menubar.addMenu("Game")
        
        new_game_action = QAction("New Game", self)
        new_game_action.triggered.connect(self.start_new_game)
        game_menu.addAction(new_game_action)
        
        high_scores_action = QAction("View High Scores", self)
        high_scores_action.triggered.connect(self.view_high_scores)
        game_menu.addAction(high_scores_action)
        
        game_menu.addSeparator()
        
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        game_menu.addAction(exit_action)
        
        # Help menu
        help_menu = menubar.addMenu("Help")
        
        rules_action = QAction("Rules", self)
        rules_action.triggered.connect(self.show_rules)
        help_menu.addAction(rules_action)
        
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def create_player_info_section(self):
        """Create the player information section with black and white styling"""
        logger.debug("Creating player info section")
        
        # Create a styled container for player info
        player_container = StyledFrame()
        player_layout = QHBoxLayout(player_container)
        player_layout.setContentsMargins(15, 15, 15, 15)
        player_layout.setSpacing(15)
        
        # Player name section with styled label
        player_label = QLabel("Player:")
        player_label.setStyleSheet("font-weight: bold; color: black;")
        player_layout.addWidget(player_label)
        
        self.player_name_input = QLineEdit("Player")
        self.player_name_input.setMinimumWidth(150)
        self.player_name_input.setStyleSheet("""
            border: 1px solid black;
            border-radius: 4px;
            padding: 5px;
        """)
        player_layout.addWidget(self.player_name_input)
        
        # Home city display with black and white styling
        home_city_container = QFrame()
        home_city_container.setStyleSheet("""
            background-color: white;
            border: 1px solid black;
            border-radius: 4px;
            padding: 5px 10px;
        """)
        home_city_layout = QHBoxLayout(home_city_container)
        home_city_layout.setContentsMargins(8, 5, 8, 5)
        
        home_icon_label = QLabel("🏠")  # Unicode home emoji
        home_icon_label.setStyleSheet("font-size: 16px; color: black;")
        home_city_layout.addWidget(home_icon_label)
        
        self.home_city_label = QLabel("")
        self.home_city_label.setStyleSheet("""
            color: black; 
            font-weight: bold; 
            font-size: 14px;
        """)
        home_city_layout.addWidget(self.home_city_label)
        
        player_layout.addWidget(home_city_container)
        
        player_layout.addStretch(1)  # Push everything to the left
        
        # High Scores button with black and white styling
        high_scores_button = QPushButton("High Scores")
        high_scores_button.setStyleSheet("""
            QPushButton {
                background-color: black;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 10px 15px;
                font-weight: bold;
                margin-right: 10px;
            }
            QPushButton:hover {
                background-color: #444;
            }
            QPushButton:pressed {
                background-color: #777;
            }
        """)
        high_scores_button.clicked.connect(self.view_high_scores)
        player_layout.addWidget(high_scores_button)
        
        # Start button with black and white styling
        start_button = QPushButton("Start New Game")
        start_button.setStyleSheet("""
            QPushButton {
                background-color: black;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 10px 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #444;
            }
            QPushButton:pressed {
                background-color: #777;
            }
        """)
        start_button.clicked.connect(self.start_new_game)
        player_layout.addWidget(start_button)
        
        # Add the container to the main layout
        self.main_layout.addWidget(player_container)
        
        # Update the game state with the default player name
        self.game_state.player_name = self.player_name_input.text()

    def create_frames(self):
        """Create the main frames for the application"""
        logger.debug("Creating frames")
        
        # Create the city selection frame
        self.city_selection = CitySelectionFrameQt(self.game_state)
        self.main_layout.addWidget(self.city_selection)
        
        # Create the results display frame
        self.results_display = ResultsDisplayFrameQt(self.game_state, self.db_manager)
        self.main_layout.addWidget(self.results_display)

    def start_new_game(self):
        """Start a new game round"""
        logger.debug("Starting new game")
        player_name = self.player_name_input.text().strip()
        
        if not player_name:
            QMessageBox.critical(self, "Error", "Please enter your name first!")
            return
        
        self.game_state.player_name = player_name
        self.city_map.generate_cities_and_distances()
        self.game_state.set_city_map(self.city_map)
        self.game_state.home_city = self.city_map.select_random_home_city()
        
        self.city_selection.update_cities_display()
        self.results_display.clear_results()
        
        self.home_city_label.setText(f"Home city: {self.game_state.home_city}")
        
        QMessageBox.information(self, "New Game", f"A new game has started!\nYour home city is {self.game_state.home_city}")

    def view_high_scores(self):
        """Show high scores from the database with enhanced statistics in black background with white text"""
        logger.debug("Viewing high scores")
        high_scores = self.db_manager.get_high_scores()
        
        if not high_scores:
            QMessageBox.information(self, "High Scores", "No high scores yet!")
            return
            
        dialog = QDialog(self)
        dialog.setWindowTitle("High Scores & Statistics")
        dialog.resize(800, 600)
        dialog.setStyleSheet("background-color: black; color: white;")
        layout = QVBoxLayout(dialog)
        
        # Add a title with bold styling
        title_label = QLabel("High Scores & Statistics")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; color: white;")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        scores_text = QTextBrowser(dialog)
        scores_text.setOpenExternalLinks(False)
        scores_text.setStyleSheet("""
            background-color: black;
            color: white;
            border: 1px solid #444;
        """)
        
        # Calculate statistics from high scores
        total_games = len(high_scores)
        algorithms_used = {}
        shortest_route = float('inf')
        longest_route = 0
        best_player = {}
        total_route_length = 0
        cities_frequency = {}
        algorithm_avg_lengths = {"Brute Force": [], "Nearest Neighbor": [], "Dynamic Programming": []}
        
        for score in high_scores:
            player, home_city, cities_visited, route_length, algorithm, time = score
            
            # Convert to appropriate types
            cities_visited = int(cities_visited)
            route_length = float(route_length)
            time = float(time)
            
            # Algorithm statistics
            if algorithm not in algorithms_used:
                algorithms_used[algorithm] = 0
            algorithms_used[algorithm] += 1
            
            # Track algorithm performance
            if algorithm in algorithm_avg_lengths:
                algorithm_avg_lengths[algorithm].append(route_length)
            
            # Route length statistics
            if route_length < shortest_route:
                shortest_route = route_length
                best_player = {'name': player, 'route': route_length, 'cities': cities_visited, 'algorithm': algorithm}
            
            if route_length > longest_route:
                longest_route = route_length
            
            total_route_length += route_length
            
            # Track city popularity
            if home_city not in cities_frequency:
                cities_frequency[home_city] = 0
            cities_frequency[home_city] += 1
        
        # Calculate algorithm averages
        algorithm_averages = {}
        for algo, lengths in algorithm_avg_lengths.items():
            if lengths:
                algorithm_averages[algo] = sum(lengths) / len(lengths)
        
        # Find most popular algorithm
        most_popular_algorithm = max(algorithms_used.items(), key=lambda x: x[1])[0]
        average_route_length = total_route_length / total_games
        
        # CSS for black background and white text styling
        css = """
        <style>
            body { 
                font-family: 'Segoe UI', Arial, sans-serif; 
                margin: 0; 
                padding: 10px; 
                background-color: black; 
                color: white; 
            }
            h2 { 
                color: white; 
                text-align: center; 
                margin-bottom: 5px; 
                font-size: 22px;
            }
            h3 { 
                color: white; 
                margin-top: 20px; 
                margin-bottom: 10px; 
                border-bottom: 2px solid white; 
                padding-bottom: 5px; 
                font-size: 18px;
            }
            .stats-container { 
                display: flex; 
                flex-wrap: wrap; 
                justify-content: space-between; 
                margin-bottom: 20px; 
            }
            .stat-box { 
                background-color: #222; 
                border-radius: 8px; 
                border: 1px solid #444; 
                padding: 12px; 
                width: 48%; 
                margin-bottom: 15px; 
            }
            .stat-title { 
                font-weight: bold; 
                color: white; 
                margin-bottom: 5px; 
            }
            .stat-value { 
                font-size: 18px; 
                color: white; 
            }
            .stat-extra { 
                font-size: 12px; 
                color: #ccc; 
            }
            table { 
                width: 100%; 
                border-collapse: collapse; 
                margin-top: 15px; 
                border: 1px solid #444;
            }
            th { 
                background-color: #333; 
                color: white; 
                text-align: left; 
                padding: 12px; 
                border: 1px solid #444;
            }
            td { 
                background-color: #111; 
                color: white;
                padding: 10px; 
                border-bottom: 1px solid #333; 
                border: 1px solid #333;
            }
            tr:nth-child(even) td { 
                background-color: #222; 
            }
            tr:hover td { 
                background-color: #333; 
            }
            .highlight-row td { 
                background-color: #444; 
                font-weight: bold; 
            }
            .bar-background { 
                background-color: #333; 
                border-radius: 4px; 
                height: 20px; 
            }
            .bar-fill { 
                background-color: white; 
                height: 100%; 
                border-radius: 4px; 
            }
            .stats-grid { 
                display: grid; 
                grid-template-columns: repeat(2, 1fr); 
                gap: 20px; 
                margin-top: 20px; 
            }
            .chart-container { 
                border: 1px solid #444; 
                border-radius: 8px; 
                padding: 15px; 
                margin-bottom: 20px; 
                background-color: #222;
            }
            .chart-title { 
                font-weight: bold; 
                margin-bottom: 10px; 
                color: white;
            }
            .performance-box { 
                border: 1px solid #444; 
                padding: 10px; 
                margin-top: 15px; 
                background-color: #222;
            }
            .performance-title { 
                font-weight: bold; 
                border-bottom: 1px solid #444; 
                padding-bottom: 5px; 
                margin-bottom: 10px; 
                color: white;
            }
            p, span, div {
                color: white;
            }
        </style>
        """
        
        # Start building content with enhanced statistics
        html_content = css + "<h2>TSP Game Statistics</h2>"
        
        # Statistics boxes
        html_content += "<div class='stats-container'>"
        
        # Best player box
        html_content += "<div class='stat-box'>"
        html_content += "<div class='stat-title'>Best Player</div>"
        html_content += f"<div class='stat-value'>{best_player['name']}</div>"
        html_content += f"<div class='stat-extra'>Route: {best_player['route']:.2f} km with {best_player['cities']} cities using {best_player['algorithm']}</div>"
        html_content += "</div>"
        
        # Total games box
        html_content += "<div class='stat-box'>"
        html_content += "<div class='stat-title'>Total Games Played</div>"
        html_content += f"<div class='stat-value'>{total_games}</div>"
        html_content += "</div>"
        
        # Best algorithm box
        html_content += "<div class='stat-box'>"
        html_content += "<div class='stat-title'>Most Popular Algorithm</div>"
        html_content += f"<div class='stat-value'>{most_popular_algorithm}</div>"
        html_content += f"<div class='stat-extra'>Used {algorithms_used[most_popular_algorithm]} times</div>"
        html_content += "</div>"
        
        # Route statistics box
        html_content += "<div class='stat-box'>"
        html_content += "<div class='stat-title'>Route Statistics</div>"
        html_content += f"<div class='stat-value'>{average_route_length:.2f} km</div>"
        html_content += f"<div class='stat-extra'>Average route length (Shortest: {shortest_route:.2f} km, Longest: {longest_route:.2f} km)</div>"
        html_content += "</div>"
        html_content += "</div>"  # End stats-container
        
        # Algorithm Performance Comparison
        html_content += "<div class='chart-container'>"
        html_content += "<div class='chart-title'>Algorithm Performance Comparison</div>"
        
        for algo, avg in sorted(algorithm_averages.items(), key=lambda x: x[1]):
            if algorithm_averages:
                # Calculate percentage relative to best algorithm
                min_avg = min(algorithm_averages.values())
                percentage = (avg / min_avg) * 100 - 100  # How much worse than the best
                
                html_content += f"<div style='margin-bottom: 15px;'>"
                html_content += f"<div style='display: flex; justify-content: space-between;'>"
                html_content += f"<span>{algo}</span><span>Avg: {avg:.2f} km</span>"
                html_content += f"</div>"
                
                # Bar representation of relative performance (shorter is better)
                bar_width = max(5, min(100, percentage * 2))  # Scale for visual purposes
                html_content += f"<div class='bar-background'>"
                html_content += f"<div class='bar-fill' style='width: {bar_width}%;'></div>"
                html_content += f"</div>"
                
                if percentage == 0:
                    html_content += f"<div style='font-size: 12px; text-align: right; color: #ccc;'>Best performing algorithm</div>"
                else:
                    html_content += f"<div style='font-size: 12px; text-align: right; color: #ccc;'>{percentage:.1f}% longer routes than best algorithm</div>"
                
                html_content += f"</div>"
        
        html_content += "</div>"
                
        # High scores table with enhanced styling
        html_content += "<h3>High Scores Leaderboard</h3>"
        html_content += "<table>"
        html_content += "<tr><th>Player</th><th>Home City</th><th>Cities</th><th>Route Length</th><th>Algorithm</th><th>Time (ms)</th></tr>"
        
        # Sort high scores by route length (ascending)
        sorted_scores = sorted(high_scores, key=lambda x: float(x[3]))
        
        for i, score in enumerate(sorted_scores):
            player, home_city, cities_visited, route_length, algorithm, time = score
            
            # Highlight the top 3 scores
            if i < 3:
                html_content += "<tr class='highlight-row'>"
            else:
                html_content += "<tr>"
                
            for item in score:
                # Format numbers to 2 decimal places if they're route length or time
                if isinstance(item, (int, float)) or (isinstance(item, str) and item.replace('.', '', 1).isdigit()):
                    try:
                        value = float(item)
                        if value == int(value):
                            html_content += f"<td>{int(value)}</td>"
                        else:
                            html_content += f"<td>{value:.2f}</td>"
                    except ValueError:
                        html_content += f"<td>{item}</td>"
                else:
                    html_content += f"<td>{item}</td>"
            html_content += "</tr>"
            
        html_content += "</table>"
        
        # Algorithm usage chart
        html_content += "<h3>Algorithm Usage Distribution</h3>"
        html_content += "<div class='chart-container'>"
        for algo, count in algorithms_used.items():
            percentage = (count / total_games) * 100
            bar_width = percentage  # Direct percentage as width
            html_content += f"<div style='margin-bottom: 15px;'>"
            html_content += f"<div style='display: flex; justify-content: space-between;'>"
            html_content += f"<span><b>{algo}</b></span><span>{percentage:.1f}% ({count} games)</span>"
            html_content += f"</div>"
            html_content += f"<div class='bar-background'>"
            html_content += f"<div class='bar-fill' style='width: {bar_width}%;'></div>"
            html_content += f"</div>"
            html_content += f"</div>"
        html_content += "</div>"
        
        # Cities frequency if there are interesting patterns
        if cities_frequency and len(cities_frequency) > 1:
            html_content += "<h3>Most Frequent Home Cities</h3>"
            html_content += "<div class='chart-container'>"
            
            # Get the top 5 cities
            top_cities = sorted(cities_frequency.items(), key=lambda x: x[1], reverse=True)[:5]
            max_freq = max(cities_frequency.values()) if cities_frequency else 1
            
            for city, freq in top_cities:
                percentage = (freq / total_games) * 100
                bar_width = (freq / max_freq) * 100  # Relative to max frequency
                
                html_content += f"<div style='margin-bottom: 15px;'>"
                html_content += f"<div style='display: flex; justify-content: space-between;'>"
                html_content += f"<span>{city}</span><span>{percentage:.1f}% ({freq} games)</span>"
                html_content += f"</div>"
                html_content += f"<div class='bar-background'>"
                html_content += f"<div class='bar-fill' style='width: {bar_width}%;'></div>"
                html_content += f"</div>"
                html_content += f"</div>"
            
            html_content += "</div>"
        
        scores_text.setHtml(html_content)
        layout.addWidget(scores_text)
        
        # Button layout at the bottom
        button_layout = QHBoxLayout()
        
        close_button = QPushButton("Close", dialog)
        close_button.clicked.connect(dialog.close)
        close_button.setStyleSheet("background-color: white; color: black; padding: 8px 16px; border-radius: 4px; font-weight: bold;")
        button_layout.addWidget(close_button)
        
        layout.addLayout(button_layout)
        
        dialog.exec_()

    def show_rules(self):
        """Display game rules"""
        logger.debug("Showing rules")
        rules = """
        <h3>Traveling Salesman Problem Game Rules:</h3>
        
        <ol>
            <li>You will be assigned a random home city.</li>
            <li>Select cities you wish to visit by checking the boxes.</li>
            <li>Try to find the shortest route that visits all selected cities and returns home.</li>
            <li>The game will calculate the shortest route using three different algorithms.</li>
            <li>Your score is saved when you correctly identify the shortest route.</li>
        </ol>
        
        <p>Good luck!</p>
        """
        
        QMessageBox.information(self, "Game Rules", rules)

    def show_about(self):
        """Show about information"""
        logger.debug("Showing about information")
        about_text = """
        <h3>Traveling Salesman Problem Game</h3>
        
        <p>A simulation game to learn about route optimization algorithms.</p>
        
        <p>The Traveling Salesman Problem is a classic algorithmic problem in computer science.
        It asks the question: "Given a list of cities and the distances between each pair of cities, 
        what is the shortest possible route that visits each city exactly once and returns to the origin city?"</p>
        """
        
        QMessageBox.information(self, "About", about_text)

    def initialize_game_display(self):
        """Initialize the game display with cities and the distance matrix"""
        logger.debug("Initializing game display")
        # Update the city selection display
        self.city_selection.update_cities_display()
        
        # Clear any previous results in the results display
        self.results_display.clear_results()
        
        # Display the home city
        self.home_city_label.setText(f"Home city: {self.game_state.home_city}")