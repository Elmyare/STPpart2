import unittest
from ControlPanel import ControlPanel
import tkinter as tk

class TestIntegration(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.app = ControlPanel(self.root)
        self.root.withdraw()  # Скрываем окно для тестов
    
    def test_full_operation(self):
        # Тест: (5 + 3) * 2 = 16
        self.app._device.process_input('5')
        self.app._device.process_input('+')
        self.app._device.process_input('3')
        self.app._device.process_input('=')
        self.app._device.process_input('*')
        self.app._device.process_input('2')
        result = self.app._device.process_input('=')
        self.assertEqual(result, "16")
    
    def tearDown(self):
        self.root.destroy()

if __name__ == '__main__':
    unittest.main()