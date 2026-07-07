from datetime import date, timedelta

from pawpal_system import Owner, Pet, Scheduler, Task


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


def test_scheduler_sorts_tasks_chronologically():
    owner = Owner(name="Jordan")
    pet = Pet(name="Mochi", species="dog", age=3)
    owner.add_pet(pet)
    scheduler = Scheduler(owner)

    evening_task = Task(
        title="Evening walk",
        time="18:00",
        due_date=date.today(),
        duration_minutes=30,
    )
    morning_task = Task(
        title="Breakfast feeding",
        time="07:30",
        due_date=date.today(),
        duration_minutes=10,
    )
    afternoon_task = Task(
        title="Medication",
        time="13:15",
        due_date=date.today(),
        duration_minutes=5,
    )

    sorted_tasks = scheduler.sort_by_time(
        [evening_task, morning_task, afternoon_task]
    )

    assert [task.title for task in sorted_tasks] == [
        "Breakfast feeding",
        "Medication",
        "Evening walk",
    ]


def test_completing_daily_task_creates_next_day_task():
    today = date.today()
    owner = Owner(name="Jordan")
    pet = Pet(name="Luna", species="cat", age=5)
    owner.add_pet(pet)
    scheduler = Scheduler(owner)
    task = Task(
        title="Breakfast feeding",
        time="08:00",
        due_date=today,
        duration_minutes=10,
        frequency="daily",
    )
    pet.add_task(task)

    next_task = scheduler.complete_task(task)

    assert task.completed is True
    assert next_task is not None
    assert next_task.title == "Breakfast feeding"
    assert next_task.time == "08:00"
    assert next_task.due_date == today + timedelta(days=1)
    assert next_task in pet.tasks


def test_scheduler_flags_duplicate_task_times():
    owner = Owner(name="Jordan")
    pet = Pet(name="Mochi", species="dog", age=3)
    owner.add_pet(pet)
    scheduler = Scheduler(owner)
    first_task = Task(
        title="Morning walk",
        time="08:00",
        due_date=date.today(),
        duration_minutes=30,
    )
    second_task = Task(
        title="Breakfast feeding",
        time="08:00",
        due_date=date.today(),
        duration_minutes=10,
    )

    conflicts = scheduler.detect_conflicts([first_task, second_task])

    assert conflicts == [
        "08:00: multiple tasks scheduled (Morning walk, Breakfast feeding)"
    ]
