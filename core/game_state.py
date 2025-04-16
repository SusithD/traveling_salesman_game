"""
Game state management for the Traveling Salesman Problem game
"""

class GameState:
    def __init__(self):
        self.player_name = ""
        self.city_map = None
        self.home_city = None
        self.selected_cities = []
        self.algorithm_results = {}
    
    def set_city_map(self, city_map):
        """Set the city map for the current game"""
        self.city_map = city_map
    
    def reset_game(self):
        """Reset the game state for a new round"""
        self.home_city = None
        self.selected_cities = []
        self.algorithm_results = {}