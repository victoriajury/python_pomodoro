import tkinter as tk
from _tkinter import TclError
from tkinter import ttk
from typing import Any

import pytest
from python_pomodoro.app import Pomodoro
from python_pomodoro.settings import Settings
from python_pomodoro.tasklist import TaskList
from python_pomodoro.tomato_timer import TomatoTimer


@pytest.fixture
def root_window():
    """Fixture to create a root window for the tests."""
    root = tk.Tk()
    yield root
    root.destroy()


@pytest.fixture
def app(root_window):
    """Fixture to initialize the main app object."""
    return Pomodoro(main_window=root_window)


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


@pytest.fixture
def tasks(root_window):
    """Fixture to initialize the TaskList object."""
    return TaskList(parent=root_window, main_window=root_window)


class TestFunctions:
    @staticmethod
    def test_object_is_hidden(object: Any) -> bool:
        with pytest.raises(TclError) as e:
            # pack_info() raises: ' window ".!button" isn't packed'
            # instead of returning empty dict, like grid_info()
            assert bool(object.pack_info()) is False
        assert "isn't packed" in e.value.__str__()
        return True


@pytest.fixture
def test_functions():
    return TestFunctions
