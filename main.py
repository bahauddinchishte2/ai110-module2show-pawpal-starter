"""CLI demo for the PawPal+ core logic."""

from datetime import date

from pawpal_system import Owner, Pet, Scheduler, Task


def find_pet_name(owner: Owner, task: Task) -> str:
    """Return the name of the pet that owns a task."""
    for pet in owner.pets:
        if task in pet.tasks:
            return pet.name
    return "Unknown pet"


def build_demo_owner() -> Owner:
    """Create sample PawPal+ data for the terminal demo."""
    today = date.today()
    owner = Owner(name="Jordan")

    mochi = Pet(name="Mochi", species="dog", age=3)
    luna = Pet(name="Luna", species="cat", age=5)

    mochi.add_task(
        Task(
            title="Morning walk",
            time="09:00",
            due_date=today,
            duration_minutes=30,
            priority="high",
            frequency="daily",
        )
    )
    luna.add_task(
        Task(
            title="Breakfast feeding",
            time="08:00",
            due_date=today,
            duration_minutes=10,
            priority="high",
            frequency="daily",
        )
    )
    mochi.add_task(
        Task(
            title="Heartworm medication",
            time="08:00",
            due_date=today,
            duration_minutes=5,
            priority="medium",
            frequency="monthly",
        )
    )
    luna.add_task(
        Task(
            title="Evening playtime",
            time="19:30",
            due_date=today,
            duration_minutes=20,
            priority="medium",
            frequency="weekly",
        )
    )

    owner.add_pet(mochi)
    owner.add_pet(luna)
    return owner


def print_today_schedule(owner: Owner) -> None:
    """Print a readable schedule for today's pet care tasks."""
    scheduler = Scheduler(owner)
    today_tasks = scheduler.sort_by_time(scheduler.get_today_tasks())

    print(f"Today's Sorted Schedule for {owner.name}")
    print("=" * 36)

    for task in today_tasks:
        pet_name = find_pet_name(owner, task)
        status = "done" if task.completed else "pending"
        print(
            f"{task.time} | {pet_name}: {task.title} "
            f"({task.duration_minutes} min) "
            f"[priority: {task.priority}] [{status}]"
        )

    print("\nMochi's Tasks")
    print("=" * 13)
    for task in scheduler.sort_by_time(scheduler.filter_by_pet("Mochi")):
        print(f"{task.time} | {task.title} [{task.priority}]")

    print("\nPending Tasks")
    print("=" * 13)
    for task in scheduler.sort_by_time(scheduler.filter_by_status(False)):
        pet_name = find_pet_name(owner, task)
        print(f"{task.time} | {pet_name}: {task.title}")

    print("\nConflict Warnings")
    print("=" * 17)
    conflicts = scheduler.detect_conflicts(today_tasks)
    if conflicts:
        for warning in conflicts:
            print(f"Warning: {warning}")
    else:
        print("No conflicts found.")

    print("\nRecurring Task Demo")
    print("=" * 19)
    recurring_source = owner.find_pet("Luna").tasks[0]
    next_task = scheduler.complete_task(recurring_source)
    if next_task is not None:
        print(
            f"Completed '{recurring_source.title}' and created next "
            f"'{next_task.title}' for {next_task.due_date}."
        )


if __name__ == "__main__":
    demo_owner = build_demo_owner()
    print_today_schedule(demo_owner)
