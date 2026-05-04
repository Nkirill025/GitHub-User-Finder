import tkinter as tk
from tkinter import messagebox, simpledialog
import requests
import json
import os

# --- Настройки ---
API_URL = "https://api.github.com/search/users"
FAV_FILE = "favorites.json"

# --- Загрузка избранного ---
def load_favorites():
    if os.path.exists(FAV_FILE):
        with open(FAV_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

# --- Сохранение избранного ---
def save_favorites(favorites):
    with open(FAV_FILE, 'w', encoding='utf-8') as f:
        json.dump(favorites, f, indent=4)

# --- Поиск пользователей ---
def search_users(query):
    try:
        response = requests.get(API_URL, params={'q': query})
        response.raise_for_status()
        data = response.json()
        return data.get('items', [])
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось выполнить запрос: {e}")
        return []

# --- Обновление списка в GUI ---
def update_listbox(results, favorites):
    listbox.delete(0, tk.END)
    for user in results:
        login = user['login']
        is_fav = login in favorites
        display_name = f"★ {login}" if is_fav else login
        listbox.insert(tk.END, display_name)

# --- Обработчик поиска ---
def on_search():
    query = entry_search.get().strip()
    if not query:
        messagebox.showwarning("Внимание", "Поле поиска не должно быть пустым")
        return

    results = search_users(query)
    favorites = load_favorites()
    update_listbox(results, favorites)

# --- Добавление в избранное ---
def add_to_favorites():
    selected = listbox.curselection()
    if not selected:
        messagebox.showwarning("Внимание", "Выберите пользователя из списка")
        return

    index = selected[0]
    user_text = listbox.get(index)
    login = user_text.replace('★ ', '').strip()

    favorites = load_favorites()
    if login not in favorites:
        favorites.append(login)
        save_favorites(favorites)
        # Обновляем отображение в списке
        update_listbox(search_users(entry_search.get().strip()), favorites)

# --- Создание GUI ---
root = tk.Tk()
root.title("GitHub User Finder")
root.geometry("400x500")

# Поле ввода
entry_search = tk.Entry(root, width=40)
entry_search.pack(pady=10)

# Кнопка поиска
btn_search = tk.Button(root, text="Поиск", command=on_search)
btn_search.pack(pady=5)

# Список результатов
listbox = tk.Listbox(root, width=40, height=20)
listbox.pack(pady=10, padx=20)

# Кнопка избранного
btn_fav = tk.Button(root, text="Добавить в избранное", command=add_to_favorites)
btn_fav.pack(pady=5)

root.mainloop()