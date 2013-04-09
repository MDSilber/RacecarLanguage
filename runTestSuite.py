import Racecar.Tests.test as test
import unittest

suite = unittest.TestLoader().loadTestsFromTestCase(test.SymbolTableTests)
unittest.TextTestRunner(verbosity=2).run(suite)
suite = unittest.TestLoader().loadTestsFromTestCase(test.TranslatorTests)
unittest.TextTestRunner(verbosity=2).run(suite)
