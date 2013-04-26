import random
import unittest
import Racecar.Compiler as Compiler
import Racecar.SymbolTable as SymbolTable


class TranslatorTests(unittest.TestCase):
    def test_empty_statement(self):
        test_string = \
            """
"""
        correct_translation = \
            """
"""
        result = Compiler.getPythonCode(test_string)

        self.assertEqual(result[0], correct_translation)

    def test_drive_forwards(self):
        test_string1 = \
            """drive forwards 10 steps
"""
        test_string2 = \
            """drive forward 10 steps
"""
        test_string3 = \
            """drive forwards 10 step
"""
        test_string4 = \
            """drive forward 10 step
"""
        correct_translation = \
            """translate_car(10, CarDirection.FORWARDS)
"""
        result1 = Compiler.getPythonCode(test_string1)
        result2 = Compiler.getPythonCode(test_string2)
        result3 = Compiler.getPythonCode(test_string3)
        result4 = Compiler.getPythonCode(test_string4)

        self.assertEqual(result1[0], correct_translation)
        self.assertEqual(result2[0], correct_translation)
        self.assertEqual(result3[0], correct_translation)
        self.assertEqual(result4[0], correct_translation)

    def test_drive_backwards(self):
        test_string1 = \
            """drive backwards 10 steps
"""
        test_string2 = \
            """drive backward 10 steps
"""
        test_string3 = \
            """drive backwards 10 step
"""
        test_string4 = \
            """drive backward 10 step
"""
        correct_translation = \
            """translate_car(10, CarDirection.BACKWARDS)
"""
        result1 = Compiler.getPythonCode(test_string1)
        result2 = Compiler.getPythonCode(test_string2)
        result3 = Compiler.getPythonCode(test_string3)
        result4 = Compiler.getPythonCode(test_string4)

        self.assertEqual(result1[0], correct_translation)
        self.assertEqual(result2[0], correct_translation)
        self.assertEqual(result3[0], correct_translation)
        self.assertEqual(result4[0], correct_translation)

    def test_turn_left(self):
        test_string = \
            """turn left
"""
        correct_translation = \
            """rotate_car(WheelDirection.LEFT)
"""
        result = Compiler.getPythonCode(test_string)

        self.assertEqual(result[0], correct_translation)

    def test_turn_right(self):
        test_string = \
            """turn right
"""
        correct_translation = \
            """rotate_car(WheelDirection.RIGHT)
"""
        result = Compiler.getPythonCode(test_string)

        self.assertEqual(result[0], correct_translation)

    def test_print(self):
        test_string = \
            """print "hello world"
"""
        correct_translation = \
            """print_to_console("hello world")
"""
        result = Compiler.getPythonCode(test_string)

        self.assertEqual(result[0], correct_translation)

    def test_declare(self):
        test_string = \
            """myNum is a number
"""
        correct_translation = \
            """myNum = None
"""
        result = Compiler.getPythonCode(test_string)

        self.assertEqual(result[0], correct_translation)

    def test_assign(self):
        test_string = \
            """set myVar to otherThing
"""
        correct_translation = \
            """myVar = otherThing
"""
        result = Compiler.getPythonCode(test_string)
        self.assertEqual(result[0], correct_translation)

    def test_define(self):
        test_string = \
            """define moveForwardFive
{
    drive forward 5
}
"""
        correct_translation = \
            """def moveForwardFive():
    translate_car(5, CarDirection.FORWARDS)
"""

        result = Compiler.getPythonCode(test_string)
        self.assertEqual(result[0], correct_translation)

    def test_function_invocation_no_params(self):
        test_string = \
            """define moveBackwardFive
{
    drive backward 5
}
define moveForwardThenBackward
{
    drive forward 5
    moveBackwardFive
}
moveForwardThenBackward
"""
        correct_translation = \
            """def moveBackwardFive():
    translate_car(5, CarDirection.BACKWARDS)
def moveForwardThenBackward():
    translate_car(5, CarDirection.FORWARDS)
    moveBackwardFive()
moveForwardThenBackward()
"""
        result = Compiler.getPythonCode(test_string)
        self.assertEqual(result[0], correct_translation)

    def test_function_invocation_with_one_parameter(self):
        test_string = \
            """move5Steps "forwards"
"""
        correct_translation = \
            """move5Steps("forwards")
"""
        result = Compiler.getPythonCode(test_string)
        self.assertEqual(result[0], correct_translation)

    def test_function_invocation_with_two_parameters(self):
        test_string = \
            """define turnLeftThenDriveStraight using numStepsTurn \
            (number) and numStepsDrive (number)
{
turn left
drive forward numStepsTurn steps
turn right
drive forward numStepsDrive steps
}
turnLeftThenDriveStraight 5 10
"""
        correct_translation = \
            """def turnLeftThenDriveStraight(numStepsTurn, numStepsDrive):
    rotate_car(WheelDirection.LEFT)
    translate_car(numStepsTurn, CarDirection.FORWARDS)
    rotate_car(WheelDirection.RIGHT)
    translate_car(numStepsDrive, CarDirection.FORWARDS)
turnLeftThenDriveStraight(5, 10)
"""
        result = Compiler.getPythonCode(test_string)
        self.assertEqual(result[0], correct_translation)

    def test_plus_expression(self):
        test_string = \
            """print (2 + 3)
"""
        correct_translation = \
            """print_to_console(((2) + (3)))
"""
        result = Compiler.getPythonCode(test_string)
        self.assertEqual(result[0], correct_translation)

    def test_times_expression(self):
        test_string = \
            """print (2 * 3)
"""
        correct_translation = \
            """print_to_console(((2) * (3)))
"""
        result = Compiler.getPythonCode(test_string)
        self.assertEqual(result[0], correct_translation)

    def test_minus_expression(self):
        test_string = \
            """print (2 - 3)
"""
        correct_translation = \
            """print_to_console(((2) - (3)))
"""
        result = Compiler.getPythonCode(test_string)
        self.assertEqual(result[0], correct_translation)

    def test_divide_expression(self):
        test_string = \
            """print (2 / 3)
"""
        correct_translation = \
            """print_to_console(((2) / (3)))
"""
        result = Compiler.getPythonCode(test_string)
        self.assertEqual(result[0], correct_translation)

    def test_all_expression(self):
        test_string = \
            """print (1 + 2 * (3 + 4))
"""
        correct_translation = \
            """print_to_console(((1) + (((2) * (((3) + (4)))))))
"""
        result = Compiler.getPythonCode(test_string)
        self.assertEqual(result[0], correct_translation)

    def test_assign_num_change(self):
        test_string = \
            """num is a number
set num to 10
set num to num*2
"""
        correct_translation = \
            """num = None
num = 10
num = ((num) * (2))
"""
        result = Compiler.getPythonCode(test_string)
        self.assertEqual(result[0], correct_translation)

    def test_assign_word_print(self):
        test_string = \
            """color is a word
set color to "blue"
print color
"""
        correct_translation = \
            """color = None
color = "blue"
print_to_console(color)
"""
        result = Compiler.getPythonCode(test_string)
        self.assertEqual(result[0], correct_translation)

    def test_if_statement(self):
        test_string = \
            """if 1
{
    print "yay"
}
"""
        correct_translation = \
            """if 1:
    print_to_console("yay")
"""
        result = Compiler.getPythonCode(test_string)
        self.assertEqual(result[0], correct_translation)

    def test_if_else_statement(self):
        test_string = \
            """if 1
{
    print "yay"
}
else
{
    print "no"
}
"""
        correct_translation = \
            """if 1:
    print_to_console("yay")
else:
    print_to_console("no")
"""
        result = Compiler.getPythonCode(test_string)
        self.assertEqual(result[0], correct_translation)

    def test_if_statement_nested(self):
        test_string = \
            """if 1
{
    print "yay"
    if 1
    {
        print "yahoo"
    }
}
"""
        correct_translation = \
            """if 1:
    print_to_console("yay")
    if 1:
        print_to_console("yahoo")
"""
        result = Compiler.getPythonCode(test_string)
        self.assertEqual(result[0], correct_translation)

    def test_if_else_statement_nested(self):
        test_string = \
            """if 1
{
    print "yay"
    if 1
    {
        print "yahoo"
    }
    else
    {
        print "oh no"
    }
}
else
{
    print "no"
}
"""
        correct_translation = \
            """if 1:
    print_to_console("yay")
    if 1:
        print_to_console("yahoo")
    else:
        print_to_console("oh no")
else:
    print_to_console("no")
"""
        result = Compiler.getPythonCode(test_string)
        self.assertEqual(result[0], correct_translation)

    def test_if_elseif_else_statement(self):
        test_string = \
            """if 1
{
    print "yay"
}
elseIf 2
{
    print "no"
}
else
{
    print "done"
}
"""
        correct_translation = \
            """if 1:
    print_to_console("yay")
elif 2:
    print_to_console("no")
else:
    print_to_console("done")
"""
        result = Compiler.getPythonCode(test_string)
        self.assertEqual(result[0], correct_translation)

    def test_if_elseif_else_statement_nested(self):
        test_string = \
            """if 1
{
    print "yay"
    if 1
    {
        print "yahoo"
    }
    elseIf 2
    {
        print "oh no"
    }
    else
    {
        print "here"
    }
}
elseIf 2
{
    print "no"
}
else
{
    print "done"
}
"""
        correct_translation = \
            """if 1:
    print_to_console("yay")
    if 1:
        print_to_console("yahoo")
    elif 2:
        print_to_console("oh no")
    else:
        print_to_console("here")
elif 2:
    print_to_console("no")
else:
    print_to_console("done")
"""
        result = Compiler.getPythonCode(test_string)
        self.assertEqual(result[0], correct_translation)

    def test_if_if_else_complicated(self):
        test_string = \
            """if 1
{
    print "yay"
    if 1
    {
        print "yahoo"
    }
    else
    {
        print "oh no"
        if 1
        {
            print "good"
        }
        if 1
        {
            print "yay"
        }
        elseIf 2
        {
            print "no"
            if 1
            {
                print "hi"
            }
        }
        elseIf 3
        {
            print "yes"
        }
        else
        {
            if 5
            {
                print "works"
            }
            print "end"
        }
    }
}
else
{
    print "no"
}
"""
        correct_translation = \
            """if 1:
    print_to_console("yay")
    if 1:
        print_to_console("yahoo")
    else:
        print_to_console("oh no")
        if 1:
            print_to_console("good")
        if 1:
            print_to_console("yay")
        elif 2:
            print_to_console("no")
            if 1:
                print_to_console("hi")
        elif 3:
            print_to_console("yes")
        else:
            if 5:
                print_to_console("works")
            print_to_console("end")
else:
    print_to_console("no")
"""
        result = Compiler.getPythonCode(test_string)
        self.assertEqual(result[0], correct_translation)

    def test_comment_singleline(self):
        test_string = \
            """:) this is a single line comment
"""
        correct_translation = \
            """
"""
        result = Compiler.getPythonCode(test_string)
        self.assertEqual(result[0], correct_translation)

    def test_comment_multiline(self):
        test_string = \
            """:-( this is
a multiline
comment
:-)
"""
        correct_translation = \
            """
"""
        result = Compiler.getPythonCode(test_string)
        self.assertEqual(result[0], correct_translation)

    def test_loop_for(self):
        test_string = \
            """myCounter is a number
set myCounter to 10
repeat myCounter times
{
    drive forward 1 step
}
"""
        correct_translation = \
            """myCounter = None
myCounter = 10
for x in range(myCounter):
    translate_car(1, CarDirection.FORWARDS)
"""
        result = Compiler.getPythonCode(test_string)
        self.assertEqual(result[0], correct_translation)

    def test_loop_for_nested(self):
        test_string = \
            """myCounter is a number
set myCounter to 10
myCounter2 is a number
set myCounter2 to 10
repeat myCounter times
{
    drive forward 1 step
    repeat myCounter2 times
    {
        drive forward 1 step
    }
}
"""
        correct_translation = \
            """myCounter = None
myCounter = 10
myCounter2 = None
myCounter2 = 10
for x in range(myCounter):
    translate_car(1, CarDirection.FORWARDS)
    for x in range(myCounter2):
        translate_car(1, CarDirection.FORWARDS)
"""
        result = Compiler.getPythonCode(test_string)
        self.assertEqual(result[0], correct_translation)

    def test_loop_while(self):
        test_string = \
            """myCounter is a number
set myCounter to 1
repeat if myCounter is not 5
{
    drive forward 1 step
    set myCounter to myCounter + 1
}
"""
        correct_translation = \
            """myCounter = None
myCounter = 1
while myCounter != 5:
    translate_car(1, CarDirection.FORWARDS)
    myCounter = ((myCounter) + (1))
"""
        result = Compiler.getPythonCode(test_string)
        self.assertEqual(result[0], correct_translation)

    def test_loop_while_nested(self):
        test_string = \
            """myCounter is a number
set myCounter to 1
myCounter2 is a number
repeat if myCounter is not 5
{
    drive forward 1 step
    set myCounter2 to 0
    repeat if myCounter2 is not 5
    {
        drive forward 1 step
        set myCounter2 to myCounter2 + 1
    }
    set myCounter to myCounter + 1
}
"""
        correct_translation = \
            """myCounter = None
myCounter = 1
myCounter2 = None
while myCounter != 5:
    translate_car(1, CarDirection.FORWARDS)
    myCounter2 = 0
    while myCounter2 != 5:
        translate_car(1, CarDirection.FORWARDS)
        myCounter2 = ((myCounter2) + (1))
    myCounter = ((myCounter) + (1))
"""
        result = Compiler.getPythonCode(test_string)
        self.assertEqual(result[0], correct_translation)

    def test_boolean_opeartors(self):
        test_string = \
            """if 1 < 2
{
    print "yes"
}
elseIf 1 is 2
{
    print "yes"
}
if 1 >= 2
{
    print "no"
}
elseIf 1 is not 2
{
    print "yes"
}
elseIf 1 > 2
{
    print "yes"
}
elseIf 1 < 2
{
    print "yes"
}
"""
        correct_translation = \
            """if 1 < 2:
    print_to_console("yes")
elif 1 == 2:
    print_to_console("yes")
if 1 >= 2:
    print_to_console("no")
elif 1 != 2:
    print_to_console("yes")
elif 1 > 2:
    print_to_console("yes")
elif 1 < 2:
    print_to_console("yes")
"""
        result = Compiler.getPythonCode(test_string)
        self.assertEqual(result[0], correct_translation)

    def test_string_concatenation(self):
        test_string = \
            """print "hey" ++ myWord
"""
        correct_translation = \
            """print_to_console((("hey") + str(myWord)))
"""
        result = Compiler.getPythonCode(test_string)
        self.assertEqual(result[0], correct_translation)

    def test_string_concatenation_complicated(self):
        test_string = \
            """print "hey" ++ myWord
"""
        correct_translation = \
            """print_to_console((str("hey") + str(myWord)))
"""
        result = Compiler.getPythonCode(test_string)
        self.assertEqual(result[0], correct_translation)

    def test_get_car_position(self):
        test_string = \
            """print getCarPosition
"""
        correct_translation = \
            """print_to_console(getCurrentPosition())
"""
        result = Compiler.getPythonCode(test_string)
        self.assertEqual(result[0], correct_translation)

    def test_template(self):
        test_string = \
            """
"""
        correct_translation = \
            """
"""
        result = Compiler.getPythonCode(test_string)
        self.assertEqual(result[0], correct_translation)


