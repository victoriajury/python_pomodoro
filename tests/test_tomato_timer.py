from unittest.mock import MagicMock, patch

import customtkinter as ctk
import pytest
from python_pomodoro.tomato_timer import SessionStatus


def test_tomato_timer_initialization(tomato_timer):
    # Assert that TomatoTimer initializes with the correct session status
    assert tomato_timer.status == SessionStatus.FOCUS
    assert tomato_timer.is_paused is False

    # Assert that time variables (minutes, seconds) are set correctly
    assert tomato_timer.minutes.get() == "25"
    assert tomato_timer.seconds.get() == "00"

    # Assert that the number of cycles is set correctly
    assert tomato_timer.cycles == 4  # Assuming DEFAULT_CYCLES is 4 in app
    assert tomato_timer.current_cycle == 1


def test_show_start_button(tomato_timer):
    # Mock the grid method to prevent actual layout changes in tests
    with patch.object(ctk.CTkButton, "grid") as mock_grid:
        tomato_timer.show_start_button()
        # Assert that grid() was called once, meaning the button was shown
        mock_grid.assert_called_once()


def test_reset_timer(tomato_timer):
    # Mock the update_styles and set_session_time methods to isolate reset behavior
    with (
        patch.object(tomato_timer, "update_styles") as mock_update_styles,
        patch.object(tomato_timer, "set_session_time") as mock_set_session_time,
    ):

        tomato_timer.reset_timer()

        # Assert the timer is paused after reset
        assert tomato_timer.is_paused is True

        # Assert that the start button is shown
        # NB: winfo_ismapped() does not work, whereas grid_info is empty dict after grid_forget()
        assert bool(tomato_timer.button_start.grid_info()) is True  # Button should be visible

        # Ensure session time and styles are reset
        mock_update_styles.assert_called_once_with(reset=True)
        mock_set_session_time.assert_called_once()


def test_start_timer(tomato_timer):
    with (
        patch.object(tomato_timer, "main_window", create=True) as mock_main_window,
        patch.object(tomato_timer, "start_next_session") as mock_start_next_session,
    ):
        mock_main_window.update = MagicMock()

        # Set timer to 1 minute to speed up test
        tomato_timer.status.value.set_time(1)
        tomato_timer.set_session_time()

        tomato_timer.start_timer(testing=True)
        assert tomato_timer.current_time == -1
        mock_start_next_session.assert_called_once()

        # Ensure that the timer starts and styles are updated
        assert tomato_timer.is_paused is False
        assert not bool(tomato_timer.button_start.grid_info())  # Button should be hidden after start


def test_pause_timer(tomato_timer):
    with patch.object(tomato_timer, "update_styles") as mock_update_styles:
        tomato_timer.is_paused = False  # restart timer
        tomato_timer.button_start.grid_forget()

        tomato_timer.pause_timer()

        assert tomato_timer.is_paused is True
        # assert tomato_timer.main_window

        assert tomato_timer.main_window.title() == "Focus Time - Paused"

        # Assert that the start button is shown
        assert bool(tomato_timer.button_start.grid_info()) is True

        # Ensure that the timer styles are updated
        mock_update_styles.assert_called_once()


def test_pause_at_zero(tomato_timer):
    # Test: Pausing the timer when it reaches zero

    # Set the timer to zero (manually simulate the timer hitting zero)
    tomato_timer.minutes.set("00")
    tomato_timer.seconds.set("00")
    tomato_timer.current_time = 0

    # Pause the timer
    tomato_timer.pause_timer()

    # Assert timer is paused and at zero
    assert tomato_timer.is_paused is True
    assert tomato_timer.minutes.get() == "00"
    assert tomato_timer.seconds.get() == "00"


def test_pause_midway(tomato_timer):
    # Test: Pausing the timer midway through a session
    with patch("python_pomodoro.tomato_timer.time.sleep"):
        # Start the timer and simulate it running halfway
        tomato_timer.minutes.set("12")
        tomato_timer.seconds.set("30")
        tomato_timer.current_time = 750  # 12 minutes and 30 seconds in seconds
        tomato_timer.is_paused = False

        # Pause the timer
        tomato_timer.pause_timer()

        # Assert the timer is paused and retains its midway values
        assert tomato_timer.is_paused is True
        assert tomato_timer.minutes.get() == "12"
        assert tomato_timer.seconds.get() == "30"


@pytest.mark.parametrize(
    "status, expected",
    [
        (SessionStatus.FOCUS, "Focus Time"),
        (SessionStatus.SHORT_BREAK, "Short Break"),
        (SessionStatus.LONG_BREAK, "Long Break"),
    ],
)
def test_set_status(tomato_timer, status, expected):
    tomato_timer.set_status(status)
    assert tomato_timer.list_selection.get() == expected


def test_update_styles(tomato_timer):
    # get the current status background image
    active_status_image = tomato_timer.bg_images[tomato_timer.status]
    timer_image = tomato_timer.timer_background["image"][0]

    assert timer_image == active_status_image.name

    tomato_timer.pause_timer()

    paused_status_image = tomato_timer.bg_images_paused[tomato_timer.status]
    timer_image = tomato_timer.timer_background["image"][0]

    assert timer_image == paused_status_image.name


