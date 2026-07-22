import json
import os

FAVORITES_FILE = "favorites.json"


def load_favorites():
    """
    Загружает избранное из файла.
    """
    if not os.path.exists(FAVORITES_FILE):
        return []

    try:
        with open(FAVORITES_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except Exception:
        return []


def save_favorites(favorites):
    """
    Сохраняет избранное в файл.
    """
    with open(FAVORITES_FILE, "w", encoding="utf-8") as file:
        json.dump(favorites, file, ensure_ascii=False, indent=4)


def add_favorite(article):
    """
    Добавить статью в избранное.
    article = ("5.10", "Хуліганство", 15)
    """
    favorites = load_favorites()

    if article not in favorites:
        favorites.append(article)
        save_favorites(favorites)


def remove_favorite(article):
    """
    Удалить статью из избранного.
    """
    favorites = load_favorites()

    if article in favorites:
        favorites.remove(article)
        save_favorites(favorites)


def is_favorite(article):
    """
    Проверяет, находится ли статья в избранном.
    """
    return article in load_favorites()


def toggle_favorite(article):
    """
    Добавляет или удаляет статью из избранного.
    """
    if is_favorite(article):
        remove_favorite(article)
    else:
        add_favorite(article)


def get_favorites():
    """
    Возвращает список избранных статей.
    """
    return load_favorites()