import time
from tkinter import PhotoImage, StringVar, ttk

from .helpers import get_image_from_resources

"""
Handles all the user interface components like buttons, sliders,
task checklists, and component layouts
"""


class TomatoTimer(ttk.Frame):
    def __init__(self, parent: ttk.Frame, main_window) -> None:
        ttk.Frame.__init__(self, parent)

        self.main_window = main_window

        self.minutes = StringVar()
        self.seconds = StringVar()
        self.minutes.set("25")
        self.seconds.set("00")

        self.current_time = int(self.minutes.get()) * 60 + int(self.seconds.get())
        self.is_paused = False

        self.bg_image = PhotoImage(file=get_image_from_resources("tomato_timer_bg.png"))

        timer_image = ttk.Label(
            # contains background tomato image and colon seperator ie M:S
            self,
            text=":",
            image=self.bg_image,
            padding=15,
            compound="center",
            style="TimerImage.TLabel",
        )
        timer_image.grid(row=0, column=0, columnspan=2)

        timer_minutes = ttk.Label(self, textvariable=self.minutes, style="TimerText.TLabel")
        timer_minutes.grid(row=0, column=0, sticky="e", padx=10)

        timer_seconds = ttk.Label(self, textvariable=self.seconds, style="TimerText.TLabel")
        timer_seconds.grid(row=0, column=1, sticky="w", padx=10)

        self.button_reset = ttk.Button(self, text="Reset", command=self.reset_timer)
        self.button_reset.grid(row=1, column=0, sticky="e", padx=5)

        self.button_pause = ttk.Button(self, text="Pause", command=self.pause_timer)
        self.button_pause.grid(row=1, column=1, sticky="w", padx=5)
        self.button_start = ttk.Button(self, text="Start", command=self.start_timer)
        self.show_start_button()

    def show_start_button(self):
        self.button_start.grid(row=1, column=1, sticky="w", padx=5)

    def start_timer(self):
        self.is_paused = False  # restart timer
        self.button_start.grid_forget()

        while self.current_time > -1 and self.is_paused is not True:
            # divmod(firstvalue = temp//60, secondvalue = temp%60)
            mins, secs = divmod(self.current_time, 60)

            # set and pad with zero
            self.minutes.set("{0:02}".format(mins))
            self.seconds.set("{0:02}".format(secs))

            # updating the GUI window after decrementing the timer 1 second
            self.main_window.update()
            time.sleep(1)
            self.current_time -= 1

    def pause_timer(self):
        self.is_paused = True
        self.show_start_button()

    def reset_timer(self):
        self.is_paused = True
        self.show_start_button()

        self.minutes.set("25")
        self.seconds.set("00")
        self.current_time = int(self.minutes.get()) * 60 + int(self.seconds.get())


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
