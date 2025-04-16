"""
City selection interface for the Traveling Salesman Problem game
"""
import tkinter as tk
from tkinter import ttk, messagebox
import logging
import traceback

logger = logging.getLogger("CitySelection")

class CitySelectionFrame(ttk.Frame):
    def __init__(self, parent, game_state):
        logger.info("Initializing CitySelectionFrame")
        super().__init__(parent, padding="10")
        self.game_state = game_state
        self.city_vars = {}
        
        # Setup the frame
        try:
            self.create_widgets()
            logger.info("CitySelectionFrame initialized successfully")
        except Exception as e:
            logger.error(f"Error in CitySelectionFrame initialization: {str(e)}")
            logger.error(traceback.format_exc())
            messagebox.showerror("Initialization Error", f"Error setting up city selection: {str(e)}")
            raise
        
    def create_widgets(self):
        """Create the widgets for city selection"""
        logger.debug("Creating widgets for CitySelectionFrame")
        # Title
        ttk.Label(self, text="Select Cities to Visit", font=("Arial", 12, "bold")).grid(
            row=0, column=0, columnspan=5, sticky=tk.W, pady=5)
        
        # Information
        ttk.Label(self, text="Check the cities you want to visit (must select at least 2):").grid(
            row=1, column=0, columnspan=5, sticky=tk.W, pady=5)
            
        # City selection area (will be populated dynamically)
        self.city_frame = ttk.Frame(self)
        self.city_frame.grid(row=2, column=0, columnspan=5, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Button area
        self.button_frame = ttk.Frame(self)
        self.button_frame.grid(row=3, column=0, columnspan=5, sticky=(tk.W, tk.E), pady=10)
        
        ttk.Button(self.button_frame, text="Calculate Routes", command=self.calculate_routes).pack(side=tk.RIGHT)
        ttk.Button(self.button_frame, text="Select All", command=self.select_all_cities).pack(side=tk.RIGHT, padx=5)
        ttk.Button(self.button_frame, text="Clear Selection", command=self.clear_selection).pack(side=tk.RIGHT)
        
        # Create a canvas for the distance matrix display
        self.matrix_frame = ttk.LabelFrame(self, text="Distance Matrix")
        self.matrix_frame.grid(row=4, column=0, columnspan=5, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        
        self.canvas = tk.Canvas(self.matrix_frame, width=600, height=300)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(self.matrix_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        self.matrix_inner_frame = ttk.Frame(self.canvas)
        self.canvas_window = self.canvas.create_window((0, 0), window=self.matrix_inner_frame, anchor=tk.NW)
        
        self.matrix_inner_frame.bind("<Configure>", self._on_frame_configure)
        self.canvas.bind("<Configure>", self._on_canvas_configure)
        
        # Make frame expandable
        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(4, weight=1)
        logger.debug("Widgets created successfully")
    
    def _on_frame_configure(self, event=None):
        """Reset the scroll region to encompass the inner frame"""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
    def _on_canvas_configure(self, event=None):
        """When canvas is resized, resize the inner frame to match"""
        if event:
            canvas_width = event.width
            self.canvas.itemconfig(self.canvas_window, width=canvas_width)
    
    def update_cities_display(self):
        """Update the city selection checkboxes based on game state"""
        logger.debug("Updating city selection checkboxes")
        # Clear existing widgets
        for widget in self.city_frame.winfo_children():
            widget.destroy()
        
        self.city_vars = {}
        
        # Get cities from the game state
        cities = self.game_state.city_map.get_cities()
        home_city = self.game_state.home_city
        
        # Create checkboxes for each city except home
        cols = 5
        for i, city in enumerate(cities):
            row, col = divmod(i, cols)
            
            # Create a variable to track checkbox state
            var = tk.BooleanVar(value=False)
            self.city_vars[city] = var
            
            # If this is the home city, disable selection and mark special
            if city == home_city:
                cb = ttk.Checkbutton(self.city_frame, text=f"{city} (Home)", state="disabled")
                cb.grid(row=row, column=col, sticky=tk.W, padx=5, pady=2)
            else:
                cb = ttk.Checkbutton(self.city_frame, text=city, variable=var)
                cb.grid(row=row, column=col, sticky=tk.W, padx=5, pady=2)
        
        # Update the distance matrix display
        self.update_distance_matrix()
        logger.debug("City selection checkboxes updated")
    
    def update_distance_matrix(self):
        """Display the distance matrix in the UI"""
        logger.debug("Updating distance matrix display")
        # Clear existing widgets
        for widget in self.matrix_inner_frame.winfo_children():
            widget.destroy()
        
        # Get the distance matrix from the game state
        cities = self.game_state.city_map.get_cities()
        distances = self.game_state.city_map.get_distances()
        
        # Create the matrix header row
        ttk.Label(self.matrix_inner_frame, text="").grid(row=0, column=0)
        for i, city in enumerate(cities):
            ttk.Label(self.matrix_inner_frame, text=city, font=("Arial", 9, "bold")).grid(row=0, column=i+1, padx=2, pady=2)
        
        # Create the matrix with distances
        for i, city1 in enumerate(cities):
            ttk.Label(self.matrix_inner_frame, text=city1, font=("Arial", 9, "bold")).grid(row=i+1, column=0, padx=2, pady=2)
            
            for j, city2 in enumerate(cities):
                if city1 == city2:
                    ttk.Label(self.matrix_inner_frame, text="---").grid(row=i+1, column=j+1, padx=2, pady=2)
                else:
                    distance = distances.get((city1, city2)) or distances.get((city2, city1))
                    ttk.Label(self.matrix_inner_frame, text=str(distance)).grid(row=i+1, column=j+1, padx=2, pady=2)
        logger.debug("Distance matrix display updated")
    
    def select_all_cities(self):
        """Select all available cities"""
        logger.debug("Selecting all cities")
        home_city = self.game_state.home_city
        for city, var in self.city_vars.items():
            if city != home_city:
                var.set(True)
        logger.debug("All cities selected")
    
    def clear_selection(self):
        """Clear all city selections"""
        logger.debug("Clearing all city selections")
        for var in self.city_vars.values():
            var.set(False)
        logger.debug("All city selections cleared")
    
    def calculate_routes(self):
        """Start the route calculation process"""
        logger.info("Starting route calculation process")
        # Get the selected cities
        selected_cities = [city for city, var in self.city_vars.items() if var.get()]
        
        # Add the home city
        selected_cities.append(self.game_state.home_city)
        
        # Check if enough cities are selected
        if len(selected_cities) < 3:  # Home + at least 2 more
            logger.error("Not enough cities selected for route calculation")
            messagebox.showerror("Error", "Please select at least 2 cities to visit!")
            return
        
        # Set the selected cities in the game state
        self.game_state.selected_cities = selected_cities
        
        # Start the calculation in the parent window
        self.master.master.results_display.calculate_and_display_routes()
        logger.info("Route calculation process started")