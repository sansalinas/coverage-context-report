import unittest
from code_demo.demo import Demo


class TestSum(unittest.TestCase):

    def test_addition_positive(self):
        addition = Demo.addition(2, 3)
        self.assertEqual(addition, 5)

    def test_addition_negative(self):
        addition = Demo.addition(2, -3)
        self.assertEqual(addition, -1)


class TestSubtraction(unittest.TestCase):

    def test_subtraction_positive(self):
        subtraction = Demo.subtraction(3, 2)
        self.assertEqual(subtraction, 1)

    def test_subtraction_negative(self):
        subtraction = Demo.subtraction(3, -2)
        self.assertEqual(subtraction, 5)
