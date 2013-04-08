import random
import unittest
import parser

class TestSequenceFunctions(unittest.TestCase):

    def test_drive_forwards(self):
        test_string = """
        drive forwards 10 steps
        """

        correct_translation = "translate_car(10, CarDirection.FORWARDS)"
        result = parser.parser.parse(test_string)

        self.assertEqual(result, correct_translation)


    def test_drive_backwards(self):
        test_string = """
        drive backwards 10 steps
        """

        correct_translation = "translate_car(10, CarDirection.BACKWARDS)"
        result = parser.parser.parse(test_string)

        self.assertEqual(result, correct_translation)


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

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestSequenceFunctions)
    unittest.TextTestRunner(verbosity=2).run(suite)