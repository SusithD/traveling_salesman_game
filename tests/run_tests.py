#!/usr/bin/env python3
"""
Main test runner for the Traveling Salesman Problem game
Run this file to execute all unit tests
"""
import unittest
import os
import sys

# Add the project root directory to the path to make imports work
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def run_tests():
    """Run all unit tests in the project"""
    print("=" * 80)
    print("Running TSP Game Unit Tests")
    print("=" * 80)
    
    # Discover and run all tests
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover(os.path.join(os.path.dirname(__file__), 'unit'))

    # Run the tests with a detailed report
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Print summary
    print("\n" + "=" * 80)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    # Return exit code based on test success
    return 0 if result.wasSuccessful() else 1

if __name__ == "__main__":
    sys.exit(run_tests())