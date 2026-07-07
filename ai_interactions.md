# AI Interactions Log

This log documents how I used an AI coding agent for the optional PawPal+ extensions.

---

## Agent Workflow

**What task did you give the agent?**

I asked the AI coding agent to extend PawPal+ beyond the base requirements by adding two optional features:

- A smarter scheduling capability that suggests the next available care slot.
- JSON persistence so pets and tasks survive between app runs.

I also asked the agent to document the workflow and update the project documentation so reviewers could understand what changed.

**What did the agent do?**

The agent modified these files:

- `pawpal_system.py`: added custom `to_dict()` and `from_dict()` methods for `Task`, `Pet`, and `Owner`; added `Owner.save_to_json()` and `Owner.load_from_json()`; added `Scheduler.find_next_available_slot()`.
- `app.py`: loaded data from `data.json` on startup, added manual save/reload buttons, saved automatically after adding pets/tasks and completing tasks, and displayed the next available 30-minute slot in the UI.
- `tests/test_pawpal.py`: added tests for JSON persistence and next-slot scheduling.
- `README.md`: documented the optional features, persistence workflow, modified files, and updated pytest output.
- `diagrams/uml_final.mmd`: updated the final UML with persistence and next-slot methods.
- `.gitignore`: added `data.json` because it is runtime user data.
- `ai_interactions.md`: documented this workflow.

The agent ran syntax checks with `python3 -m py_compile` and ran the test suite with `python -m pytest`.

**What did you have to verify or fix manually?**

I verified that a custom dictionary approach was better than adding a library like `marshmallow` because the project only needs simple dataclass serialization. I also checked that `data.json` should be ignored by git so local app state does not get committed accidentally.

The main manual review step was making sure the new optional features did not break the original scheduler behavior. The final pytest run passed with 7 tests, including the original sorting, recurrence, and conflict tests.
