from dataclasses import dataclass
from tkinter import Checkbutton, IntVar, Tk, ttk
from typing import Optional
from uuid import UUID, uuid4

"""
Handles creation of tasks in tasklist.
New tasks are created as checkboxes and when completed/checked are coloured grey.
"""


@dataclass
class Task:
    id: UUID
    title: str
    is_complete: bool = False
    checkbox: Optional[Checkbutton] = None


class TaskList(ttk.Frame):
    def __init__(self, parent: ttk.Frame, main_window: Tk) -> None:
        ttk.Frame.__init__(self, parent)
        self.configure(border=1, borderwidth=1, relief="sunken", padding=10)
        self.main_window = main_window

        # TASKLIST GUI COMPONENTS
        label1 = ttk.Label(self, text="Task List", font=("", 14))
        label1.pack(side="top")

        self.task_list = ttk.Frame(self, padding=5)
        self.task_list.pack(side="top")

        # Create some test tasks:
        task1_id = uuid4()
        self.tasks_by_id: dict[UUID, Task] = {task1_id: Task(id=task1_id, title="Some task")}
        for _, task in self.tasks_by_id.items():
            self.create_task_checkbutton(task)

        self.entry_task_input = ttk.Entry(self)

        self.button_add_task = ttk.Button(self, text="Add new task", command=self.show_task_entry_input)
        self.button_add_task.pack(side="bottom")

        self.button_save_task = ttk.Button(self, text="Save task", command=self.save_new_task)

    def show_task_entry_input(self) -> None:
        self.button_add_task.pack_forget()
        self.button_save_task.pack(side="bottom")
        self.entry_task_input.pack(side="bottom", pady=10)
        self.entry_task_input.focus()
        # Press enter key to save task
        self.main_window.bind("<Return>", self.save_new_task)

    def save_new_task(self, event=None) -> None:
        self.button_save_task.pack_forget()
        self.entry_task_input.pack_forget()
        self.button_add_task.pack(side="bottom")

        task = Task(uuid4(), self.entry_task_input.get())
        if task.title:
            self.create_task_checkbutton(task)

        # Prevent new task creation with enter key and clear input
        self.main_window.unbind("<Return>")
        self.entry_task_input.delete(0, "end")
        self.focus()

    def create_task_checkbutton(self, task: Task) -> None:
        is_complete = IntVar()
        checked = 1 if task.is_complete else 0
        is_complete.set(checked)
        checkbox = Checkbutton(
            self.task_list,
            text=task.title,
            variable=is_complete,
            justify="left",
            wraplength=180,
            command=lambda: self.toggle_task_complete(task, is_complete),
        )
        checkbox.pack(anchor="w")
        task.checkbox = checkbox

    def toggle_task_complete(self, task: Task, is_checked: IntVar):
        off_color = "black"
        on_color = "gray"
        if task.checkbox:
            task.checkbox["fg"] = on_color if is_checked.get() else off_color
