from dataclasses import dataclass
from string import punctuation
from tkinter import Checkbutton, IntVar, Tk, ttk
from typing import Optional
from uuid import UUID, uuid4

import customtkinter as ctk

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

        self.tasks_by_id: dict[UUID, Task] = {}

        self.label_task_input = ctk.CTkLabel(self)
        self.entry_task_input = ttk.Entry(self)

        self.button_add_task = ctk.CTkButton(self, text="Add new task", command=self.show_task_entry_input)
        self.button_add_task.pack(side="bottom")

        self.button_save_task = ctk.CTkButton(self, text="Save task", command=self.save_new_task)
        self.button_clear_task = ctk.CTkButton(self, text="Clear completed", command=self.clear_completed_tasks)
        self.show_hide_clear_task_button()

    def show_task_entry_input(self, event=None) -> None:
        self.button_add_task.pack_forget()
        self.label_task_input.pack_forget()
        self.button_save_task.pack(side="bottom")
        self.entry_task_input.pack(side="bottom", pady=10)
        self.entry_task_input.focus_set()
        # Press enter key to save task
        self.main_window.bind("<Return>", self.save_new_task)

    def save_new_task(self, event=None) -> UUID | None:
        input_data = self.entry_task_input.get()

        error = False

        if not len(input_data) > 0:  # no text entered
            self.label_task_input.configure(text="Please enter a task...", text_color="grey")
            error = True
        elif not len(input_data) < 100:  # text too long
            self.label_task_input.configure(text="Task too long (max 100 chars.)", text_color="grey")
            error = True
        elif all(char in punctuation for char in input_data):  # only punctuation
            self.label_task_input.configure(text="Please enter a valid task name.", text_color="grey")
            error = True
        elif all(char.isspace() for char in input_data):  # only whitespaces
            self.label_task_input.configure(text="Please enter a valid task name.", text_color="grey")
            error = True
        elif any(task.title for task in self.tasks_by_id.values() if input_data.lower() == task.title.lower()):
            # check for duplicates
            self.label_task_input.configure(text="Duplicate task name.", text_color="grey")
            error = True

        if not error:
            id = uuid4()
            task = Task(id=id, title=input_data)
            self.create_task_checkbutton(task)
            self.tasks_by_id[id] = task
            self.show_hide_clear_task_button()

            # Prevent new task creation with enter key and clear input
            self.main_window.unbind("<Return>")
            self.entry_task_input.delete(0, "end")
            self.button_add_task.focus()
            self.main_window.bind("<Return>", self.show_task_entry_input)

            self.button_save_task.pack_forget()
            self.entry_task_input.pack_forget()
            self.label_task_input.pack_forget()
            self.button_add_task.pack(side="bottom")
            return id

        self.label_task_input.pack(side="bottom")
        return None

    def show_hide_clear_task_button(self) -> None:
        if len(self.tasks_by_id) > 0:
            self.button_clear_task.pack()
        else:
            self.button_clear_task.pack_forget()

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

    def toggle_task_complete(self, task: Task, checked: IntVar) -> None:
        off_color = "black"
        on_color = "gray"
        if task.checkbox:
            task.checkbox["fg"] = on_color if checked.get() else off_color
            task.is_complete = bool(checked.get())
        else:
            self.tasks_by_id.pop(task.id)

    def clear_completed_tasks(self) -> None:
        uuids = []
        for _, task in self.tasks_by_id.items():
            if task.checkbox and task.is_complete:
                uuids.append(task.id)
                task.checkbox.destroy()
        for id in uuids:
            self.tasks_by_id.pop(id)
        self.show_hide_clear_task_button()
