"""
Visualization utilities for the Traveling Salesman Problem game
Provides functions for creating charts and visualizations
"""
import logging
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

logger = logging.getLogger("Visualization")

class PerformanceChart(FigureCanvas):
    """
    A chart widget for displaying algorithm performance metrics
    """
    def __init__(self, parent=None, width=8, height=6, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.fig.patch.set_facecolor('#222222')  # Dark background
        super().__init__(self.fig)
        self.setParent(parent)

    def plot_route_lengths(self, algorithm_results):
        """Plot a bar chart comparing algorithm route lengths"""
        try:
            # Clear previous plots
            self.fig.clear()
            
            # Create the axes
            ax = self.fig.add_subplot(111)
            ax.set_facecolor('#333333')  # Dark background for the plot area
            
            # Prepare data
            algorithms = list(algorithm_results.keys())
            route_lengths = [algorithm_results[algo]['length'] for algo in algorithms]
            
            # Colors for each algorithm
            colors = {
                "Brute Force": "#e74c3c",
                "Nearest Neighbor": "#3498db",
                "Dynamic Programming": "#2ecc71"
            }
            bar_colors = [colors.get(algo, "#9b59b6") for algo in algorithms]
            
            # Find the best algorithm (shortest route)
            min_index = route_lengths.index(min(route_lengths))
            
            # Create the bar chart
            bars = ax.bar(algorithms, route_lengths, color=bar_colors, alpha=0.7)
            
            # Highlight the best algorithm
            bars[min_index].set_alpha(1.0)
            bars[min_index].set_edgecolor('#27ae60')
            bars[min_index].set_linewidth(2)
            
            # Add value labels on top of bars
            for i, v in enumerate(route_lengths):
                ax.text(i, v + 0.1, f"{v:.1f}", ha='center', va='bottom', color='white', fontweight='bold')
            
            # Customize the plot
            ax.set_title('Route Length Comparison', color='white', fontsize=14)
            ax.set_ylabel('Route Length (km)', color='white')
            ax.set_xlabel('Algorithm', color='white')
            ax.tick_params(colors='white')
            
            # Customize grid
            ax.grid(True, linestyle='--', alpha=0.3)
            
            # Customize spines
            for spine in ax.spines.values():
                spine.set_edgecolor('#555555')
            
            # Add a note about which is better
            ax.annotate('Lower is better', xy=(0.02, 0.95), xycoords='axes fraction', 
                       color='#2ecc71', fontsize=10, ha='left')
            
            # Adjust layout
            self.fig.tight_layout()
            self.draw()
            
            return True
            
        except Exception as e:
            logger.error(f"Error creating route length chart: {e}")
            return False
    
    def plot_execution_times(self, algorithm_results):
        """Plot a bar chart comparing algorithm execution times"""
        try:
            # Clear previous plots
            self.fig.clear()
            
            # Create the axes
            ax = self.fig.add_subplot(111)
            ax.set_facecolor('#333333')  # Dark background for the plot area
            
            # Prepare data
            algorithms = list(algorithm_results.keys())
            execution_times = [algorithm_results[algo]['time'] for algo in algorithms]
            
            # Colors for each algorithm
            colors = {
                "Brute Force": "#e74c3c",
                "Nearest Neighbor": "#3498db",
                "Dynamic Programming": "#2ecc71"
            }
            bar_colors = [colors.get(algo, "#9b59b6") for algo in algorithms]
            
            # Find the fastest algorithm
            min_index = execution_times.index(min(execution_times))
            
            # Create the bar chart
            bars = ax.bar(algorithms, execution_times, color=bar_colors, alpha=0.7)
            
            # Highlight the fastest algorithm
            bars[min_index].set_alpha(1.0)
            bars[min_index].set_edgecolor('#27ae60')
            bars[min_index].set_linewidth(2)
            
            # Add value labels on top of bars
            for i, v in enumerate(execution_times):
                ax.text(i, v + 0.0001, f"{v:.6f}s", ha='center', va='bottom', color='white', fontweight='bold')
            
            # Customize the plot
            ax.set_title('Execution Time Comparison', color='white', fontsize=14)
            ax.set_ylabel('Time (seconds)', color='white')
            ax.set_xlabel('Algorithm', color='white')
            ax.tick_params(colors='white')
            
            # Customize grid
            ax.grid(True, linestyle='--', alpha=0.3)
            
            # Customize spines
            for spine in ax.spines.values():
                spine.set_edgecolor('#555555')
            
            # Add a note about which is better
            ax.annotate('Lower is better', xy=(0.02, 0.95), xycoords='axes fraction', 
                       color='#2ecc71', fontsize=10, ha='left')
                       
            # Use logarithmic scale if times vary greatly
            if max(execution_times) / min(execution_times) > 10:
                ax.set_yscale('log')
                ax.annotate('Logarithmic scale', xy=(0.98, 0.95), xycoords='axes fraction', 
                           color='#3498db', fontsize=10, ha='right')
            
            # Adjust layout
            self.fig.tight_layout()
            self.draw()
            
            return True
            
        except Exception as e:
            logger.error(f"Error creating execution time chart: {e}")
            return False
            
    def plot_performance_comparison(self, algorithm_results):
        """Plot a dual-metric chart comparing both route length and execution time"""
        try:
            # Clear previous plots
            self.fig.clear()
            
            # Create the axes - 2 subplots
            ax1 = self.fig.add_subplot(121)  # Route lengths
            ax2 = self.fig.add_subplot(122)  # Execution times
            
            ax1.set_facecolor('#333333')
            ax2.set_facecolor('#333333')
            
            # Prepare data
            algorithms = list(algorithm_results.keys())
            route_lengths = [algorithm_results[algo]['length'] for algo in algorithms]
            execution_times = [algorithm_results[algo]['time'] for algo in algorithms]
            
            # Colors for each algorithm
            colors = {
                "Brute Force": "#e74c3c",
                "Nearest Neighbor": "#3498db",
                "Dynamic Programming": "#2ecc71"
            }
            bar_colors = [colors.get(algo, "#9b59b6") for algo in algorithms]
            
            # Plot route lengths
            min_length_index = route_lengths.index(min(route_lengths))
            bars1 = ax1.bar(algorithms, route_lengths, color=bar_colors, alpha=0.7)
            bars1[min_length_index].set_alpha(1.0)
            bars1[min_length_index].set_edgecolor('#27ae60')
            bars1[min_length_index].set_linewidth(2)
            
            # Plot execution times
            min_time_index = execution_times.index(min(execution_times))
            bars2 = ax2.bar(algorithms, execution_times, color=bar_colors, alpha=0.7)
            bars2[min_time_index].set_alpha(1.0)
            bars2[min_time_index].set_edgecolor('#27ae60')
            bars2[min_time_index].set_linewidth(2)
            
            # Add value labels
            for i, v in enumerate(route_lengths):
                ax1.text(i, v + (max(route_lengths) * 0.02), f"{v:.1f}", ha='center', va='bottom', color='white', fontsize=9)
            
            for i, v in enumerate(execution_times):
                ax2.text(i, v + (max(execution_times) * 0.05), f"{v:.5f}s", ha='center', va='bottom', color='white', fontsize=9)
            
            # Customize route length plot
            ax1.set_title('Route Length', color='white', fontsize=12)
            ax1.set_ylabel('Distance (km)', color='white')
            ax1.tick_params(axis='x', labelrotation=30, colors='white')
            ax1.tick_params(axis='y', colors='white')
            ax1.grid(True, linestyle='--', alpha=0.3)
            ax1.annotate('Lower is better', xy=(0.02, 0.95), xycoords='axes fraction', 
                       color='#2ecc71', fontsize=8, ha='left')
            
            # Customize execution time plot
            ax2.set_title('Execution Time', color='white', fontsize=12)
            ax2.set_ylabel('Time (seconds)', color='white')
            ax2.tick_params(axis='x', labelrotation=30, colors='white')
            ax2.tick_params(axis='y', colors='white')
            ax2.grid(True, linestyle='--', alpha=0.3)
            ax2.annotate('Lower is better', xy=(0.02, 0.95), xycoords='axes fraction', 
                       color='#2ecc71', fontsize=8, ha='left')
            
            # Use logarithmic scale if times vary greatly
            if max(execution_times) / min(execution_times) > 10:
                ax2.set_yscale('log')
                ax2.annotate('Log scale', xy=(0.98, 0.95), xycoords='axes fraction', 
                           color='#3498db', fontsize=8, ha='right')
            
            # Customize spines
            for spine in ax1.spines.values():
                spine.set_edgecolor('#555555')
            for spine in ax2.spines.values():
                spine.set_edgecolor('#555555')
            
            # Main title
            self.fig.suptitle('Algorithm Performance Comparison', color='white', fontsize=14)
            
            # Adjust layout
            self.fig.tight_layout()
            self.draw()
            
            return True
            
        except Exception as e:
            logger.error(f"Error creating performance comparison chart: {e}")
            return False

def plot_route_on_map(route, distances):
    """
    Create a visualization of the route on a simple map
    This is a placeholder for a more sophisticated visualization
    
    Args:
        route: List of cities in the route
        distances: Dictionary of distances between cities
    
    Returns:
        A matplotlib figure showing the route
    """
    try:
        # Create a new figure
        fig = plt.figure(figsize=(8, 6), facecolor='#222222')
        ax = fig.add_subplot(111)
        ax.set_facecolor('#333333')
        
        # Create a simple 2D representation of cities
        city_positions = {}
        
        # First, we need to calculate 2D positions for cities
        # This is a simplified approach - for real applications, use actual geo-coordinates
        
        # Number of cities (excluding duplicates)
        unique_cities = list(set(route))
        n_cities = len(unique_cities)
        
        # Place cities randomly on a circle
        radius = 10
        angles = np.linspace(0, 2 * np.pi, n_cities, endpoint=False)
        
        for i, city in enumerate(unique_cities):
            x = radius * np.cos(angles[i])
            y = radius * np.sin(angles[i])
            city_positions[city] = (x, y)
        
        # Plot the route
        for i in range(len(route)-1):
            city1, city2 = route[i], route[i+1]
            x1, y1 = city_positions[city1]
            x2, y2 = city_positions[city2]
            
            # Draw the connection line
            ax.plot([x1, x2], [y1, y2], 'w-', alpha=0.7, linewidth=2)
            
            # Add a direction arrow
            dx, dy = x2 - x1, y2 - y1
            ax.arrow(x1, y1, dx * 0.8, dy * 0.8, head_width=0.6, head_length=0.8, 
                    fc='white', ec='white', alpha=0.7)
        
        # Draw the cities
        for city, (x, y) in city_positions.items():
            is_start = city == route[0]
            color = '#2ecc71' if is_start else '#3498db'
            ax.plot(x, y, 'o', markersize=10, color=color)
            
            # Add city labels
            ax.text(x, y + 0.8, city, ha='center', va='bottom', color='white', 
                   fontsize=9, fontweight='bold' if is_start else 'normal')
        
        # Customize the plot
        ax.set_title('Route Visualization', color='white', fontsize=14)
        ax.set_aspect('equal')
        ax.grid(False)
        ax.set_xlim(-radius*1.5, radius*1.5)
        ax.set_ylim(-radius*1.5, radius*1.5)
        
        # Hide axes
        ax.set_xticks([])
        ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_visible(False)
        
        # Add a legend
        ax.plot([], [], 'o', color='#2ecc71', label='Start/End City')
        ax.plot([], [], 'o', color='#3498db', label='Intermediate Cities')
        ax.legend(facecolor='#333333', edgecolor='#555555', labelcolor='white')
        
        # Add route information
        total_distance = 0
        for i in range(len(route)-1):
            city1, city2 = route[i], route[i+1]
            key = (city1, city2)
            rev_key = (city2, city1)
            if key in distances:
                total_distance += distances[key]
            elif rev_key in distances:
                total_distance += distances[rev_key]
        
        ax.text(0, -radius*1.2, f"Total Distance: {total_distance:.2f} km", 
               ha='center', va='center', color='white', fontsize=12)
        
        fig.tight_layout()
        return fig
        
    except Exception as e:
        logger.error(f"Error creating route map: {e}")
        return None