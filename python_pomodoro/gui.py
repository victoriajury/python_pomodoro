from tkinter import PhotoImage, ttk

from .helpers import get_image_from_resources

"""
Handles all the user interface components like buttons, sliders,
task checklists, and component layouts
"""


class TomatoTimer(ttk.Frame):
    def __init__(self, parent: ttk.Frame) -> None:
        ttk.Frame.__init__(self, parent)

        self.bg_image = PhotoImage(file=get_image_from_resources("tomato_timer_bg.png"))

        timer = ttk.Label(
            self,
            text="Timer",
            image=self.bg_image,
            compound="center",
            padding=10,
        )
        timer.grid(row=0, column=0, columnspan=2)

        button_reset = ttk.Button(self, text="Reset")
        button_reset.grid(row=1, column=0, sticky="e", padx=5)

        button_start = ttk.Button(self, text="Start")
        button_start.grid(row=1, column=1, sticky="w", padx=5)


class TaskList(ttk.Frame):
    def __init__(self, parent: ttk.Frame) -> None:
        ttk.Frame.__init__(self, parent)
        self.configure(border=1, borderwidth=1, relief="sunken", padding=10)

        label1 = ttk.Label(self, text="Tasks")
        label1.pack(side="top")

        self.task_list = ttk.Frame(self, padding=15)
        self.task_list.pack(side="top")

        ttk.Checkbutton(self.task_list, text="List item...").pack()
        ttk.Checkbutton(self.task_list, text="List item...").pack()
        ttk.Checkbutton(self.task_list, text="List item...").pack()

        button_add_task = ttk.Button(self, text="Add new task")
        button_add_task.pack(side="bottom")


class SettingSlider(ttk.Frame):
    def __init__(self, parent: ttk.Frame, label_text: str, min_value: int, max_value: int) -> None:
        ttk.Frame.__init__(self, parent)

        label1 = ttk.Label(self, text=label_text)
        label1.grid(row=0, column=0)

        slider = ttk.Scale(self, length=150, from_=min_value, to=max_value)
        # label2 = ttk.Label(self, text="Slider")
        slider.grid(row=1, column=0)
