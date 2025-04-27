"""
Demo/Automatic mode manager for the Traveling Salesman Problem game
Handles automated demonstration of the application flow
"""
import logging
import random
import time
from PyQt5.QtCore import QObject, QTimer, pyqtSignal

logger = logging.getLogger("DemoManager")

class DemoManager(QObject):
    """
    Manager for running automated demonstrations of the application
    Controls flow, timing, and automatic selections for a full walkthrough
    """
    
    # Signal to notify when demo has completed
    demo_completed = pyqtSignal()
    
    # Signal to notify when demo has been canceled
    demo_canceled = pyqtSignal()
    
    def __init__(self, flow_manager):
        """
        Initialize the demo manager with a reference to the game flow manager
        
        Args:
            flow_manager: Reference to the main GameFlowManager
        """
        super().__init__()
        self.flow_manager = flow_manager
        self.is_running = False
        self.current_step = 0
        self.demo_timer = QTimer(self)
        self.demo_timer.timeout.connect(self.execute_next_step)
        self.demo_steps = []
        self.step_delays = []
        
    def start_demo(self):
        """Start the automatic demonstration"""
        if self.is_running:
            logger.warning("Demo already running")
            return False
            
        logger.info("Starting automated demo mode")
        self.is_running = True
        self.current_step = 0
        
        # Reset game state if needed
        self.flow_manager.reset_game()
        
        # Define the sequence of demo steps and their delays
        self.setup_demo_sequence()
        
        # Start the timer for the first step
        if self.step_delays and self.demo_steps:
            self.demo_timer.start(self.step_delays[0])
            return True
        else:
            logger.error("Demo steps not properly set up")
            self.is_running = False
            return False
    
    def setup_demo_sequence(self):
        """Set up the sequence of steps and delays for the demo"""
        self.demo_steps = [
            self.setup_welcome_screen,    # Set up welcome screen (player name)
            self.go_to_mission_screen,    # Move to mission screen
            self.go_to_city_selection,    # Move to city selection
            self.select_cities,           # Select cities
            self.go_to_prediction_screen, # Move to prediction screen
            self.make_prediction,         # Make algorithm prediction
            self.run_calculations,        # Run calculations
            self.view_results,            # View results
            self.view_summary,            # View summary
            self.complete_demo            # Complete demo
        ]
        
        # Delays in milliseconds between steps
        self.step_delays = [
            2000,  # Wait 2s before entering name
            3000,  # Wait 3s on mission screen
            2000,  # Wait 2s before selecting cities
            3000,  # Wait 3s after selecting cities
            3000,  # Wait 3s on prediction screen
            2500,  # Wait 2.5s after making prediction
            4000,  # Wait 4s on calculating screen (animation will run)
            8000,  # Wait 8s on results screen to view charts
            4000,  # Wait 4s on summary screen
            2000   # Wait 2s before completing demo
        ]
    
    def execute_next_step(self):
        """Execute the next step in the demo sequence"""
        if not self.is_running:
            return
        
        if self.current_step < len(self.demo_steps):
            try:
                # Stop the timer while executing the current step
                self.demo_timer.stop()
                
                # Execute the current step
                self.demo_steps[self.current_step]()
                
                # Move to the next step
                self.current_step += 1
                
                # Start the timer for the next step if there is one
                if self.current_step < len(self.step_delays):
                    self.demo_timer.start(self.step_delays[self.current_step])
                else:
                    self.stop_demo()
                    self.demo_completed.emit()
                    
            except Exception as e:
                logger.error(f"Error executing demo step {self.current_step}: {e}")
                self.stop_demo()
                self.demo_canceled.emit()
        else:
            self.stop_demo()
            self.demo_completed.emit()
    
    def stop_demo(self):
        """Stop the automated demonstration"""
        if self.is_running:
            logger.info("Stopping automated demo mode")
            self.demo_timer.stop()
            self.is_running = False
            return True
        return False
    
    def setup_welcome_screen(self):
        """Set up the welcome screen with a demo player name"""
        logger.info("Demo: Setting up welcome screen")
        self.flow_manager.show_welcome_screen()
        
        # Automatically set a demo username
        self.flow_manager.game_state.set_player_name("Demo User")
        
        # Update the name input field if accessible
        try:
            welcome_screen = self.flow_manager.welcome_screen
            welcome_screen.name_input.setText("Demo User")
        except:
            pass
    
    def go_to_mission_screen(self):
        """Move to the mission screen"""
        logger.info("Demo: Moving to mission screen")
        self.flow_manager.show_mission_screen()
    
    def go_to_city_selection(self):
        """Move to the city selection screen"""
        logger.info("Demo: Moving to city selection screen")
        self.flow_manager.show_city_selection_screen()
    
    def select_cities(self):
        """Select random cities for the demo"""
        logger.info("Demo: Selecting cities")
        
        # Get all available cities
        city_map = self.flow_manager.game_state.city_map
        all_cities = city_map.get_cities()
        
        # Select a random home city
        home_city = random.choice(all_cities)
        self.flow_manager.game_state.home_city = home_city
        
        # Select 4-6 random cities to visit (excluding home city)
        other_cities = [c for c in all_cities if c != home_city]
        num_to_select = min(len(other_cities), random.randint(4, 6))
        selected_cities = random.sample(other_cities, num_to_select)
        
        # Add home city to selected cities
        selected_cities.append(home_city)
        
        # Update the game state
        self.flow_manager.game_state.selected_cities = selected_cities
        
        # Update the UI to reflect selected cities
        try:
            city_selection_screen = self.flow_manager.city_selection_screen
            city_selection_screen.update_display()  # This should refresh the city buttons
            
            # Make sure the selection counter is updated
            city_selection_screen.update_selection_count()
        except Exception as e:
            logger.error(f"Error updating city selection UI: {e}")
    
    def go_to_prediction_screen(self):
        """Move to the algorithm prediction screen"""
        logger.info("Demo: Moving to prediction screen")
        self.flow_manager.show_prediction_screen()
    
    def make_prediction(self):
        """Make a random algorithm prediction"""
        logger.info("Demo: Making algorithm prediction")
        
        # Randomly choose an algorithm
        algorithms = ["Brute Force", "Nearest Neighbor", "Dynamic Programming"]
        selected_algorithm = random.choice(algorithms)
        
        # Set the prediction in the game state
        self.flow_manager.game_state.user_prediction = selected_algorithm
        
        # Update the UI to reflect the selection
        try:
            prediction_screen = self.flow_manager.prediction_screen
            
            # Find the radio button for the selected algorithm
            for button in prediction_screen.algorithm_group.buttons():
                if button.text() == selected_algorithm:
                    button.setChecked(True)
                    prediction_screen.algorithm_selected(button)
                    break
        except Exception as e:
            logger.error(f"Error updating prediction UI: {e}")
        
        # Continue to the calculating screen
        self.flow_manager.show_calculating_screen(selected_algorithm)
    
    def run_calculations(self):
        """Let the calculations run"""
        logger.info("Demo: Watching calculations run")
        # This step is passive - the calculation animations will play automatically
        # and the results screen will appear automatically when done
    
    def view_results(self):
        """View the results and visualizations"""
        logger.info("Demo: Viewing results and visualizations")
        # This step is passive - we're just lingering on the results screen
        # to give time to see the visualizations
    
    def view_summary(self):
        """View the summary screen"""
        logger.info("Demo: Viewing summary screen")
        self.flow_manager.show_summary_screen()
    
    def complete_demo(self):
        """Complete the demo"""
        logger.info("Demo: Completing demo and returning to welcome screen")
        self.flow_manager.show_welcome_screen()
        self.flow_manager.welcome_screen.update_display()
        # Demo is now complete, the demo_completed signal will be emitted