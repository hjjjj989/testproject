import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

DATA_FILE = 'movies.json'

class MovieLibrary:
    def __init__(self, root):
        self.root = root
        self.root.title('Movie Library')
        self.movies = []

        # --- Ввод полей ---
        frame = ttk.Frame(root)
        frame.pack(pady=10, padx=10, fill='x')
        # Название
        ttk.Label(frame, text='Название:').grid(row=0, column=0, padx=5, sticky='e')
        self.title_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.title_var, width=20).grid(row=0, column=1)
        # Жанр
        ttk.Label(frame, text='Жанр:').grid(row=0, column=2, padx=5, sticky='e')
        self.genre_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.genre_var, width=15).grid(row=0, column=3)
        # Год
        ttk.Label(frame, text='Год:').grid(row=0, column=4, padx=5, sticky='e')
        self.year_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.year_var, width=6).grid(row=0, column=5)
        # Рейтинг
        ttk.Label(frame, text='Рейтинг:').grid(row=0, column=6, padx=5, sticky='e')
        self.rating_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.rating_var, width=4).grid(row=0, column=7)
        # Кнопка добавить
        ttk.Button(frame, text='Добавить фильм', command=self.add_movie).grid(row=0, column=8, padx=10)

        # --- Фильтрация ---
        filter_frame = ttk.Frame(root)
        filter_frame.pack(pady=5)
        ttk.Label(filter_frame, text='Фильтр по жанру:').grid(row=0, column=0)
        self.filter_genre = tk.StringVar()
        ttk.Entry(filter_frame, textvariable=self.filter_genre, width=12).grid(row=0, column=1)
        ttk.Label(filter_frame, text='Фильтр по году:').grid(row=0, column=2)
        self.filter_year = tk.StringVar()
        ttk.Entry(filter_frame, textvariable=self.filter_year, width=8).grid(row=0, column=3)
        ttk.Button(filter_frame, text='Применить фильтр', command=self.apply_filters).grid(row=0, column=4, padx=6)
        ttk.Button(filter_frame, text='Сбросить', command=self.reset_filters).grid(row=0, column=5)

        # --- Таблица фильмов ---
        columns = ['Название', 'Жанр', 'Год', 'Рейтинг']
        self.tree = ttk.Treeview(root, columns=columns, show='headings', height=10)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100 if col != 'Название' else 200)
        self.tree.pack(padx=10, pady=10, fill='both', expand=True)

        self.load_movies()

    def add_movie(self):
        title = self.title_var.get().strip()
        genre = self.genre_var.get().strip()
        year = self.year_var.get().strip()
        rating = self.rating_var.get().strip()
        # Валидация
        if not title or not genre or not year or not rating:
            messagebox.showerror('Ошибка', 'Все поля должны быть заполнены!')
            return
        try:
            year = int(year)
        except ValueError:
            messagebox.showerror('Ошибка', 'Год должен быть числом!')
            return
        try:
            rating = float(rating)
            if not (0 <= rating <= 10):
                raise ValueError
        except ValueError:
            messagebox.showerror('Ошибка', 'Рейтинг должен быть числом от 0 до 10!')
            return
        movie = {"Название": title, "Жанр": genre, "Год": year, "Рейтинг": rating}
        self.movies.append(movie)
        self.save_movies()
        self.reset_fields()
        self.show_movies(self.movies)

    def reset_fields(self):
        self.title_var.set('')
        self.genre_var.set('')
        self.year_var.set('')
        self.rating_var.set('')

    def show_movies(self, movies):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for movie in movies:
            self.tree.insert('', 'end', values=[movie[k] for k in ['Название', 'Жанр', 'Год', 'Рейтинг']])

    def save_movies(self):
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.movies, f, ensure_ascii=False, indent=2)

    def load_movies(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, 'r', encoding='utf-8') as f:
                    self.movies = json.load(f)
            except Exception:
                self.movies = []
        self.show_movies(self.movies)

    def apply_filters(self):
        genre = self.filter_genre.get().strip().lower()
        year = self.filter_year.get().strip()
        movies = self.movies
        if genre:
            movies = [m for m in movies if m['Жанр'].lower() == genre]
        if year:
            movies = [m for m in movies if str(m['Год']) == year]
        self.show_movies(movies)

    def reset_filters(self):
        self.filter_genre.set('')
        self.filter_year.set('')
        self.show_movies(self.movies)

if __name__ == '__main__':
    root = tk.Tk()
    app = MovieLibrary(root)
    root.mainloop()


