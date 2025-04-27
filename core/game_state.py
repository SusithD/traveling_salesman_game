"""
Game state manager for the Traveling Salesman Problem game
"""
import logging
from typing import Dict, List, Any

class GameState:
    """
    Maintains the current state of the game including cities, routes, and results
    """
    
    def __init__(self):
        self.city_map = None
        self.selected_cities = []
        self.home_city = None
        self.algorithm_results = {}
        self.shortest_algorithm = None
        self.user_prediction = None
        self.player_name = None
        
        # Setup logging
        self.logger = logging.getLogger("GameState")
    
    def reset_game(self):
        """Reset the game state for a new game"""
        self.selected_cities = []
        self.algorithm_results = {}
        self.shortest_algorithm = None
        self.user_prediction = None
        self.logger.info("Game state reset")
    
    def set_city_map(self, city_map):
        """Set the city map for the current game"""
        self.city_map = city_map
        self.logger.info(f"City map set with {len(city_map.get_cities())} cities")
    
    def set_home_city(self, home_city):
        """Set the home city for the current route"""
        self.home_city = home_city
        self.logger.info(f"Home city set to {home_city}")
        
        # Ensure home city is in the selected cities
        if home_city not in self.selected_cities:
            self.selected_cities.append(home_city)
    
    def add_city(self, city):
        """Add a city to the selected cities"""
        if city not in self.selected_cities:
            self.selected_cities.append(city)
            self.logger.info(f"Added city: {city}")
    
    def remove_city(self, city):
        """Remove a city from the selected cities"""
        if city in self.selected_cities and city != self.home_city:
            self.selected_cities.remove(city)
            self.logger.info(f"Removed city: {city}")
        elif city == self.home_city:
            self.logger.warning(f"Cannot remove home city: {city}")
    
    def set_player_name(self, name):
        """Set the player's name"""
        self.player_name = name
        self.logger.info(f"Player name set to: {name}")
    
    def set_user_prediction(self, algorithm_name):
        """Set the user's prediction for which algorithm will perform best"""
        self.user_prediction = algorithm_name
        self.logger.info(f"User prediction set to: {algorithm_name}")
    
    def get_prediction_result(self):
        """Check if the user's prediction was correct"""
        if not self.user_prediction or not self.shortest_algorithm:
            return False
        return self.user_prediction == self.shortest_algorithm
    
    def set_algorithm_results(self, results):
        """Set the algorithm results and determine the shortest path"""
        self.algorithm_results = results
        
        # Find the algorithm with the shortest path
        if results:
            self.shortest_algorithm = min(results, key=lambda algorithm: results[algorithm]["length"])
            self.logger.info(f"Algorithm results set. Shortest path found by: {self.shortest_algorithm}")
    
    def get_available_cities(self):
        """Get list of cities that can be selected"""
        if not self.city_map:
            return []
        return self.city_map.get_cities()
    
    def get_distance_between(self, city1, city2):
        """Get the distance between two cities"""
        if not self.city_map:
            return 0
        return self.city_map.get_distance(city1, city2)
    
    def is_valid_game_state(self):
        """Check if the current game state is valid to run algorithms"""
        if not self.city_map:
            self.logger.error("No city map has been set")
            return False
        
        if not self.selected_cities or len(self.selected_cities) < 2:
            self.logger.error("Insufficient cities selected")
            return False
        
        if not self.home_city:
            self.logger.error("No home city has been set")
            return False
        
        return True