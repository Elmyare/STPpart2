import tkinter as tk
from tkinter import messagebox, simpledialog
from PhoneBook import PhoneBook

class PhoneBookApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Телефонная книга")
        self.phone_book = PhoneBook()
        self.filename = "phonebook.json"
        
        self.phone_book.load_from_file(self.filename)
        self.create_widgets()
        self.update_entries_list()
    
    def create_widgets(self):
        # Фрейм для ввода данных
        input_frame = tk.Frame(self.root, padx=10, pady=10)
        input_frame.pack(fill=tk.X)
        
        tk.Label(input_frame, text="Имя:").grid(row=0, column=0, sticky=tk.W)
        self.name_entry = tk.Entry(input_frame, width=30)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(input_frame, text="Телефон:").grid(row=1, column=0, sticky=tk.W)
        self.phone_entry = tk.Entry(input_frame, width=30)
        self.phone_entry.grid(row=1, column=1, padx=5, pady=5)
        
        # Фрейм для кнопок
        button_frame = tk.Frame(self.root, padx=10, pady=5)
        button_frame.pack(fill=tk.X)
        
        tk.Button(button_frame, text="Добавить", command=self.add_entry).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Поиск", command=self.search_entry).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Редактировать", command=self.edit_entry).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Удалить", command=self.delete_entry).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Очистить книгу", command=self.clear_phonebook).pack(side=tk.LEFT, padx=5)
        
        # Список записей
        list_frame = tk.Frame(self.root, padx=10, pady=10)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        self.entries_listbox = tk.Listbox(list_frame, width=50, height=15)
        self.entries_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(list_frame, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.entries_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.entries_listbox.yview)
        
        self.entries_listbox.bind("<Double-Button-1>", self.show_phones)
    
    def update_entries_list(self):
        self.entries_listbox.delete(0, tk.END)
        for name in self.phone_book.get_all_entries():
            self.entries_listbox.insert(tk.END, name)
    
    def add_entry(self):
        name = self.name_entry.get().strip()
        phone = self.phone_entry.get().strip()
        
        if not name or not phone:
            messagebox.showerror("Ошибка", "Заполните все поля!")
            return
        
        self.phone_book.add_entry(name, phone)
        self.update_entries_list()
        self.phone_book.save_to_file(self.filename)
        
        self.name_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        messagebox.showinfo("Успех", "Запись добавлена!")
    
    def search_entry(self):
        search_term = simpledialog.askstring("Поиск", "Введите имя для поиска:")
        if search_term:
            results = self.phone_book.search(search_term)
            if results:
                message = f"Телефоны для {search_term}:\n" + "\n".join(results)
                messagebox.showinfo("Результаты поиска", message)
            else:
                messagebox.showinfo("Результаты поиска", "Записи не найдены")
    
    def edit_entry(self):
        selected = self.entries_listbox.curselection()
        if not selected:
            messagebox.showerror("Ошибка", "Выберите запись для редактирования!")
            return
        
        old_name = self.entries_listbox.get(selected)
        phones = self.phone_book.search(old_name)
        
        if not phones:
            return
        
        new_name = simpledialog.askstring("Редактирование", "Новое имя:", initialvalue=old_name)
        if not new_name:
            return
        
        new_phone = simpledialog.askstring("Редактирование", "Новый телефон:", initialvalue=phones[0])
        if not new_phone:
            return
        
        self.phone_book.edit_entry(old_name, new_name, new_phone)
        self.update_entries_list()
        self.phone_book.save_to_file(self.filename)
        messagebox.showinfo("Успех", "Запись обновлена!")
    
    def delete_entry(self):
        selected = self.entries_listbox.curselection()
        if not selected:
            messagebox.showerror("Ошибка", "Выберите запись для удаления!")
            return
        
        name = self.entries_listbox.get(selected)
        phones = self.phone_book.search(name)
        
        if len(phones) > 1:
            phone_to_delete = simpledialog.askstring("Удаление", 
                                                   f"Выберите телефон для удаления (оставьте пустым для удаления всех):\n{', '.join(phones)}")
            if phone_to_delete is None:
                return
        else:
            phone_to_delete = None if not phones else phones[0]
        
        if phone_to_delete == "":
            self.phone_book.delete_entry(name)
        else:
            self.phone_book.delete_entry(name, phone_to_delete)
        
        self.update_entries_list()
        self.phone_book.save_to_file(self.filename)
        messagebox.showinfo("Успех", "Запись удалена!")
    
    def clear_phonebook(self):
        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите очистить всю телефонную книгу?"):
            self.phone_book.clear()
            self.update_entries_list()
            self.phone_book.save_to_file(self.filename)
            messagebox.showinfo("Успех", "Телефонная книга очищена!")
    
    def show_phones(self, event):
        selected = self.entries_listbox.curselection()
        if selected:
            name = self.entries_listbox.get(selected)
            phones = self.phone_book.search(name)
            if phones:
                messagebox.showinfo("Телефоны", f"{name}:\n" + "\n".join(phones))
    
    def on_closing(self):
        self.phone_book.save_to_file(self.filename)
        self.root.destroy()