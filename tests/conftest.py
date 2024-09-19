import tkinter as tk

import pytest
from python_pomodoro.app import Pomodoro


@pytest.fixture
def app():
    root = tk.Tk()
    app = Pomodoro(root)
    return app
