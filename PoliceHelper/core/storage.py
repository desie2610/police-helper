import json
import os

FAVORITES_FILE = "favorites.json"


def load_data():
    """
    Загружает данные из favorites.json.
    """

    if not os.path.exists(FAVORITES_FILE):
        return []

    try:
        with open(FAVORITES_FILE, "r", encoding="utf-8") as file:
            return json.load(file)

    except (json.JSONDecodeError, OSError):
        return []


def save_data(data):
    """
    Сохраняет данные в favorites.json.
    """

    with open(FAVORITES_FILE, "w", encoding="utf-8") as file:
        json.dump(
            data,
            file,
            ensure_ascii=False,
            indent=4
        )


def clear_data():
    """
    Полностью очищает избранное.
    """

    save_data([])


def file_exists():
    """
    Проверяет существование файла.
    """

    return os.path.exists(FAVORITES_FILE)