"""
Game flow manager for the Traveling Salesman Problem game
Manages transitions between screens to create a step-by-step game flow
"""
import logging
import random
from PyQt5.QtWidgets import QStackedWidget, QMessageBox, QVBoxLayout, QWidget, QSizePolicy
from PyQt5.QtCore import QObject, pyqtSignal, Qt

from core.game_state import GameState
from core.city_map import CityMap
from core.route_calculator import RouteCalculator
from database.db_manager import DatabaseManager

from gui.screens.welcome_screen import WelcomeScreen
from gui.screens.mission_screen import MissionScreen
from gui.screens.city_selection_screen import CitySelectionScreen
from gui.screens.prediction_screen import PredictionScreen
from gui.screens.calculating_screen import CalculatingScreen
from gui.screens.results_screen import ResultsScreen
from gui.screens.summary_screen import SummaryScreen

logger = logging.getLogger("GameFlowManager")

class GameFlowManager(QObject):
    """
    Manager for the game flow, coordinating transitions between screens
    """
    # Signal for when calculations are complete
    calculations_complete = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Initialize main container widget
        self.main_container = QWidget(parent)
        self.main_container.setObjectName("gameFlowContainer")
        
        # Configure main layout
        self.main_layout = QVBoxLayout(self.main_container)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        self.main_layout.setAlignment(Qt.AlignCenter)
        
        # Initialize stack widget to manage screens
        self.stack = QStackedWidget()
        self.stack.setObjectName("screenStack")
        # Make sure the stacked widget expands to fill available space
        self.stack.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        # Add stack to main layout
        self.main_layout.addWidget(self.stack)
        
        # Initialize game state and database
        self.game_state = GameState()
        self.db_manager = DatabaseManager()
        
        # Initialize screens
        self.welcome_screen = WelcomeScreen(self)
        self.mission_screen = MissionScreen(self)
        self.city_selection_screen = CitySelectionScreen(self)
        self.prediction_screen = PredictionScreen(self)
        self.calculating_screen = CalculatingScreen(self)
        self.results_screen = ResultsScreen(self)
        self.summary_screen = SummaryScreen(self)
        
        # Add screens to stack
        self.stack.addWidget(self.welcome_screen)
        self.stack.addWidget(self.mission_screen)
        self.stack.addWidget(self.city_selection_screen)
        self.stack.addWidget(self.prediction_screen)
        self.stack.addWidget(self.calculating_screen)
        self.stack.addWidget(self.results_screen)
        self.stack.addWidget(self.summary_screen)
        
        # Connect signals
        self.calculations_complete.connect(self.show_results_screen)
        
        # Initialize city map
        self._initialize_city_map()
        
        # Start with welcome screen
        self.show_welcome_screen()
    
    def _initialize_city_map(self):
        """Initialize a default city map"""
        city_map = CityMap()
        
        # Add cities and distances
        cities = [
            "New York", "Los Angeles", "Chicago", "Miami", "Dallas", 
            "Seattle", "Boston", "Denver", "Atlanta", "Phoenix"
        ]
        
        for city in cities:
            city_map.add_city(city)
        
        # Create random distances between cities (for simplicity)
        for i, city1 in enumerate(cities):
            for j, city2 in enumerate(cities):
                if i < j:  # Only need one direction, the matrix is symmetric
                    distance = random.uniform(200, 2000)  # Random distance between 200-2000 km
                    city_map.add_distance(city1, city2, distance)
        
        self.game_state.set_city_map(city_map)
        
        # Set a random home city
        self.game_state.home_city = random.choice(cities)
    
    def reset_game(self):
        """Reset the game for a new round"""
        self.game_state.reset_game()
        self._initialize_city_map()
    
    def get_widget(self):
        """Return the main container widget containing all screens"""
        return self.main_container
    
    def _scroll_to_top(self):
        """Helper method to scroll to the top of the screen when switching screens"""
        # Find parent scroll area
        parent = self.main_container.parent()
        while parent and not parent.objectName() == "mainScrollArea":
            parent = parent.parent()
            
        # If found, scroll to top
        if parent and parent.objectName() == "mainScrollArea":
            parent.verticalScrollBar().setValue(0)
    
    def show_welcome_screen(self):
        """Display the welcome screen"""
        logger.info("Showing welcome screen")
        self._scroll_to_top()
        self.stack.setCurrentWidget(self.welcome_screen)
    
    def show_mission_screen(self):
        """Display the mission briefing screen"""
        logger.info("Showing mission screen")
        self.mission_screen.update_display()
        self._scroll_to_top()
        self.stack.setCurrentWidget(self.mission_screen)
    
    def show_city_selection_screen(self):
        """Display the city selection screen"""
        logger.info("Showing city selection screen")
        self.city_selection_screen.update_display()
        self._scroll_to_top()
        self.stack.setCurrentWidget(self.city_selection_screen)
    
    def is_valid_for_prediction_screen(self):
        """Check if conditions are met to show the prediction screen"""
        if not self.game_state.selected_cities or len(self.game_state.selected_cities) < 3:
            logger.error("Insufficient cities selected")
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.warning(
                self.stack.currentWidget(),
                "Insufficient Cities",
                "You must select at least 2 cities to visit besides your home city!",
                QMessageBox.Ok
            )
            return False
        
        if not self.game_state.home_city:
            logger.error("No home city set")
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.warning(
                self.stack.currentWidget(),
                "Home City Required",
                "A home city must be set before continuing!",
                QMessageBox.Ok
            )
            return False
            
        # Ensure home city is in the selected cities
        if self.game_state.home_city not in self.game_state.selected_cities:
            self.game_state.selected_cities.append(self.game_state.home_city)
            
        return True

    def show_prediction_screen(self):
        """Display the algorithm prediction screen if validation passes"""
        logger.info("Validating for prediction screen")
        if not self.is_valid_for_prediction_screen():
            return
            
        logger.info("Showing prediction screen")
        self.prediction_screen.update_display()
        self._scroll_to_top()
        self.stack.setCurrentWidget(self.prediction_screen)
    
    def is_valid_for_calculating_screen(self):
        """Check if conditions are met to show the calculating screen"""
        if not self.is_valid_for_prediction_screen():
            return False
            
        if not self.game_state.user_prediction:
            logger.error("No algorithm prediction made")
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.warning(
                self.stack.currentWidget(),
                "Prediction Required",
                "Please select an algorithm prediction before continuing!",
                QMessageBox.Ok
            )
            return False
            
        return True
    
    def show_calculating_screen(self, user_prediction):
        """Display the calculating animation screen and start calculation if validation passes"""
        logger.info(f"Validating for calculating screen - user predicted: {user_prediction}")
        if not self.is_valid_for_calculating_screen():
            return
            
        logger.info(f"Showing calculating screen - user predicted: {user_prediction}")
        self.game_state.user_prediction = user_prediction
        self.calculating_screen.update_display()
        self._scroll_to_top()
        self.stack.setCurrentWidget(self.calculating_screen)
        
        # Start the calculation process
        self.calculating_screen.start_calculation()
        
        # Start calculations in background
        self._run_algorithms()
    
    def is_valid_for_results_screen(self):
        """Check if conditions are met to show the results screen"""
        if not self.game_state.algorithm_results:
            logger.error("No algorithm results available")
            return False
            
        return True

    def show_results_screen(self):
        """Display the results screen after calculations complete if validation passes"""
        logger.info("Validating for results screen")
        if not self.is_valid_for_results_screen():
            logger.error("Cannot show results - validation failed")
            return
            
        logger.info("Showing results screen")
        self.results_screen.setup_results()
        self._scroll_to_top()
        self.stack.setCurrentWidget(self.results_screen)
    
    def show_summary_screen(self):
        """Display the final summary screen"""
        logger.info("Showing summary screen")
        
        # Save the game results to the database
        self._save_game_results()
        
        self.summary_screen.update_display()
        self._scroll_to_top()
        self.stack.setCurrentWidget(self.summary_screen)
    
    def _run_algorithms(self):
        """Run all TSP algorithms and update the game state with results"""
        logger.info("Running TSP algorithms")
        
        selected_cities = self.game_state.selected_cities
        city_map = self.game_state.city_map
        home_city = self.game_state.home_city
        distances = city_map.get_distances()
        
        if not selected_cities or not city_map or not home_city:
            logger.error("Cannot run algorithms: missing required game state")
            return
        
        try:
            calculator = RouteCalculator()
            results = {}
            
            # Run Brute Force algorithm
            from utils.timer import Timer
            timer = Timer()
            
            # Run Brute Force algorithm
            timer.start()
            route_bf, distance_bf = calculator.brute_force(selected_cities, distances, home_city)
            time_bf = timer.stop()
            results["Brute Force"] = {
                "route": route_bf,
                "length": distance_bf,
                "time": time_bf,
                "complexity": "O(n!)"
            }
            
            # Run Nearest Neighbor algorithm
            timer.start()
            route_nn, distance_nn = calculator.nearest_neighbor(selected_cities, distances, home_city)
            time_nn = timer.stop()
            results["Nearest Neighbor"] = {
                "route": route_nn,
                "length": distance_nn,
                "time": time_nn,
                "complexity": "O(n²)"
            }
            
            # Run Dynamic Programming algorithm
            timer.start()
            route_dp, distance_dp = calculator.dynamic_programming(selected_cities, distances, home_city)
            time_dp = timer.stop()
            results["Dynamic Programming"] = {
                "route": route_dp,
                "length": distance_dp,
                "time": time_dp,
                "complexity": "O(n²2ⁿ)"
            }
            
            # Find the shortest route
            shortest_algorithm = min(results, key=lambda algorithm: results[algorithm]["length"])
            
            # Update game state with results
            self.game_state.algorithm_results = results
            self.game_state.shortest_algorithm = shortest_algorithm
            
            # Emit signal that calculations are complete
            self.calculations_complete.emit()
            
        except Exception as e:
            logger.error(f"Error running algorithms: {str(e)}")
            QMessageBox.critical(
                self.stack, 
                "Algorithm Error",
                f"An error occurred while running the algorithms: {str(e)}"
            )
    
    def _save_game_results(self):
        """Save the game results to the database"""
        if not self.game_state.algorithm_results:
            return
            
        player_name = self.game_state.player_name
        home_city = self.game_state.home_city
        cities_visited = len(self.game_state.selected_cities)
        shortest_algorithm = self.game_state.shortest_algorithm
        
        if shortest_algorithm:
            result = self.game_state.algorithm_results[shortest_algorithm]
            route = result["route"]
            route_length = result["length"]
            execution_time = result["time"]
            
            try:
                self.db_manager.save_game_result(
                    player_name=player_name,
                    home_city=home_city,
                    cities_visited=cities_visited,
                    route=route,
                    route_length=route_length,
                    algorithm=shortest_algorithm,
                    execution_time=execution_time
                )
                logger.info(f"Game results saved for {player_name}")
            except Exception as e:
                logger.error(f"Error saving game results: {str(e)}")