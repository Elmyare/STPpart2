import unittest
from ControlDevice import ControlDevice

class TestControlDevice(unittest.TestCase):
    def setUp(self):
        self.device = ControlDevice()
    
    def test_basic_operations(self):
        # Тест: 5 + 3 = 8
        self.device.process_input('5')
        self.device.process_input('+')
        self.device.process_input('3')
        result = self.device.process_input('=')
        self.assertEqual(result, "8")
    
    def test_memory_operations(self):
        # Тест памяти: 5 MS, MR → 5
        self.device.process_input('5')
        self.device.memory_store()
        self.device.process_input('C')
        result = self.device.memory_recall()
        self.assertEqual(result, "5")
    
    def test_fraction_input(self):
        # Тест ввода дроби: 5 Frac 2 = 5/2
        self.device.process_input('5')
        self.device.process_input('Frac')
        self.device.process_input('2')
        self.assertEqual(self.device._editor.buffer, "5/2")
        self.assertEqual(str(self.device._editor.number), "5/2")
    
    def test_function_operations(self):
        # Тест: 4 Sqr = 16
        self.device.process_input('4')
        result = self.device.process_input('Sqr')
        self.assertEqual(result, "16")
        
        # Тест: 2 Rev = 1/2
        self.device.process_input('2')
        result = self.device.process_input('Rev')
        self.assertEqual(result, "1/2")

if __name__ == '__main__':
    unittest.main()