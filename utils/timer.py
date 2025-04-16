"""
Timer utility for measuring algorithm performance
"""
import time

class Timer:
    def __init__(self):
        self.start_time = None
    
    def start(self):
        """Start the timer"""
        self.start_time = time.perf_counter()
    
    def stop(self):
        """Stop the timer and return elapsed time in milliseconds"""
        if self.start_time is None:
            raise ValueError("Timer was not started")
        
        elapsed_time = (time.perf_counter() - self.start_time) * 1000  # Convert to milliseconds
        self.start_time = None
        return elapsed_time