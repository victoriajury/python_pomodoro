import tkinter as tk
from tkinter import ttk

import pytest
from python_pomodoro.settings import Settings
from python_pomodoro.tomato_timer import TomatoTimer


@pytest.fixture
def root_window():
    """Fixture to create a root window for the tests."""
    root = tk.Tk()
    yield root
    root.destroy()


@pytest.fixture
def tomato_timer(root_window):
    """Fixture to initialize the TomatoTimer object."""
    return TomatoTimer(parent=root_window, main_window=root_window)


@pytest.fixture
def settings(root_window):
    """Fixture to initialize the Settings object."""
    settings_button = ttk.Button(root_window)
    settings_button.pack()
    timer = TomatoTimer(parent=root_window, main_window=root_window)
    return Settings(parent=root_window, main_window=root_window, timer=timer, controller=settings_button)
