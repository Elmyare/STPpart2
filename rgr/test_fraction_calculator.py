import unittest
from fractions import Fraction
from FractionCalculator import FractionCalculator

class TestFractionCalculator(unittest.TestCase):
    def setUp(self):
        self.calc = FractionCalculator()

    def test_initial_state(self):
        self.assertEqual(self.calc.current_value, Fraction(0, 1))
        self.assertIsNone(self.calc.stored_value)
        self.assertIsNone(self.calc.operation)
        self.assertTrue(self.calc.waiting_for_operand)

    def test_reset(self):
        self.calc.current_value = Fraction(3, 4)
        self.calc.reset()
        self.assertEqual(self.calc.current_value, Fraction(0, 1))
        self.assertIsNone(self.calc.stored_value)

    def test_input_digits(self):
        self.assertEqual(self.calc.process_input('5'), '5')
        self.assertEqual(self.calc.process_input('3'), '53')
        self.assertEqual(self.calc.current_value, Fraction(53, 1))

    def test_fraction_input(self):
        self.assertEqual(self.calc.process_input('5'), '5')
        self.assertEqual(self.calc.process_input('Frac'), '5/')
        self.assertEqual(self.calc.process_input('2'), '5/2')
        self.assertEqual(self.calc.current_value, Fraction(5, 2))

    def test_decimal_input(self):
        self.assertEqual(self.calc.process_input('2'), '2')
        self.assertEqual(self.calc.process_input('.'), '2.')
        self.assertEqual(self.calc.process_input('5'), '2.5')
        self.assertEqual(self.calc.current_value, Fraction(5, 2))

    def test_basic_operations(self):
        # 3/4 + 1/2 = 5/4
        self.calc.process_input('3')
        self.calc.process_input('Frac')
        self.calc.process_input('4')
        self.calc.process_input('+')
        self.calc.process_input('1')
        self.calc.process_input('Frac')
        self.calc.process_input('2')
        self.assertEqual(self.calc.process_input('='), '5/4')
        self.assertEqual(self.calc.current_value, Fraction(5, 4))

    def test_multiplication(self):
        # 2 * 3/4 = 3/2
        self.calc.process_input('2')
        self.calc.process_input('*')
        self.calc.process_input('3')
        self.calc.process_input('Frac')
        self.calc.process_input('4')
        self.assertEqual(self.calc.process_input('='), '3/2')
        self.assertEqual(self.calc.current_value, Fraction(3, 2))

    def test_division(self):
        # 5/2 / 2 = 5/4
        self.calc.process_input('5')
        self.calc.process_input('Frac')
        self.calc.process_input('2')
        self.calc.process_input('/')
        self.calc.process_input('2')
        self.assertEqual(self.calc.process_input('='), '5/4')

    def test_square_function(self):
        self.calc.process_input('3')
        self.calc.process_input('Frac')
        self.calc.process_input('4')
        self.assertEqual(self.calc.process_input('Sqr'), '9/16')
        self.assertEqual(self.calc.current_value, Fraction(9, 16))

    def test_reciprocal_function(self):
        self.calc.process_input('2')
        self.calc.process_input('Frac')
        self.calc.process_input('5')
        self.assertEqual(self.calc.process_input('Rev'), '5/2')
        self.assertEqual(self.calc.current_value, Fraction(5, 2))

    def test_sign_change(self):
        self.calc.process_input('3')
        self.calc.process_input('Frac')
        self.calc.process_input('4')
        self.assertEqual(self.calc.process_input('+/-'), '-3/4')
        self.assertEqual(self.calc.current_value, Fraction(-3, 4))

    def test_division_by_zero(self):
        self.calc.process_input('5')
        self.calc.process_input('/')
        self.calc.process_input('0')
        with self.assertRaises(ValueError) as context:
            self.calc.process_input('=')
        self.assertEqual(str(context.exception), "Деление на ноль")

    def test_memory_operations(self):
        self.calc.process_input('3')
        self.calc.process_input('Frac')
        self.calc.process_input('4')
        self.calc.memory_store()
        
        self.calc.process_input('C')
        self.assertEqual(self.calc.memory_recall(), '3/4')
        
        self.calc.process_input('2')
        self.calc.memory_add()
        self.assertEqual(self.calc.memory, Fraction(11, 4))
        
        self.calc.memory_clear()
        self.assertIsNone(self.calc.memory)

    def test_continuous_operations(self):
        # 5 + 3 = 8; 8 * 2 = 16
        self.calc.process_input('5')
        self.calc.process_input('+')
        self.calc.process_input('3')
        self.assertEqual(self.calc.process_input('='), '8')
        self.calc.process_input('*')
        self.calc.process_input('2')
        self.assertEqual(self.calc.process_input('='), '16')

    def test_repeated_equals(self):
        # 5 + 3 = 8; = 11; = 14 (повтор последней операции)
        self.calc.process_input('5')
        self.calc.process_input('+')
        self.calc.process_input('3')
        self.assertEqual(self.calc.process_input('='), '8')
        self.assertEqual(self.calc.process_input('='), '11')
        self.assertEqual(self.calc.process_input('='), '14')

    def test_invalid_fraction_input(self):
        with self.assertRaises(ValueError):
            self.calc.process_input('5')
            self.calc.process_input('Frac')
            self.calc.process_input('0')  # 5/0 - недопустимо

if __name__ == '__main__':
    unittest.main()