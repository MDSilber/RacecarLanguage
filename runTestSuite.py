import Racecar.Tests.test as test
import unittest

suite = unittest.TestLoader().loadTestsFromTestCase(test.TestSequenceFunctions)
unittest.TextTestRunner(verbosity=2).run(suite)
