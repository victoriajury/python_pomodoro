from tkinter import IntVar, Scale, Tk, ttk

from .timer import DEFAULT_CYCLES, SessionStatus

"""
Handles all the settings components like control sliders,
for breaks and cycles.
"""


class Settings(ttk.Frame):
    def __init__(self, parent: ttk.Frame, main_window: Tk) -> None:
        ttk.Frame.__init__(self, parent)
        self.main_window = main_window

        setting_focus = SettingSlider(self, "Focus time", 5, 60, int(SessionStatus.FOCUS.value["default_time"][0]))
        setting_focus.grid(row=0, column=0, ipadx=5)

        setting_cycles = SettingSlider(self, "Cycles", 1, 10, DEFAULT_CYCLES)
        setting_cycles.grid(row=0, column=1, ipadx=5)

        setting_short_break = SettingSlider(
            self, "Short Break", 1, 10, int(SessionStatus.SHORT_BREAK.value["default_time"][0])
        )
        setting_short_break.grid(row=1, column=0, ipadx=5, ipady=10)

        setting_long_break = SettingSlider(
            self, "Long Break", 5, 45, int(SessionStatus.LONG_BREAK.value["default_time"][0])
        )
        setting_long_break.grid(row=1, column=1, ipadx=5, ipady=10)

        settings_button = ttk.Button(self, text="Settings")
        settings_button.grid(row=2, column=0, columnspan=2)


class SettingSlider(ttk.Frame):
    def __init__(self, parent: ttk.Frame, label_text: str, min_value: int, max_value: int, default_value: int) -> None:
        ttk.Frame.__init__(self, parent)
        self.value = IntVar()

        self.value.set(default_value)

        self.slider_name_label = ttk.Label(self, text=label_text)
        self.slider_name_label.grid(row=1, column=0, pady=3)

        self.slider = Scale(self, variable=self.value, length=150, from_=min_value, to=max_value, orient="horizontal")
        self.slider.grid(row=0, column=0)
