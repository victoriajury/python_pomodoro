import pytest
from python_pomodoro.settings import SettingSlider
from python_pomodoro.tomato_timer import DEFAULT_CYCLES, SessionStatus


def test_settings_initialization(settings):
    # TODO
    pass


def test_reset_slider_defaults(settings):
    # Change all slider values
    settings.setting_focus_time.set_slider_value(30)
    settings.setting_short_break.set_slider_value(9)
    settings.setting_long_break.set_slider_value(18)
    settings.setting_cycles.set_slider_value(6)

    settings.reset_slider_defaults()

    # Ensure all sliders are set back to their default values
    assert settings.setting_focus_time.get_slider_value() == SessionStatus.FOCUS.value.default_time.minutes
    assert settings.setting_short_break.get_slider_value() == SessionStatus.SHORT_BREAK.value.default_time.minutes
    assert settings.setting_long_break.get_slider_value() == SessionStatus.LONG_BREAK.value.default_time.minutes
    assert settings.setting_cycles.get_slider_value() == DEFAULT_CYCLES


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


def test_close_settings(settings, test_functions):
    settings.button.pack_forget()
    settings.pack()
    # Assert that the setting pannel is shown
    assert bool(settings.pack_info()) is True
    # Assert that the settings button is hidden
    assert test_functions.test_object_is_hidden(settings.button)

    timer_sliders = ["setting_focus_time", "setting_short_break", "setting_long_break"]

    # change the slider value without saving
    for slider in timer_sliders:
        settings.__getattribute__(slider).set_slider_value(17)
    settings.setting_cycles.set_slider_value(8)

    settings.close_settings()

    # Assert that sliders have reverted to previous values
    for slider, session in zip(timer_sliders, list(SessionStatus)):
        assert settings.__getattribute__(slider).get_slider_value() == session.value.time.minutes
    assert settings.setting_cycles.get_slider_value() == settings.timer.get_cycles()

    # Assert that the setting button is shown
    assert bool(settings.button.pack_info()) is True

    # Assert that the settings panel is hidden
    assert test_functions.test_object_is_hidden(settings)


def test_slider_min_max_boundaries():
    slider = SettingSlider(parent=None, label_text="Focus time", min_value=5, max_value=60, default_value=25)
    # Test setting within boundaries
    slider.set_slider_value(13)
    assert slider.get_slider_value() == 13

    # Test setting below the minimum
    slider.set_slider_value(3)
    assert slider.get_slider_value() == 5  # Ensure it is clamped to the min value

    # Test setting above the maximum
    slider.set_slider_value(70)
    assert slider.get_slider_value() == 60  # Ensure it is clamped to the max value


def test_update_label(settings):
    slider = settings.setting_focus_time

    # Assert label set with default value:
    assert slider.slider_name_label._text == "Focus time:  25"

    slider.slider._command(17)

    # Assert label updated:
    assert slider.slider_name_label._text == "Focus time:  17"
