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
        main_window.title("Pomodoro")
        main_window.minsize(600, 620)
        main_window.maxsize(700, 680)

        # Content frame
        top_container = ttk.Frame(main_window, padding=5, style="Container.TFrame")
        top_container.pack(side="top", fill="both", expand=True)

        self.timer = TomatoTimer(top_container, main_window)
        self.timer.pack(side="left", fill="y")

        tasks = TaskList(top_container, main_window)
        tasks.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        # Settings frame
        bottom_container = ttk.Frame(main_window, padding=5, style="Container.TFrame")
        bottom_container.pack(side="top", fill="both", expand=True)

        settings = Settings(bottom_container, self.timer)
        settings.pack(side="top", fill="y")


def main() -> None:
    root = tk.Tk()
    _ = Pomodoro(root)
    root.mainloop()


if __name__ == "__main__":
    main()
