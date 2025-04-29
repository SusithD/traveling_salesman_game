#!/usr/bin/env python3
"""
Performance Benchmark for TSP Algorithms
Collects and analyzes performance data for Traveling Salesman Problem algorithms.
"""

import sys
import os
import time
import random
import csv
import statistics
from datetime import datetime

# Add parent directory to path so we can import from project
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import project modules
from core.route_calculator import RouteCalculator
from core.city_map import CityMap

# Configure matplotlib for visualization
try:
    import matplotlib.pyplot as plt
    import numpy as np
    HAS_MATPLOTLIB = True
except ImportError:
    print("Matplotlib not installed. Charts will not be generated.")
    HAS_MATPLOTLIB = False

def generate_test_scenario(num_cities=10, seed=None):
    """
    Generate a test scenario with the specified number of cities.
    
    Args:
        num_cities: Number of cities to generate
        seed: Random seed (for reproducibility)
        
    Returns:
        Tuple of (cities, distances, home_city)
    """
    if seed is not None:
        random.seed(seed)
        
    # Create cities with names A, B, C, etc.
    city_names = [chr(65 + i) for i in range(min(num_cities, 26))]
    # If we need more than 26 cities, use AA, AB, etc.
    if num_cities > 26:
        for i in range(num_cities - 26):
            city_names.append(f"A{chr(65 + i)}")
            
    # Create city map and add cities
    city_map = CityMap()
    for city in city_names:
        city_map.add_city(city)
    
    # Generate distances between cities
    city_map.generate_cities_and_distances()
    
    # Select home city
    home_city = city_map.select_random_home_city()
    
    return city_map.get_cities(), city_map.get_distances(), home_city

def benchmark_algorithm(algorithm_func, cities, distances, home_city, num_runs=3):
    """
    Benchmark a specific algorithm.
    
    Args:
        algorithm_func: The algorithm function to benchmark
        cities: List of cities
        distances: Dictionary of distances
        home_city: Starting/ending city
        num_runs: Number of times to run the algorithm (to get average)
        
    Returns:
        Dictionary with execution time statistics
    """
    times = []
    routes = []
    lengths = []
    
    for _ in range(num_runs):
        start_time = time.time()
        route, length = algorithm_func(cities, distances, home_city)
        end_time = time.time()
        execution_time = (end_time - start_time) * 1000  # Convert to milliseconds
        
        times.append(execution_time)
        routes.append(route)
        lengths.append(length)
    
    # Return statistics
    return {
        "min_time": min(times),
        "max_time": max(times),
        "avg_time": statistics.mean(times),
        "median_time": statistics.median(times),
        "std_dev": statistics.stdev(times) if len(times) > 1 else 0,
        "route_length": statistics.mean(lengths),
        "num_cities": len(cities),
    }

def run_benchmarks(city_counts=None, num_runs=3, num_rounds=10):
    """
    Run benchmarks for different algorithms and city counts.
    
    Args:
        city_counts: List of city counts to test
        num_runs: Number of runs per algorithm per city count
        num_rounds: Number of game rounds (different city configurations)
        
    Returns:
        Dictionary with benchmark results
    """
    if city_counts is None:
        city_counts = [5, 6, 7, 8, 9, 10, 11, 12]
        
    route_calculator = RouteCalculator()
    algorithms = {
        "Brute Force": route_calculator.brute_force,
        "Nearest Neighbor": route_calculator.nearest_neighbor,
        "Dynamic Programming": route_calculator.dynamic_programming
    }
    
    results = {
        "city_counts": city_counts,
        "algorithms": list(algorithms.keys()),
        "rounds": [],
    }
    
    # Run benchmarks for each round
    for round_num in range(1, num_rounds + 1):
        print(f"\nRunning Round {round_num}/{num_rounds}")
        round_results = {"round": round_num, "data": {}}
        
        # Test each city count
        for city_count in city_counts:
            print(f"  Testing with {city_count} cities...")
            # Generate a single test scenario for all algorithms
            cities, distances, home_city = generate_test_scenario(city_count, seed=round_num + city_count)
            
            # Test each algorithm
            for algo_name, algo_func in algorithms.items():
                print(f"    Running {algo_name}...")
                
                try:
                    # Skip brute force for large city counts to avoid excessive runtime
                    if algo_name == "Brute Force" and city_count > 11:
                        print(f"    Skipping {algo_name} for {city_count} cities (would take too long)")
                        stats = {
                            "min_time": None,
                            "max_time": None,
                            "avg_time": None,
                            "median_time": None,
                            "std_dev": None,
                            "route_length": None,
                            "num_cities": city_count,
                        }
                    else:
                        stats = benchmark_algorithm(algo_func, cities, distances, home_city, num_runs)
                        print(f"    {algo_name}: Avg time = {stats['avg_time']:.2f} ms, Route length = {stats['route_length']:.2f}")
                except Exception as e:
                    print(f"    Error running {algo_name} with {city_count} cities: {e}")
                    stats = {
                        "min_time": None,
                        "max_time": None,
                        "avg_time": None,
                        "median_time": None,
                        "std_dev": None,
                        "route_length": None,
                        "num_cities": city_count,
                        "error": str(e)
                    }
                
                # Store results
                if city_count not in round_results["data"]:
                    round_results["data"][city_count] = {}
                round_results["data"][city_count][algo_name] = stats
        
        # Add round results
        results["rounds"].append(round_results)
        
        # Save intermediate results after each round
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        save_results_to_csv(results, f"tsp_benchmark_round{round_num}_{timestamp}.csv")
    
    return results