@pytest.mark.parametrize(
    "status, cycle, expected_status, expected_cycle",
    [
        (SessionStatus.FOCUS, 1, SessionStatus.SHORT_BREAK, 1),
        (SessionStatus.FOCUS, 4, SessionStatus.LONG_BREAK, 4),
        (SessionStatus.SHORT_BREAK, 1, SessionStatus.FOCUS, 2),
        (SessionStatus.LONG_BREAK, 4, SessionStatus.FOCUS, 1),
    ],
)
def test_start_next_session_click_yes(tomato_timer, status, cycle, expected_status, expected_cycle):
    with (
        patch.object(tomato_timer, "alert_session_ended", return_value=True) as mock_alert_session_ended,
        patch.object(tomato_timer, "start_timer") as mock_start_timer,
    ):
        tomato_timer.set_status(status)
        tomato_timer.current_cycle = cycle

        tomato_timer.start_next_session()
        mock_alert_session_ended.assert_called_once_with(expected_status)
        mock_start_timer.assert_called_once()

        assert tomato_timer.status == expected_status
        assert tomato_timer.current_cycle == expected_cycle


@pytest.mark.parametrize(
    "status, cycle, expected_status, expected_cycle",
    [
        (SessionStatus.FOCUS, 1, SessionStatus.SHORT_BREAK, 1),
        (SessionStatus.FOCUS, 4, SessionStatus.LONG_BREAK, 4),
        (SessionStatus.SHORT_BREAK, 1, SessionStatus.FOCUS, 2),
        (SessionStatus.LONG_BREAK, 4, SessionStatus.FOCUS, 1),
    ],
)
def test_start_next_session_click_no(tomato_timer, status, cycle, expected_status, expected_cycle):
    with (
        patch.object(tomato_timer, "alert_session_ended", return_value=False) as mock_alert_session_ended,
        patch.object(tomato_timer, "start_timer") as mock_start_timer,
    ):
        tomato_timer.set_status(status)
        tomato_timer.current_cycle = cycle

        tomato_timer.start_next_session()
        mock_alert_session_ended.assert_called_once_with(expected_status)
        mock_start_timer.assert_not_called

        assert tomato_timer.status == expected_status
        assert tomato_timer.current_cycle == expected_cycle

        # Test window title if user clicks 'No' in alert
        assert "Pomodoro - Click Start to begin" in tomato_timer.main_window.title()


@pytest.mark.parametrize(
    "status, cycle, next_session, cycle_msg, title, msg_session",
    [
        (SessionStatus.FOCUS, 1, SessionStatus.SHORT_BREAK, "", "Focus Time has ended", "short break"),
        (SessionStatus.FOCUS, 4, SessionStatus.LONG_BREAK, "", "Focus Time has ended", "long break"),
        (
            SessionStatus.SHORT_BREAK,
            1,
            SessionStatus.FOCUS,
            "You have completed cycle 1 of 4.\n",
            "Short Break has ended",
            "focus time",
        ),
        (SessionStatus.LONG_BREAK, 4, SessionStatus.FOCUS, "", "Long Break has ended", "focus time"),
    ],
)
def test_alert_session_ended(tomato_timer, status, cycle, next_session, cycle_msg, title, msg_session):
    with (
        patch("python_pomodoro.tomato_timer.playsound") as mock_playsound,
        patch("python_pomodoro.tomato_timer.messagebox") as mock_messagebox,
    ):
        tomato_timer.set_status(status)
        tomato_timer.current_cycle = cycle

        message = f"{cycle_msg}Would you like to start the next {msg_session}?"

        mock_messagebox.return_value.get.return_value = "Yes"
        response = tomato_timer.alert_session_ended(next_session)

        mock_playsound.assert_called_once()

        mock_messagebox.assert_called_once_with(
            tomato_timer.main_window,
            title=title,
            message=message,
            icon="question",
            option_1="Yes",
            option_2="No",
            justify="center",
        )

        mock_messagebox.return_value.get.assert_called_once()

        assert response is True

        mock_messagebox.return_value.get.return_value = "No"
        response = tomato_timer.alert_session_ended(next_session)

        assert response is False


@pytest.mark.parametrize(
    "status_str, expected_status",
    [
        ("Focus Time", SessionStatus.FOCUS),
        ("Short Break", SessionStatus.SHORT_BREAK),
        ("Long Break", SessionStatus.LONG_BREAK),
    ],
)
def test_change_session_status(tomato_timer, status_str, expected_status):
    # Mock the update_styles and set_session_time methods to isolate reset behavior
    with (
        patch.object(tomato_timer, "update_styles") as mock_update_styles,
        patch.object(tomato_timer, "set_session_time") as mock_set_session_time,
    ):

        tomato_timer.change_session_status(status_str)

        # Assert the timer is paused after reset
        assert tomato_timer.is_paused is True

        # Assert that the start button is shown
        assert bool(tomato_timer.button_start.grid_info()) is True

        # Ensure session time and styles are reset
        mock_update_styles.assert_called_once_with(reset=True)
        mock_set_session_time.assert_called_once()

        assert tomato_timer.main_window.title() == f"Pomodoro - Start {status_str}"
        assert tomato_timer.list_selection.get() == expected_status.value.title
        assert tomato_timer.status == expected_status


def test_change_session_dropdown_clicked(tomato_timer):
    # Mock the call to change_session_status to isolate reset behavior
    with patch.object(tomato_timer, "change_session_status") as mock_selection:

        tomato_timer.option_menu_session_status.children["!dropdownmenu"].invoke(0)
        mock_selection.assert_called_once()


"""
# TODO: Test when timer use after() instead of sleep()

def test_timer_starts_countdown(tomato_timer):
    with patch.object(tomato_timer.main_window, "after") as mock_after:
        tomato_timer.start_timer()

        # Assert the after method was called, meaning the timer started ticking
        mock_after.assert_called_once()

        # Ensure that the timer is not paused
        assert tomato_timer.is_paused is False
"""
