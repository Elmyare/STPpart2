import tkinter as tk
from tkinter import messagebox
from FractionCalculator import FractionCalculator
import re

class FractionCalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Калькулятор дробей")
        self.calculator = FractionCalculator()
        self.display_format = 'fraction'
        self._setup_ui()

    def _setup_ui(self):
        # Главное окно
        self.display_var = tk.StringVar()
        self.display_var.set("0")
        
        # Фрейм дисплея
        display_frame = tk.Frame(self.root)
        display_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Поле ввода
        self.display = tk.Entry(
            display_frame, 
            textvariable=self.display_var,
            font=('Arial', 24),
            bd=5,
            justify='right',
            state='normal',
            readonlybackground='white'
        )
        self.display.pack(fill=tk.X, ipady=10)
        self.display.bind('<Key>', self._handle_key_press)
        self.display.bind('<Return>', lambda e: self._on_button_click('='))
        self.display.focus_set()

        # Меню
        menubar = tk.Menu(self.root)
        
        # Меню Правка
        edit_menu = tk.Menu(menubar, tearoff=0)
        edit_menu.add_command(label="Копировать", command=self._copy_to_clipboard)
        edit_menu.add_command(label="Вставить", command=self._paste_from_clipboard)
        menubar.add_cascade(label="Правка", menu=edit_menu)
        
        # Меню Настройка
        settings_menu = tk.Menu(menubar, tearoff=0)
        settings_menu.add_command(label="Формат дроби", command=lambda: self._set_display_format('fraction'))
        settings_menu.add_command(label="Формат десятичной", command=lambda: self._set_display_format('decimal'))
        menubar.add_cascade(label="Настройка", menu=settings_menu)
        
        # Меню Справка
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="О программе", command=self._show_about)
        menubar.add_cascade(label="Справка", menu=help_menu)
        
        self.root.config(menu=menubar)
        
        # Кнопки памяти
        memory_frame = tk.Frame(self.root)
        memory_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Button(memory_frame, text="MC", width=5, command=self._memory_clear).pack(side=tk.LEFT)
        tk.Button(memory_frame, text="MR", width=5, command=self._memory_recall).pack(side=tk.LEFT)
        tk.Button(memory_frame, text="MS", width=5, command=self._memory_store).pack(side=tk.LEFT)
        tk.Button(memory_frame, text="M+", width=5, command=self._memory_add).pack(side=tk.LEFT)
        
        # Основные кнопки
        button_frame = tk.Frame(self.root)
        button_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        buttons = [
            '7', '8', '9', '/', 'Sqr',
            '4', '5', '6', '*', 'Rev',
            '1', '2', '3', '-', 'C',
            '0', '+/-', '=', '+', 'Frac'
        ]
        
        for i, text in enumerate(buttons):
            row = i // 5
            col = i % 5
            btn = tk.Button(
                button_frame, 
                text=text, 
                width=5, 
                height=2,
                font=('Arial', 14),
                command=lambda t=text: self._on_button_click(t)
            )
            btn.grid(row=row, column=col, sticky='nsew', padx=3, pady=3)
            button_frame.grid_columnconfigure(col, weight=1)
            button_frame.grid_rowconfigure(row, weight=1)
        self.display_var.trace_add('write', self._validate_input)

    def _handle_key_press(self, event):
        allowed_chars = {'0','1','2','3','4','5','6','7','8','9','/','-','.',"+", "*"}
        
        if event.char in allowed_chars:
            try:
                result = self.calculator.process_input(event.char)
                self.display_var.set(result)
                # Перемещаем курсор в конец после ввода
                self.display.icursor(tk.END)
            except ValueError as e:
                messagebox.showerror("Ошибка", str(e))
            return "break"
        elif event.keysym in ('BackSpace', 'Delete', 'Left', 'Right'):
            return
        else:
            return "break"

    def _validate_input(self, *args):
        """Автоматическая проверка вводимых данных"""
        current_text = self.display_var.get()
        if not re.match(r'^[-+]?[0-9]*\.?[0-9]*([/][0-9]*)?$', current_text):
            self.display_var.set(current_text[:-1])  # Удаляем последний недопустимый символ

    def _on_button_click(self, button):
        try:
            result = self.calculator.process_input(button)
            self.display_var.set(result)
            # Перемещаем курсор в конец после операции
            self.display.icursor(tk.END)
        except ValueError as e:
            messagebox.showerror("Ошибка", str(e))
        self.display.focus_set()

    def _update_display(self):
        current_value = self.calculator.current_value
        if self.display_format == 'fraction':
            if current_value.denominator == 1:
                self.display_var.set(str(current_value.numerator))
            else:
                self.display_var.set(f"{current_value.numerator}/{current_value.denominator}")
        else:
            self.display_var.set(str(float(current_value)))
        
        # Перемещаем курсор в конец
        self.display.icursor(tk.END)

    def _memory_store(self):
        result = self.calculator.memory_store()
        self.display_var.set(result)
        self.display.focus_set()

    def _memory_recall(self):
        try:
            result = self.calculator.memory_recall()
            self.display_var.set(result)
        except ValueError as e:
            messagebox.showerror("Ошибка", str(e))
        self.display.focus_set()

    def _memory_clear(self):
        result = self.calculator.memory_clear()
        self.display_var.set(result)
        self.display.focus_set()

    def _memory_add(self):
        try:
            result = self.calculator.memory_add()
            self.display_var.set(result)
        except ValueError as e:
            messagebox.showerror("Ошибка", str(e))
        self.display.focus_set()

    def _copy_to_clipboard(self):
        self.root.clipboard_clear()
        self.root.clipboard_append(self.display_var.get())
        self.display.focus_set()

    def _paste_from_clipboard(self):
        try:
            text = self.root.clipboard_get()
            if re.match(r'^[-+]?[0-9]*\.?[0-9]+(/[0-9]+)?$', text):
                for char in text:
                    self.calculator.process_input(char)
                self._update_display()
        except (tk.TclError, ValueError) as e:
            messagebox.showerror("Ошибка", f"Некорректные данные: {str(e)}")
        self.display.focus_set()

    def _set_display_format(self, format_type):
        self.display_format = format_type
        self._update_display()
        self.display.focus_set()

    def _show_about(self):
        messagebox.showinfo("О программе", 
                          "Калькулятор дробей\n"
                          "Поддерживает операции: +, -, *, /\n"
                          "Функции: x², 1/x\n"
                          "Форматы вывода: дробь/десятичная\n"
                          "Маландий И.И. 2025 г.")
        self.display.focus_set()