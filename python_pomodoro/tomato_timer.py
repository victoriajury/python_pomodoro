from dataclasses import dataclass
from enum import Enum
from tkinter import PhotoImage, StringVar, ttk

import customtkinter as ctk
from CTkMessagebox import CTkMessagebox as messagebox
from playsound3 import playsound

from .helpers import get_image_from_resources

"""
Handles all the timer UI components and functionality such as start/pause and
reset buttons or drop-down list to choose the current session.
Displays the timer as Label components with a background image, and are updated as
the timer runs in a while loop.
Data for text colours and defaults are stored in the SessionStatus enum as Session
dataclasses with methods to set the time or reset the defaults.
"""

DEFAULT_CYCLES = 4
TEST_MODE = False


@dataclass
class Time:
    minutes: int
    seconds: int


@dataclass
class Session:
    title: str
    time: Time
    default_time: Time
    image: str
    image_paused: str
    foreground: str
    background: str
    foreground_paused: str
    background_paused: str

    def set_time(self, minutes: int) -> None:
        self.time = Time(minutes=minutes, seconds=0)

    def set_time_to_default(self) -> None:
        self.time = self.default_time


class SessionStatus(Enum):
    FOCUS = Session(
        title="Focus Time",
        time=Time(0, 0),
        default_time=Time(25, 0),
        image="tomato_red_bg.png",
        image_paused="tomato_red_dark_bg.png",
        foreground="#ffc9c9",
        background="#f55453",
        foreground_paused="#ec9291",
        background_paused="#d24847",
    )
    SHORT_BREAK = Session(
        title="Short Break",
        time=Time(0, 0),
        default_time=Time(5, 0),
        image="tomato_yellow_bg.png",
        image_paused="tomato_yellow_dark_bg.png",
        foreground="#ffecc5",
        background="#f5c944",
        foreground_paused="#dcbf70",
        background_paused="#c5a237",
    )
    LONG_BREAK = Session(
        title="Long Break",
        time=Time(0, 0),
        default_time=Time(15, 0),
        image="tomato_green_bg.png",
        image_paused="tomato_green_dark_bg.png",
        foreground="#c2f8c2",
        background="#76c776",
        foreground_paused="#87c387",
        background_paused="#5fa05f",
    )


