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
        
        # Initialize DP table
        # dp[mask][i] = minimum distance to visit all cities in mask and end at city i
        dp = {}
        
        # Initialize path reconstruction table
        path = {}
        
        # Base case - starting at home city
        for i in range(n):
            if i != home_idx:
                dp[(1 << home_idx) | (1 << i), i] = dist_matrix[home_idx][i]
                path[(1 << home_idx) | (1 << i), i] = home_idx
        
        # Iterate over all subsets of cities
        for subset_size in range(3, n + 1):
            for subset in itertools.combinations(range(n), subset_size):
                # Skip if home city is not in subset
                if home_idx not in subset:
                    continue
                
                # Create mask for this subset
                mask = 0
                for i in subset:
                    mask |= 1 << i
                
                # Try all cities as the ending city
                for end in subset:
                    if end == home_idx:
                        continue
                    
                    # Previous mask without the end city
                    prev_mask = mask & ~(1 << end)
                    
                    # Find the best path to this city
                    min_dist = float('inf')
                    best_prev = -1
                    
                    for prev in subset:
                        if prev == end or prev == home_idx:
                            continue
                        
                        if (prev_mask, prev) in dp:
                            current_dist = dp[(prev_mask, prev)] + dist_matrix[prev][end]
                            if current_dist < min_dist:
                                min_dist = current_dist
                                best_prev = prev
                    
                    if best_prev != -1:
                        dp[(mask, end)] = min_dist
                        path[(mask, end)] = best_prev
        
        # Find the best path back to home
        all_cities_mask = (1 << n) - 1
        min_dist = float('inf')
        best_last = -1
        
        for last in range(n):
            if last != home_idx:
                if (all_cities_mask, last) in dp:
                    current_dist = dp[(all_cities_mask, last)] + dist_matrix[last][home_idx]
                    if current_dist < min_dist:
                        min_dist = current_dist
                        best_last = last
        
        # Reconstruct the path
        if best_last == -1:
            # This should not happen if there's a valid solution
            return [home_city], 0
        
        # Start with the last city before returning home
        mask = all_cities_mask
        current = best_last
        route_indices = [home_idx]  # End at home
        route_indices.append(current)
        
        # Reconstruct the path backwards
        while current != home_idx:
            prev = path[(mask, current)]
            route_indices.append(prev)
            mask &= ~(1 << current)
            current = prev
        
        # Reverse and convert back to city names
        route_indices.reverse()
        route = [cities[i] for i in route_indices]
        
        # Validate the route before returning
        validate_route(route, home_city)
        
        return route, min_dist