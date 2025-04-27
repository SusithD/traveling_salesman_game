"""
Brute force algorithm implementation for the Traveling Salesman Problem
"""
import itertools

def solve_tsp_brute_force(cities, distances, home_city):
    """
    Find the shortest route using brute force approach.
    
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
    
    return best_route, best_length