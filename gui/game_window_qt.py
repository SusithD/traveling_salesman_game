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
        """Show high scores from the database"""
        logger.debug("Viewing high scores")
        high_scores = self.db_manager.get_high_scores()
        
        if not high_scores:
            QMessageBox.information(self, "High Scores", "No high scores yet!")
            return
            
        dialog = QDialog(self)
        dialog.setWindowTitle("High Scores")
        dialog.resize(600, 400)
        layout = QVBoxLayout(dialog)
        
        scores_text = QTextBrowser(dialog)
        scores_text.setOpenExternalLinks(False)
        
        # Format the high scores as HTML
        html_content = "<h2>High Scores</h2><table border='1' cellspacing='0' cellpadding='5'>"
        html_content += "<tr><th>Player</th><th>Home City</th><th>Cities Visited</th><th>Route Length</th><th>Algorithm</th><th>Time (ms)</th></tr>"
        
        for score in high_scores:
            html_content += "<tr>"
            for item in score:
                html_content += f"<td>{item}</td>"
            html_content += "</tr>"
            
        html_content += "</table>"
        scores_text.setHtml(html_content)
        
        layout.addWidget(scores_text)
        
        close_button = QPushButton("Close", dialog)
        close_button.clicked.connect(dialog.close)
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