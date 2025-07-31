import unittest

# Discover and run all tests in the calculator_tests directory
loader = unittest.TestLoader()
suite = loader.discover('tests', pattern='test_*.py')

runner = unittest.TextTestRunner(verbosity=2)
runner.run(suite)