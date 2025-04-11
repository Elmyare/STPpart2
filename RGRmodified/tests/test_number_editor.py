import unittest
from NumberEditor import NumberEditor
from fractions import Fraction

class TestNumberEditor(unittest.TestCase):
    def setUp(self):
        self.editor = NumberEditor()
    
    def test_initial_state(self):
        self.assertEqual(self.editor.buffer, "0")
        self.assertEqual(self.editor.number.value, Fraction(0))
        self.assertTrue(self.editor.waiting_for_operand)
    
    def test_process_digit(self):
        self.editor.process_digit('5')
        self.assertEqual(self.editor.buffer, "5")
        self.assertEqual(self.editor.number.value, Fraction(5))
    
    def test_add_fraction(self):
        self.editor.process_digit('5')
        self.editor.add_fraction()
        self.assertEqual(self.editor.buffer, "5/")
        self.editor.process_digit('2')
        self.assertEqual(self.editor.number.value, Fraction(5, 2))
    
    def test_backspace_delete(self):
        self.editor.process_digit('1')
        self.editor.process_digit('2')
        self.editor.process_digit('3')
        self.assertEqual(self.editor.buffer, "123")
        
        # Backspace удаляет последний символ
        self.editor.process_backspace()
        self.assertEqual(self.editor.buffer, "12")
        
        # Delete удаляет символ справа (если курсор не в конце)
        self.editor._cursor_pos = 1
        self.editor.process_delete()
        self.assertEqual(self.editor.buffer, "1")
    
    def test_square_inverse(self):
        self.editor.process_digit('4')
        self.editor.square()
        self.assertEqual(self.editor.number.value, Fraction(16))
        
        self.editor.process_digit('2')
        self.editor.inverse()
        self.assertEqual(self.editor.number.value, Fraction(1, 2))

if __name__ == '__main__':
    unittest.main()