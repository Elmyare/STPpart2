from fractions import Fraction

class Number:
    """Класс для представления числа (дроби)"""
    def __init__(self, value=0):
        self._value = Fraction(value)
    
    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, new_value):
        self._value = Fraction(new_value)
    
    def __str__(self):
        return str(self._value)
    
    def to_float(self):
        return float(self._value)
    
    def is_zero(self):
        return self._value == 0
    
    def inverse(self):
        if self._value == 0:
            raise ZeroDivisionError("Деление на ноль")
        self._value = 1 / self._value
    
    def square(self):
        self._value **= 2
    
    def negate(self):
        self._value *= -1