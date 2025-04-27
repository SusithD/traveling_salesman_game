import unittest
import time
from utils.timer import Timer

class TestTimer(unittest.TestCase):
    def setUp(self):
        self.timer = Timer()
    
    def test_timer_measurement(self):
        """Test that timer correctly measures elapsed time"""
        self.timer.start()
        
        # Sleep for 100ms
        time.sleep(0.1)
        
        elapsed = self.timer.stop()
        
        # Check that elapsed time is approximately 100ms (with some margin for error)
        self.assertGreaterEqual(elapsed, 90)  # At least 90ms
        self.assertLessEqual(elapsed, 150)    # Not more than 150ms (allowing overhead)
    
    def test_stop_without_start(self):
        """Test that timer raises error when stopped without starting"""
        with self.assertRaises(ValueError):
            self.timer.stop()
    
    def test_multiple_measurements(self):
        """Test that timer can be reused for multiple measurements"""
        # First measurement
        self.timer.start()
        time.sleep(0.01)  # 10ms
        first = self.timer.stop()
        
        # Second measurement
        self.timer.start()
        time.sleep(0.02)  # 20ms
        second = self.timer.stop()
        
        # Check both measurements are reasonable
        self.assertGreaterEqual(first, 8)  # At least 8ms
        self.assertGreaterEqual(second, 15)  # At least 15ms
        
        # Second should be longer than first
        self.assertGreater(second, first)
    
    def test_timer_reset_on_stop(self):
        """Test that timer resets start_time when stopped"""
        self.timer.start()
        self.timer.stop()
        
        # Timer should be reset, so stopping it again should raise an error
        with self.assertRaises(ValueError):
            self.timer.stop()

if __name__ == '__main__':
    unittest.main()