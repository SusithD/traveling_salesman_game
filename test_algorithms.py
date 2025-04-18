from core.route_calculator import RouteCalculator
import time

def test_algorithms_with_known_data():
    print("Testing TSP Algorithms with a known dataset")
    print("=" * 50)
    
    cities = ["A", "B", "C", "D", "E"]
    home_city = "A"
    
    distances = {
        ("A", "B"): 10,
        ("A", "C"): 20,
        ("A", "D"): 30, 
        ("A", "E"): 40,
        ("B", "C"): 10,
        ("B", "D"): 25,
        ("B", "E"): 30,
        ("C", "D"): 10,
        ("C", "E"): 20,
        ("D", "E"): 10,
    }
    
    calculator = RouteCalculator()
    
    start_time = time.time()
    bf_route, bf_length = calculator.brute_force(cities, distances, home_city)
    bf_time = (time.time() - start_time) * 1000
    
    start_time = time.time()
    nn_route, nn_length = calculator.nearest_neighbor(cities, distances, home_city)
    nn_time = (time.time() - start_time) * 1000
    
    start_time = time.time()
    dp_route, dp_length = calculator.dynamic_programming(cities, distances, home_city)
    dp_time = (time.time() - start_time) * 1000
    
    print(f"Brute Force:        {bf_route} | Length: {bf_length} | Time: {bf_time:.4f}ms")
    print(f"Nearest Neighbor:   {nn_route} | Length: {nn_length} | Time: {nn_time:.4f}ms")
    print(f"Dynamic Programming: {dp_route} | Length: {dp_length} | Time: {dp_time:.4f}ms")
    print("\n")
    
    if bf_length <= nn_length and bf_length <= dp_length:
        print("Brute Force found the shortest route (expected for small datasets)")
    elif nn_length <= bf_length and nn_length <= dp_length:
        print("Nearest Neighbor found the shortest route (unexpected for general cases)")
    elif dp_length <= bf_length and dp_length <= nn_length:
        print("Dynamic Programming found the shortest route (expected)")
    
    print("\nTesting with a dataset where nearest neighbor is non-optimal")
    print("=" * 50)
    
    cities2 = ["A", "B", "C", "D", "E"]
    distances2 = {
        ("A", "B"): 10,
        ("A", "C"): 15,
        ("A", "D"): 20,
        ("A", "E"): 15,
        ("B", "C"): 5,
        ("B", "D"): 30,
        ("B", "E"): 25,
        ("C", "D"): 30,
        ("C", "E"): 25,
        ("D", "E"): 10,
    }
    
    start_time = time.time()
    bf_route2, bf_length2 = calculator.brute_force(cities2, distances2, home_city)
    bf_time2 = (time.time() - start_time) * 1000
    
    start_time = time.time()
    nn_route2, nn_length2 = calculator.nearest_neighbor(cities2, distances2, home_city)
    nn_time2 = (time.time() - start_time) * 1000
    
    start_time = time.time()
    dp_route2, dp_length2 = calculator.dynamic_programming(cities2, distances2, home_city)
    dp_time2 = (time.time() - start_time) * 1000
    
    print(f"Brute Force:        {bf_route2} | Length: {bf_length2} | Time: {bf_time2:.4f}ms")
    print(f"Nearest Neighbor:   {nn_route2} | Length: {nn_length2} | Time: {nn_time2:.4f}ms")
    print(f"Dynamic Programming: {dp_route2} | Length: {dp_length2} | Time: {dp_time2:.4f}ms")
    
    print("\nDifference between shortest (optimal) and Nearest Neighbor: {:.2f}%".format(
        ((nn_length2 / min(bf_length2, dp_length2)) - 1) * 100
    ))

if __name__ == "__main__":
    test_algorithms_with_known_data()
