from datetime import date, time
from pathlib import Path

import streamlit as st

from pawpal_system import Owner, Pet, Scheduler, Task


DATA_FILE = Path("data.json")


def find_pet_name(owner: Owner, task: Task) -> str:
    """Return the name of the pet that owns a task."""
    for pet in owner.pets:
        if task in pet.tasks:
            return pet.name
    return "Unknown pet"


def get_or_create_pet(owner: Owner, pet_name: str, species: str) -> Pet:
    """Return an existing pet or create a new one for the owner."""
    pet = owner.find_pet(pet_name)
    if pet is None:
        pet = Pet(name=pet_name, species=species)
        owner.add_pet(pet)
    return pet


def task_rows(owner: Owner, tasks: list[Task]) -> list[dict[str, object]]:
    """Convert owner task objects into table-friendly rows."""
    rows: list[dict[str, object]] = []
    for task in tasks:
        rows.append(
            {
                "pet": find_pet_name(owner, task),
                "due date": task.due_date.isoformat(),
                "time": task.time,
                "task": task.title,
                "duration": task.duration_minutes,
                "priority": task.priority,
                "frequency": task.frequency,
                "status": "done" if task.completed else "pending",
            }
        )
    return rows


def schedule_rows(owner: Owner, tasks: list[Task]) -> list[dict[str, object]]:
    """Convert scheduled task objects into table-friendly rows."""
    rows: list[dict[str, object]] = []
    for task in tasks:
        rows.append(
            {
                "time": task.time,
                "pet": find_pet_name(owner, task),
                "task": task.title,
                "duration": task.duration_minutes,
                "priority": task.priority,
                "frequency": task.frequency,
                "status": "done" if task.completed else "pending",
            }
        )
    return rows


st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Plan pet care tasks, spot scheduling conflicts, and keep recurring routines moving.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.
"""
    )

with st.expander("What this app can do", expanded=True):
    st.markdown(
        """
