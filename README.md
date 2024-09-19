# python_pomodoro
A Pomodoro Timer Application using Python and Tkinter.

This project aims to develop my skills in: OOP, event-driven programming, UI/UX design, testing and validation, software deployment.

###  What is the Pomodoro technique?

Method of time management to help improve productivity:
- Work for 25 minutes, then take a 5-minute break.
- After 4 cycles, take a longer break (e.g., 15-30 minutes).

### What will the UI look like?
Development of this app will incorporate the following features.

- Simple, user-friendly GUI.
- Start/Stop/Pause/Reset buttons for timer.
- Customizable work/break intervals. Sliders to adjust values.
- Visual or sound alerts at the end of each session. Prompt to continue to next task or work/break session.
- Task checklist, tasks crossed out after completion.

![Image](https://github.com/user-attachments/assets/ab106b6b-d030-443a-9661-233a161124af)

More details on how the UI will work:

![Image](https://github.com/user-attachments/assets/98d5a6dc-b0bf-45d1-8ee7-ecf9e64a0581)

## Project set up

**My local environment is installed on a Fedora Linux laptop.**

### Dependencies:
- Python 3.11+
- pip
- pipenv
- tkinter

Check Python version:
```
$ python --version
Python 3.12.5
```

### Install tkinter on Fedora Linux
https://www.geeksforgeeks.org/how-to-install-tkinter-on-linux/

For Fedora users, use the following command:
```
sudo dnf install python3-tkinter
```
Verify installation: a pop-up window opened with two buttons appears, showing the current version of Tkinter installed.
```
python -m tkinter
```

### Install pip on Fedora Linux
https://packaging.python.org/en/latest/guides/installing-using-linux-tools/

```
$ sudo dnf install python3-pip python3-wheel

$ pip --version
pip 23.2.1
```

### Install pipenv 
https://pipenv.pypa.io/en/latest/index.html

**Rationale:** [Poetry](https://python-poetry.org/) is another Python virtual environment and dependency management tool, however this project is not very big or particularly complex and has minimal dependencies, therefore I have opted to use Pipenv, which I am more familiar with.

```
$ pip install pipenv --user

$ pipenv --version
pipenv, version 2024.0.1
```

Create and activate the virtual environment and spawn a shell within it
```
pipenv shell
```
Install packages
```
pipenv install [OPTIONS] [PACKAGES]...
```

### Run the tests

#### Coverage with Pytest
```
$ coverage run -m pytest
```
#### View report in terminal
```
$ coverage report
```
#### Generate reports

This then works with Coverage Gutters VS Code extension to view coverage in module's python files.
```
$ coverage xml
```

## Resources

### Further information:
- https://www.pomodorotechnique.com/
- https://en.wikipedia.org/wiki/Pomodoro_Technique

### Other similar applications:
Here are a few Pomodoro apps which I've used for inspiration:

- https://pomofocus.io/
- https://pomodor.app/timer
- https://github.com/Splode/pomotroid
