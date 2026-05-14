import tkinter as tk
from tkinter import ttk, messagebox
import requests
import json
import os
from datetime import datetime

class CurrencyConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("Конвертер валют")
        self.root.geometry("600x500")

        # API ключ (замените на ваш)
        self.api_key = "YOUR_API_KEY"  # Получите на exchangerate-api.com
        self.base_url = "https://api.exchangerate-api.com/v4/latest/"

        # Переменные
        self.amount = tk.StringVar()
        self.from_currency = tk.StringVar(value="USD")
        self.to_currency = tk.StringVar(value="RUB")
        self.result = tk.StringVar()

        # История
        self.history = []
        self.load_history()

        self.create_widgets()

    def create_widgets(self):
        # Заголовок
        ttk.Label(self.root, text="Конвертер валют", font=("Arial", 16, "bold")).pack(pady=10)

        # Выбор валют
        frame_currencies = ttk.Frame(self.root)
        frame_currencies.pack(pady=10)

        ttk.Label(frame_currencies, text="Из:").grid(row=0, column=0, padx=5)
        from_combo = ttk.Combobox(frame_currencies, textvariable=self.from_currency,
                                   values=self.get_currencies(), width=10)
        from_combo.grid(row=0, column=1, padx=5)

        ttk.Label(frame_currencies, text="В:").grid(row=0, column=2, padx=5)
        to_combo = ttk.Combobox(frame_currencies, textvariable=self.to_currency,
                               values=self.get_currencies(), width=10)
        to_combo.grid(row=0, column=3, padx=5)

        # Поле ввода суммы
        ttk.Label(self.root, text="Сумма:").pack()
        amount_entry = ttk.Entry(self.root, textvariable=self.amount, width=20)
        amount_entry.pack(pady=5)

        # Кнопка конвертации
        convert_btn = ttk.Button(self.root, text="Конвертировать", command=self.convert_currency)
        convert_btn.pack(pady=10)

        # Результат
        ttk.Label(self.root, text="Результат:").pack()
        result_label = ttk.Label(self.root, textvariable=self.result, font=("Arial", 12, "bold"))
        result_label.pack(pady=5)

        # Таблица истории
        ttk.Label(self.root, text="История конвертаций:").pack(pady=(20, 5))

        columns = ("Дата", "Сумма", "Из", "В", "Результат")
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings", height=8)

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)

        self.tree.pack(padx=20, pady=10, fill="both", expand=True)

        # Заполнить таблицу историей
        self.update_history_table()

    def get_currencies(self):
        """Получить список доступных валют"""
        return ["USD", "EUR", "GBP", "JPY", "CAD", "AUD", "CHF", "CNY", "RUB"]

    def convert_currency(self):
        try:
            # Проверка ввода
            amount = float(self.amount.get())
            if amount <= 0:
                messagebox.showerror("Ошибка", "Сумма должна быть положительным числом!")
                return

            from_curr = self.from_currency.get()
            to_curr = self.to_currency.get()

            # Получение курса через API
            response = requests.get(f"{self.base_url}{from_curr}")
            data = response.json()

            if response.status_code != 200 or "rates" not in data:
                messagebox.showerror("Ошибка", "Не удалось получить курсы валют!")
                return

            rate = data["rates"].get(to_curr)
            if not rate:
                messagebox.showerror("Ошибка", f"Курс для валюты {to_curr} не найден!")
                return

            result = amount * rate

            # Обновление результата
            self.result.set(f"{result:.2f} {to_curr}")

            # Добавление в историю
            conversion = {
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "amount": amount,
                "from": from_curr,
                "to": to_curr,
                "result": result
            }
            self.history.append(conversion)
            self.save_history()
            self.update_history_table()

        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректное число!")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка: {e}")

    def load_history(self):
        """Загрузить историю из файла"""
        if os.path.exists("history.json"):
            try:
                with open("history.json", "r", encoding="utf-8") as f:
                    self.history = json.load(f)
            except:
                self.history = []

    def save_history(self):
        """Сохранить историю в файл"""
        with open("history.json", "w", encoding="utf-8") as f:
            json.dump(self.history, f, ensure_ascii=False, indent=2)

    def update_history_table(self):
        """Обновить таблицу истории"""
        for item in self.tree.get_children():
            self.tree.delete(item)

        for record in reversed(self.history[-10:]):  # Последние 10 записей
            self.tree.insert("", "end", values=(
                record["date"],
                f"{record['amount']:.2f}",
                record["from"],
                record["to"],
                f"{record['result']:.2f}"
            ))

if __name__ == "__main__":
    root = tk.Tk()
    app = CurrencyConverter(root)
    root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = CurrencyConverter(root)
    root.mainloop()