- Store owner, pet, and care task information
- Sort today's schedule by task time
- Filter tasks by pet and completion status
- Warn when two tasks share the same scheduled time
- Create the next occurrence for daily or weekly recurring tasks
"""
    )

st.divider()

st.subheader("Owner Profile")

if "owner" not in st.session_state:
    st.session_state.owner = Owner.load_from_json(DATA_FILE)

owner = st.session_state.owner
owner_name = st.text_input("Owner name", value=owner.name)
owner.name = owner_name
scheduler = Scheduler(owner)

persistence_col1, persistence_col2 = st.columns(2)
with persistence_col1:
    if st.button("Save data"):
        owner.save_to_json(DATA_FILE)
        st.success(f"Saved pets and tasks to {DATA_FILE}.")
with persistence_col2:
    if st.button("Reload saved data"):
        st.session_state.owner = Owner.load_from_json(DATA_FILE)
        st.success(f"Reloaded pets and tasks from {DATA_FILE}.")
        st.rerun()

st.subheader("Pets")
pet_name = st.text_input("New pet name", value="Mochi")
species = st.selectbox("New pet species", ["dog", "cat", "other"])

if st.button("Add pet"):
    if pet_name.strip():
        get_or_create_pet(owner, pet_name.strip(), species)
        owner.save_to_json(DATA_FILE)
        st.success(f"Added {pet_name.strip()} to {owner.name}'s profile.")
    else:
        st.warning("Enter a pet name before adding a pet.")

if owner.pets:
    st.write("Current pets:")
    st.table([{"name": pet.name, "species": pet.species} for pet in owner.pets])
else:
    st.info("No pets yet. Add one above before scheduling tasks.")

st.markdown("### Tasks")
st.caption("Tasks feed into the Scheduler for sorting, filtering, conflicts, and recurrence.")

col1, col2 = st.columns(2)
with col1:
    pet_options = [pet.name for pet in owner.pets]
    if pet_options:
        selected_pet_name = st.selectbox("Pet for this task", pet_options)
    else:
        selected_pet_name = None
        st.selectbox("Pet for this task", ["Add a pet first"], disabled=True)
    task_title = st.text_input("Task title", value="Morning walk")
    task_time = st.time_input("Task time", value=time(8, 0))
with col2:
    task_due_date = st.date_input("Due date", value=date.today())
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
    frequency = st.selectbox("Frequency", ["once", "daily", "weekly"])

if st.button("Add task"):
    cleaned_task_title = task_title.strip()

    if not owner.pets:
        st.warning("Add a pet before adding a task.")
    elif not cleaned_task_title:
        st.warning("Enter a task title before adding a task.")
    else:
        pet = owner.find_pet(selected_pet_name)
        if pet is None:
            st.warning("Select an existing pet before adding a task.")
        else:
            pet.add_task(
                Task(
                    title=cleaned_task_title,
                    time=task_time.strftime("%H:%M"),
                    due_date=task_due_date,
                    duration_minutes=int(duration),
                    priority=priority,
                    frequency=frequency,
                )
            )
            owner.save_to_json(DATA_FILE)
            st.success(f"Added '{cleaned_task_title}' for {pet.name}.")

all_tasks = scheduler.sort_by_time(owner.get_all_tasks())
current_tasks = task_rows(owner, all_tasks)
if current_tasks:
    st.write("Current tasks sorted by time:")
    st.table(current_tasks)
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Today's Smart Schedule")
st.caption("This view uses Scheduler.get_today_tasks(), sort_by_time(), and detect_conflicts().")

today_tasks = scheduler.sort_by_time(scheduler.get_today_tasks())
if today_tasks:
    st.success(f"Today's schedule for {owner.name} is sorted chronologically.")
    st.table(schedule_rows(owner, today_tasks))

    conflicts = scheduler.detect_conflicts(today_tasks)
    if conflicts:
        for warning in conflicts:
            st.warning(
                f"Schedule conflict: {warning}. Consider moving one task to a different time."
            )
    else:
        st.success("No exact-time conflicts found for today.")
else:
    st.info("No tasks scheduled for today yet.")

next_slot = scheduler.find_next_available_slot()
if next_slot is None:
    st.warning("No open 30-minute start times remain between 08:00 and 20:00 today.")
else:
    st.info(f"Next available 30-minute slot today: {next_slot}")

st.subheader("Filter Tasks")
st.caption("Use Scheduler filters to focus on one pet or one completion state.")

filter_col1, filter_col2 = st.columns(2)
with filter_col1:
    pet_filter_options = ["All pets"] + [pet.name for pet in owner.pets]
    pet_filter = st.selectbox("Pet filter", pet_filter_options)
with filter_col2:
    status_filter = st.selectbox("Status filter", ["All tasks", "Pending", "Done"])

filtered_tasks = (
    owner.get_all_tasks()
    if pet_filter == "All pets"
    else scheduler.filter_by_pet(pet_filter)
)
if status_filter != "All tasks":
    completed = status_filter == "Done"
    status_tasks = scheduler.filter_by_status(completed)
    filtered_tasks = [task for task in filtered_tasks if task in status_tasks]

filtered_tasks = scheduler.sort_by_time(filtered_tasks)
if filtered_tasks:
    st.table(task_rows(owner, filtered_tasks))
else:
    st.info("No tasks match those filters.")

st.subheader("Complete a Task")
st.caption("Daily and weekly tasks create the next occurrence when completed.")

pending_tasks = scheduler.sort_by_time(scheduler.filter_by_status(False))
if pending_tasks:
    task_labels = [
        (
            f"{task.due_date.isoformat()} {task.time} | "
            f"{find_pet_name(owner, task)} | {task.title} ({task.frequency})"
        )
        for task in pending_tasks
    ]
    selected_task_label = st.selectbox("Task to complete", task_labels)
    selected_task = pending_tasks[task_labels.index(selected_task_label)]

    if st.button("Mark selected task complete"):
        next_task = scheduler.complete_task(selected_task)
        owner.save_to_json(DATA_FILE)
        if next_task is None:
            st.success(f"Marked '{selected_task.title}' complete.")
        else:
            st.success(
                f"Marked '{selected_task.title}' complete and added the next "
                f"{next_task.frequency} occurrence for {next_task.due_date.isoformat()}."
            )
            st.table(schedule_rows(owner, [next_task]))
else:
    st.info("No pending tasks to complete.")
