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


def test_owner_data_saves_and_loads_from_json(tmp_path):
    file_path = tmp_path / "data.json"
    owner = Owner(name="Jordan")
    pet = Pet(name="Mochi", species="dog", age=3)
    pet.add_task(
        Task(
            title="Morning walk",
            time="09:00",
            due_date=date(2026, 7, 7),
            duration_minutes=30,
            priority="high",
            frequency="daily",
        )
    )
    owner.add_pet(pet)

    owner.save_to_json(file_path)
    loaded_owner = Owner.load_from_json(file_path)

    assert loaded_owner.name == "Jordan"
    assert loaded_owner.pets[0].name == "Mochi"
    assert loaded_owner.pets[0].tasks[0].title == "Morning walk"
    assert loaded_owner.pets[0].tasks[0].due_date == date(2026, 7, 7)
    assert loaded_owner.pets[0].tasks[0].frequency == "daily"


def test_scheduler_finds_next_available_slot():
    target_date = date(2026, 7, 7)
    owner = Owner(name="Jordan")
    pet = Pet(name="Luna", species="cat", age=5)
    owner.add_pet(pet)
    scheduler = Scheduler(owner)
    pet.add_task(
        Task(
            title="Breakfast feeding",
            time="08:00",
            due_date=target_date,
            duration_minutes=10,
        )
    )
    pet.add_task(
        Task(
            title="Medication",
            time="08:30",
            due_date=target_date,
            duration_minutes=5,
        )
    )

    next_slot = scheduler.find_next_available_slot(
        target_date=target_date,
        start_time="08:00",
        end_time="09:00",
        interval_minutes=30,
    )

    assert next_slot == "09:00"
