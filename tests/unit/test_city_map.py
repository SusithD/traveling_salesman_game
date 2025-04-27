import unittest
from core.city_map import CityMap

class TestCityMap(unittest.TestCase):
    def setUp(self):
        self.city_map = CityMap()
        
    def test_add_city(self):
        """Test adding cities to the map"""
        # Add a city
        result = self.city_map.add_city("London")
        self.assertTrue(result)
        self.assertIn("London", self.city_map.get_cities())
        
        # Add the same city again (should return False)
        result = self.city_map.add_city("London")
        self.assertFalse(result)
        self.assertEqual(self.city_map.get_cities().count("London"), 1)
        
        # Add another city
        result = self.city_map.add_city("Paris")
        self.assertTrue(result)
        self.assertIn("Paris", self.city_map.get_cities())
        
        # Verify position was generated
        self.assertIn("London", self.city_map.get_city_positions())
        self.assertIn("Paris", self.city_map.get_city_positions())
        
    def test_generate_cities_and_distances(self):
        """Test generating random distances between cities"""
        # Add some cities
        cities = ["London", "Paris", "Berlin", "Rome", "Madrid"]
        for city in cities:
            self.city_map.add_city(city)
        
        # Generate distances
        self.city_map.generate_cities_and_distances()
        
        # Check that distances were generated for all city pairs
        for i, city1 in enumerate(cities):
            for city2 in cities[i+1:]:
                # Check city positions were generated
                self.assertIn(city1, self.city_map.get_city_positions())
                self.assertIn(city2, self.city_map.get_city_positions())
                
                # Check distance exists (both directions)
                self.assertIn((city1, city2), self.city_map.get_distances())
                self.assertIn((city2, city1), self.city_map.get_distances())
                
                # Check distances are within range (50-100)
                distance = self.city_map.get_distance(city1, city2)
                self.assertGreaterEqual(distance, 50)
                self.assertLessEqual(distance, 100)
                
                # Check distances are symmetric
                self.assertEqual(
                    self.city_map.get_distance(city1, city2),
                    self.city_map.get_distance(city2, city1)
                )
    
    def test_select_random_home_city(self):
        """Test selecting a random home city"""
        # Add some cities
        cities = ["London", "Paris", "Berlin", "Rome", "Madrid"]
        for city in cities:
            self.city_map.add_city(city)
        
        # Select a random home city multiple times to test randomness
        home_cities = set()
        for _ in range(10):
            home_city = self.city_map.select_random_home_city()
            self.assertIn(home_city, cities)
            home_cities.add(home_city)
        
        # It's possible but unlikely that only one city is ever chosen in 10 attempts
        # This is a probabilistic test that could occasionally fail
        self.assertGreater(len(home_cities), 1, 
                         "Random home city selection should produce multiple cities over 10 attempts")
    
    def test_get_distance(self):
        """Test getting distances between cities"""
        # Add cities and explicit distances
        self.city_map.add_city("London")
        self.city_map.add_city("Paris")
        self.city_map.add_distance("London", "Paris", 75)
        
        # Get distance
        self.assertEqual(self.city_map.get_distance("London", "Paris"), 75)
        self.assertEqual(self.city_map.get_distance("Paris", "London"), 75)
        
        # Same city should return 0
        self.assertEqual(self.city_map.get_distance("London", "London"), 0)
        
        # Test error case
        with self.assertRaises(ValueError):
            self.city_map.get_distance("London", "Berlin")
    
    def test_add_distance(self):
        """Test adding distances between cities"""
        # Add distance between two cities (should automatically add cities)
        self.city_map.add_distance("Tokyo", "Seoul", 85)
        
        # Check cities were added
        self.assertIn("Tokyo", self.city_map.get_cities())
        self.assertIn("Seoul", self.city_map.get_cities())
        
        # Check distance was added (both directions)
        self.assertEqual(self.city_map.get_distance("Tokyo", "Seoul"), 85)
        self.assertEqual(self.city_map.get_distance("Seoul", "Tokyo"), 85)
        
        # Update existing distance
        self.city_map.add_distance("Tokyo", "Seoul", 90)
        self.assertEqual(self.city_map.get_distance("Tokyo", "Seoul"), 90)

if __name__ == '__main__':
    unittest.main()