from tkinter import Tk, ttk


class TaskList(ttk.Frame):
    def __init__(self, parent: ttk.Frame, main_window: Tk) -> None:
        ttk.Frame.__init__(self, parent)
        self.configure(border=1, borderwidth=1, relief="sunken", padding=10)
        self.main_window = main_window

        label1 = ttk.Label(self, text="Tasks")
        label1.pack(side="top")

        self.task_list = ttk.Frame(self, padding=15)
        self.task_list.pack(side="top")

        ttk.Checkbutton(self.task_list, text="List item...").pack()
        ttk.Checkbutton(self.task_list, text="List item...").pack()
        ttk.Checkbutton(self.task_list, text="List item...").pack()

        button_add_task = ttk.Button(self, text="Add new task")
        button_add_task.pack(side="bottom")
