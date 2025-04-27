"""
Route calculator for the Traveling Salesman Problem
Runs various algorithms and measures their performance
"""
import logging
import time
from typing import Dict, List, Tuple, Any
import numpy as np

logger = logging.getLogger("RouteCalculator")

class RouteCalculator:
    """
    Calculates routes using different algorithms and measures their performance
    """
    def __init__(self):
        """Initialize the route calculator"""
        pass
    
    def calculate_all_routes(self, cities: List[str], distances: np.ndarray, home_city: str) -> Dict[str, Dict[str, Any]]:
        """
        Calculate routes using all available algorithms
        
        Args:
            cities: List of city names
            distances: Distance matrix for the cities
            home_city: The home city (starting and ending point)
        
        Returns:
            Dictionary with results for each algorithm
        """
        results = {}
        
        # Import algorithms
        from algorithms.brute_force import solve_tsp_brute_force
        from algorithms.nearest_neighbor import solve_tsp_nearest_neighbor
        from algorithms.dynamic_programming import solve_tsp_dynamic_programming
        
        # Setup for algorithms
        city_indices = {city: i for i, city in enumerate(cities)}
        home_idx = city_indices[home_city]
        
        # Execute each algorithm and time it
        try:
            # Brute Force
            start_time = time.time()
            bf_route_indices, bf_distance = solve_tsp_brute_force(distances, home_idx)
            bf_time = time.time() - start_time
            bf_route = [cities[i] for i in bf_route_indices]
            
            results["Brute Force"] = {
                "route": bf_route,
                "length": bf_distance,
                "time": bf_time
            }
            logger.info(f"Brute Force: distance={bf_distance:.2f}, time={bf_time:.6f}s")
        except Exception as e:
            logger.error(f"Error running Brute Force algorithm: {e}")
            results["Brute Force"] = {
                "route": ["Error"],
                "length": float('inf'),
                "time": 0
            }
        
        try:
            # Nearest Neighbor
            start_time = time.time()
            nn_route_indices, nn_distance = solve_tsp_nearest_neighbor(distances, home_idx)
            nn_time = time.time() - start_time
            nn_route = [cities[i] for i in nn_route_indices]
            
            results["Nearest Neighbor"] = {
                "route": nn_route,
                "length": nn_distance,
                "time": nn_time
            }
            logger.info(f"Nearest Neighbor: distance={nn_distance:.2f}, time={nn_time:.6f}s")
        except Exception as e:
            logger.error(f"Error running Nearest Neighbor algorithm: {e}")
            results["Nearest Neighbor"] = {
                "route": ["Error"],
                "length": float('inf'),
                "time": 0
            }
        
        try:
            # Dynamic Programming (Held-Karp algorithm)
            start_time = time.time()
            dp_route_indices, dp_distance = solve_tsp_dynamic_programming(distances, home_idx)
            dp_time = time.time() - start_time
            dp_route = [cities[i] for i in dp_route_indices]
            
            results["Dynamic Programming"] = {
                "route": dp_route,
                "length": dp_distance,
                "time": dp_time
            }
            logger.info(f"Dynamic Programming: distance={dp_distance:.2f}, time={dp_time:.6f}s")
        except Exception as e:
            logger.error(f"Error running Dynamic Programming algorithm: {e}")
            results["Dynamic Programming"] = {
                "route": ["Error"],
                "length": float('inf'),
                "time": 0
            }
            
        return results
    
    def find_shortest_algorithm(self, results: Dict[str, Dict[str, Any]]) -> str:
        """
        Find the algorithm that produced the shortest route
        
        Args:
            results: Dictionary with results for each algorithm
            
        Returns:
            Name of the algorithm with shortest route
        """
        shortest_distance = float('inf')
        shortest_algo = None
        
        for algo_name, data in results.items():
            if data['length'] < shortest_distance:
                shortest_distance = data['length']
                shortest_algo = algo_name
                
        return shortest_algo