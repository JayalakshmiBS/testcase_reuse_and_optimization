#!/usr/bin/env python3
import unittest
import os
import sys

def run_tests():
    # Add project root to Python path
    sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
    
    # Discover and run all tests
    loader = unittest.TestLoader()
    suite = loader.discover('tests', pattern='test_*.py')
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Exit with status code (0 if all passed)
    return not result.wasSuccessful()

if __name__ == '__main__':
    sys.exit(run_tests())