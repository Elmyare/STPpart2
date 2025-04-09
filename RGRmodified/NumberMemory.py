from Number import Number

class NumberMemory:
    """Класс для хранения чисел в памяти"""
    def __init__(self):
        self._memory = None
        self._active = False
    
    @property
    def memory(self):
        return self._memory
    
    @property
    def is_active(self):
        return self._active
    
    def store(self, number):
        self._memory = number.value
        self._active = True
    
    def recall(self):
        if self._memory is not None:
            return Number(self._memory)
        return Number(0)
    
    def clear(self):
        self._memory = None
        self._active = False
    
    def add(self, number):
        if self._memory is not None:
            self._memory += number.value
        else:
            self._memory = number.value
        self._active = True