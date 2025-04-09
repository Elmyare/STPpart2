from NumberEditor import NumberEditor
from Processor import Processor
from NumberMemory import NumberMemory
from fractions import Fraction

class ControlDevice:
    """Устройство управления калькулятором"""
    def __init__(self):
        self._editor = NumberEditor()
        self._processor = Processor()
        self._memory = NumberMemory()
    
    def process_input(self, input_str):
        try:
            if input_str == 'C':
                self._editor.reset()
                self._processor.clear_operation()
                return str(self._editor.number)
            
            elif input_str in ['+', '-', '*', '/']:
                if not self._editor.waiting_for_operand:
                    self._calculate()
                self._processor.set_operation(input_str)
                self._processor.store_number(self._editor.number)
                self._editor._waiting_for_operand = True
                return str(self._processor.get_stored_number())
            
            elif input_str == '=':
                if self._processor._current_operation is None and self._processor._last_operation:
                    result = self._processor.repeat_last_operation(self._editor.number)
                    self._editor._number = result
                    self._editor._buffer = str(result)
                    self._editor._waiting_for_operand = True
                else:
                    self._calculate()
                return str(self._editor.number)
            
            elif input_str == '+/-':
                self._editor.negate()
                return str(self._editor.number)
            
            elif input_str == 'Frac':
                self._editor.add_fraction()
                return self._editor.buffer
            
            elif input_str == 'Sqr':
                self._editor.number.square()
                self._editor._waiting_for_operand = True
                self._editor._buffer = str(self._editor.number)
                return str(self._editor.number)
            
            elif input_str == 'Rev':
                self._editor.number.inverse()
                self._editor._waiting_for_operand = True
                self._editor._buffer = str(self._editor.number)
                return str(self._editor.number)
            
            elif input_str.isdigit() or input_str == '.':
                self._editor.process_digit(input_str)
                return self._editor.buffer
            
            return self._editor.buffer
            
        except (ValueError, ZeroDivisionError) as e:
            self._editor.reset()
            raise ValueError(str(e))
    
    def _calculate(self):
        stored_num = self._processor.get_stored_number()
        if stored_num is not None and self._processor._current_operation:
            result = self._processor.execute(stored_num, self._editor.number)
            self._editor._number = result
            self._editor._buffer = str(result)
            self._editor._waiting_for_operand = True
            self._processor.clear_operation()
    
    def memory_store(self):
        self._memory.store(self._editor.number)
        return str(self._memory.memory)
    
    def memory_recall(self):
        recalled = self._memory.recall()
        self._editor._number = recalled
        self._editor._buffer = str(recalled)
        self._editor._waiting_for_operand = True
        return str(recalled)
    
    def memory_clear(self):
        self._memory.clear()
        return "0"
    
    def memory_add(self):
        self._memory.add(self._editor.number)
        return str(self._memory.memory)