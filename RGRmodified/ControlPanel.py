import re
from ControlDevice import ControlDevice
import tkinter as tk
from tkinter import messagebox

class ControlPanel:
    """Панель управления калькулятором (GUI)"""
    def __init__(self, root):
        self._root = root
        self._root.title("Калькулятор дробей")
        self._device = ControlDevice()
        self._display_format = 'fraction'
        self._setup_ui()
    
    def _setup_ui(self):
        # Главное окно
        self._display_var = tk.StringVar()
        self._display_var.set("0")
        
        # Фрейм дисплея
        display_frame = tk.Frame(self._root)
        display_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Поле ввода
        self._display = tk.Entry(
            display_frame, 
            textvariable=self._display_var,
            font=('Arial', 24),
            bd=5,
            justify='right',
            state='normal',
            readonlybackground='white'
        )
        self._display.pack(fill=tk.X, ipady=10)
        self._display.bind('<Key>', self._handle_key_press)
        self._display.bind('<Return>', lambda e: self._on_button_click('='))
        self._display.focus_set()

        # Меню
        menubar = tk.Menu(self._root)
        
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
        
        self._root.config(menu=menubar)
        
        # Кнопки памяти
        memory_frame = tk.Frame(self._root)
        memory_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Button(memory_frame, text="MC", width=5, command=self._memory_clear).pack(side=tk.LEFT)
        tk.Button(memory_frame, text="MR", width=5, command=self._memory_recall).pack(side=tk.LEFT)
        tk.Button(memory_frame, text="MS", width=5, command=self._memory_store).pack(side=tk.LEFT)
        tk.Button(memory_frame, text="M+", width=5, command=self._memory_add).pack(side=tk.LEFT)
        
        # Основные кнопки
        button_frame = tk.Frame(self._root)
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
        self._display_var.trace_add('write', self._validate_input)

    def _handle_key_press(self, event):
        allowed_chars = {'0','1','2','3','4','5','6','7','8','9','/','-','.',"+", "*"}
        
        if event.char in allowed_chars:
            try:
                result = self._device.process_input(event.char)
                self._display_var.set(result)
                self._display.icursor(tk.END)
            except ValueError as e:
                messagebox.showerror("Ошибка", str(e))
            return "break"
        elif event.keysym in ('BackSpace', 'Delete', 'Left', 'Right'):
            return
        else:
            return "break"

    def _validate_input(self, *args):
        current_text = self._display_var.get()
        if not re.match(r'^[-+]?[0-9]*\.?[0-9]*([/][0-9]*)?$', current_text):
            self._display_var.set(current_text[:-1])

    def _on_button_click(self, button):
        try:
            result = self._device.process_input(button)
            self._display_var.set(result)
            self._display.icursor(tk.END)
        except ValueError as e:
            messagebox.showerror("Ошибка", str(e))
        self._display.focus_set()

    def _memory_store(self):
        result = self._device.memory_store()
        self._display_var.set(result)
        self._display.focus_set()

    def _memory_recall(self):
        try:
            result = self._device.memory_recall()
            self._display_var.set(result)
        except ValueError as e:
            messagebox.showerror("Ошибка", str(e))
        self._display.focus_set()

    def _memory_clear(self):
        result = self._device.memory_clear()
        self._display_var.set(result)
        self._display.focus_set()

    def _memory_add(self):
        try:
            result = self._device.memory_add()
            self._display_var.set(result)
        except ValueError as e:
            messagebox.showerror("Ошибка", str(e))
        self._display.focus_set()

    def _copy_to_clipboard(self):
        self._root.clipboard_clear()
        self._root.clipboard_append(self._display_var.get())
        self._display.focus_set()

    def _paste_from_clipboard(self):
        try:
            text = self._root.clipboard_get()
            if re.match(r'^[-+]?[0-9]*\.?[0-9]+(/[0-9]+)?$', text):
                for char in text:
                    self._device.process_input(char)
                self._display_var.set(self._device._editor.buffer)
        except (tk.TclError, ValueError) as e:
            messagebox.showerror("Ошибка", f"Некорректные данные: {str(e)}")
        self._display.focus_set()

    def _set_display_format(self, format_type):
        self._display_format = format_type
        current_value = self._device._editor.number
        if format_type == 'fraction':
            if current_value.value.denominator == 1:
                self._display_var.set(str(current_value.value.numerator))
            else:
                self._display_var.set(f"{current_value.value.numerator}/{current_value.value.denominator}")
        else:
            self._display_var.set(str(float(current_value.value)))
        self._display.focus_set()

    def _show_about(self):
        messagebox.showinfo("О программе", 
                          "Калькулятор дробей\n"
                          "Поддерживает операции: +, -, *, /\n"
                          "Функции: x², 1/x\n"
                          "Форматы вывода: дробь/десятичная\n"
                          "Маландий И.И. 2025 г.")
        self._display.focus_set()