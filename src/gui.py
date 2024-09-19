from tkinter import ttk

"""
Handles all the user interface components like buttons, sliders,
task checklists, and component layouts
"""


class TomatoTimer(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)

        label1 = ttk.Label(self, text="Timer")
        label1.grid(row=0, column=0, columnspan=2)

        button_reset = ttk.Button(self, text="Reset")
        button_reset.grid(row=1, column=0)

        button_start = ttk.Button(self, text="Start")
        button_start.grid(row=1, column=1)


class TaskList(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)

        label1 = ttk.Label(self, text="Tasks")
        label1.grid(row=0, column=0)

        self.task_list = ttk.Frame(self, padding=15)
        self.task_list.grid(row=1, column=0)

        ttk.Checkbutton(self.task_list, text="List item...").grid(row=0, column=0)
        ttk.Checkbutton(self.task_list, text="List item...").grid(row=1, column=0)
        ttk.Checkbutton(self.task_list, text="List item...").grid(row=2, column=0)

        button_add_task = ttk.Button(self, text="Add new task")
        button_add_task.grid(row=2, column=0)


class SettingSlider(ttk.Frame):
    def __init__(self, parent, label_text, min_value, max_value):
        ttk.Frame.__init__(self, parent)

        label1 = ttk.Label(self, text=label_text)
        label1.grid(row=0, column=0)

        slider = ttk.Scale(self, length=150, from_=min_value, to=max_value)
        # label2 = ttk.Label(self, text="Slider")
        slider.grid(row=1, column=0)
