# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

Three core user actions I want PawPal+ to support are:

- Add a pet to an owner's profile.
- Schedule care tasks such as feeding, walks, medication, or appointments.
- View an organized daily schedule with conflicts or recurring tasks handled by the system.

My initial UML design uses four main classes: `Owner`, `Pet`, `Task`, and `Scheduler`. `Owner` stores the person using the app and manages a list of pets. `Pet` stores basic pet details and the tasks assigned to that pet. `Task` represents one care activity, including its title, time, due date, duration, priority, frequency, and completion status. `Scheduler` acts as the system's organizing layer. It retrieves tasks from the owner and pets, sorts tasks by time, filters tasks by pet or status, detects scheduling conflicts, and handles recurring tasks.

I chose this structure because it keeps each class focused on one responsibility. The pet and task classes model the real-world data, while the scheduler handles logic that crosses multiple pets.

**b. Design changes**

Yes. My initial design treated tasks mostly as static items on a list, but the final implementation needed tasks to create future tasks when they repeat. I added `Task.create_next_occurrence()` so each task owns the simple recurrence rule for daily and weekly repeats.

I also made `Scheduler` the place where cross-pet logic lives. Instead of having each `Pet` sort or compare tasks independently, `Scheduler` reads all tasks from `Owner`, filters them by date/pet/status, sorts them, detects conflicts, and completes recurring tasks. That made the UI and tests simpler because they can call one scheduling layer instead of duplicating logic.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

The scheduler currently considers due date, scheduled time, pet name, completion status, and task frequency. Due date matters because `get_today_tasks()` should only show tasks that belong on today's plan. Time matters because pet owners need a schedule they can follow in order. Pet name and completion status matter because the owner may want to focus on one pet or only see tasks that still need attention. Frequency matters because daily and weekly tasks should continue after they are completed.

I prioritized time sorting and completion status first because they make the schedule immediately useful in both the CLI and the UI. I treated priority as descriptive for now instead of using it to reorder tasks, because Phase 4 specifically required sorting by time and the app is still a simple care planner.

**b. Tradeoffs**

One tradeoff is that conflict detection only checks for exact time matches, such as two tasks both scheduled at `08:00`. It does not calculate whether task durations overlap, such as an `08:00` task lasting 45 minutes and an `08:30` task starting before the first one ends.

This tradeoff is reasonable for the current version because exact-time conflicts are easy for a beginner-friendly scheduler to explain and test. A duration-overlap algorithm would be more realistic, but it would add complexity before the core object relationships and CLI workflow are fully established.

---

## 3. AI Collaboration

**a. How you used AI**

I used AI to brainstorm edge cases, draft focused pytest functions, check whether the UI reflected the backend logic, and polish documentation. The most helpful prompts were specific and testable, such as asking for important scheduler edge cases or asking which UML changes matched the final implementation.

AI was especially useful for turning broad project requirements into concrete engineering tasks: sorting tests, recurrence tests, conflict warnings, final README sections, and a final UML file.

**b. Judgment and verification**

I did not treat generated tests as correct just because they looked reasonable. I checked them against the actual method names and return values in `pawpal_system.py`, then ran `python -m pytest` to verify they passed.

I also verified the Streamlit changes by running syntax checks and starting the app locally. That helped confirm that the UI code was not only descriptive, but actually connected to the `Scheduler` methods.

---

## 4. Testing and Verification

**a. What you tested**

I tested marking a task complete, adding a task to a pet, sorting tasks chronologically, creating the next daily task after completion, and detecting duplicate task times.

These tests are important because they cover the core promise of PawPal+: the app should organize care tasks reliably, preserve pet/task relationships, continue recurring routines, and warn owners when the schedule has an obvious conflict.

**b. Confidence**

My confidence level is 4 out of 5 stars. The scheduler works for the main happy paths and the most important beginner-friendly edge case: exact duplicate times.

If I had more time, I would test invalid inputs, pets with no tasks, multiple pets with overlapping schedules, weekly recurrence, monthly recurrence, leap-day behavior, and duration-based conflicts where tasks overlap even if they do not start at the exact same time.

---

## 5. Reflection

**a. What went well**

I am most satisfied with how the same backend logic now appears in three places: tests, the CLI demo, and the Streamlit UI. Sorting, conflict detection, filtering, and recurrence are not just hidden methods; the user can see and use them.

**b. What you would improve**

In another iteration, I would redesign time handling to use actual `datetime` objects instead of `HH:MM` strings. That would make duration-overlap conflicts, time zones, and date/time sorting more reliable.

I would also add IDs to tasks. Right now the app identifies tasks by object references and display labels, which is fine for a small in-memory app, but IDs would be better for editing, deleting, persistence, and avoiding ambiguity when two tasks have the same title and time.

**c. Key takeaway**

My biggest takeaway is that AI is strongest when I use it as a design and verification partner, not as a replacement for judgment. The useful pattern was: ask for ideas, compare them to the code, implement a small change, run tests, then document what the system actually does.