#still to test:
#
#test getLocation and compare it to others
#test can move back and forward


class SymbolTableTests(unittest.TestCase):

    def test_symbol_table_entry_validate(self):
        '''Tests the SymbolTableEntry.validateWithTableEntry() function.
        In particular, ensures two same-named entries with different scopes
        are not equal, and an entry without a type matches an existing entry
        that has a type and the same name and scope, but not one with a
        different scope.'''

        entry1 = SymbolTable.SymbolTableEntry("name1", "word", "global")
        entry2 = SymbolTable.SymbolTableEntry("name1", "word", "local")

        self.assertFalse(entry1.validateWithTableEntry(entry2))
        self.assertFalse(entry2.validateWithTableEntry(entry1))

        entry3 = SymbolTable.SymbolTableEntry("name1", "", "global")

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

        entry3 = SymbolTable.SymbolTableEntry("name1", "", "global")

        self.assertTrue(table.verifyEntry(entry3))
        self.assertFalse(table.verifyEntry(entry2))

    def test_symbol_table_get_entry(self):
        '''Tests the SymbolLookupTable.getEntry() function.'''
        table = SymbolTable.SymbolLookupTable()

        entry1 = SymbolTable.SymbolTableEntry("name1", "word", "global")
        entry2 = SymbolTable.SymbolTableEntry("name1", "word", "local")
        entry3 = SymbolTable.SymbolTableEntry("name1", "", "global")

        table.addEntry(entry1)

        entry4 = table.getEntry(entry3)

        self.assertTrue(entry3.validateWithTableEntry(entry4))
        self.assertRaises(Exception, table.getEntry, entry2)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TranslatorTests)
    unittest.TextTestRunner(verbosity=2).run(suite)
