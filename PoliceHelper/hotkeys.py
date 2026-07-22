from pynput import keyboard
import threading


class HotkeyManager:

    def __init__(self, root):
        self.root = root

        self.visible = True

        self.ctrl_pressed = False

    # --------------------------
    # Скрыть / показать окно
    # --------------------------

    def toggle_window(self):

        if self.visible:

            self.root.withdraw()

        else:

            self.root.deiconify()

            self.root.lift()

            self.root.attributes("-topmost", True)

            self.root.focus_force()

        self.visible = not self.visible

    # --------------------------
    # Нажатие клавиши
    # --------------------------

    def on_press(self, key):

        try:

            if key in (
                keyboard.Key.ctrl_l,
                keyboard.Key.ctrl_r
            ):
                self.ctrl_pressed = True

            elif (
                self.ctrl_pressed
                and hasattr(key, "char")
                and key.char
                and key.char.lower() == "x"
            ):
                self.root.after(
                    0,
                    self.toggle_window
                )

        except Exception:
            pass

    # --------------------------
    # Отпускание клавиши
    # --------------------------

    def on_release(self, key):

        if key in (
            keyboard.Key.ctrl_l,
            keyboard.Key.ctrl_r
        ):
            self.ctrl_pressed = False

    # --------------------------
    # Запуск слушателя
    # --------------------------

    def start(self):

        listener = keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release
        )

        thread = threading.Thread(
            target=listener.run,
            daemon=True
        )

        thread.start()