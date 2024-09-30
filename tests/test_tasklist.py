from tkinter import Checkbutton, IntVar
from unittest.mock import patch
from uuid import uuid4

import pytest
from python_pomodoro.tasklist import Task


def test_settings_initialization(tasks):
    pass


def test_show_task_entry_input(tasks, test_functions):

    tasks.show_task_entry_input()

    # Assert that the save and entry input is shown
    assert bool(tasks.button_save_task.pack_info()) is True
    assert bool(tasks.entry_task_input.pack_info()) is True

    # Assert that the add task button is hidden
    assert test_functions.test_object_is_hidden(tasks.button_add_task)


@pytest.mark.parametrize(
    "text",
    (
        "Some new task",
        "Hello!",
        "123 test",
        "123456",
        "test123",
        "test 123!",
        "@abc",
    ),
)
def test_save_new_task_valid(tasks, test_functions, text):

    assert len(tasks.tasks_by_id) == 1

    tasks.entry_task_input.insert(0, text)

    task_id = tasks.save_new_task()

    # Assert that the save task button and input is hidden
    assert test_functions.test_object_is_hidden(tasks.button_save_task)
    assert test_functions.test_object_is_hidden(tasks.entry_task_input)

    # Assert that the add task button is shown
    assert bool(tasks.button_add_task.pack_info()) is True

    assert task_id is not None

    assert len(tasks.tasks_by_id) == 2
    assert tasks.tasks_by_id[task_id].title == text


def test_save_new_task_invalid_empty_string(tasks):
    assert len(tasks.tasks_by_id) == 1

    text = ""
    tasks.entry_task_input.insert(0, text)

    task_id = tasks.save_new_task()

    assert tasks.label_task_input["text"] == "Please enter a task..."
    assert bool(tasks.label_task_input.pack_info()) is True
    assert task_id is None
    assert len(tasks.tasks_by_id) == 1  # No new task added


@pytest.mark.parametrize(
    "text",
    ("    ", "!!!!", "%%%%", "#####", " \t \n "),
)
def test_save_new_task_invalid(tasks, text):
    assert len(tasks.tasks_by_id) == 1

    tasks.entry_task_input.insert(0, text)

    task_id = tasks.save_new_task()

    # Ensure the task is not added
    assert tasks.label_task_input["text"] == "Please enter a valid task name."
    assert task_id is None
    assert len(tasks.tasks_by_id) == 1  # No new task added


def test_save_invalid_duplicate_tasks(tasks):
    assert len(tasks.tasks_by_id) == 1

    text = "Test task"
    tasks.entry_task_input.insert(0, text)

    task_id_1 = tasks.save_new_task()

    assert len(tasks.tasks_by_id) == 2  # New task added
    assert tasks.tasks_by_id[task_id_1].title == text

    # Add the same task again
    tasks.entry_task_input.insert(0, text)
    task_id_2 = tasks.save_new_task()

    assert tasks.label_task_input["text"] == "Duplicate task name."
    assert task_id_2 is None
    assert len(tasks.tasks_by_id) == 2  # No new task added

    tasks.entry_task_input.delete(0, "end")

    text = "Test task 2"
    tasks.entry_task_input.insert(0, text)

    task_id_3 = tasks.save_new_task()

    assert len(tasks.tasks_by_id) == 3  # New task added
    assert tasks.tasks_by_id[task_id_3].title == text


def test_save_task_with_max_length(tasks):
    assert len(tasks.tasks_by_id) == 1

    long_title = "A" * 300  # Exceeding reasonable max length (e.g., 255 chars)
    tasks.entry_task_input.insert(0, long_title)

    tasks.save_new_task()

    # Ensure the task title is truncated or properly handled
    assert tasks.label_task_input["text"] == "Task too long (max 100 chars.)"
    assert len(tasks.tasks_by_id) == 1  # No new task added


def test_show_hide_clear_task_button(tasks, test_functions):
    # Add new task
    text = "Some new test task"
    tasks.entry_task_input.insert(0, text)
    tasks.save_new_task()

    tasks.show_hide_clear_task_button()
    # Assert that the save and entry input is shown
    assert bool(tasks.button_clear_task.pack_info()) is True

    tasks.tasks_by_id.clear()

    tasks.show_hide_clear_task_button()
    # Assert that the clear task button is hidden
    assert test_functions.test_object_is_hidden(tasks.button_clear_task)


def test_create_task_checkbutton(tasks):
    # Mock the call to toggle_task_complete to isolate reset behavior
    with patch.object(tasks, "toggle_task_complete") as mock_toggle:
        # Add a new task to the dict tasks_by_id
        id = uuid4()
        title = "Some task title"
        task = Task(
            id=id,
            title=title,
            is_complete=False,
        )

        tasks.create_task_checkbutton(task)

        task.checkbox.invoke()
        mock_toggle.assert_called_once()

        assert task.checkbox["text"] == title


def test_toggle_task_complete(tasks):
    # Add a new task to the dict tasks_by_id
    id = uuid4()
    title = "Some task title"
    tasks.tasks_by_id[id] = task = Task(id=id, title=title, is_complete=False, checkbox=Checkbutton(tasks, text=title))

    assert len(tasks.tasks_by_id) == 2

    is_complete = IntVar()
    is_complete.set(1)

    tasks.toggle_task_complete(task, is_complete)
    assert task.is_complete

    task.checkbox = None
    tasks.toggle_task_complete(task, is_complete)

    assert len(tasks.tasks_by_id) == 1


def test_clear_completed_tasks(tasks, test_functions):
    # Add new task
    text = "Some new test task"
    tasks.entry_task_input.insert(0, text)
    tasks.save_new_task()

    assert len(tasks.tasks_by_id) == 2

    tasks.clear_completed_tasks()

    is_complete = IntVar()
    is_complete.set(1)
    for task in tasks.tasks_by_id.values():
        tasks.toggle_task_complete(task, is_complete)

        assert task.is_complete

    tasks.clear_completed_tasks()

    assert len(tasks.tasks_by_id) == 0

    # Assert that the clear task button is hidden
    assert test_functions.test_object_is_hidden(tasks.button_clear_task)


def test_clear_completed_no_tasks_completed(tasks, test_functions):
    tasks.clear_completed_tasks()

    assert len(tasks.tasks_by_id) == 1  # No tasks should be removed
    assert bool(tasks.button_clear_task.pack_info()) is True


def test_clear_tasks_when_empty(tasks, test_functions):
    tasks.tasks_by_id.clear()  # Simulate an empty task list

    tasks.show_hide_clear_task_button()
    assert test_functions.test_object_is_hidden(tasks.button_clear_task)  # Clear button should be hidden


def test_clear_completed_with_mixed_statuses(tasks):
    assert len(tasks.tasks_by_id) == 1

    # Create one complete and one incomplete task
    complete_task = Task(
        id=uuid4(), title="Complete Task", is_complete=True, checkbox=Checkbutton(tasks, text="Complete Task")
    )
    incomplete_task = Task(
        id=uuid4(), title="Incomplete Task", is_complete=False, checkbox=Checkbutton(tasks, text="Incomplete Task")
    )
    tasks.tasks_by_id[complete_task.id] = complete_task
    tasks.tasks_by_id[incomplete_task.id] = incomplete_task

    tasks.clear_completed_tasks()

    # Only the incomplete task should remain
    assert len(tasks.tasks_by_id) == 2
    assert incomplete_task.id in tasks.tasks_by_id
    assert complete_task.id not in tasks.tasks_by_id
