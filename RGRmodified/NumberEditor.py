from Number import Number
from fractions import Fraction

class NumberEditor:
    """Класс для редактирования чисел"""
    def __init__(self):
        self._buffer = "0"
        self._number = Number()
        self._waiting_for_operand = True
    
    @property
    def number(self):
        return self._number
    
    @property
    def buffer(self):
        return self._buffer
    
    @property
    def waiting_for_operand(self):
        return self._waiting_for_operand
    
    def reset(self):
        self._buffer = "0"
        self._number = Number()
        self._waiting_for_operand = True
    
    def process_digit(self, digit):
        if self._waiting_for_operand:
            self._buffer = "0"
            self._waiting_for_operand = False
            
        if digit == '.' and '.' in self._buffer:
            return
            
        if self._buffer == "0" and digit != '.':
            self._buffer = digit
        else:
            self._buffer += digit
        
        self._update_number()
    
    def add_fraction(self):
        if '/' not in self._buffer:
            self._buffer += '/'
            self._waiting_for_operand = False
    
    def negate(self):
        self._number.negate()
        self._buffer = str(self._number)
    
    def _update_number(self):
        try:
            if '/' in self._buffer:
                parts = self._buffer.split('/')
                if len(parts) == 2 and parts[0] and parts[1]:
                    if int(parts[1]) == 0:
                        raise ZeroDivisionError("Деление на ноль")
                    self._number.value = Fraction(int(parts[0]), int(parts[1]))
            else:
                self._number.value = Fraction(float(self._buffer))
        except (ValueError, ZeroDivisionError):
            raise ValueError("Некорректный ввод дроби")