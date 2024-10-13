from tkinter import IntVar, Tk, ttk

import customtkinter as ctk

from .tomato_timer import DEFAULT_CYCLES, SessionStatus, TomatoTimer

"""
Handles all the settings for the Pomodoro app by calling get and set methods on the
Scale slider controls and passing the values to the SessionStatus enum.

The timer methods for setting the status and resetting are called when the save button is pressed.
Lastly the Settings frame is hidden and the main window resized.
"""


class Settings(ctk.CTkFrame):
    def __init__(self, parent: ttk.Frame, main_window: Tk, timer: TomatoTimer, controller: ttk.Button) -> None:
        ctk.CTkFrame.__init__(self, master=parent)
        self.configure(fg_color="transparent")
        self.main_window = main_window
        self.timer = timer
        self.button = controller

        self.setting_focus_time = SettingSlider(
            self, "Focus time", 5, 60, SessionStatus.FOCUS.value.default_time.minutes
        )
        self.setting_focus_time.grid(row=0, column=0, padx=15)

        self.setting_cycles = SettingSlider(self, "Cycles", 1, 10, DEFAULT_CYCLES)
        self.setting_cycles.grid(row=0, column=1, padx=15)

        self.setting_short_break = SettingSlider(
            self, "Short Break", 1, 10, SessionStatus.SHORT_BREAK.value.default_time.minutes
        )
        self.setting_short_break.grid(row=1, column=0, padx=15, pady=10)

        self.setting_long_break = SettingSlider(
            self, "Long Break", 5, 45, SessionStatus.LONG_BREAK.value.default_time.minutes
        )
        self.setting_long_break.grid(row=1, column=1, padx=15, pady=10)

        self.frame_buttons = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_buttons.grid(row=2, column=0, columnspan=2)
        self.button_reset = ctk.CTkButton(self.frame_buttons, text="Reset", command=self.reset_slider_defaults)
        self.button_reset.grid(row=2, column=0, sticky="e", padx=5, pady=10)
        self.button_save = ctk.CTkButton(self.frame_buttons, text="Save", command=self.update_settings)
        self.button_save.grid(row=2, column=1, sticky="w", padx=5, pady=10)
        self.button_cancel = ctk.CTkButton(self.frame_buttons, text="Cancel", command=self.close_settings)
        self.button_cancel.grid(row=2, column=2, sticky="w", padx=5, pady=10)

    def reset_slider_defaults(self) -> None:
        self.setting_focus_time.set_slider_value(SessionStatus.FOCUS.value.default_time.minutes)
        self.setting_short_break.set_slider_value(SessionStatus.SHORT_BREAK.value.default_time.minutes)
        self.setting_long_break.set_slider_value(SessionStatus.LONG_BREAK.value.default_time.minutes)
        self.setting_cycles.set_slider_value(DEFAULT_CYCLES)

    def update_settings(self) -> None:
        focus_minutes = self.setting_focus_time.get_slider_value()
        SessionStatus.FOCUS.value.set_time(focus_minutes)

        short_break_minutes = self.setting_short_break.get_slider_value()
        SessionStatus.SHORT_BREAK.value.set_time(short_break_minutes)

        long_break_minutes = self.setting_long_break.get_slider_value()
        SessionStatus.LONG_BREAK.value.set_time(long_break_minutes)

        cycles = self.setting_cycles.get_slider_value()
        self.timer.set_cycles(cycles)
        self.timer.current_cycle = 1  # reset cycles after updating settings

        self.timer.set_status(SessionStatus.FOCUS)
        self.timer.reset_timer()
        self.close_settings()

    def close_settings(self) -> None:
        # hide settings after saving
        timer_sliders = ["setting_focus_time", "setting_short_break", "setting_long_break"]

        # User presses cancel without saving the changes to settings
        for s, session in zip(timer_sliders, list(SessionStatus)):
            self.setting_changes_cancelled(s, session)
        if self.setting_cycles.get_slider_value() != self.timer.get_cycles():
            self.setting_cycles.set_slider_value(self.timer.get_cycles())

        self.pack_forget()
        self.button.pack(side="bottom", fill="x", padx=10, pady=10)
        self.resize_window()

    def setting_changes_cancelled(self, slider: str, session: SessionStatus) -> None:
        # User presses cancel without saving the changes to settings
        if self.__getattribute__(slider).get_slider_value() != session.value.time.minutes:
            self.__getattribute__(slider).set_slider_value(session.value.time.minutes)

    def resize_window(self) -> None:
        self.main_window.minsize(600, 538)
        self.main_window.maxsize(600, 538)


class SettingSlider(ctk.CTkFrame):
    def __init__(self, parent: ttk.Frame, label_text: str, min_value: int, max_value: int, default_value: int) -> None:
        ctk.CTkFrame.__init__(self, master=parent)
        self.configure(fg_color="transparent")
        self.label_text = label_text
        self.value = IntVar()
        self.min_value = min_value
        self.max_value = max_value

        self.value.set(default_value)

        self.slider_name_label = ctk.CTkLabel(
            self, text=f"{self.label_text}:  {int(self.value.get())}", justify="left", anchor="w"
        )
        self.slider_name_label.pack(side="top", fill="x", padx=5, pady=2)

        self.slider = ctk.CTkSlider(
            self,
            variable=self.value,
            width=260,
            from_=self.min_value,
            to=self.max_value,
            orientation="horizontal",
            command=self.update_label,
            number_of_steps=(max_value - min_value),
        )
        self.slider.pack(
            side="left",
            pady=10,
        )

    def set_slider_value(self, value: int) -> None:
        # Ensure slider value does not exceed min or max values
        if value < self.min_value:
            self.value.set(self.min_value)
        elif value > self.max_value:
            self.value.set(self.max_value)
        else:
            self.value.set(value)

    def get_slider_value(self) -> int:
        return self.value.get()

    def update_label(self, value) -> None:
        self.slider_name_label.configure(text=f"{self.label_text}:  {int(value)}")
