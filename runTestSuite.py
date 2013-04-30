import Racecar.Tests.test as test
import unittest

print "Symbol Table Tests"
print "**********************************************************************"
print
suite = unittest.TestLoader().loadTestsFromTestCase(test.SymbolTableTests)
unittest.TextTestRunner(verbosity=2).run(suite)
print
print
print "Translator Tests"
print "**********************************************************************"
print
suite = unittest.TestLoader().loadTestsFromTestCase(test.TranslatorTests)
unittest.TextTestRunner(verbosity=2).run(suite)
print
print
print "Semantic Analyzer Tests"
print "**********************************************************************"
print
suite = unittest.TestLoader().loadTestsFromTestCase(test.SemanticAnalyzerTests)
unittest.TextTestRunner(verbosity=2).run(suite)
