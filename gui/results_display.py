"""
Results display for the Traveling Salesman Problem game
"""
import tkinter as tk
from tkinter import ttk, messagebox
import time
import logging
import traceback
from core.route_calculator import RouteCalculator
from database.db_manager import DatabaseManager
from utils.timer import Timer

logger = logging.getLogger("ResultsDisplay")

# Try importing matplotlib, but handle it gracefully if it fails
try:
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    MATPLOTLIB_AVAILABLE = True
    logger.info("Matplotlib successfully imported")
except ImportError as e:
    MATPLOTLIB_AVAILABLE = False
    logger.warning(f"Matplotlib import failed: {e}. Visualizations will be disabled.")
    print("Warning: Matplotlib not available. Visualizations will be disabled.")

class ResultsDisplayFrame(ttk.Frame):
    def __init__(self, parent, game_state):
        logger.info("Initializing ResultsDisplayFrame")
        try:
            super().__init__(parent, padding="10")
            self.game_state = game_state
            self.route_calculator = RouteCalculator()
            self.db_manager = DatabaseManager()
            self.timer = Timer()
            
            self.create_widgets()
            logger.info("ResultsDisplayFrame initialized successfully")
        except Exception as e:
            logger.error(f"Error in ResultsDisplayFrame initialization: {str(e)}")
            logger.error(traceback.format_exc())
            messagebox.showerror("Initialization Error", f"Error setting up results display: {str(e)}")
            raise
    
    def create_widgets(self):
        """Create the widgets for results display"""
        # Title
        ttk.Label(self, text="Route Calculation Results", font=("Arial", 12, "bold")).grid(
            row=0, column=0, columnspan=2, sticky=tk.W, pady=5)
        
        # Create a notebook with tabs for each algorithm
        self.notebook = ttk.Notebook(self)
        self.notebook.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        # Create frames for each algorithm tab
        self.brute_force_frame = ttk.Frame(self.notebook, padding=10)
        self.nearest_neighbor_frame = ttk.Frame(self.notebook, padding=10)
        self.dynamic_programming_frame = ttk.Frame(self.notebook, padding=10)
        self.comparison_frame = ttk.Frame(self.notebook, padding=10)
        
        self.notebook.add(self.brute_force_frame, text="Brute Force")
        self.notebook.add(self.nearest_neighbor_frame, text="Nearest Neighbor")
        self.notebook.add(self.dynamic_programming_frame, text="Dynamic Programming")
        self.notebook.add(self.comparison_frame, text="Comparison")
        
        # Setup each algorithm tab
        self.setup_algorithm_tab(self.brute_force_frame, "Brute Force")
        self.setup_algorithm_tab(self.nearest_neighbor_frame, "Nearest Neighbor")
        self.setup_algorithm_tab(self.dynamic_programming_frame, "Dynamic Programming")
        self.setup_comparison_tab()
        
        # User interaction area
        ttk.Label(self, text="Select what you think is the shortest route:").grid(
            row=2, column=0, sticky=tk.W, pady=(10, 5))
        
        self.user_choice = tk.StringVar()
        algorithms = ["Brute Force", "Nearest Neighbor", "Dynamic Programming"]
        self.choice_dropdown = ttk.Combobox(self, textvariable=self.user_choice, values=algorithms, state="readonly")
        self.choice_dropdown.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=(10, 5))
        
        ttk.Button(self, text="Submit Answer", command=self.check_answer).grid(
            row=3, column=0, columnspan=2, sticky=tk.E, pady=5)
        
        # Make frame expandable
        self.columnconfigure(1, weight=1)
        self.rowconfigure(1, weight=1)
    
    def setup_algorithm_tab(self, tab_frame, algorithm_name):
        """Set up a tab for an algorithm"""
        # Results text area
        result_text = tk.Text(tab_frame, height=10, width=60, wrap=tk.WORD)
        result_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        scrollbar = ttk.Scrollbar(tab_frame, orient=tk.VERTICAL, command=result_text.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        result_text.configure(yscrollcommand=scrollbar.set)
        
        # Make the tab expandable
        tab_frame.columnconfigure(0, weight=1)
        tab_frame.rowconfigure(0, weight=1)
        
        # Store text reference
        if algorithm_name == "Brute Force":
            self.brute_force_text = result_text
        elif algorithm_name == "Nearest Neighbor":
            self.nearest_neighbor_text = result_text
        else:  # Dynamic Programming
            self.dynamic_programming_text = result_text
        
        # Only create visualization if matplotlib is available
        if MATPLOTLIB_AVAILABLE:
            # Figure for route visualization
            figure_frame = ttk.Frame(tab_frame)
            figure_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
            
            try:
                fig = plt.Figure(figsize=(6, 4))
                canvas = FigureCanvasTkAgg(fig, figure_frame)
                canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
                
                # Store references
                if algorithm_name == "Brute Force":
                    self.brute_force_fig = fig
                    self.brute_force_canvas = canvas
                elif algorithm_name == "Nearest Neighbor":
                    self.nearest_neighbor_fig = fig
                    self.nearest_neighbor_canvas = canvas
                else:  # Dynamic Programming
                    self.dynamic_programming_fig = fig
                    self.dynamic_programming_canvas = canvas
            except Exception as e:
                print(f"Error creating matplotlib figure: {e}")
                error_label = ttk.Label(figure_frame, text="Visualization unavailable. Install matplotlib for route visualization.")
                error_label.pack(pady=20)
        else:
            # Display message if matplotlib is not available
            info_label = ttk.Label(
                tab_frame, 
                text="Matplotlib is not available. Install it to see route visualizations.",
                foreground="red"
            )
            info_label.grid(row=1, column=0, columnspan=2, pady=20)
        
    def setup_comparison_tab(self):
        """Set up the comparison tab"""
        comparison_frame = ttk.Frame(self.comparison_frame)
        comparison_frame.pack(fill=tk.BOTH, expand=True)
        
        # Table for algorithm comparison
        columns = ('algorithm', 'route_length', 'time', 'complexity')
        self.comparison_tree = ttk.Treeview(comparison_frame, columns=columns, show='headings')
        
        self.comparison_tree.heading('algorithm', text='Algorithm')
        self.comparison_tree.heading('route_length', text='Route Length')
        self.comparison_tree.heading('time', text='Time (ms)')
        self.comparison_tree.heading('complexity', text='Time Complexity')
        
        self.comparison_tree.column('algorithm', width=150)
        self.comparison_tree.column('route_length', width=100)
        self.comparison_tree.column('time', width=100)
        self.comparison_tree.column('complexity', width=150)
        
        self.comparison_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(comparison_frame, orient=tk.VERTICAL, command=self.comparison_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.comparison_tree.configure(yscroll=scrollbar.set)
        
        # Only create visualization if matplotlib is available
        if MATPLOTLIB_AVAILABLE:
            # Figure for comparison visualization
            fig_frame = ttk.Frame(self.comparison_frame)
            fig_frame.pack(fill=tk.BOTH, expand=True, pady=10)
            
            try:
                self.comparison_fig = plt.Figure(figsize=(6, 4))
                self.comparison_canvas = FigureCanvasTkAgg(self.comparison_fig, fig_frame)
                self.comparison_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            except Exception as e:
                print(f"Error creating comparison figure: {e}")
                error_label = ttk.Label(fig_frame, text="Chart visualization unavailable. Install matplotlib for visual comparisons.")
                error_label.pack(pady=20)
        else:
            # Display message if matplotlib is not available
            info_label = ttk.Label(
                self.comparison_frame, 
                text="Matplotlib is not available. Install it to see algorithm performance comparisons graphically.",
                foreground="red"
            )
            info_label.pack(pady=20)
    
    def clear_results(self):
        """Clear all result displays"""
        # Clear text areas
        if hasattr(self, 'brute_force_text'):
            self.brute_force_text.delete(1.0, tk.END)
            self.nearest_neighbor_text.delete(1.0, tk.END)
            self.dynamic_programming_text.delete(1.0, tk.END)
        
        # Clear figures only if matplotlib is available
        if MATPLOTLIB_AVAILABLE and hasattr(self, 'brute_force_fig'):
            try:
                self.brute_force_fig.clear()
                self.nearest_neighbor_fig.clear()
                self.dynamic_programming_fig.clear()
                self.comparison_fig.clear()
                
                self.brute_force_canvas.draw()
                self.nearest_neighbor_canvas.draw()
                self.dynamic_programming_canvas.draw()
                self.comparison_canvas.draw()
            except Exception as e:
                print(f"Error clearing matplotlib figures: {e}")
        
        # Clear comparison tree
        if hasattr(self, 'comparison_tree'):
            for item in self.comparison_tree.get_children():
                self.comparison_tree.delete(item)
        
        # Reset user choice
        if hasattr(self, 'user_choice'):
            self.user_choice.set('')
    
    def calculate_and_display_routes(self):
        """Calculate and display routes using all algorithms"""
        if not self.game_state.selected_cities:
            messagebox.showerror("Error", "No cities selected!")
            return
        
        # Get necessary data
        cities = self.game_state.selected_cities
        distances = self.game_state.city_map.get_distances()
        home_city = self.game_state.home_city
        
        # Dictionary to store results
        results = {}
        
        # Calculate using brute force
        self.timer.start()
        brute_force_route, brute_force_length = self.route_calculator.brute_force(
            cities, distances, home_city)
        brute_force_time = self.timer.stop()
        
        results["Brute Force"] = {
            "route": brute_force_route,
            "length": brute_force_length,
            "time": brute_force_time,
            "complexity": "O(n!)"
        }
        
        # Calculate using nearest neighbor
        self.timer.start()
        nearest_neighbor_route, nearest_neighbor_length = self.route_calculator.nearest_neighbor(
            cities, distances, home_city)
        nearest_neighbor_time = self.timer.stop()
        
        results["Nearest Neighbor"] = {
            "route": nearest_neighbor_route,
            "length": nearest_neighbor_length,
            "time": nearest_neighbor_time,
            "complexity": "O(n²)"
        }
        
        # Calculate using dynamic programming
        self.timer.start()
        dp_route, dp_length = self.route_calculator.dynamic_programming(
            cities, distances, home_city)
        dp_time = self.timer.stop()
        
        results["Dynamic Programming"] = {
            "route": dp_route,
            "length": dp_length,
            "time": dp_time,
            "complexity": "O(n²2ⁿ)"
        }
        
        # Store results in game state
        self.game_state.algorithm_results = results
        
        # Find the algorithm with the shortest route
        min_length = float('inf')
        self.shortest_algorithm = None
        
        for algo, result in results.items():
            if result["length"] < min_length:
                min_length = result["length"]
                self.shortest_algorithm = algo
        
        # Display results
        self.display_algorithm_results("Brute Force", results["Brute Force"])
        self.display_algorithm_results("Nearest Neighbor", results["Nearest Neighbor"])
        self.display_algorithm_results("Dynamic Programming", results["Dynamic Programming"])
        self.display_comparison(results)
    
    def display_algorithm_results(self, algorithm_name, result):
        """Display results for a specific algorithm"""
        # Get the appropriate text widget
        if algorithm_name == "Brute Force":
            text_widget = self.brute_force_text
            if MATPLOTLIB_AVAILABLE:
                fig = self.brute_force_fig
                canvas = self.brute_force_canvas
        elif algorithm_name == "Nearest Neighbor":
            text_widget = self.nearest_neighbor_text
            if MATPLOTLIB_AVAILABLE:
                fig = self.nearest_neighbor_fig
                canvas = self.nearest_neighbor_canvas
        else:  # Dynamic Programming
            text_widget = self.dynamic_programming_text
            if MATPLOTLIB_AVAILABLE:
                fig = self.dynamic_programming_fig
                canvas = self.dynamic_programming_canvas
        
        # Clear previous content
        text_widget.delete(1.0, tk.END)
        
        # Add result information
        text_widget.insert(tk.END, f"Algorithm: {algorithm_name}\n\n")
        text_widget.insert(tk.END, f"Route: {' -> '.join(result['route'])}\n\n")
        text_widget.insert(tk.END, f"Total Distance: {result['length']} km\n\n")
        text_widget.insert(tk.END, f"Calculation Time: {result['time']:.4f} ms\n\n")
        text_widget.insert(tk.END, f"Time Complexity: {result['complexity']}\n\n")
        
        # Highlight if this is the shortest route
        if algorithm_name == self.shortest_algorithm:
            text_widget.insert(tk.END, "THIS IS THE SHORTEST ROUTE!\n", "highlight")
            text_widget.tag_configure("highlight", background="yellow", font=("Arial", 10, "bold"))
        
        # Visualize the route only if matplotlib is available
        if MATPLOTLIB_AVAILABLE:
            try:
                fig.clear()
                self.visualize_route(fig, result['route'], self.game_state.city_map.get_city_positions())
                canvas.draw()
            except Exception as e:
                print(f"Error visualizing route: {e}")
    
    def visualize_route(self, fig, route, city_positions):
        """Visualize the route on the figure"""
        ax = fig.add_subplot(111)
        
        # Plot city positions
        x_coords = [city_positions[city][0] for city in route]
        y_coords = [city_positions[city][1] for city in route]
        
        # Create a complete loop by adding the first city at the end
        x_coords.append(x_coords[0])
        y_coords.append(y_coords[0])
        
        # Plot cities
        ax.scatter(x_coords[:-1], y_coords[:-1], color='blue')
        
        # Mark home city
        home_index = route.index(self.game_state.home_city)
        ax.scatter(x_coords[home_index], y_coords[home_index], color='red', s=100, marker='*')
        
        # Plot route
        ax.plot(x_coords, y_coords, 'k-')
        
        # Add city labels
        for i, city in enumerate(route):
            ax.annotate(city, (x_coords[i], y_coords[i]), textcoords="offset points", 
                        xytext=(0, 5), ha='center')
        
        ax.set_title("Route Visualization")
        ax.set_xlabel("X Coordinate")
        ax.set_ylabel("Y Coordinate")
        ax.grid(True)

    def display_comparison(self, results):
        """Display comparison of all algorithms"""
        # Clear previous entries
        for item in self.comparison_tree.get_children():
            self.comparison_tree.delete(item)
        
        # Add results to the comparison table
        for algo, result in results.items():
            # Highlight the shortest route
            tags = ("shortest",) if algo == self.shortest_algorithm else ()
            
            self.comparison_tree.insert('', tk.END, values=(
                algo,
                f"{result['length']:.2f} km",
                f"{result['time']:.4f} ms",
                result['complexity']
            ), tags=tags)
        
        # Configure tag for highlighting
        self.comparison_tree.tag_configure("shortest", background="light green")
        
        # Create bar chart comparison only if matplotlib is available
        if MATPLOTLIB_AVAILABLE and hasattr(self, 'comparison_fig') and hasattr(self, 'comparison_canvas'):
            try:
                self.comparison_fig.clear()
                ax = self.comparison_fig.add_subplot(111)
                
                algorithms = list(results.keys())
                lengths = [results[algo]["length"] for algo in algorithms]
                times = [results[algo]["time"] for algo in algorithms]
                
                # Create grouped bar chart
                x = range(len(algorithms))
                width = 0.35
                
                # Create two separate y-axes for different scales
                ax.bar(x, lengths, width, label='Route Length (km)')
                ax.set_ylabel('Route Length (km)')
                ax.set_xlabel('Algorithm')
                ax.set_xticks(x)
                ax.set_xticklabels(algorithms)
                
                # Twin axis for time
                ax2 = ax.twinx()
                ax2.bar([i + width for i in x], times, width, color='orange', label='Time (ms)')
                ax2.set_ylabel('Time (ms)')
                
                # Add legend
                lines1, labels1 = ax.get_legend_handles_labels()
                lines2, labels2 = ax2.get_legend_handles_labels()
                ax.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
                
                self.comparison_fig.tight_layout()
                self.comparison_canvas.draw()
            except Exception as e:
                print(f"Error creating comparison chart: {e}")

    def check_answer(self):
        """Check the user's answer and record in database if correct"""
        if not self.user_choice.get():
            messagebox.showerror("Error", "Please select an algorithm first!")
            return
        
        if not hasattr(self, 'shortest_algorithm'):
            messagebox.showerror("Error", "No routes have been calculated yet!")
            return
        
        user_choice = self.user_choice.get()
        
        if user_choice == self.shortest_algorithm:
            messagebox.showinfo("Correct!", 
                               f"Congratulations! {user_choice} is indeed the algorithm that found the shortest route.")
            
            # Save the result in the database
            self.save_result_to_database(user_choice)
        else:
            messagebox.showinfo("Incorrect", 
                               f"Sorry, that's not correct. The {self.shortest_algorithm} algorithm found the shortest route.")
    
    def save_result_to_database(self, algorithm):
        """Save the successful game result to the database"""
        player_name = self.game_state.player_name
        home_city = self.game_state.home_city
        cities_visited = len(self.game_state.selected_cities)
        route = self.game_state.algorithm_results[algorithm]["route"]
        route_length = self.game_state.algorithm_results[algorithm]["length"]
        time_taken = self.game_state.algorithm_results[algorithm]["time"]
        
        self.db_manager.save_game_result(
            player_name=player_name,
            home_city=home_city,
            cities_visited=cities_visited,
            route=route,
            route_length=route_length,
            algorithm=algorithm,
            execution_time=time_taken
        )
        
        messagebox.showinfo("Saved", "Your result has been saved to the high scores!")