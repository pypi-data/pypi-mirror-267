import unittest
from karray import settings
from test_long import TestLong
from test_array_initialization import TestArrayInitialization
from test_array_operations import TestArrayOperations
from test_array_insert import TestArrayInsert
from test_array_filehandling import TestArrayFileHandling
from test_array_choice import TestArrayChoice

if __name__ == '__main__':
    settings.data_type = 'sparse'
    test_loader = unittest.TestLoader()
    test_suite = unittest.TestSuite()

    test_suite.addTests(test_loader.loadTestsFromTestCase(TestLong))
    test_suite.addTests(test_loader.loadTestsFromTestCase(TestArrayInitialization))
    test_suite.addTests(test_loader.loadTestsFromTestCase(TestArrayOperations))
    test_suite.addTests(test_loader.loadTestsFromTestCase(TestArrayInsert))
    test_suite.addTests(test_loader.loadTestsFromTestCase(TestArrayFileHandling))
    test_suite.addTests(test_loader.loadTestsFromTestCase(TestArrayChoice))

    test_runner = unittest.TextTestRunner(verbosity=2)
    test_runner.run(test_suite)
