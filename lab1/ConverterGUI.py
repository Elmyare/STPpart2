import tkinter as tk
from tkinter import ttk, messagebox
from Converter import Converter

class ConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Конвертер систем счисления")
        self.converter = Converter()
        self.history = []
        
        self.create_menu()
        self.create_widgets()
        
    def create_menu(self):
        menubar = tk.Menu(self.root)
        
        # Меню Файл
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Выход", command=self.root.quit)
        menubar.add_cascade(label="Файл", menu=file_menu)
        
        # Меню История
        history_menu = tk.Menu(menubar, tearoff=0)
        history_menu.add_command(label="Показать историю", command=self.show_history)
        history_menu.add_command(label="Очистить историю", command=self.clear_history)
        menubar.add_cascade(label="История", menu=history_menu)
        
        # Меню Справка
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="О программе", command=self.show_help)
        menubar.add_cascade(label="Справка", menu=help_menu)
        
        self.root.config(menu=menubar)
    
    def create_widgets(self):
        # Основной фрейм
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Поля ввода систем счисления
        ttk.Label(main_frame, text="Основание исходной системы (p1):").grid(row=0, column=0, sticky=tk.W)
        self.p1_var = tk.IntVar(value=10)
        self.p1_spin = ttk.Spinbox(main_frame, from_=2, to=36, textvariable=self.p1_var, width=5)
        self.p1_spin.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        
        ttk.Label(main_frame, text="Основание целевой системы (p2):").grid(row=1, column=0, sticky=tk.W)
        self.p2_var = tk.IntVar(value=2)
        self.p2_spin = ttk.Spinbox(main_frame, from_=2, to=36, textvariable=self.p2_var, width=5)
        self.p2_spin.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Поле ввода числа
        ttk.Label(main_frame, text="Число для конвертации:").grid(row=2, column=0, sticky=tk.W)
        self.number_entry = ttk.Entry(main_frame, width=20)
        self.number_entry.grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Кнопки калькулятора
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.grid(row=3, column=0, columnspan=2, pady=10)
        
        buttons = [
            '0', '1', '2', '3',
            '4', '5', '6', '7',
            '8', '9', 'A', 'B',
            'C', 'D', 'E', 'F',
            '.', '←', 'C', 'Конвертировать'
        ]
        
        for i, button in enumerate(buttons):
            row = i // 4
            col = i % 4
            if button == '←':
                btn = ttk.Button(buttons_frame, text=button, command=self.delete_last_char)
            elif button == 'C':
                btn = ttk.Button(buttons_frame, text=button, command=self.clear_entry)
            elif button == 'Конвертировать':
                btn = ttk.Button(buttons_frame, text=button, command=self.convert)
                btn.grid(row=row, column=col, columnspan=2, sticky=tk.EW, padx=2, pady=2)
                continue
            else:
                btn = ttk.Button(buttons_frame, text=button, 
                                command=lambda b=button: self.append_to_entry(b))
            
            btn.grid(row=row, column=col, sticky=tk.EW, padx=2, pady=2)
        
        # Поле результата
        ttk.Label(main_frame, text="Результат:").grid(row=4, column=0, sticky=tk.W)
        self.result_var = tk.StringVar()
        self.result_entry = ttk.Entry(main_frame, textvariable=self.result_var, 
                                     state='readonly', width=20)
        self.result_entry.grid(row=4, column=1, sticky=tk.W, padx=5, pady=5)
    
    def append_to_entry(self, char):
        current = self.number_entry.get()
        self.number_entry.delete(0, tk.END)
        self.number_entry.insert(0, current + char)
    
    def delete_last_char(self):
        current = self.number_entry.get()
        self.number_entry.delete(0, tk.END)
        self.number_entry.insert(0, current[:-1])
    
    def clear_entry(self):
        self.number_entry.delete(0, tk.END)
    
    def validate_number(self, number: str, base: int) -> bool:
        """Проверяет, что число соответствует указанной системе счисления"""
        valid_digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        max_digit = valid_digits[base - 1]
        
        for char in number.upper():
            if char == '.':
                continue
            if char not in valid_digits:
                return False
            if valid_digits.index(char) >= base:
                return False
        return True
    
    def convert(self):
        number = self.number_entry.get().upper()
        p1 = self.p1_var.get()
        p2 = self.p2_var.get()
        
        if not number:
            messagebox.showerror("Ошибка", "Введите число для конвертации")
            return
        
        # Проверка на пустую строку после точки
        if '.' in number:
            int_part, frac_part = number.split('.')
            if not int_part and not frac_part:
                messagebox.showerror("Ошибка", "Некорректный формат числа")
                return
        
        # Проверка на несколько точек
        if number.count('.') > 1:
            messagebox.showerror("Ошибка", "Число может содержать только одну точку")
            return
        
        # Проверка соответствия числа системе счисления p1
        if not self.validate_number(number, p1):
            messagebox.showerror(
                "Ошибка", 
                f"Число '{number}' содержит символы, недопустимые в системе с основанием {p1}\n"
            )
            return
        
        try:
            result = self.converter.convert(number, p1, p2)
            self.result_var.set(result)
            
            # Добавляем в историю
            history_entry = f"{number} (p1={p1}) → {result} (p2={p2})"
            self.history.append(history_entry)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при конвертации: {str(e)}")
    
    def show_history(self):
        if not self.history:
            messagebox.showinfo("История", "История конвертаций пуста")
            return
        
        history_window = tk.Toplevel(self.root)
        history_window.title("История конвертаций")
        
        text = tk.Text(history_window, wrap=tk.WORD, width=50, height=15)
        text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        for entry in reversed(self.history):
            text.insert(tk.END, entry + "\n")
        
        text.config(state=tk.DISABLED)
        
        close_button = ttk.Button(history_window, text="Закрыть", 
                                command=history_window.destroy)
        close_button.pack(pady=5)
    
    def clear_history(self):
        self.history = []
        messagebox.showinfo("История", "История конвертаций очищена")
    
    def show_help(self):
        help_text = """Конвертер систем счисления

Позволяет переводить числа между системами счисления с основаниями от 2 до 36.

Инструкция:
1. Укажите основание исходной системы (p1)
2. Укажите основание целевой системы (p2)
3. Введите число для конвертации
4. Нажмите кнопку "Конвертировать"

Используйте кнопки калькулятора для ввода чисел или вводите вручную.

Допустимые символы: 0-9, A-Z (регистр не важен)
Для системы с основанием N допустимы цифры от 0 до N-1
"""
        messagebox.showinfo("Справка", help_text)