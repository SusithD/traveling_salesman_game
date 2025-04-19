"""
Route calculators using different algorithms for the Traveling Salesman Problem
"""
import itertools
from utils.validation import validate_route

class RouteCalculator:
    def brute_force(self, cities, distances, home_city):
        """
        Find the shortest route using brute force approach.
        This tries all possible permutations of cities.
        
        Parameters:
        - cities: List of cities to visit
        - distances: Dictionary of distances between cities
        - home_city: Starting and ending city
        
        Returns:
        - Tuple of (best_route, best_route_length)
        """
        # Get cities to visit (excluding home city)
        cities_to_visit = [city for city in cities if city != home_city]
        
        # Best route found so far
        best_route = None
        best_length = float('inf')
        
        # Try all permutations of cities
        for perm in itertools.permutations(cities_to_visit):
            # Create a complete route starting and ending at home
            route = [home_city] + list(perm) + [home_city]
            
            # Calculate the total distance
            total_distance = 0
            for i in range(len(route) - 1):
                city1, city2 = route[i], route[i+1]
                distance_key = (city1, city2)
                reverse_key = (city2, city1)
                
                if distance_key in distances:
                    total_distance += distances[distance_key]
                elif reverse_key in distances:
                    total_distance += distances[reverse_key]
                else:
                    raise ValueError(f"No distance found between {city1} and {city2}")
            
            # Update best route if this one is shorter
            if total_distance < best_length:
                best_length = total_distance
                best_route = route
        
        # Validate the route before returning
        validate_route(best_route, home_city)
        
        return best_route, best_length
    
    def nearest_neighbor(self, cities, distances, home_city):
        """
        Find a route using the nearest neighbor heuristic.
        Always visits the closest unvisited city.
        
        Parameters:
        - cities: List of cities to visit
        - distances: Dictionary of distances between cities
        - home_city: Starting and ending city
        
        Returns:
        - Tuple of (route, route_length)
        """
        # Create a list of unvisited cities
        unvisited = list(cities)
        unvisited.remove(home_city)
        
        # Start at home city
        current_city = home_city
        route = [current_city]
        total_distance = 0
        
        # Visit each city in order of closest distance
        while unvisited:
            # Find the closest city
            closest_city = None
            min_distance = float('inf')
            
            for city in unvisited:
                distance_key = (current_city, city)
                reverse_key = (city, current_city)
                
                if distance_key in distances:
                    distance = distances[distance_key]
                elif reverse_key in distances:
                    distance = distances[reverse_key]
                else:
                    raise ValueError(f"No distance found between {current_city} and {city}")
                
                if distance < min_distance:
                    min_distance = distance
                    closest_city = city
            
            # Visit the closest city
            route.append(closest_city)
            total_distance += min_distance
            current_city = closest_city
            unvisited.remove(closest_city)
        
        # Return to home city
        distance_key = (current_city, home_city)
        reverse_key = (home_city, current_city)
        
        if distance_key in distances:
            total_distance += distances[distance_key]
        elif reverse_key in distances:
            total_distance += distances[reverse_key]
        else:
            raise ValueError(f"No distance found between {current_city} and {home_city}")
        
        route.append(home_city)
        
        # Validate the route before returning
        validate_route(route, home_city)
        
        return route, total_distance
    
    def dynamic_programming(self, cities, distances, home_city):
        """
        Find the shortest route using dynamic programming.
        This uses the Held-Karp algorithm.
        
        Parameters:
        - cities: List of cities to visit
        - distances: Dictionary of distances between cities
        - home_city: Starting and ending city
        
        Returns:
        - Tuple of (route, route_length)
        """
        # Create a mapping of cities to indices
        city_indices = {city: i for i, city in enumerate(cities)}
        index_to_city = {i: city for i, city in enumerate(cities)}
        home_idx = city_indices[home_city]
        
        n = len(cities)
        
        # Create a distance matrix
        dist_matrix = [[0] * n for _ in range(n)]
        for i, city1 in enumerate(cities):
            for j, city2 in enumerate(cities):
                if i == j:
                    dist_matrix[i][j] = 0
                else:
                    distance_key = (city1, city2)
                    reverse_key = (city2, city1)
                    
                    if distance_key in distances:
                        dist_matrix[i][j] = distances[distance_key]
                    elif reverse_key in distances:
                        dist_matrix[i][j] = distances[reverse_key]
                    else:
                        raise ValueError(f"No distance found between {city1} and {city2}")
        
        # For very small number of cities, use brute force approach
        if n <= 3:
            return self.brute_force(cities, distances, home_city)
            
        # Use a simpler DP approach for better reliability
        # We'll use a recursive approach with memoization
        memo = {}
        
        # Function to compute the shortest path from current to home,
        # having visited all cities in visited_mask
        def tsp_dp(current, visited_mask):
            # If all cities are visited, return to home
            if visited_mask == (1 << n) - 1:
                return dist_matrix[current][home_idx], [home_idx]
            
            # If we've computed this state before, return the memoized result
            if (current, visited_mask) in memo:
                return memo[(current, visited_mask)]
            
            min_dist = float('inf')
            best_path = None
            
            # Try visiting each unvisited city
            for next_city in range(n):
                # Skip if already visited or if it's the same as current
                if visited_mask & (1 << next_city) or next_city == current:
                    continue
                
                # Calculate distance through this next city
                next_visited_mask = visited_mask | (1 << next_city)
                distance_to_next = dist_matrix[current][next_city]
                
                # Recursive call to find the best path after visiting next_city
                remaining_dist, remaining_path = tsp_dp(next_city, next_visited_mask)
                total_dist = distance_to_next + remaining_dist
                
                if total_dist < min_dist:
                    min_dist = total_dist
                    best_path = [next_city] + remaining_path
            
            # Memoize and return the result
            memo[(current, visited_mask)] = (min_dist, best_path)
            return min_dist, best_path
        
        # Start the algorithm from the home city
        # Only the home city is visited initially
        initial_mask = 1 << home_idx
        total_distance, path_indices = tsp_dp(home_idx, initial_mask)
        
        # Convert indices back to city names
        path = [home_city]  # Start at home city
        for idx in path_indices:
            path.append(index_to_city[idx])
        
        # Validate the route before returning
        validate_route(path, home_city)
        
        return path, total_distance