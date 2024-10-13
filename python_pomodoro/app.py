import customtkinter as ctk

from .settings import Settings
from .tasklist import TaskList
from .tomato_timer import TomatoTimer

"""
Main entry point application.
It will initialize the Tkinter window, setup the app layout, and call the
necessary modules (e.g., GUI, timer, tasks)
"""


class App(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Pomodoro")

        ctk.set_default_color_theme("green")

        # Content frame
        top_container = ctk.CTkFrame(self, fg_color="transparent")
        top_container.pack(side="top", fill="both", expand=True, padx=5, pady=15)

        self.timer = TomatoTimer(top_container, self)
        self.timer.pack(side="left", fill="y", padx=7)

        tasks = TaskList(top_container, self)
        tasks.pack(side="left", fill="both", expand=True, padx=7)

        # Settings frame
        bottom_container = ctk.CTkFrame(self, fg_color="transparent")
        bottom_container.pack(side="top", fill="both", expand=True, padx=10, pady=10)

        self.settings_button = ctk.CTkButton(bottom_container, text="Settings", command=self.show_settings)
        self.settings_button.pack(side="bottom", fill="x")

        self.settings = Settings(bottom_container, self, self.timer, self.settings_button)
        self.settings.resize_window()  # defines initial window dimensions

    def show_settings(self) -> None:
        # expand window to show settings
        self.settings_button.pack_forget()
        self.minsize(600, 700)
        self.maxsize(600, 700)
        self.settings.pack(side="top", fill="y")


def main() -> None:
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()
