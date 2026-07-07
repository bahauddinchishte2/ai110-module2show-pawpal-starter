"""Core PawPal+ domain classes and scheduling interfaces."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any


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

    def to_dict(self) -> dict[str, Any]:
        """Convert this task into JSON-friendly data."""
        return {
            "title": self.title,
            "time": self.time,
            "due_date": self.due_date.isoformat(),
            "duration_minutes": self.duration_minutes,
            "priority": self.priority,
            "frequency": self.frequency,
            "completed": self.completed,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Task":
        """Create a task from JSON-friendly data."""
        return cls(
            title=str(data["title"]),
            time=str(data["time"]),
            due_date=date.fromisoformat(str(data["due_date"])),
            duration_minutes=int(data["duration_minutes"]),
            priority=str(data.get("priority", "medium")),
            frequency=str(data.get("frequency", "once")),
            completed=bool(data.get("completed", False)),
        )

    def create_next_occurrence(self) -> "Task | None":
        """Create the next recurring task when this task repeats."""
        if self.frequency == "daily":
            next_date = self.due_date + timedelta(days=1)
        elif self.frequency == "weekly":
            next_date = self.due_date + timedelta(weeks=1)
        else:
            return None

        return Task(
            title=self.title,
            time=self.time,
            due_date=next_date,
            duration_minutes=self.duration_minutes,
            priority=self.priority,
            frequency=self.frequency,
        )


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

    def to_dict(self) -> dict[str, Any]:
        """Convert this pet and its tasks into JSON-friendly data."""
        return {
            "name": self.name,
            "species": self.species,
            "age": self.age,
            "tasks": [task.to_dict() for task in self.tasks],
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Pet":
        """Create a pet and its tasks from JSON-friendly data."""
        return cls(
            name=str(data["name"]),
            species=str(data["species"]),
            age=int(data.get("age", 0)),
            tasks=[Task.from_dict(task_data) for task_data in data.get("tasks", [])],
        )

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

    def to_dict(self) -> dict[str, Any]:
        """Convert this owner and all pets into JSON-friendly data."""
        return {
            "name": self.name,
            "pets": [pet.to_dict() for pet in self.pets],
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Owner":
        """Create an owner from JSON-friendly data."""
        return cls(
            name=str(data["name"]),
            pets=[Pet.from_dict(pet_data) for pet_data in data.get("pets", [])],
        )

    def save_to_json(self, file_path: str | Path) -> None:
        """Save owner, pet, and task data to a JSON file."""
        path = Path(file_path)
        path.write_text(json.dumps(self.to_dict(), indent=2), encoding="utf-8")

    @classmethod
    def load_from_json(
        cls,
        file_path: str | Path,
        default_name: str = "Jordan",
    ) -> "Owner":
        """Load owner data from JSON, or return a new owner when no file exists."""
        path = Path(file_path)
        if not path.exists():
            return cls(name=default_name)

        return cls.from_dict(json.loads(path.read_text(encoding="utf-8")))

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

    def find_next_available_slot(
        self,
        target_date: date | None = None,
        start_time: str = "08:00",
        end_time: str = "20:00",
        interval_minutes: int = 30,
    ) -> str | None:
        """Return the next open start time on a day using fixed time intervals."""
        schedule_date = target_date or date.today()
        occupied_times = {
            task.time for task in self.owner.get_all_tasks() if task.due_date == schedule_date
        }
        current_slot = datetime.strptime(start_time, "%H:%M")
        final_slot = datetime.strptime(end_time, "%H:%M")

        while current_slot <= final_slot:
            candidate = current_slot.strftime("%H:%M")
            if candidate not in occupied_times:
                return candidate
            current_slot += timedelta(minutes=interval_minutes)

        return None

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
        conflicts: list[str] = []
        tasks_by_time: dict[str, list[Task]] = {}

        for task in tasks:
            tasks_by_time.setdefault(task.time, []).append(task)

        for task_time, scheduled_tasks in tasks_by_time.items():
            if len(scheduled_tasks) > 1:
                task_titles = ", ".join(task.title for task in scheduled_tasks)
                conflicts.append(f"{task_time}: multiple tasks scheduled ({task_titles})")

        return conflicts

    def complete_task(self, task: Task) -> Task | None:
        """Complete a task and return its next occurrence when recurring."""
        task.mark_complete()
        next_task = task.create_next_occurrence()

        if next_task is None:
            return None

        for pet in self.owner.pets:
            if task in pet.tasks:
                pet.add_task(next_task)
                return next_task

        return next_task
