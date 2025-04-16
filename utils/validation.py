"""
Validation utilities for the Traveling Salesman Problem game
"""

def validate_distance_range(distance):
    """
    Validate and adjust distance to be within the required range (50-100 km)
    
    Parameters:
    - distance: The calculated distance between cities
    
    Returns:
    - Adjusted distance within the range 50-100 km
    """
    # Scale the distance to fit within 50-100 range
    MIN_DISTANCE = 50
    MAX_DISTANCE = 100
    
    # If the original distance is outside our range, scale it
    if distance < MIN_DISTANCE:
        return MIN_DISTANCE + (distance / 100) * (MAX_DISTANCE - MIN_DISTANCE)
    elif distance > MAX_DISTANCE:
        return MIN_DISTANCE + ((distance % 50) / 50) * (MAX_DISTANCE - MIN_DISTANCE)
    
    return distance

def validate_route(route, home_city):
    """
    Validate that a route is valid for the TSP
    
    Parameters:
    - route: The route to validate
    - home_city: The starting and ending city
    
    Raises:
    - ValueError: If the route is invalid
    """
    if not route:
        raise ValueError("Route cannot be empty")
    
    if route[0] != home_city or route[-1] != home_city:
        raise ValueError(f"Route must start and end at the home city ({home_city})")
    
    # Check for duplicates (except home city which appears twice)
    cities_count = {}
    for city in route:
        if city not in cities_count:
            cities_count[city] = 0
        cities_count[city] += 1
    
    # Home city should appear exactly twice (start and end)
    if cities_count[home_city] != 2:
        raise ValueError(f"Home city ({home_city}) must appear exactly twice (start and end)")
    
    # All other cities should appear exactly once
    for city, count in cities_count.items():
        if city != home_city and count != 1:
            raise ValueError(f"City {city} must be visited exactly once")
    
    return True