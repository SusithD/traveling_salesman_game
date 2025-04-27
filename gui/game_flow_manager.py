"""
Game flow manager for the Traveling Salesman Problem game
Manages transitions between screens to create a step-by-step game flow
"""
import logging
import random
from PyQt5.QtWidgets import QStackedWidget, QMessageBox
from PyQt5.QtCore import QObject, pyqtSignal

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
        
        # Initialize stack widget to manage screens
        self.stack = QStackedWidget(parent)
        
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
        """Return the stacked widget containing all screens"""
        return self.stack
    
    def show_welcome_screen(self):
        """Display the welcome screen"""
        logger.info("Showing welcome screen")
        self.stack.setCurrentWidget(self.welcome_screen)
    
    def show_mission_screen(self):
        """Display the mission briefing screen"""
        logger.info("Showing mission screen")
        self.mission_screen.update_display()
        self.stack.setCurrentWidget(self.mission_screen)
    
    def show_city_selection_screen(self):
        """Display the city selection screen"""
        logger.info("Showing city selection screen")
        self.city_selection_screen.update_display()
        self.stack.setCurrentWidget(self.city_selection_screen)
    
    def show_prediction_screen(self):
        """Display the algorithm prediction screen"""
        logger.info("Showing prediction screen")
        self.prediction_screen.update_display()
        self.stack.setCurrentWidget(self.prediction_screen)
    
    def show_calculating_screen(self, user_prediction):
        """Display the calculating animation screen and start calculation"""
        logger.info(f"Showing calculating screen - user predicted: {user_prediction}")
        self.game_state.user_prediction = user_prediction
        self.calculating_screen.update_display()
        self.stack.setCurrentWidget(self.calculating_screen)
        
        # Start the calculation process
        self.calculating_screen.start_calculation()
        
        # Start calculations in background
        self._run_algorithms()
    
    def show_results_screen(self):
        """Display the results screen after calculations complete"""
        logger.info("Showing results screen")
        self.results_screen.setup_results()
        self.stack.setCurrentWidget(self.results_screen)
    
    def show_summary_screen(self):
        """Display the final summary screen"""
        logger.info("Showing summary screen")
        
        # Save the game results to the database
        self._save_game_results()
        
        self.summary_screen.update_display()
        self.stack.setCurrentWidget(self.summary_screen)
    
    def _run_algorithms(self):
        """Run all TSP algorithms and update the game state with results"""
        logger.info("Running TSP algorithms")
        
        selected_cities = self.game_state.selected_cities
        city_map = self.game_state.city_map
        home_city = self.game_state.home_city
        
        if not selected_cities or not city_map or not home_city:
            logger.error("Cannot run algorithms: missing required game state")
            return
        
        try:
            calculator = RouteCalculator(city_map, selected_cities, home_city)
            results = {}
            
            # Run Brute Force algorithm
            route_bf, distance_bf, time_bf = calculator.calculate_brute_force()
            results["Brute Force"] = {
                "route": route_bf,
                "length": distance_bf,
                "time": time_bf,
                "complexity": "O(n!)"
            }
            
            # Run Nearest Neighbor algorithm
            route_nn, distance_nn, time_nn = calculator.calculate_nearest_neighbor()
            results["Nearest Neighbor"] = {
                "route": route_nn,
                "length": distance_nn,
                "time": time_nn,
                "complexity": "O(n²)"
            }
            
            # Run Dynamic Programming algorithm
            route_dp, distance_dp, time_dp = calculator.calculate_dynamic_programming()
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