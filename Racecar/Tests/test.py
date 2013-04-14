import random
import unittest
import Racecar.Compiler as Compiler
import Racecar.SymbolTable as SymbolTable

class TranslatorTests(unittest.TestCase):

    def test_drive_forwards(self):
        test_string1 = "drive forwards 10 steps\n"
        test_string2 = "drive forward 10 steps\n"
        test_string3 = "drive forwards 10 step\n"
        test_string4 = "drive forward 10 step\n"

        correct_translation = "translate_car(10, CarDirection.FORWARDS)\n"
        result1 = Compiler.getPythonCode(test_string1)
        result2 = Compiler.getPythonCode(test_string2)
        result3 = Compiler.getPythonCode(test_string3)
        result4 = Compiler.getPythonCode(test_string4)

        self.assertEqual(result1, correct_translation)
        self.assertEqual(result2, correct_translation)
        self.assertEqual(result3, correct_translation)
        self.assertEqual(result4, correct_translation)

    def test_drive_backwards(self):
        test_string1 = "drive backwards 10 steps\n"
        test_string2 = "drive backward 10 steps\n"
        test_string3 = "drive backwards 10 step\n"
        test_string4 = "drive backward 10 step\n"

        correct_translation = "translate_car(10, CarDirection.BACKWARDS)\n"
        result1 = Compiler.getPythonCode(test_string1)
        result2 = Compiler.getPythonCode(test_string2)
        result3 = Compiler.getPythonCode(test_string3)
        result4 = Compiler.getPythonCode(test_string4)

        self.assertEqual(result1, correct_translation)
        self.assertEqual(result2, correct_translation)
        self.assertEqual(result3, correct_translation)
        self.assertEqual(result4, correct_translation)


    def test_steer_left(self):
        test_string = "steer left\n"

        correct_translation = "rotate_car(WheelDirection.LEFT)\n"
        result = Compiler.getPythonCode(test_string)

        self.assertEqual(result, correct_translation)

    def test_steer_right(self):
        test_string = "steer right\n"

        correct_translation = "rotate_car(WheelDirection.RIGHT)\n"
        result = Compiler.getPythonCode(test_string)

        self.assertEqual(result, correct_translation)

    def test_print(self):
        test_string = "print \"hello world\"\n"

        correct_translation = "print_to_console(\"hello world\")\n"
        result = Compiler.getPythonCode(test_string)

        self.assertEqual(result, correct_translation)

    def test_declare(self):
        test_string = "myNum is a number\n"
        correct_translation = "myNum = None\n"
        result = Compiler.getPythonCode(test_string)

        self.assertEqual(result, correct_translation)

    def test_assign(self):
        test_string = "set myVar to otherThing\n"
        correct_translation = "myVar = otherThing\n"

        result = Compiler.getPythonCode(test_string)

        self.assertEqual(result, correct_translation)
    
    def test_define(self):
        test_string = "define moveForwardFive\n{drive forward 5\n}\n"
        correct_translation = "def moveForwardFive():\n    translate_car(5, CarDirection.FORWARDS)\n"

        result = Compiler.getPythonCode(test_string)
        self.assertEqual(result, correct_translation)



class SymbolTableTests(unittest.TestCase):

    def test_symbol_table_entry_validate(self):
        '''Tests the SymbolTableEntry.validateWithTableEntry() function.
        In particular, ensures two same-named entries with different scopes
        are not equal, and an entry without a type matches an existing entry
        that has a type and the same name and scope, but not one with a different
        scope.'''

        entry1 = SymbolTable.SymbolTableEntry("name1", "word", "global")
        entry2 = SymbolTable.SymbolTableEntry("name1", "word", "local")

        self.assertFalse(entry1.validateWithTableEntry(entry2))
        self.assertFalse(entry2.validateWithTableEntry(entry1))

        entry3 = SymbolTable.SymbolTableEntry("name1","","global")

        self.assertTrue(entry3.validateWithTableEntry(entry1))
        self.assertFalse(entry3.validateWithTableEntry(entry2))

    def test_symbol_table_add_entry_twice(self):
        '''Tests whether adding a duplicate entry results in an error.'''
        table = SymbolTable.SymbolLookupTable()

        entry1 = SymbolTable.SymbolTableEntry("name1", "word", "global")

        table.addEntry(entry1)
        
        self.assertRaises(Exception, table.addEntry, entry1)

    def test_symbol_table_verify(self):
        '''Tests the SymbolLookupTable.verifyEntry() function.'''
        table = SymbolTable.SymbolLookupTable()

        entry1 = SymbolTable.SymbolTableEntry("name1", "word", "global")
        entry2 = SymbolTable.SymbolTableEntry("name1", "word", "local")

        table.addEntry(entry1)

        self.assertTrue(table.verifyEntry(entry1))
        self.assertFalse(table.verifyEntry(entry2))
        
        entry3 = SymbolTable.SymbolTableEntry("name1","","global")

        self.assertTrue(table.verifyEntry(entry3))
        self.assertFalse(table.verifyEntry(entry2))

    def test_symbol_table_get_entry(self):
        '''Tests the SymbolLookupTable.getEntry() function.'''
        table = SymbolTable.SymbolLookupTable()

        entry1 = SymbolTable.SymbolTableEntry("name1", "word", "global")
        entry2 = SymbolTable.SymbolTableEntry("name1", "word", "local")
        entry3 = SymbolTable.SymbolTableEntry("name1","","global")

        table.addEntry(entry1)

        entry4 = table.getEntry(entry3)
        
        self.assertTrue(entry3.validateWithTableEntry(entry4))
        self.assertRaises(Exception, table.getEntry, entry2)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TranslatorTests)
    unittest.TextTestRunner(verbosity=2).run(suite)
