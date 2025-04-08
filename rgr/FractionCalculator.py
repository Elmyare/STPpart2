from fractions import Fraction
import re

class FractionCalculator:
    def __init__(self):
        self.reset()
        
    def reset(self):
        self.current_value = Fraction(0, 1)
        self.stored_value = None
        self.operation = None
        self.waiting_for_operand = True
        #self.memory = None
        #self.memory_active = False
        self.input_buffer = "0"
        self.last_operation = None
        self.last_operand = None

    def process_input(self, input_str):
        """Основной метод обработки ввода"""
        try:
            if input_str == 'C':
                self.reset()
                return "0"
            
            elif input_str in ['+', '-', '*', '/']:
                if not self.waiting_for_operand:
                    self._calculate()
                self.operation = input_str
                self.stored_value = self.current_value
                self.waiting_for_operand = True
                self.input_buffer = "0"
                return str(self.stored_value)
            
            elif input_str == '=':
                if self.operation is None and self.last_operation:
                    # Повтор последней операции
                    self.operation = self.last_operation
                    self.stored_value = self.current_value
                    self.current_value = self.last_operand
                self._calculate()
                return str(self.current_value)
            
            elif input_str == '+/-':
                self.current_value *= -1
                self.input_buffer = str(self.current_value)
                return self.input_buffer
            
            elif input_str == 'Frac':
                if '/' not in self.input_buffer:
                    self.input_buffer += '/'
                return self.input_buffer
            
            elif input_str == 'Sqr':
                self.current_value **= 2
                self.input_buffer = str(self.current_value)
                self.waiting_for_operand = True
                return self.input_buffer
            
            elif input_str == 'Rev':
                self.current_value = 1 / self.current_value
                self.input_buffer = str(self.current_value)
                self.waiting_for_operand = True
                return self.input_buffer
            
            elif input_str.isdigit() or input_str == '.':
                return self._process_digit(input_str)
            
            return self.input_buffer
            
        except (ValueError, ZeroDivisionError) as e:
            self.reset()
            raise ValueError(str(e))

    def _process_digit(self, digit):
        if self.waiting_for_operand:
            self.input_buffer = "0"
            self.waiting_for_operand = False
            
        if digit == '.' and '.' in self.input_buffer:
            return self.input_buffer
            
        if self.input_buffer == "0" and digit != '.':
            self.input_buffer = digit
        else:
            self.input_buffer += digit
            
        self._update_current_value()
        return self.input_buffer

    def _update_current_value(self):
        try:
            if '/' in self.input_buffer:
                parts = self.input_buffer.split('/')
                if len(parts) == 2 and parts[0] and parts[1]:
                    if int(parts[1]) == 0:
                        raise ZeroDivisionError("Деление на ноль")
                    self.current_value = Fraction(int(parts[0]), int(parts[1]))
            else:
                self.current_value = Fraction(float(self.input_buffer))
        except (ValueError, ZeroDivisionError):
            raise ValueError("Некорректный ввод дроби")

    def _calculate(self):
        if self.operation and self.stored_value is not None:
            try:
                if self.operation == '+':
                    self.current_value = self.stored_value + self.current_value
                elif self.operation == '-':
                    self.current_value = self.stored_value - self.current_value
                elif self.operation == '*':
                    self.current_value = self.stored_value * self.current_value
                elif self.operation == '/':
                    self.current_value = self.stored_value / self.current_value
                
                self.last_operation = self.operation
                self.last_operand = self.current_value - self.stored_value if self.operation == '+' else None
                self.input_buffer = str(self.current_value)
                self.operation = None
                self.waiting_for_operand = True
                
            except ZeroDivisionError:
                raise ValueError("Деление на ноль")

    def memory_store(self):
        self.memory = self.current_value
        self.memory_active = True
        return str(self.memory)  # Возвращаем сохранённое значение

    def memory_recall(self):
        if self.memory is not None:
            self.current_value = self.memory
            self.input_buffer = str(self.memory)
            self.waiting_for_operand = True
            return self.input_buffer
        return "0"

    def memory_clear(self):
        self.memory = None
        self.memory_active = False
        return "0"

    def memory_add(self):
        if self.memory is not None:
            self.memory += self.current_value
        else:
            self.memory = self.current_value
        self.memory_active = True
        return str(self.memory)