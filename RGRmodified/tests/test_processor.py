import unittest
from fractions import Fraction
from Processor import Processor
from Number import Number

class TestProcessor(unittest.TestCase):
    def setUp(self):
        self.proc = Processor()
        self.num1 = Number(10)
        self.num2 = Number(2)
    
    def test_execute_operations(self):
        # Тестирование всех операций
        self.proc.set_operation('+')
        result = self.proc.execute(self.num1, self.num2)
        self.assertEqual(result.value, Fraction(12))
        
        self.proc.set_operation('-')
        result = self.proc.execute(self.num1, self.num2)
        self.assertEqual(result.value, Fraction(8))
        
        self.proc.set_operation('*')
        result = self.proc.execute(self.num1, self.num2)
        self.assertEqual(result.value, Fraction(20))
        
        self.proc.set_operation('/')
        result = self.proc.execute(self.num1, self.num2)
        self.assertEqual(result.value, Fraction(5))
    
    def test_repeat_operation(self):
        self.proc.set_operation('+')
        self.proc.execute(self.num1, self.num2)
        repeated = self.proc.repeat_last_operation(Number(5))
        self.assertEqual(repeated.value, Fraction(7))  # 5 + 2
    
    def test_clear_operation(self):
        self.proc.set_operation('+')
        self.proc.clear_operation()
        self.assertIsNone(self.proc._current_operation)

if __name__ == '__main__':
    unittest.main()