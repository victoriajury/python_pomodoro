# python_pomodoro

![Tests Status](./reports/badges/tests-badge.svg?dummy=8484744)
![Coverage Status](./reports/badges/coverage-badge.svg?dummy=8484744)

A Pomodoro Timer Application using Python and Tkinter.

**This project aims to develop my skills in:** OOP, event-driven programming, UI/UX design, testing and validation, software deployment.

**What is the Pomodoro technique?**

Method of time management to help improve productivity:

- Work for 25 minutes, then take a 5-minute break.
- After 4 cycles, take a longer break (e.g., 15-30 minutes).

![Image](https://github.com/user-attachments/assets/09c780f8-f094-4d17-9ba0-c1a9c576fcf0)
![Image](https://github.com/user-attachments/assets/6e2631df-809a-4b10-a0f3-2189cd3f83d4)

## Installation

### Dependencies

- Python 3.11+
- pip
- pipenv
- tkinter

#### Install pipenv

```bash
pip install pipenv --user
```

#### Install venv and dependency packages

```bash
pipenv install
```

## Usage

To run the application from a terminal

```bash
python -m python_pomodoro.app
```

### Settings

Sliders in the settings panel set the timers and number of cycles.

### Adding tasks

Users can add tasks and clear completed tasks, which deletes them.

## Resources

For information on the project development, see [/dev.md](dev.md)

### Styles

UI styled with `customtkinter` library:

- <https://customtkinter.tomschimansky.com/>

Add-ons:

- <https://github.com/Akascape/CTkMessagebox>

### Further information

- <https://www.pomodorotechnique.com/>
- <https://en.wikipedia.org/wiki/Pomodoro_Technique>

### Other similar applications

Here are a few Pomodoro apps which I've used for inspiration:

- <https://pomofocus.io/>
- <https://pomodor.app/timer>
- <https://github.com/Splode/pomotroid>
