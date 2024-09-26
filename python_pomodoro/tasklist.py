from dataclasses import dataclass
from tkinter import Checkbutton, IntVar, Tk, ttk


@dataclass
class Task:
    title: str
    is_complete: bool = False


class TaskList(ttk.Frame):
    def __init__(self, parent: ttk.Frame, main_window: Tk) -> None:
        ttk.Frame.__init__(self, parent)
        self.configure(border=1, borderwidth=1, relief="sunken", padding=10)
        self.main_window = main_window

        label1 = ttk.Label(self, text="Task List", font=("", 14))
        label1.pack(side="top")

        self.task_list = ttk.Frame(self, padding=5)
        self.task_list.pack(side="top")

        self.tasks: list[Task] = []
        for task in self.tasks:
            self.create_task_checkbutton(task)

        self.entry_task_input = ttk.Entry(self)

        self.button_add_task = ttk.Button(self, text="Add new task", command=self.show_task_entry_input)
        self.button_add_task.pack(side="bottom")
        self.button_save_task = ttk.Button(self, text="Save task", command=self.save_new_task)

    def show_task_entry_input(self) -> None:
        self.button_add_task.pack_forget()
        self.button_save_task.pack(side="bottom")
        self.entry_task_input.pack(side="bottom", pady=10)
        self.main_window.bind("<Return>", self.save_new_task)

    def save_new_task(self, event=None) -> None:
        self.button_save_task.pack_forget()
        self.entry_task_input.pack_forget()
        self.button_add_task.pack(side="bottom")
        task = Task(self.entry_task_input.get())
        if task.title:
            self.create_task_checkbutton(task)
            self.tasks.append(task)
        self.main_window.unbind("<Return>")
        self.entry_task_input.delete(0, "end")

    def create_task_checkbutton(self, task: Task) -> None:
        var_is_complete = IntVar()
        checked = 1 if task.is_complete else 0
        var_is_complete.set(checked)
        Checkbutton(self.task_list, text=task.title, variable=var_is_complete, justify="left", wraplength=180).pack(
            anchor="w"
        )
