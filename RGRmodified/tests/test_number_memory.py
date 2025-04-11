import unittest
from fractions import Fraction
from NumberMemory import NumberMemory
from Number import Number

class TestNumberMemory(unittest.TestCase):
    def setUp(self):
        self.mem = NumberMemory()
        self.num = Number(5)
    
    def test_store_recall(self):
        self.mem.store(self.num)
        recalled = self.mem.recall()
        self.assertEqual(recalled.value, Fraction(5))
        self.assertTrue(self.mem.is_active)
    
    def test_clear(self):
        self.mem.store(self.num)
        self.mem.clear()
        self.assertIsNone(self.mem.memory)
        self.assertFalse(self.mem.is_active)
    
    def test_add(self):
        self.mem.add(self.num)
        self.assertEqual(self.mem.memory, Fraction(5))
        self.mem.add(Number(3))
        self.assertEqual(self.mem.memory, Fraction(8))

if __name__ == '__main__':
    unittest.main()