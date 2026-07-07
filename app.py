from datetime import date

import streamlit as st

from pawpal_system import Owner, Pet, Scheduler, Task


def get_or_create_pet(owner: Owner, pet_name: str, species: str) -> Pet:
    """Return an existing pet or create a new one for the owner."""
    pet = owner.find_pet(pet_name)
    if pet is None:
        pet = Pet(name=pet_name, species=species)
        owner.add_pet(pet)
    return pet


def task_rows(owner: Owner) -> list[dict[str, object]]:
    """Convert owner task objects into table-friendly rows."""
    rows: list[dict[str, object]] = []
    for pet in owner.pets:
        for task in pet.tasks:
            rows.append(
                {
                    "pet": pet.name,
                    "species": pet.species,
                    "time": task.time,
                    "task": task.title,
                    "duration": task.duration_minutes,
                    "priority": task.priority,
                    "status": "done" if task.completed else "pending",
                }
            )
    return rows


def schedule_rows(owner: Owner, tasks: list[Task]) -> list[dict[str, object]]:
    """Convert scheduled task objects into table-friendly rows."""
    rows: list[dict[str, object]] = []
    for task in tasks:
        pet_name = "Unknown"
        for pet in owner.pets:
            if task in pet.tasks:
                pet_name = pet.name
                break

        rows.append(
            {
                "time": task.time,
                "pet": pet_name,
                "task": task.title,
                "duration": task.duration_minutes,
                "priority": task.priority,
                "status": "done" if task.completed else "pending",
            }
        )
    return rows


st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This app now connects the Streamlit interface to the PawPal+ backend classes in
`pawpal_system.py`.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Owner Profile")
owner_name = st.text_input("Owner name", value="Jordan")

if "owner" not in st.session_state:
    st.session_state.owner = Owner(name=owner_name)

owner = st.session_state.owner
owner.name = owner_name

st.subheader("Pets")
pet_name = st.text_input("New pet name", value="Mochi")
species = st.selectbox("New pet species", ["dog", "cat", "other"])

if st.button("Add pet"):
    if pet_name.strip():
        get_or_create_pet(owner, pet_name.strip(), species)
        st.success(f"Added {pet_name.strip()} to {owner.name}'s profile.")
    else:
        st.warning("Enter a pet name before adding a pet.")

if owner.pets:
    st.write("Current pets:")
    st.table([{"name": pet.name, "species": pet.species} for pet in owner.pets])
else:
    st.info("No pets yet. Add one above before scheduling tasks.")

st.markdown("### Tasks")
st.caption("Add a few tasks. These now feed into the PawPal+ backend classes.")

col1, col2 = st.columns(2)
with col1:
    pet_options = [pet.name for pet in owner.pets]
    if pet_options:
        selected_pet_name = st.selectbox("Pet for this task", pet_options)
    else:
        selected_pet_name = None
        st.selectbox("Pet for this task", ["Add a pet first"], disabled=True)
    task_title = st.text_input("Task title", value="Morning walk")
    task_time = st.time_input("Task time", value="08:00")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

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
                    due_date=date.today(),
                    duration_minutes=int(duration),
                    priority=priority,
                )
            )
            st.success(f"Added '{cleaned_task_title}' for {pet.name}.")

current_tasks = task_rows(owner)
if current_tasks:
    st.write("Current tasks:")
    st.table(current_tasks)
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("This button calls your Scheduler class from pawpal_system.py.")

if st.button("Generate schedule"):
    scheduler = Scheduler(owner)
    today_tasks = scheduler.sort_by_time(scheduler.get_today_tasks())

    if today_tasks:
        st.success(f"Generated today's schedule for {owner.name}.")
        st.table(schedule_rows(owner, today_tasks))
    else:
        st.info("No tasks scheduled for today yet.")
