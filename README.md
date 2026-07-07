# PawPal+ (Module 2 Project)

**PawPal+** is a Streamlit app that helps a pet owner plan daily care tasks for their pets.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

This project includes a small scheduling backend, a Streamlit interface, pytest coverage, and a final Mermaid UML diagram.

## What the App Does

PawPal+ lets a pet owner:

- Enter basic owner and pet information
- Add pet care tasks with due date, time, duration, priority, and recurrence
- View today's schedule sorted by time
- See warnings when two tasks are scheduled at the exact same time
- Find the next available 30-minute care slot for today
- Filter tasks by pet and completion status
- Mark tasks complete and automatically create the next daily or weekly occurrence
- Save pets and tasks to `data.json` so they persist between app runs

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Run the Streamlit App

```bash
streamlit run app.py
```

### Run the CLI Demo

```bash
python3 main.py
```

## Features

- **Sorting by time:** `Scheduler.sort_by_time()` returns tasks in chronological order using their `HH:MM` scheduled time.
- **Today's schedule:** `Scheduler.get_today_tasks()` filters the owner's tasks to only the tasks due today.
- **Pet and status filters:** `Scheduler.filter_by_pet()` and `Scheduler.filter_by_status()` help the UI focus on one pet or pending/completed tasks.
- **Conflict warnings:** `Scheduler.detect_conflicts()` flags exact duplicate task times and shows the affected task names.
- **Next available slot:** `Scheduler.find_next_available_slot()` scans today's schedule and returns the first open fixed-interval start time.
- **Daily and weekly recurrence:** `Scheduler.complete_task()` marks a task complete and adds the next occurrence for recurring tasks.
- **JSON persistence:** `Owner.save_to_json()` and `Owner.load_from_json()` use custom dictionary conversion to save and reload owner, pet, and task data.
- **Owner, pet, and task model:** `Owner`, `Pet`, and `Task` keep the scheduling data organized and easy to test.

## Persistence Workflow

PawPal+ stores runtime data in `data.json`. When the Streamlit app starts, it calls `Owner.load_from_json("data.json")`; if the file does not exist yet, the app starts with a new owner profile. When a user adds a pet, adds a task, marks a task complete, or clicks **Save data**, the app calls `Owner.save_to_json("data.json")`.

The persistence code uses custom `to_dict()` and `from_dict()` methods instead of adding a serialization library. This keeps the project lightweight and makes the date conversion explicit: task due dates are saved as ISO strings and loaded back with `date.fromisoformat()`.

Files modified for this extension:

- `pawpal_system.py`: added JSON serialization methods and the next-slot scheduling helper.
- `app.py`: added save/reload controls, automatic saves after key actions, and next-slot display.
- `tests/test_pawpal.py`: added tests for JSON persistence and next available slot logic.
- `.gitignore`: ignored runtime `data.json`.
- `ai_interactions.md`: documented the agent workflow for the optional extension.

## System Architecture

The final Mermaid UML source is saved at `diagrams/uml_final.mmd`. It reflects the final implementation in `pawpal_system.py`, including the relationships between `Owner`, `Pet`, `Task`, and `Scheduler`.

## 🧪 Testing PawPal+

Run the automated test suite from an activated virtual environment:

```bash
python -m pytest
```

The tests cover core PawPal+ scheduling reliability: marking tasks complete, adding tasks to pets, chronological sorting, daily recurrence creation, and duplicate-time conflict detection.

Successful test output:

```text
============================= test session starts ==============================
platform darwin -- Python 3.14.5, pytest-9.1.1, pluggy-1.6.0
rootdir: /Users/bu7/_dev-project-pc/Codepath/ai110-module2show-pawpal-starter
plugins: anyio-4.14.1
collected 7 items

tests/test_pawpal.py .......                                             [100%]

============================== 7 passed in 0.02s ===============================
```

**Confidence Level:** ★★★★☆ 4/5

The current tests give strong confidence in the core scheduler behaviors, especially sorting, recurrence, and exact-time conflict detection. More tests for invalid input, monthly recurrence, and UI workflows would raise confidence further.

## Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.sort_by_time()` | Sorts tasks by `HH:MM` time strings so the daily plan appears chronologically. |
| Next open slot | `Scheduler.find_next_available_slot()` | Suggests the first available fixed-interval start time for today's care plan. |
| Filtering | `Scheduler.filter_by_pet()`, `Scheduler.filter_by_status()` | Shows one pet's tasks or tasks matching a completion state. |
| Conflict handling | `Scheduler.detect_conflicts()` | Returns warning messages when multiple tasks are scheduled at the same exact time. |
| Recurring tasks | `Task.create_next_occurrence()`, `Scheduler.complete_task()` | Completing a daily or weekly task creates the next task occurrence on the correct future date. |
| Persistence | `Owner.save_to_json()`, `Owner.load_from_json()` | Saves and reloads owner, pet, and task data through `data.json`. |

## Demo Walkthrough

The Streamlit app starts with an owner profile and pet list. A user can add pets, then create tasks with a title, due date, scheduled time, duration, priority, and frequency.

Example workflow:

1. Add a pet such as Mochi the dog or Luna the cat.
2. Add tasks like "Morning walk" at `09:00`, "Breakfast feeding" at `08:00`, or "Medication" at `08:00`.
3. Review the current task table, which is sorted by time through the Scheduler.
4. Check Today's Smart Schedule to see only today's tasks in chronological order.
5. If two tasks share the same exact time, the app shows a `st.warning` conflict message with the time and task names.
6. Check the suggested next available 30-minute slot for another care task.
7. Use the filter controls to focus on one pet or only pending/done tasks.
8. Mark a recurring daily or weekly task complete; the app creates the next occurrence automatically and saves it to `data.json`.

Running `python3 main.py` prints the same core scheduler behavior in the terminal:

```text
Today's Sorted Schedule for Jordan
====================================
08:00 | Mochi: Heartworm medication (5 min) [priority: medium] [pending]
08:00 | Luna: Breakfast feeding (10 min) [priority: high] [pending]
09:00 | Mochi: Morning walk (30 min) [priority: high] [pending]
19:30 | Luna: Evening playtime (20 min) [priority: medium] [pending]

Mochi's Tasks
=============
08:00 | Heartworm medication [medium]
09:00 | Morning walk [high]

Pending Tasks
=============
08:00 | Mochi: Heartworm medication
08:00 | Luna: Breakfast feeding
09:00 | Mochi: Morning walk
19:30 | Luna: Evening playtime

Conflict Warnings
=================
Warning: 08:00: multiple tasks scheduled (Heartworm medication, Breakfast feeding)

Recurring Task Demo
===================
Completed 'Breakfast feeding' and created next 'Breakfast feeding' for 2026-07-08.
```
