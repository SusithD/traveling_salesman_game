import unittest
from core.route_calculator import RouteCalculator

class TestRouteCalculator(unittest.TestCase):
    def setUp(self):
        self.calculator = RouteCalculator()
        
        # Test data set 1: Simple 5-city graph
        self.cities1 = ["A", "B", "C", "D", "E"]
        self.home_city1 = "A"
        self.distances1 = {
            ("A", "B"): 10,
            ("A", "C"): 20,
            ("A", "D"): 30, 
            ("A", "E"): 40,
            ("B", "C"): 10,
            ("B", "D"): 25,
            ("B", "E"): 30,
            ("C", "D"): 10,
            ("C", "E"): 20,
            ("D", "E"): 10,
        }
        
        # Test data set 2: Graph where nearest neighbor is non-optimal
        self.cities2 = ["A", "B", "C", "D", "E"]
        self.home_city2 = "A"
        self.distances2 = {
            ("A", "B"): 10,
            ("A", "C"): 15,
            ("A", "D"): 20,
            ("A", "E"): 15,
            ("B", "C"): 5,
            ("B", "D"): 30,
            ("B", "E"): 25,
            ("C", "D"): 30,
            ("C", "E"): 25,
            ("D", "E"): 10,
        }
        
        # Known optimal solution for test data set 1
        self.optimal_length1 = 80  # The optimal path is A-B-C-D-E-A with length 10+10+10+10+40=80
        
        # Known optimal solution for test data set 2
        self.optimal_length2 = 70  # The optimal path is A-B-C-E-D-A with length 10+5+25+10+20=70

    def test_brute_force_correctness(self):
        """Test that brute force finds the optimal solution"""
        route1, length1 = self.calculator.brute_force(self.cities1, self.distances1, self.home_city1)
        self.assertEqual(length1, self.optimal_length1)
        self.assertEqual(route1[0], self.home_city1)
        self.assertEqual(route1[-1], self.home_city1)
        
        route2, length2 = self.calculator.brute_force(self.cities2, self.distances2, self.home_city2)
        self.assertEqual(length2, self.optimal_length2)
        self.assertEqual(route2[0], self.home_city2)
        self.assertEqual(route2[-1], self.home_city2)

    def test_dynamic_programming_correctness(self):
        """Test that dynamic programming finds the optimal solution"""
        route1, length1 = self.calculator.dynamic_programming(self.cities1, self.distances1, self.home_city1)
        self.assertEqual(length1, self.optimal_length1)
        self.assertEqual(route1[0], self.home_city1)
        self.assertEqual(route1[-1], self.home_city1)
        
        route2, length2 = self.calculator.dynamic_programming(self.cities2, self.distances2, self.home_city2)
        self.assertEqual(length2, self.optimal_length2)
        self.assertEqual(route2[0], self.home_city2)
        self.assertEqual(route2[-1], self.home_city2)

    def test_nearest_neighbor_correctness(self):
        """Test that nearest neighbor produces a valid (though possibly non-optimal) solution"""
        route1, length1 = self.calculator.nearest_neighbor(self.cities1, self.distances1, self.home_city1)
        self.assertEqual(route1[0], self.home_city1)
        self.assertEqual(route1[-1], self.home_city1)
        self.assertLessEqual(len(route1), len(self.cities1) + 1)  # n cities + return to start
        
        route2, length2 = self.calculator.nearest_neighbor(self.cities2, self.distances2, self.home_city2)
        self.assertEqual(route2[0], self.home_city2)
        self.assertEqual(route2[-1], self.home_city2)
        self.assertLessEqual(len(route2), len(self.cities2) + 1)

    def test_all_cities_visited(self):
        """Test that all algorithms visit all cities exactly once"""
        for algorithm in [self.calculator.brute_force, self.calculator.nearest_neighbor, self.calculator.dynamic_programming]:
            route, _ = algorithm(self.cities1, self.distances1, self.home_city1)
            
            # Check all cities are in the route
            for city in self.cities1:
                self.assertIn(city, route)
            
            # Check home city appears exactly twice (start and end)
            self.assertEqual(route.count(self.home_city1), 2)
            
            # Check other cities appear exactly once
            for city in self.cities1:
                if city != self.home_city1:
                    self.assertEqual(route.count(city), 1)

    def test_distance_lookup(self):
        """Test that the algorithms handle distance lookup correctly in both directions"""
        # Create asymmetric distances (only one direction specified)
        asymmetric_distances = {
            ("A", "B"): 10,
            ("A", "C"): 20,
            ("B", "C"): 5,
        }
        cities = ["A", "B", "C"]
        
        # All algorithms should be able to handle this
        for algorithm in [self.calculator.brute_force, self.calculator.nearest_neighbor, self.calculator.dynamic_programming]:
            route, length = algorithm(cities, asymmetric_distances, "A")
            self.assertEqual(len(route), len(cities) + 1)  # All cities + return to start

    def test_error_handling(self):
        """Test that algorithms raise appropriate errors for invalid inputs"""
        # Missing distance
        incomplete_distances = {
            ("A", "B"): 10,
            # Missing A-C distance
            ("B", "C"): 15,
        }
        cities = ["A", "B", "C"]
        
        for algorithm in [self.calculator.brute_force, self.calculator.nearest_neighbor, self.calculator.dynamic_programming]:
            with self.assertRaises(ValueError):
                algorithm(cities, incomplete_distances, "A")

    def test_edge_cases(self):
        """Test edge cases like small number of cities"""
        # Test with just 2 cities
        small_cities = ["A", "B"]
        small_distances = {("A", "B"): 10}
        
        for algorithm in [self.calculator.brute_force, self.calculator.nearest_neighbor, self.calculator.dynamic_programming]:
            route, length = algorithm(small_cities, small_distances, "A")
            self.assertEqual(route, ["A", "B", "A"])
            self.assertEqual(length, 20)

if __name__ == '__main__':
    unittest.main()