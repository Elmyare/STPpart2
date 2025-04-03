import json
import os
from collections import defaultdict

class PhoneBook:
    def __init__(self):
        self.entries = defaultdict(list)
        
    def add_entry(self, name, phone):
        """Добавляет запись, автоматически сортируя по именам"""
        if phone not in self.entries[name]:  # Проверка на дубликаты
            self.entries[name].append(phone)
            self.entries[name].sort()
        self.entries = dict(sorted(self.entries.items())) # Аналог multimap'a делаем
    
    def edit_entry(self, old_name, new_name, new_phone):
        """Редактирует запись с сохранением всех телефонов"""
        if old_name in self.entries:
            phones = self.entries.pop(old_name)
            if new_phone in phones:
                phones.remove(new_phone)
            self.add_entry(new_name, new_phone)
            for phone in phones:
                self.add_entry(new_name, phone)
            return True
        return False
    
    def delete_entry(self, name, phone=None):
        """Удаляет либо конкретный телефон, либо все записи по имени"""
        if name in self.entries:
            if phone:
                if phone in self.entries[name]:
                    self.entries[name].remove(phone)
                    if not self.entries[name]:
                        del self.entries[name]
            else:
                del self.entries[name]
            return True
        return False
    
    def search(self, name):
        """Возвращает все телефоны для имени (аналог equal_range в multimap)"""
        return self.entries.get(name, [])
    
    def get_all_entries(self):
        """Возвращает все записи в виде отсортированного словаря"""
        return dict(sorted(self.entries.items()))
    
    def clear(self):
        """Очищает все записи"""
        self.entries.clear()
    
    def save_to_file(self, filename):
        """Сохраняет в JSON файл"""
        with open(filename, 'w') as f:
            json.dump(dict(self.entries), f, ensure_ascii=False, indent=2)
    
    def load_from_file(self, filename):
        """Загружает из JSON файла"""
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                loaded = json.load(f)
                self.entries = defaultdict(list)
                for name, phones in loaded.items():
                    self.entries[name] = phones
                self.entries = dict(sorted(self.entries.items()))