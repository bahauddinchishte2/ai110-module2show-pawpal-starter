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
        raise NotImplementedError

    def create_next_occurrence(self) -> "Task | None":
        """Create the next recurring task when this task repeats."""
        raise NotImplementedError


@dataclass
class Pet:
    """Store one pet and the care tasks assigned to it."""

    name: str
    species: str
    age: int = 0
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a care task to this pet."""
        raise NotImplementedError

    def get_pending_tasks(self) -> list[Task]:
        """Return this pet's incomplete tasks."""
        raise NotImplementedError


@dataclass
class Owner:
    """Manage a pet owner's pets and their combined care tasks."""

    name: str
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner."""
        raise NotImplementedError

    def find_pet(self, name: str) -> Pet | None:
        """Find a pet by name."""
        raise NotImplementedError

    def get_all_tasks(self) -> list[Task]:
        """Return every task across all pets."""
        raise NotImplementedError


class Scheduler:
    """Organize, filter, and manage tasks for an owner."""

    def __init__(self, owner: Owner) -> None:
        """Initialize the scheduler with an owner."""
        self.owner = owner

    def get_today_tasks(self, today: date | None = None) -> list[Task]:
        """Return tasks due today."""
        raise NotImplementedError

    def sort_by_time(self, tasks: list[Task]) -> list[Task]:
        """Return tasks sorted by their scheduled time."""
        raise NotImplementedError

    def filter_by_pet(self, pet_name: str) -> list[Task]:
        """Return tasks for one pet."""
        raise NotImplementedError

    def filter_by_status(self, completed: bool) -> list[Task]:
        """Return tasks matching a completion status."""
        raise NotImplementedError

    def detect_conflicts(self, tasks: list[Task]) -> list[str]:
        """Return warnings for tasks scheduled at the same time."""
        raise NotImplementedError

    def complete_task(self, task: Task) -> Task | None:
        """Complete a task and return its next occurrence when recurring."""
        raise NotImplementedError