class TomatoTimer(ctk.CTkFrame):
    def __init__(self, parent: ctk.CTkFrame, main_window: ctk.CTk) -> None:
        ctk.CTkFrame.__init__(self, master=parent)
        self.main_window = main_window

        # DEFAULT STATUS & TIMES
        self.status = SessionStatus.FOCUS
        self.is_paused = False
        self.minutes = StringVar()
        self.seconds = StringVar()
        self.cycles = DEFAULT_CYCLES
        self.current_cycle = 1
        for s in list(SessionStatus):
            s.value.set_time_to_default()

        # APPEARANCE & STYLES

        # TODO Should be using ctk.CTkImage, but the master attribute is missing. Fails tests as image is destroyed.
        # https://github.com/TomSchimansky/CustomTkinter/discussions/2543
        self.bg_images: dict[SessionStatus, PhotoImage] = {
            status: PhotoImage(file=get_image_from_resources(status.value.image), master=self)
            for status in SessionStatus
        }
        self.bg_images_paused: dict[SessionStatus, PhotoImage] = {
            status: PhotoImage(file=get_image_from_resources(status.value.image_paused), master=self)
            for status in SessionStatus
        }
        self.styles = ttk.Style(self)
        self.styles.configure(
            "TimerText.TLabel",
            font=("", 45, "bold"),
            justify="center",
        )
        self.styles.configure("OptionMenu.TMenubutton", width=16)

        # TIMER GUI COMPONENTS
        self.timer_background = ctk.CTkLabel(
            # contains background tomato image and colon seperator ie M:S
            self,
            text=":",
            image=self.bg_images[self.status],
            font=("", 40, "bold"),
            compound="center",
        )
        self.timer_background.grid(row=0, column=0, columnspan=2, padx=10, pady=15)

        timer_minutes = ttk.Label(self, textvariable=self.minutes, style="TimerText.TLabel")
        timer_minutes.grid(row=0, column=0, sticky="e", padx=10)

        timer_seconds = ttk.Label(self, textvariable=self.seconds, style="TimerText.TLabel")
        timer_seconds.grid(row=0, column=1, sticky="w", padx=10)

        self.label_cycles = ctk.CTkLabel(self, text=f"Cycle: {self.current_cycle} of {self.cycles}")
        self.label_cycles.grid(row=0, column=0, columnspan=2, sticky="s", pady=10)

        self.button_reset = ctk.CTkButton(self, text="Reset", command=self.reset_timer)
        self.button_reset.grid(row=1, column=0, sticky="e", padx=5, pady=10)

        self.button_pause = ctk.CTkButton(self, text="Pause", command=self.pause_timer)
        self.button_pause.grid(row=1, column=1, sticky="w", padx=5, pady=10)

        self.button_start = ctk.CTkButton(self, text="Start", command=self.start_timer)
        self.show_start_button()

        session_status_list: list[str] = [status.value.title for status in list(SessionStatus)]
        self.list_selection = StringVar()
        self.list_selection.set(self.status.value.title)
        self.option_menu_session_status = ctk.CTkOptionMenu(
            self,
            values=session_status_list,
            command=lambda x: self.change_session_status(x),
            variable=self.list_selection,
            width=290,
        )
        self.option_menu_session_status.grid(row=2, column=0, columnspan=2)

        self.set_session_time()
        self.update_styles()

    def show_start_button(self) -> None:
        self.button_start.grid(row=1, column=1, sticky="w", padx=5, pady=10)

    def set_cycles(self, cycles: int) -> None:
        self.cycles = cycles
        self.label_cycles.configure(text=f"Cycle: {self.current_cycle} of {cycles}")

    def get_cycles(self) -> int:
        return self.cycles

    def set_status(self, status: SessionStatus) -> None:
        self.status = status
        self.list_selection.set(self.status.value.title)

    def set_session_time(self) -> None:
        # set session time and pad with zeros
        mins = self.status.value.time.minutes
        secs = self.status.value.time.seconds
        self.minutes.set("{0:02}".format(mins))
        self.seconds.set("{0:02}".format(secs))
        self.current_time = int(self.minutes.get()) * 60 + int(self.seconds.get())

    def update_styles(self, reset: bool = False) -> None:
        if self.is_paused and reset is False:
            self.timer_background.configure(
                image=self.bg_images_paused[self.status], text_color=self.status.value.foreground_paused
            )
            self.styles.configure("TimerImage.TLabel", foreground=self.status.value.foreground_paused)
            self.styles.configure(
                "TimerText.TLabel",
                background=self.status.value.background_paused,
                foreground=self.status.value.foreground_paused,
            )
        else:
            self.timer_background.configure(image=self.bg_images[self.status], text_color=self.status.value.foreground)
            self.styles.configure("TimerImage.TLabel", foreground=self.status.value.foreground)
            self.styles.configure(
                "TimerText.TLabel",
                background=self.status.value.background,
                foreground=self.status.value.foreground,
            )

    def start_timer(self) -> None:
        self.is_paused = False  # restart timer
        self.button_start.grid_forget()
        self.update_styles()

        self._countdown(self.current_time)

    def _countdown(self, count: int) -> None:
        # self.main_window.update()
        self.current_time = count

        if self.current_time > -1 and self.is_paused is not True:
            # divmod(firstvalue = temp//60, secondvalue = temp%60)
            mins, secs = divmod(count, 60)
            # set time and pad with zero
            self.minutes.set("{0:02}".format(mins))
            self.seconds.set("{0:02}".format(secs))
            self.main_window.title(f"Pomodoro - {self.status.value.title} - {self.minutes.get()}:{self.seconds.get()}")
            # Call the countdown function recursively until timer runs out
            ms = 5 if TEST_MODE else 1000

            self.main_window.after(ms, self._countdown, count - 1)
        else:
            self.is_paused = True

        if self.current_time == -1:
            self.start_next_session()

    def pause_timer(self) -> None:
        self.is_paused = True
        self.main_window.title(f"{self.status.value.title} - Paused")
        self.show_start_button()
        self.update_styles()

    def reset_timer(self) -> None:
        self.is_paused = True
        self.show_start_button()
        self.set_session_time()
        self.update_styles(reset=True)
        self.main_window.title(f"Pomodoro - {self.status.value.title}")

    def start_next_session(self) -> None:
        if self.status in [SessionStatus.SHORT_BREAK, SessionStatus.LONG_BREAK]:
            next_session = SessionStatus.FOCUS
            start = self.alert_session_ended(next_session)
            # Increment cycle
            self.current_cycle = self.current_cycle + 1 if self.current_cycle < self.cycles else 1
        elif self.current_cycle == self.cycles:
            next_session = SessionStatus.LONG_BREAK
            start = self.alert_session_ended(next_session)
        else:
            next_session = SessionStatus.SHORT_BREAK
            start = self.alert_session_ended(next_session)

        self.set_status(next_session)
        self.label_cycles.configure(text=f"Cycle: {self.current_cycle} of {self.cycles}")
        self.main_window.title(f"Pomodoro - {self.status.value.title}")
        self.show_start_button()
        self.set_session_time()
        self.update_styles(reset=True)

        if start:
            self.start_timer()
        else:
            self.main_window.title(f"Pomodoro - Click Start to begin {self.status.value.title}")

    def alert_session_ended(self, next_session: SessionStatus) -> bool:
        playsound("resources/sounds/short_alert.mp3", block=False)
        cycle_msg = (
            f"You have completed cycle {self.current_cycle} of {self.cycles}.\n"
            if self.status == SessionStatus.SHORT_BREAK
            else ""
        )
        msg = messagebox(
            self.main_window,
            title=f"{self.status.value.title} has ended",
            message=f"{cycle_msg}Would you like to start the next {next_session.value.title.lower()}?",
            icon="question",
            option_1="Yes",
            option_2="No",
            justify="center",
        )
        response = msg.get()
        if response == "Yes":
            return True
        return False

    def change_session_status(self, status_var: StringVar) -> None:
        self.is_paused = True
        for status in list(SessionStatus):
            if status_var == status.value.title:
                self.set_status(status)
        self.main_window.title(f"Pomodoro - Start {self.status.value.title}")
        self.show_start_button()
        self.set_session_time()
        self.update_styles(reset=True)
