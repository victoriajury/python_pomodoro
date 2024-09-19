import tkinter as tk

"""
Main entry point application.
It will initialize the Tkinter window, setup the app layout, and call the
necessary modules (e.g., GUI, timer, tasks)
"""


class Pomodoro:
    def __init__(self, main_window) -> None:
        # style main window title
        main_window.title("Pomodoro")


def main():
    root = tk.Tk()
    _ = Pomodoro(root)
    root.mainloop()


if __name__ == "__main__":
    main()
