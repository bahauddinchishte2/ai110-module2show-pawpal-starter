"""Core PawPal+ domain classes and scheduling interfaces."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date


@dataclass
class Task:
    """Represent one pet care activity on the schedule."""

    title: str
    time: str
    due_date: date
    duration_minutes: int
    priority: str = "medium"
    frequency: str = "once"
    completed: bool = False

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.completed = True

    def create_next_occurrence(self) -> "Task | None":
        """Create the next recurring task when this task repeats."""
        return None


@dataclass
class Pet:
    """Store one pet and the care tasks assigned to it."""

    name: str
    species: str
    age: int = 0
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a care task to this pet."""
        self.tasks.append(task)

    def get_pending_tasks(self) -> list[Task]:
        """Return this pet's incomplete tasks."""
        return [task for task in self.tasks if not task.completed]


@dataclass
class Owner:
    """Manage a pet owner's pets and their combined care tasks."""

    name: str
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner."""
        self.pets.append(pet)

    def find_pet(self, name: str) -> Pet | None:
        """Find a pet by name."""
        normalized_name = name.strip().lower()
        for pet in self.pets:
            if pet.name.lower() == normalized_name:
                return pet
        return None

    def get_all_tasks(self) -> list[Task]:
        """Return every task across all pets."""
        all_tasks: list[Task] = []
        for pet in self.pets:
            all_tasks.extend(pet.tasks)
        return all_tasks


class Scheduler:
    """Organize, filter, and manage tasks for an owner."""

    def __init__(self, owner: Owner) -> None:
        """Initialize the scheduler with an owner."""
        self.owner = owner

    def get_today_tasks(self, today: date | None = None) -> list[Task]:
        """Return tasks due today."""
        target_date = today or date.today()
        return [task for task in self.owner.get_all_tasks() if task.due_date == target_date]

    def sort_by_time(self, tasks: list[Task]) -> list[Task]:
        """Return tasks sorted by their scheduled time."""
        return sorted(tasks, key=lambda task: task.time)

    def filter_by_pet(self, pet_name: str) -> list[Task]:
        """Return tasks for one pet."""
        pet = self.owner.find_pet(pet_name)
        if pet is None:
            return []
        return pet.tasks

    def filter_by_status(self, completed: bool) -> list[Task]:
        """Return tasks matching a completion status."""
        return [task for task in self.owner.get_all_tasks() if task.completed == completed]

    def detect_conflicts(self, tasks: list[Task]) -> list[str]:
        """Return warnings for tasks scheduled at the same time."""
        return []

    def complete_task(self, task: Task) -> Task | None:
        """Complete a task and return its next occurrence when recurring."""
        task.mark_complete()
        return task.create_next_occurrence()
