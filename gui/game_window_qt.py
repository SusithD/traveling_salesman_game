"""
Main game window for the Traveling Salesman Problem game (PyQt5 Version)
"""
import logging
import traceback
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTabWidget,
    QLabel, QLineEdit, QPushButton, QMessageBox, QMenu, QMenuBar,
    QAction, QDialog, QTextBrowser
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
        """Create the player information section"""
        logger.debug("Creating player info section")
        player_layout = QHBoxLayout()
        
        player_label = QLabel("Player Name:")
        player_layout.addWidget(player_label)
        
        self.player_name_input = QLineEdit("Player")
        player_layout.addWidget(self.player_name_input)
        
        start_button = QPushButton("Start New Game")
        start_button.clicked.connect(self.start_new_game)
        player_layout.addWidget(start_button)
        
        self.home_city_label = QLabel("")
        self.home_city_label.setStyleSheet("color: blue; font-weight: bold;")
        player_layout.addWidget(self.home_city_label)
        
        player_layout.addStretch(1)  # Add stretch to push everything to the left
        
        self.main_layout.addLayout(player_layout)
        
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
        """Show high scores from the database with enhanced statistics and modern design"""
        logger.debug("Viewing high scores")
        high_scores = self.db_manager.get_high_scores()
        
        if not high_scores:
            QMessageBox.information(self, "High Scores", "No high scores yet!")
            return
            
        dialog = QDialog(self)
        dialog.setWindowTitle("High Scores & Statistics")
        dialog.resize(800, 600)
        layout = QVBoxLayout(dialog)
        
        scores_text = QTextBrowser(dialog)
        scores_text.setOpenExternalLinks(False)
        
        # Calculate statistics from high scores
        total_games = len(high_scores)
        algorithms_used = {}
        shortest_route = float('inf')
        longest_route = 0
        best_player = {}
        total_route_length = 0
        cities_frequency = {}
        
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
        
        # Find most popular algorithm
        most_popular_algorithm = max(algorithms_used.items(), key=lambda x: x[1])[0]
        average_route_length = total_route_length / total_games
        
        # CSS for modern styling
        css = """
        <style>
            body { font-family: 'Segoe UI', Arial, sans-serif; margin: 0; padding: 10px; background-color: #f8f9fa; color: #333; }
            h2 { color: #2c3e50; text-align: center; margin-bottom: 5px; }
            h3 { color: #3498db; margin-top: 20px; margin-bottom: 10px; border-bottom: 2px solid #3498db; padding-bottom: 5px; }
            .stats-container { display: flex; flex-wrap: wrap; justify-content: space-between; margin-bottom: 20px; }
            .stat-box { background-color: #fff; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); padding: 12px; width: 48%; margin-bottom: 15px; }
            .stat-title { font-weight: bold; color: #2c3e50; margin-bottom: 5px; }
            .stat-value { font-size: 18px; color: #2980b9; }
            .stat-extra { font-size: 12px; color: #7f8c8d; }
            table { width: 100%; border-collapse: collapse; margin-top: 15px; border-radius: 6px; overflow: hidden; box-shadow: 0 0 20px rgba(0,0,0,0.1); }
            th { background-color: #3498db; color: white; text-align: left; padding: 12px; }
            td { background-color: white; padding: 10px; border-bottom: 1px solid #ddd; }
            tr:hover td { background-color: #f1f9ff; }
            .highlight-row td { background-color: #e8f8f5; font-weight: bold; }
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
                
        # High scores table with enhanced styling
        html_content += "<h3>High Scores</h3>"
        html_content += "<table>"
        html_content += "<tr><th>Player</th><th>Home City</th><th>Cities Visited</th><th>Route Length</th><th>Algorithm</th><th>Time (ms)</th></tr>"
        
        for score in high_scores:
            player, home_city, cities_visited, route_length, algorithm, time = score
            
            # Highlight the row if this is the best score
            if float(route_length) == shortest_route:
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
        html_content += "<h3>Algorithm Usage</h3>"
        html_content += "<div class='stat-box' style='width: 100%'>"
        max_count = max(algorithms_used.values())
        for algo, count in algorithms_used.items():
            percentage = (count / total_games) * 100
            bar_width = (count / max_count) * 100
            html_content += f"<div style='margin-bottom: 10px;'>"
            html_content += f"<div style='display: flex; justify-content: space-between;'>"
            html_content += f"<span>{algo}</span><span>{percentage:.1f}% ({count} games)</span>"
            html_content += f"</div>"
            html_content += f"<div style='background-color: #eee; border-radius: 4px; height: 20px;'>"
            html_content += f"<div style='background-color: #3498db; width: {bar_width}%; height: 100%; border-radius: 4px;'></div>"
            html_content += f"</div>"
            html_content += f"</div>"
        html_content += "</div>"
        
        scores_text.setHtml(html_content)
        layout.addWidget(scores_text)
        
        close_button = QPushButton("Close", dialog)
        close_button.clicked.connect(dialog.close)
        close_button.setStyleSheet("background-color: #3498db; color: white; padding: 8px 16px; border-radius: 4px;")
        layout.addWidget(scores_text)
        
        close_button = QPushButton("Close", dialog)
        close_button.clicked.connect(dialog.close)
        close_button.setStyleSheet("background-color: #3498db; color: white; padding: 8px 16px; border-radius: 4px;")
        layout.addWidget(close_button)
        
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