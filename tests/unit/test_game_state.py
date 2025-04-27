import unittest
from unittest.mock import MagicMock, patch
from core.game_state import GameState
from core.city_map import CityMap

class TestGameState(unittest.TestCase):
    def setUp(self):
        self.game_state = GameState()
        self.city_map = CityMap()
        
        # Add some test cities to the map
        cities = ["London", "Paris", "Berlin", "Rome", "Madrid"]
        for city in cities:
            self.city_map.add_city(city)
        
        # Add some test distances
        self.city_map.add_distance("London", "Paris", 75)
        self.city_map.add_distance("London", "Berlin", 85)
        self.city_map.add_distance("Paris", "Berlin", 65)
        
        self.game_state.set_city_map(self.city_map)
    
    def test_reset_game(self):
        """Test resetting the game state"""
        # Setup some initial state
        self.game_state.selected_cities = ["London", "Paris", "Berlin"]
        self.game_state.algorithm_results = {"brute_force": {"route": ["A", "B", "A"], "length": 20}}
        self.game_state.shortest_algorithm = "brute_force"
        self.game_state.user_prediction = "dynamic_programming"
        
        # Reset the game
        self.game_state.reset_game()
        
        # Check the state was reset
        self.assertEqual(self.game_state.selected_cities, [])
        self.assertEqual(self.game_state.algorithm_results, {})
        self.assertIsNone(self.game_state.shortest_algorithm)
        self.assertIsNone(self.game_state.user_prediction)
    
    def test_set_city_map(self):
        """Test setting the city map"""
        city_map = CityMap()
        city_map.add_city("Tokyo")
        city_map.add_city("Seoul")
        
        self.game_state.set_city_map(city_map)
        self.assertEqual(self.game_state.city_map, city_map)
    
    def test_set_home_city(self):
        """Test setting the home city"""
        self.game_state.set_home_city("London")
        self.assertEqual(self.game_state.home_city, "London")
        self.assertIn("London", self.game_state.selected_cities)
        
        # Test setting a new home city that's not in selected cities yet
        self.game_state.selected_cities = ["Paris", "Berlin"]
        self.game_state.set_home_city("London")
        self.assertEqual(self.game_state.home_city, "London")
        self.assertIn("London", self.game_state.selected_cities)
    
    def test_add_city(self):
        """Test adding a city"""
        self.game_state.add_city("London")
        self.assertIn("London", self.game_state.selected_cities)
        
        # Adding the same city again should not duplicate it
        self.game_state.add_city("London")
        self.assertEqual(self.game_state.selected_cities.count("London"), 1)
        
        # Add another city
        self.game_state.add_city("Paris")
        self.assertIn("Paris", self.game_state.selected_cities)
    
    def test_remove_city(self):
        """Test removing a city"""
        # Add some cities
        self.game_state.add_city("London")
        self.game_state.add_city("Paris")
        
        # Remove a city
        self.game_state.remove_city("Paris")
        self.assertNotIn("Paris", self.game_state.selected_cities)
        
        # Try to remove a non-existent city (should not error)
        self.game_state.remove_city("Tokyo")
        
        # Set home city and try to remove it (should not allow)
        self.game_state.set_home_city("London")
        self.game_state.remove_city("London")
        self.assertIn("London", self.game_state.selected_cities)
    
    def test_set_player_name(self):
        """Test setting the player name"""
        self.game_state.set_player_name("John Doe")
        self.assertEqual(self.game_state.player_name, "John Doe")
    
    def test_set_user_prediction(self):
        """Test setting the user prediction"""
        self.game_state.set_user_prediction("brute_force")
        self.assertEqual(self.game_state.user_prediction, "brute_force")
    
    def test_get_prediction_result(self):
        """Test checking if the user's prediction was correct"""
        # No prediction made yet
        self.assertFalse(self.game_state.get_prediction_result())
        
        # Make prediction but no algorithm results yet
        self.game_state.set_user_prediction("brute_force")
        self.assertFalse(self.game_state.get_prediction_result())
        
        # Set algorithm results where prediction is correct
        self.game_state.set_algorithm_results({
            "brute_force": {"route": ["A", "B", "A"], "length": 20},
            "nearest_neighbor": {"route": ["A", "B", "A"], "length": 25},
            "dynamic_programming": {"route": ["A", "B", "A"], "length": 20}
        })
        self.assertTrue(self.game_state.get_prediction_result())
        
        # Set algorithm results where prediction is wrong
        self.game_state.set_user_prediction("nearest_neighbor")
        self.assertFalse(self.game_state.get_prediction_result())
    
    def test_set_algorithm_results(self):
        """Test setting the algorithm results"""
        results = {
            "brute_force": {"route": ["A", "B", "A"], "length": 20},
            "nearest_neighbor": {"route": ["A", "B", "A"], "length": 25},
            "dynamic_programming": {"route": ["A", "B", "A"], "length": 20}
        }
        
        self.game_state.set_algorithm_results(results)
        self.assertEqual(self.game_state.algorithm_results, results)
        
        # Both brute_force and dynamic_programming have the same length
        # In case of a tie, the first one in the dictionary is chosen
        self.assertIn(self.game_state.shortest_algorithm, ["brute_force", "dynamic_programming"])
    
    def test_get_available_cities(self):
        """Test getting available cities"""
        available_cities = self.game_state.get_available_cities()
        self.assertEqual(set(available_cities), set(["London", "Paris", "Berlin", "Rome", "Madrid"]))
        
        # Test with no city map
        self.game_state.city_map = None
        self.assertEqual(self.game_state.get_available_cities(), [])
    
    def test_get_distance_between(self):
        """Test getting the distance between cities"""
        distance = self.game_state.get_distance_between("London", "Paris")
        self.assertEqual(distance, 75)
        
        # Test with no city map
        self.game_state.city_map = None
        self.assertEqual(self.game_state.get_distance_between("London", "Paris"), 0)
    
    def test_is_valid_game_state(self):
        """Test checking if the game state is valid to run algorithms"""
        # Not valid initially (no home city and no selected cities)
        self.assertFalse(self.game_state.is_valid_game_state())
        
        # Set home city and add some cities
        self.game_state.set_home_city("London")
        self.game_state.add_city("Paris")
        
        # Now should be valid
        self.assertTrue(self.game_state.is_valid_game_state())
        
        # Reset selected cities
        self.game_state.selected_cities = []
        self.assertFalse(self.game_state.is_valid_game_state())
        
        # Set just the home city
        self.game_state.set_home_city("London")
        self.assertFalse(self.game_state.is_valid_game_state())  # Only one city, need at least two
        
        # Set city map to None
        self.game_state.add_city("Paris")
        self.game_state.city_map = None
        self.assertFalse(self.game_state.is_valid_game_state())

if __name__ == '__main__':
    unittest.main()