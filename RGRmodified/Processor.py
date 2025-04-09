from Number import Number

class Processor:
    def __init__(self):
        self._current_operation = None
        self._stored_number = None
        self._last_operation = None
        self._last_operand = None  # Для сложения/вычитания
        self._multiplier = None    # Для умножения
        self._divisor = None       # Для деления

    def set_operation(self, operation):
        self._current_operation = operation

    def execute(self, number1, number2):
        if self._current_operation is None:
            return number1
        
        try:
            if self._current_operation == '+':
                result = number1.value + number2.value
                self._last_operand = Number(number2.value)
            elif self._current_operation == '-':
                result = number1.value - number2.value
                self._last_operand = Number(number2.value)
            elif self._current_operation == '*':
                result = number1.value * number2.value
                # Сохраняем второй операнд (множитель) для повторных операций
                self._multiplier = Number(number2.value)
            elif self._current_operation == '/':
                result = number1.value / number2.value
                # Сохраняем второй операнд (делитель) для повторных операций
                self._divisor = Number(number2.value)
            
            self._last_operation = self._current_operation
            return Number(result)
        except ZeroDivisionError:
            raise ValueError("Деление на ноль")

    def repeat_last_operation(self, number):
        if not self._last_operation:
            return number
            
        if self._last_operation == '+':
            return Number(number.value + self._last_operand.value)
        elif self._last_operation == '-':
            return Number(number.value - self._last_operand.value)
        elif self._last_operation == '*':
            return Number(number.value * self._multiplier.value)
        elif self._last_operation == '/':
            return Number(number.value / self._divisor.value)
        return number

    def clear_operation(self):
        self._current_operation = None

    def store_number(self, number):
        self._stored_number = Number(number.value)

    def get_stored_number(self):
        return Number(self._stored_number.value) if self._stored_number else None