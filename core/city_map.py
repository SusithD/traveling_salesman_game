"""
City map generation and management for the Traveling Salesman Problem game
"""
import random
import math
from utils.validation import validate_distance_range

class CityMap:
    def __init__(self):
        self.cities = ['City A', 'City B', 'City C', 'City D', 'City E', 
                      'City F', 'City G', 'City H', 'City I', 'City J']
        self.distances = {}
        self.city_positions = {}  # For visualization
        
    def generate_cities_and_distances(self):
        """Generate random distances between cities"""
        # Clear existing distances
        self.distances = {}
        self.city_positions = {}
        
        # Generate random positions for cities (for visualization)
        for city in self.cities:
            self.city_positions[city] = (random.uniform(0, 100), random.uniform(0, 100))
        
        # Generate random distances between cities
        for i, city1 in enumerate(self.cities):
            for city2 in self.cities[i+1:]:
                # Calculate Euclidean distance between cities based on positions
                x1, y1 = self.city_positions[city1]
                x2, y2 = self.city_positions[city2]
                
                # Base distance from positions
                base_distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
                
                # Add some randomness but keep within range
                distance = round(validate_distance_range(base_distance), 2)
                
                # Store distance (both directions)
                self.distances[(city1, city2)] = distance
                self.distances[(city2, city1)] = distance
    
    def select_random_home_city(self):
        """Select a random city to be the home city"""
        return random.choice(self.cities)
    
    def get_cities(self):
        """Return the list of cities"""
        return self.cities
    
    def get_distances(self):
        """Return the distances dictionary"""
        return self.distances
    
    def get_city_positions(self):
        """Return city positions for visualization"""
        return self.city_positions
    
    def get_distance(self, city1, city2):
        """Get the distance between two cities"""
        if city1 == city2:
            return 0
        
        key = (city1, city2)
        if key in self.distances:
            return self.distances[key]
        
        # If not found, try the reverse order
        key = (city2, city1)
        if key in self.distances:
            return self.distances[key]
        
        raise ValueError(f"No distance found between {city1} and {city2}")