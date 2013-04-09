import random
import unittest
import Racecar.Parser as Parser
import Racecar.SymbolTable as SymbolTable

class TestSequenceFunctions(unittest.TestCase):

    def test_drive_forwards(self):
        test_string = """
        drive forwards 10 steps
        """

        correct_translation = "translate_car(10, CarDirection.FORWARDS)"
        result = Parser.parseString(test_string)

        self.assertEqual(result, correct_translation)


    def test_drive_backwards(self):
        test_string = """
        drive backwards 10 steps
        """

        correct_translation = "translate_car(10, CarDirection.BACKWARDS)"
        result = Parser.parseString(test_string)

        self.assertEqual(result, correct_translation)


    def test_steer_left(self):
        test_string = """
        steer left
        """

        correct_translation = "rotate_car(WheelDirection.LEFT)"
        result = Parser.parseString(test_string)

        self.assertEqual(result, correct_translation)

    def test_steer_right(self):
        test_string = """
        steer right
        """

        correct_translation = "rotate_car(WheelDirection.RIGHT)"
        result = Parser.parseString(test_string)

        self.assertEqual(result, correct_translation)

    def test_symbol_table_entry_validate(self):
        entry1 = SymbolTable.SymbolTableEntry("name1", "word", "global")
        entry2 = SymbolTable.SymbolTableEntry("name1", "word", "local")

        self.assertFalse(entry1.validateWithTableEntry(entry2))
        self.assertFalse(entry2.validateWithTableEntry(entry1))

    def test_symbol_table_add_entry_twice(self):
        table = SymbolTable.SymbolLookupTable()

        entry1 = SymbolTable.SymbolTableEntry("name1", "word", "global")
        entry2 = SymbolTable.SymbolTableEntry("name1", "word", "local")

        table.addEntry(entry1)
        
        self.assertRaises(Exception, table.addEntry, entry1)
        

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestSequenceFunctions)
    unittest.TextTestRunner(verbosity=2).run(suite)
