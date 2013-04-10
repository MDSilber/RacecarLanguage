import random
import unittest
import parser

class TestSequenceFunctions(unittest.TestCase):

    def test_drive_forwards(self):
        test_string1 = """
        drive forwards 10 steps
        """
        test_string2 = """
        drive forward 10 steps
        """
        test_string3 = """
        drive forwards 10 step
        """
        test_string4 = """
        drive forward 10 step
        """

        correct_translation = "translate_car(10, CarDirection.FORWARDS)"
        result1 = parser.parser.parse(test_string1)
        result2 = parser.parser.parse(test_string2)
        result3 = parser.parser.parse(test_string3)
        result4 = parser.parser.parse(test_string4)

        self.assertEqual(result1, correct_translation)
        self.assertEqual(result2, correct_translation)
        self.assertEqual(result3, correct_translation)
        self.assertEqual(result4, correct_translation)

    def test_drive_backwards(self):
        test_string1 = """
        drive backwards 10 steps
        """
        test_string2 = """
        drive backward 10 steps
        """
        test_string3 = """
        drive backwards 10 step
        """
        test_string4 = """
        drive backward 10 step
        """

        correct_translation = "translate_car(10, CarDirection.BACKWARDS)"
        result1 = parser.parser.parse(test_string1)
        result2 = parser.parser.parse(test_string2)
        result3 = parser.parser.parse(test_string3)
        result4 = parser.parser.parse(test_string4)

        self.assertEqual(result1, correct_translation)
        self.assertEqual(result2, correct_translation)
        self.assertEqual(result3, correct_translation)
        self.assertEqual(result4, correct_translation)


    def test_steer_left(self):
        test_string = """
        steer left
        """

        correct_translation = "rotate_car(WheelDirection.LEFT)"
        result = parser.parser.parse(test_string)

        self.assertEqual(result, correct_translation)

    def test_steer_right(self):
        test_string = """
        steer right
        """

        correct_translation = "rotate_car(WheelDirection.RIGHT)"
        result = parser.parser.parse(test_string)

        self.assertEqual(result, correct_translation)

    def test_print(self):
        test_string = """
        print "hello world"
        """

        correct_translation = "print_to_console(\"hello world\")"
        result = parser.parser.parse(test_string)

        self.assertEqual(result, correct_translation)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestSequenceFunctions)
    unittest.TextTestRunner(verbosity=2).run(suite)















a