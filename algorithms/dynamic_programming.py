"""
Dynamic programming algorithm implementation for the Traveling Salesman Problem
"""
import itertools

def solve_tsp_dynamic_programming(cities, distances, home_city):
    """
    Find the shortest route using dynamic programming (Held-Karp algorithm).
    
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
                    dp