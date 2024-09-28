from _tkinter import TclError

import pytest
from python_pomodoro.tomato_timer import SessionStatus


def test_settings_initialization(settings):
    pass


def test_resetslider_defaults(settings):

    settings.reset_slider_defaults()

    assert settings.setting_focus_time.value.get() == 25
    assert settings.setting_short_break.value.get() == 5
    assert settings.setting_long_break.value.get() == 15
    assert settings.setting_cycles.value.get() == 4


@pytest.mark.parametrize(
    "slider, value, expected",
    [
        ("setting_focus_time", 12, SessionStatus.FOCUS),
        ("setting_short_break", 9, SessionStatus.SHORT_BREAK),
        ("setting_long_break", 18, SessionStatus.LONG_BREAK),
    ],
)
def test_update_settings_sessions(settings, slider, value, expected):
    settings.__getattribute__(slider).set_slider_value(value)
    slider_value = settings.__getattribute__(slider).get_slider_value()

    settings.update_settings()

    assert slider_value == expected.value.time.minutes


def test_update_settings_cycles(settings):
    settings.setting_cycles.set_slider_value(6)
    slider_value = settings.setting_cycles.get_slider_value()

    settings.update_settings()

    assert settings.timer.get_cycles() == slider_value


def test_close_settings(settings):
    settings.button.pack_forget()
    settings.pack()
    # Assert that the setting frame is shown
    assert bool(settings.pack_info()) is True
    with pytest.raises(TclError):
        # pack_info() raises: ' window ".!button" isn't packed'
        # instead of returning empty dict, like grid_info()
        assert bool(settings.button.pack_info()) is False

    settings.close_settings()

    # Assert that the setting button is shown
    assert bool(settings.button.pack_info()) is True
    with pytest.raises(TclError):
        assert bool(settings.pack_info()) is False
