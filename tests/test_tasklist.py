from tkinter import IntVar


def test_settings_initialization(tasks):
    pass


def test_show_task_entry_input(tasks, test_functions):

    tasks.show_task_entry_input()

    # Assert that the save and entry input is shown
    assert bool(tasks.button_save_task.pack_info()) is True
    assert bool(tasks.entry_task_input.pack_info()) is True

    # Assert that the add task button is hidden
    assert test_functions.test_object_is_hidden(tasks.button_add_task)


def test_save_new_task(tasks, test_functions):

    assert len(tasks.tasks_by_id) == 1

    text = "Some new test task"
    tasks.entry_task_input.insert(0, text)
    task_id = tasks.save_new_task()

    # Assert that the save task button and input is hidden
    assert test_functions.test_object_is_hidden(tasks.button_save_task)
    assert test_functions.test_object_is_hidden(tasks.entry_task_input)

    # Assert that the add task button is shown
    assert bool(tasks.button_add_task.pack_info()) is True

    assert len(tasks.tasks_by_id) == 2
    assert tasks.tasks_by_id[task_id].title == text


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
    text = "Some new test task"
    tasks.entry_task_input.insert(0, text)
    task_id = tasks.save_new_task()

    assert tasks.tasks_by_id[task_id].checkbox["text"] == text


def test_toggle_task_complete(tasks):
    is_complete = IntVar()
    is_complete.set(1)
    for task in tasks.tasks_by_id.values():
        tasks.toggle_task_complete(task, is_complete)

        assert task.is_complete


def test_clear_completed_tasks(tasks, test_functions):
    # Add new task
    text = "Some new test task"
    tasks.entry_task_input.insert(0, text)
    tasks.save_new_task()

    tasks.clear_completed_tasks()

    assert len(tasks.tasks_by_id) == 2

    is_complete = IntVar()
    is_complete.set(1)
    for task in tasks.tasks_by_id.values():
        tasks.toggle_task_complete(task, is_complete)

        assert task.is_complete

    tasks.clear_completed_tasks()

    assert len(tasks.tasks_by_id) == 0

    # Assert that the clear task button is hidden
    assert test_functions.test_object_is_hidden(tasks.button_clear_task)
