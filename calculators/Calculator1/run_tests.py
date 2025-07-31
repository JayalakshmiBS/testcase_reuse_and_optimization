import unittest

if __name__ == '__main__':
    # Use the same discovery pattern unittest would use
    loader = unittest.TestLoader()
    suite = loader.discover('tests', pattern='test_*.py')
    
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)