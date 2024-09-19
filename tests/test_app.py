import tkinter as tk
from unittest.mock import patch

# import pytest
from python_pomodoro.app import main


# A simple test to check that root.mainloop() is called
# Mock the mainloop method to prevent it from blocking the test
@patch.object(tk.Tk, "mainloop")
def test_mainloop(mock_mainloop):
    # Call the function that initializes and starts the app
    main()

    # Check if mainloop was called
    mock_mainloop.assert_called_once()
