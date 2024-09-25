import tkinter as tk
from tkinter import Tk, ttk

from .settings import Settings
from .tasklist import TaskList
from .tomato_timer import TomatoTimer

"""
Main entry point application.
It will initialize the Tkinter window, setup the app layout, and call the
necessary modules (e.g., GUI, timer, tasks)
"""


class Pomodoro:
    def __init__(self, main_window: Tk) -> None:
        self.main_window = main_window
        self.main_window.title("Pomodoro")

        # Content frame
        top_container = ttk.Frame(self.main_window, padding=5, style="Container.TFrame")
        top_container.pack(side="top", fill="both", expand=True)

        self.timer = TomatoTimer(top_container, self.main_window)
        self.timer.pack(side="left", fill="y")

        tasks = TaskList(top_container, self.main_window)
        tasks.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        # Settings frame
        bottom_container = ttk.Frame(self.main_window, padding=5, style="Container.TFrame")
        bottom_container.pack(side="top", fill="both", expand=True)

        self.settings_button = ttk.Button(bottom_container, text="Settings", command=self.show_settings)
        self.settings_button.pack(side="bottom", fill="x")

        self.settings = Settings(bottom_container, self.main_window, self.timer, self.settings_button)
        self.settings.resize_window()  # defines initial window dimensions

    def show_settings(self) -> None:
        # expand window to show settings
        self.settings_button.pack_forget()
        self.main_window.minsize(600, 700)
        self.main_window.maxsize(600, 700)
        self.settings.pack(side="top", fill="y")


def main() -> None:
    root = tk.Tk()
    _ = Pomodoro(root)
    root.mainloop()


if __name__ == "__main__":
    main()
