import unittest
from Number import Number
from fractions import Fraction

class TestNumber(unittest.TestCase):
    def setUp(self):
        self.num = Number(3)
    
    def test_initialization(self):
        self.assertEqual(str(Number(2)), "2")
        self.assertEqual(str(Number(0.5)), "1/2")
        self.assertEqual(str(Number(Fraction(3, 4))), "3/4")
    
    def test_value_property(self):
        self.num.value = 5
        self.assertEqual(self.num.value, Fraction(5))
    
    def test_inverse(self):
        self.num.value = 4
        self.num.inverse()
        self.assertEqual(self.num.value, Fraction(1, 4))
        with self.assertRaises(ZeroDivisionError):
            Number(0).inverse()
    
    def test_square(self):
        self.num.square()
        self.assertEqual(self.num.value, Fraction(9))
    
    def test_negate(self):
        self.num.negate()
        self.assertEqual(self.num.value, Fraction(-3))
    
    def test_is_zero(self):
        self.assertFalse(self.num.is_zero())
        self.assertTrue(Number(0).is_zero())

if __name__ == '__main__':
    unittest.main()