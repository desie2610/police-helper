import customtkinter as ctk
import tkinter as tk

from config import *

from data.articles import ARTICLES
from data.fines import FINES

from core.search import search_articles, search_fines

from data.favorites import (
    get_favorites,
    toggle_favorite,
)


class PoliceHelperUI:

    def __init__(self, root):

        self.root = root

        self.mode = "articles"

        self.start_x = 0
        self.start_y = 0

        self.build_window()
        self.build_header()
        self.build_tabs()
        self.build_search()
        self.build_scroll()

        self.show_articles()

    # --------------------------
    # Окно
    # --------------------------

    def build_window(self):

        self.root.title("Police Helper")

        self.root.geometry("500x700")

        self.root.attributes("-topmost", True)

        self.root.configure(
            fg_color=BACKGROUND_COLOR
        )

    # --------------------------
    # Верхняя панель
    # --------------------------

    def build_header(self):

        self.header = ctk.CTkFrame(
            self.root,
            fg_color=FRAME_COLOR,
            corner_radius=12
        )

        self.header.pack(
            fill="x",
            padx=10,
            pady=10
        )

        self.title = ctk.CTkLabel(
            self.header,
            text="🚔 Police Helper",
            font=("Segoe UI", 22, "bold")
        )

        self.title.pack(
            side="left",
            padx=15,
            pady=12
        )

        self.header.bind("<Button-1>", self.start_move)
        self.header.bind("<B1-Motion>", self.move_window)

        self.title.bind("<Button-1>", self.start_move)
        self.title.bind("<B1-Motion>", self.move_window)

    # --------------------------
    # Вкладки
    # --------------------------

    def build_tabs(self):

        self.tabs = ctk.CTkFrame(
            self.root,
            fg_color="transparent"
        )

        self.tabs.pack(
            fill="x",
            padx=10
        )

        self.articles_btn = ctk.CTkButton(
            self.tabs,
            text="🚔 Розшуки",
            command=self.show_articles
        )

        self.articles_btn.pack(
            side="left",
            expand=True,
            padx=4
        )

        self.fines_btn = ctk.CTkButton(
            self.tabs,
            text="💰 Штрафи",
            command=self.show_fines
        )

        self.fines_btn.pack(
            side="left",
            expand=True,
            padx=4
        )

        self.favorite_btn = ctk.CTkButton(
            self.tabs,
            text="⭐ Обране",
            command=self.show_favorites
        )

        self.favorite_btn.pack(
            side="left",
            expand=True,
            padx=4
        )

    # --------------------------
    # Поиск
    # --------------------------

    def build_search(self):

        self.search = ctk.CTkEntry(
            self.root,
            placeholder_text="Пошук...",
            height=40
        )

        self.search.pack(
            fill="x",
            padx=10,
            pady=10
        )

        self.search.bind(
            "<KeyRelease>",
            self.update_search
        )

    # --------------------------
    # Список
    # --------------------------

    def build_scroll(self):

        self.scroll = ctk.CTkScrollableFrame(
            self.root,
            fg_color=FRAME_COLOR,
            corner_radius=12
        )

        self.scroll.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=5
        )
         # --------------------------
    # Очистка списка
    # --------------------------

    def clear_scroll(self):
        for widget in self.scroll.winfo_children():
            widget.destroy()

    # --------------------------
    # Отобразить карточки
    # --------------------------

    def draw_items(self, data, is_fine=False):

        self.clear_scroll()

        if not data:
            label = ctk.CTkLabel(
                self.scroll,
                text="Нічого не знайдено",
                font=("Segoe UI", 18)
            )
            label.pack(pady=20)
            return

        for item in data:

            frame = ctk.CTkFrame(
                self.scroll,
                corner_radius=10
            )

            frame.pack(
                fill="x",
                padx=5,
                pady=5
            )

            if is_fine:
                number, title, price = item
                value = price
                color = "#ffb347"
            else:
                number, title, minutes = item
                value = f"{minutes} ХВ"
                color = "#4CAF50"

            left = ctk.CTkLabel(
                frame,
                text=f"Стаття {number}\n{title}",
                justify="left",
                anchor="w",
                font=("Segoe UI", 15, "bold")
            )

            left.pack(
                side="left",
                padx=15,
                pady=10
            )

            right = ctk.CTkLabel(
                frame,
                text=value,
                text_color=color,
                font=("Segoe UI", 16, "bold")
            )

            right.pack(
                side="right",
                padx=15
            )

            frame.bind(
                "<Double-Button-1>",
                lambda e, a=item: self.favorite_click(a)
            )

            left.bind(
                "<Double-Button-1>",
                lambda e, a=item: self.favorite_click(a)
            )

            right.bind(
                "<Double-Button-1>",
                lambda e, a=item: self.favorite_click(a)
            )

            frame.bind(
                "<Button-1>",
                lambda e, a=item: self.copy_article(a)
            )

            left.bind(
                "<Button-1>",
                lambda e, a=item: self.copy_article(a)
            )

            right.bind(
                "<Button-1>",
                lambda e, a=item: self.copy_article(a)
            )

    # --------------------------
    # Вкладка Розшуки
    # --------------------------

    def show_articles(self):

        self.mode = "articles"

        self.search.delete(0, "end")

        self.draw_items(
            ARTICLES,
            False
        )

    # --------------------------
    # Вкладка Штрафи
    # --------------------------

    def show_fines(self):

        self.mode = "fines"

        self.search.delete(0, "end")

        self.draw_items(
            FINES,
            True
        )

    # --------------------------
    # Вкладка Обране
    # --------------------------

    def show_favorites(self):

        self.mode = "favorites"

        self.search.delete(0, "end")

        favorites = get_favorites()

        self.draw_items(
            favorites,
            False
        )
        # --------------------------
    # Поиск
    # --------------------------

    def update_search(self, event=None):

        query = self.search.get().strip()

        if self.mode == "articles":
            self.draw_items(
                search_articles(query),
                False
            )

        elif self.mode == "fines":
            self.draw_items(
                search_fines(query),
                True
            )

        elif self.mode == "favorites":

            favorites = get_favorites()

            if query == "":
                self.draw_items(favorites, False)
                return

            result = []

            for item in favorites:

                number = item[0]
                title = item[1]

                if (
                    query.casefold() in number.casefold()
                    or
                    query.casefold() in title.casefold()
                ):
                    result.append(item)

            self.draw_items(result, False)

    # --------------------------
    # Копирование статьи
    # --------------------------

    def copy_article(self, article):

        text = f"Стаття {article[0]} - {article[1]}"

        self.root.clipboard_clear()
        self.root.clipboard_append(text)

    # --------------------------
    # Избранное
    # --------------------------

    def favorite_click(self, article):

        toggle_favorite(article)

        if self.mode == "favorites":
            self.show_favorites()

    # --------------------------
    # Перетаскивание окна
    # --------------------------

    def start_move(self, event):

        self.start_x = event.x
        self.start_y = event.y

    def move_window(self, event):

        x = self.root.winfo_x() + event.x - self.start_x
        y = self.root.winfo_y() + event.y - self.start_y

        self.root.geometry(f"+{x}+{y}")
        # --------------------------
    # Подсветка активной вкладки
    # --------------------------

    def update_tab_colors(self):

        active = "#2563eb"
        inactive = "#3b3b3b"

        self.articles_btn.configure(fg_color=inactive)
        self.fines_btn.configure(fg_color=inactive)
        self.favorite_btn.configure(fg_color=inactive)

        if self.mode == "articles":
            self.articles_btn.configure(fg_color=active)

        elif self.mode == "fines":
            self.fines_btn.configure(fg_color=active)

        elif self.mode == "favorites":
            self.favorite_btn.configure(fg_color=active)

    # --------------------------
    # Обновить окно
    # --------------------------

    def refresh(self):

        if self.mode == "articles":
            self.show_articles()

        elif self.mode == "fines":
            self.show_fines()

        else:
            self.show_favorites()

        self.update_tab_colors()

    # --------------------------
    # Горячее обновление
    # --------------------------

    def reload(self):
        self.refresh()

    # --------------------------
    # Закрытие приложения
    # --------------------------

    def close(self):
        self.root.destroy()