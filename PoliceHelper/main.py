import customtkinter as ctk

from ui import PoliceHelperUI
from hotkeys import HotkeyManager


def main():
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()

    app = PoliceHelperUI(root)

    hotkeys = HotkeyManager(root)
    hotkeys.start()

    root.mainloop()


if __name__ == "__main__":
    main()