def save_results_to_csv(results, filename):
    """
    Save benchmark results to a CSV file.
    
    Args:
        results: Dictionary with benchmark results
        filename: Output filename
    """
    # Create full path
    filepath = os.path.join(os.path.dirname(__file__), filename)
    
    with open(filepath, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        
        # Write header
        header = ["Round", "Cities", "Algorithm", "Avg Time (ms)", "Min Time (ms)", 
                  "Max Time (ms)", "Median Time (ms)", "Std Dev", "Route Length"]
        writer.writerow(header)
        
        # Write data
        for round_data in results["rounds"]:
            round_num = round_data["round"]
            for city_count, algo_results in round_data["data"].items():
                for algo_name, stats in algo_results.items():
                    row = [
                        round_num,
                        city_count,
                        algo_name,
                        stats["avg_time"],
                        stats["min_time"],
                        stats["max_time"],
                        stats["median_time"],
                        stats["std_dev"],
                        stats["route_length"]
                    ]
                    writer.writerow(row)
    
    print(f"Results saved to {filepath}")
    return filepath

def create_performance_charts(results, save_dir=None):
    """
    Create performance charts from benchmark results.
    
    Args:
        results: Dictionary with benchmark results
        save_dir: Directory to save charts (optional)
    """
    if not HAS_MATPLOTLIB:
        print("Matplotlib not installed. Skipping chart generation.")
        return
    
    if save_dir is None:
        save_dir = os.path.dirname(__file__)
    
    # Prepare data for plotting
    city_counts = results["city_counts"]
    algorithms = results["algorithms"]
    
    # Create a dictionary to hold average times across all rounds
    avg_times = {algo: [0 for _ in city_counts] for algo in algorithms}
    avg_lengths = {algo: [0 for _ in city_counts] for algo in algorithms}
    count_valid = {algo: [0 for _ in city_counts] for algo in algorithms}
    
    # Calculate averages across all rounds
    for round_data in results["rounds"]:
        for i, city_count in enumerate(city_counts):
            if city_count in round_data["data"]:
                for algo in algorithms:
                    if algo in round_data["data"][city_count]:
                        stats = round_data["data"][city_count][algo]
                        if stats["avg_time"] is not None:
                            avg_times[algo][i] += stats["avg_time"]
                            avg_lengths[algo][i] += stats["route_length"]
                            count_valid[algo][i] += 1
    
    # Calculate final averages
    for algo in algorithms:
        for i in range(len(city_counts)):
            if count_valid[algo][i] > 0:
                avg_times[algo][i] /= count_valid[algo][i]
                avg_lengths[algo][i] /= count_valid[algo][i]
            else:
                avg_times[algo][i] = float('nan')
                avg_lengths[algo][i] = float('nan')
    
    # Create execution time chart
    plt.figure(figsize=(12, 8))
    colors = ['r', 'g', 'b']
    markers = ['o', 's', '^']
    
    for i, algo in enumerate(algorithms):
        plt.plot(city_counts, avg_times[algo], 
                 marker=markers[i], 
                 color=colors[i], 
                 label=algo,
                 linewidth=2,
                 markersize=8)
    
    plt.title('TSP Algorithm Performance Comparison', fontsize=16)
    plt.xlabel('Number of Cities', fontsize=14)
    plt.ylabel('Average Execution Time (ms)', fontsize=14)
    plt.grid(True, alpha=0.3)
    plt.legend(fontsize=12)
    plt.yscale('log')  # Logarithmic scale helps when there are big differences
    
    # Add text annotations with exact times
    for i, algo in enumerate(algorithms):
        for j, city_count in enumerate(city_counts):
            if not np.isnan(avg_times[algo][j]):
                plt.annotate(f'{avg_times[algo][j]:.1f}', 
                             (city_counts[j], avg_times[algo][j]),
                             textcoords="offset points",
                             xytext=(0, 10),
                             ha='center',
                             fontsize=8)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    time_chart_path = os.path.join(save_dir, f'tsp_execution_times_{timestamp}.png')
    plt.savefig(time_chart_path, dpi=300, bbox_inches='tight')
    print(f"Time chart saved to {time_chart_path}")
    
    # Create route length comparison chart
    plt.figure(figsize=(12, 8))
    
    for i, algo in enumerate(algorithms):
        plt.plot(city_counts, avg_lengths[algo], 
                 marker=markers[i], 
                 color=colors[i], 
                 label=algo,
                 linewidth=2,
                 markersize=8)
    
    plt.title('TSP Algorithm Route Length Comparison', fontsize=16)
    plt.xlabel('Number of Cities', fontsize=14)
    plt.ylabel('Average Route Length', fontsize=14)
    plt.grid(True, alpha=0.3)
    plt.legend(fontsize=12)
    
    length_chart_path = os.path.join(save_dir, f'tsp_route_lengths_{timestamp}.png')
    plt.savefig(length_chart_path, dpi=300, bbox_inches='tight')
    print(f"Length chart saved to {length_chart_path}")
    
    # Create time vs. optimality chart (normalized)
    plt.figure(figsize=(12, 8))
    
    x_data = []
    y_data = []
    colors_data = []
    sizes_data = []
    labels = []
    
    for i, algo in enumerate(algorithms):
        for j, city_count in enumerate(city_counts):
            if (not np.isnan(avg_times[algo][j]) and 
                not np.isnan(avg_lengths[algo][j]) and 
                avg_lengths["Brute Force"][j] > 0):
                
                # Only add if we have all the data needed
                if not np.isnan(avg_lengths["Brute Force"][j]):
                    x_data.append(avg_times[algo][j])
                    
                    # Calculate how close this solution is to the optimal (brute force)
                    optimality = avg_lengths[algo][j] / avg_lengths["Brute Force"][j]
                    y_data.append(optimality)
                    
                    colors_data.append(colors[i])
                    sizes_data.append(50 + city_count * 5)  # Size represents city count
                    labels.append(f"{algo} ({city_count} cities)")
    
    # Create the scatter plot
    if x_data:  # Only create if we have valid data
        plt.scatter(x_data, y_data, c=colors_data, s=sizes_data, alpha=0.7)
        
        for i, label in enumerate(labels):
            plt.annotate(label, (x_data[i], y_data[i]), fontsize=8)
            
        plt.title('Time-Optimality Tradeoff', fontsize=16)
        plt.xlabel('Execution Time (ms)', fontsize=14)
        plt.ylabel('Route Length Ratio (Algorithm / Optimal)', fontsize=14)
        plt.grid(True, alpha=0.3)
        plt.xscale('log')
        
        tradeoff_chart_path = os.path.join(save_dir, f'tsp_time_optimality_tradeoff_{timestamp}.png')
        plt.savefig(tradeoff_chart_path, dpi=300, bbox_inches='tight')
        print(f"Tradeoff chart saved to {tradeoff_chart_path}")

def main():
    """Main function to run benchmarks and generate charts."""
    print("TSP Algorithm Performance Benchmark")
    print("==================================")
    
    # Set up parameters
    city_counts = [4, 5, 6, 7, 8, 9, 10, 11]  # Default city counts to test
    num_runs = 3      # Number of runs per algorithm (for averaging)
    num_rounds = 10   # Number of game rounds (different city configurations)
    
    # Run benchmarks
    results = run_benchmarks(city_counts, num_runs, num_rounds)
    
    # Save final results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_path = save_results_to_csv(results, f"tsp_benchmark_final_{timestamp}.csv")
    
    # Generate charts
    create_performance_charts(results)
    
    print("\nBenchmark complete!")
    print(f"Results saved to {csv_path}")

if __name__ == "__main__":
    main()