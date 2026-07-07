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
            time="08:00",
            due_date=today,
            duration_minutes=30,
            priority="high",
            frequency="daily",
        )
    )
    luna.add_task(
        Task(
            title="Breakfast feeding",
            time="07:30",
            due_date=today,
            duration_minutes=10,
            priority="high",
            frequency="daily",
        )
    )
    mochi.add_task(
        Task(
            title="Heartworm medication",
            time="18:00",
            due_date=today,
            duration_minutes=5,
            priority="medium",
            frequency="monthly",
        )
    )

    owner.add_pet(mochi)
    owner.add_pet(luna)
    return owner


def print_today_schedule(owner: Owner) -> None:
    """Print a readable schedule for today's pet care tasks."""
    scheduler = Scheduler(owner)
    today_tasks = scheduler.sort_by_time(scheduler.get_today_tasks())

    print(f"Today's Schedule for {owner.name}")
    print("=" * 29)

    for task in today_tasks:
        pet_name = find_pet_name(owner, task)
        status = "done" if task.completed else "pending"
        print(
            f"{task.time} | {pet_name}: {task.title} "
            f"({task.duration_minutes} min) "
            f"[priority: {task.priority}] [{status}]"
        )


if __name__ == "__main__":
    demo_owner = build_demo_owner()
    print_today_schedule(demo_owner)
