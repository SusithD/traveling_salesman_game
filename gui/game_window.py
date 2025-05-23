"""
Main game window for the Traveling Salesman Problem game
"""
import tkinter as tk
from tkinter import ttk, messagebox
import sys
from gui.city_selection import CitySelectionFrame
from gui.results_display import ResultsDisplayFrame
from core.game_state import GameState
from core.city_map import CityMap
from database.db_manager import DatabaseManager

class GameWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Traveling Salesman Problem Game")
        self.root.geometry("1000x700")
        self.root.resizable(True, True)
        
        self.db_manager = DatabaseManager()
        self.game_state = GameState()
        self.city_map = CityMap()
        
        self.create_menu()
        self.create_frames()
        self.setup_layout()
        
        # Player info frame
        self.player_frame = ttk.Frame(self.root, padding="10")
        self.player_frame.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        ttk.Label(self.player_frame, text="Player Name:").grid(row=0, column=0, sticky=tk.W)
        self.player_name = tk.StringVar()
        ttk.Entry(self.player_frame, textvariable=self.player_name).grid(row=0, column=1, sticky=(tk.W, tk.E))
        
        ttk.Button(self.player_frame, text="Start New Game", command=self.start_new_game).grid(row=0, column=2, padx=5)

    def create_menu(self):
        """Create the main menu"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        game_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Game", menu=game_menu)
        game_menu.add_command(label="New Game", command=self.start_new_game)
        game_menu.add_command(label="View High Scores", command=self.view_high_scores)
        game_menu.add_separator()
        game_menu.add_command(label="Exit", command=self.root.quit)
        
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="Rules", command=self.show_rules)
        help_menu.add_command(label="About", command=self.show_about)

    def create_frames(self):
        """Create the main frames for the application"""
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)
        
        self.city_selection = CitySelectionFrame(self.main_frame, self.game_state)
        self.results_display = ResultsDisplayFrame(self.main_frame, self.game_state)

    def setup_layout(self):
        """Set up the layout of frames"""
        self.city_selection.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.results_display.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(0, weight=1)
        self.main_frame.rowconfigure(1, weight=1)

    def start_new_game(self):
        """Start a new game round"""
        if not self.player_name.get().strip():
            messagebox.showerror("Error", "Please enter your name first!")
            return
            
        self.game_state.player_name = self.player_name.get()
        self.city_map.generate_cities_and_distances()
        self.game_state.set_city_map(self.city_map)
        self.game_state.home_city = self.city_map.select_random_home_city()
        
        self.city_selection.update_cities_display()
        self.results_display.clear_results()
        
        messagebox.showinfo("New Game", f"A new game has started!\nYour home city is {self.game_state.home_city}")

    def view_high_scores(self):
        """Show high scores from the database"""
        high_scores = self.db_manager.get_high_scores()
        
        if not high_scores:
            messagebox.showinfo("High Scores", "No high scores yet!")
            return
            
        score_window = tk.Toplevel(self.root)
        score_window.title("High Scores")
        score_window.geometry("600x400")
        
        columns = ('name', 'home_city', 'cities_visited', 'route_length', 'algorithm', 'time')
        tree = ttk.Treeview(score_window, columns=columns, show='headings')
        
        tree.heading('name', text='Player')
        tree.heading('home_city', text='Home City')
        tree.heading('cities_visited', text='Cities Visited')
        tree.heading('route_length', text='Route Length')
        tree.heading('algorithm', text='Algorithm')
        tree.heading('time', text='Time (ms)')
        
        for score in high_scores:
            tree.insert('', tk.END, values=score)
            
        tree.pack(fill='both', expand=True)
        
        scrollbar = ttk.Scrollbar(score_window, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def show_rules(self):
        """Display game rules"""
        rules = """
        Traveling Salesman Problem Game Rules:
        
        1. You will be assigned a random home city.
        2. Select cities you wish to visit by checking the boxes.
        3. Try to find the shortest route that visits all selected cities and returns home.
        4. The game will calculate the shortest route using three different algorithms.
        5. Your score is saved when you correctly identify the shortest route.
        
        Good luck!
        """
        messagebox.showinfo("Game Rules", rules)

    def show_about(self):
        """Show about information"""
        about_text = """
        Traveling Salesman Problem Game
        
        A simulation game to learn about route optimization algorithms.
        
        The Traveling Salesman Problem is a classic algorithmic problem in computer science.
        It asks the question: "Given a list of cities and the distances between each pair of cities, 
        what is the shortest possible route that visits each city exactly once and returns to the origin city?"
        """
        messagebox.showinfo("About", about_text)

    def run(self):
        """Run the application main loop"""
        self.root.mainloop()
        return 0