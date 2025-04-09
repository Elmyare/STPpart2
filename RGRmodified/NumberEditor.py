from Number import Number
from fractions import Fraction

class NumberEditor:
    """Класс для редактирования чисел"""
    def __init__(self):
        self._buffer = "0"
        self._number = Number()
        self._waiting_for_operand = True
        self._last_function_result = None
        self._cursor_pos = 0
    
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
            self._cursor_pos = 1
            self._waiting_for_operand = False
            
        if digit == '.' and '.' in self._buffer:
            return self._buffer
            
        if self._buffer == "0" and digit != '.':
            self._buffer = digit
            self._cursor_pos = 1
        else:
            # Вставляем символ на позицию курсора
            self._buffer = self._buffer[:self._cursor_pos] + digit + self._buffer[self._cursor_pos:]
            self._cursor_pos += 1
        
        self._update_number()
        return self._buffer
    
    def add_fraction(self):
        if '/' not in self._buffer:
            if self._waiting_for_operand:
                self._buffer = "0"
                self._waiting_for_operand = False
                
            # Добавляем дробь на позицию курсора
            self._buffer = self._buffer[:self._cursor_pos] + '/' + self._buffer[self._cursor_pos:]
            self._cursor_pos += 1  # Перемещаем курсор после дроби
            self._update_number()
        return self._buffer
    
    def negate(self):
        self._number.negate()
        self._buffer = str(self._number)
    
    def square(self):
        self._number.square()
        self._last_function_result = Number(self._number.value)  # Сохраняем результат
        self._waiting_for_operand = True
        self._buffer = str(self._number)
        return self._buffer

    def inverse(self):
        self._number.inverse()
        self._last_function_result = Number(self._number.value)  # Сохраняем результат
        self._waiting_for_operand = True
        self._buffer = str(self._number)
        return self._buffer

    def process_backspace(self):
        """Удаляет символ слева от курсора"""
        if len(self._buffer) >= 1 and self._cursor_pos > 0:
            self._buffer = self._buffer[:self._cursor_pos-1] + self._buffer[self._cursor_pos:]
            self._cursor_pos -= 1
            if not self._buffer:  # Если строка пуста
                self._buffer = "0"
                self._cursor_pos = 1
        self._update_number()
        return self._buffer

    def process_delete(self):
        """Удаляет символ справа от курсора"""
        if self._cursor_pos < len(self._buffer):
            self._buffer = self._buffer[:self._cursor_pos] + self._buffer[self._cursor_pos+1:]
            if not self._buffer:  # Если строка пуста
                self._buffer = "0"
                self._cursor_pos = 1
        self._update_number()
        return self._buffer

    def move_cursor_left(self):
        self._cursor_pos = max(0, self._cursor_pos - 1)
        return self._cursor_pos

    def move_cursor_right(self):
        self._cursor_pos = min(len(self._buffer), self._cursor_pos + 1)
        return self._cursor_pos

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