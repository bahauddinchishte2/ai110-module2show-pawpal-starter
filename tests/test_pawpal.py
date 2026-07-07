from datetime import date

from pawpal_system import Pet, Task


def test_mark_complete_updates_status():
    task = Task(
        title="Morning walk",
        time="08:00",
        due_date=date.today(),
        duration_minutes=30,
    )

    task.mark_complete()

    assert task.completed is True


def test_add_task_increases_pet_task_count():
    pet = Pet(name="Mochi", species="dog", age=3)
    task = Task(
        title="Breakfast feeding",
        time="07:30",
        due_date=date.today(),
        duration_minutes=10,
    )

    pet.add_task(task)

    assert len(pet.tasks) == 1
