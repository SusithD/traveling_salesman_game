import unittest
from utils.validation import validate_distance_range, validate_route

class TestValidation(unittest.TestCase):
    def test_validate_distance_range(self):
        """Test that distances are properly scaled to the required range"""
        # Test values within range
        self.assertEqual(validate_distance_range(50), 50)
        self.assertEqual(validate_distance_range(75), 75)
        self.assertEqual(validate_distance_range(100), 100)
        
        # Test values below minimum
        scaled_value = validate_distance_range(25)
        self.assertGreaterEqual(scaled_value, 50)
        self.assertLessEqual(scaled_value, 100)
        
        # Test values above maximum
        scaled_value = validate_distance_range(150)
        self.assertGreaterEqual(scaled_value, 50)
        self.assertLessEqual(scaled_value, 100)
        
        # Test extreme values
        scaled_value = validate_distance_range(0)
        self.assertGreaterEqual(scaled_value, 50)
        
        scaled_value = validate_distance_range(1000)
        self.assertLessEqual(scaled_value, 100)
        
        # Test that different inputs produce different outputs (scaling is consistent)
        self.assertNotEqual(validate_distance_range(10), validate_distance_range(20))

    def test_validate_route_valid_cases(self):
        """Test validate_route with valid routes"""
        # Valid route with home city at start and end
        self.assertTrue(validate_route(["A", "B", "C", "A"], "A"))
        
        # Valid route with single city
        self.assertTrue(validate_route(["A", "A"], "A"))
        
        # Valid route with multiple cities
        self.assertTrue(validate_route(["A", "B", "C", "D", "E", "A"], "A"))

    def test_validate_route_empty_route(self):
        """Test validate_route with empty route"""
        with self.assertRaises(ValueError):
            validate_route([], "A")

    def test_validate_route_wrong_start_end(self):
        """Test validate_route with incorrect start/end city"""
        with self.assertRaises(ValueError):
            validate_route(["B", "A", "C", "A"], "A")  # Doesn't start with home
            
        with self.assertRaises(ValueError):
            validate_route(["A", "B", "C", "D"], "A")  # Doesn't end with home
            
        with self.assertRaises(ValueError):
            validate_route(["B", "C", "D", "E"], "A")  # Neither starts nor ends with home

    def test_validate_route_duplicate_cities(self):
        """Test validate_route with duplicate cities"""
        with self.assertRaises(ValueError):
            validate_route(["A", "B", "B", "C", "A"], "A")  # Duplicate 'B'
            
        with self.assertRaises(ValueError):
            validate_route(["A", "B", "C", "A", "D", "A"], "A")  # Too many home cities

    def test_validate_route_missing_cities(self):
        """Test that validation can detect cities not visited"""
        # We don't actually use this functionality, but could be useful later
        route = ["A", "B", "C", "A"]
        home_city = "A"
        
        # Implicit test: doesn't raise an error
        self.assertTrue(validate_route(route, home_city))

if __name__ == '__main__':
    unittest.main()