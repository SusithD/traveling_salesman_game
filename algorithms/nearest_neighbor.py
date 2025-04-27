"""
Nearest neighbor algorithm implementation for the Traveling Salesman Problem
"""

def solve_tsp_nearest_neighbor(cities, distances, home_city):
    """
    Find a route using the nearest neighbor heuristic.
    
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
    
    return route, total_distance