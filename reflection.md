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

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

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

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
