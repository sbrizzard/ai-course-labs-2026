## DEVELOPMENT.md

### 实际实现
- **add**:
  - Input: `title` (string)
  - Creates a new task with `id` set to the next available integer (default 1), `title` trimmed, and `done` set to `False`.
  - Updates `tasks.json` with the new task.
- **list**:
  - Lists all tasks with their `id`, `done` status (as '完成' or '待办'), and `title`.
- **done**:
  - Takes `task_id` as input, finds the task with matching `id`, sets `done` to `True`, and updates `tasks.json`.

### JSON Path
- The `DATA` path is derived from `__file__` using `Path(__file__).resolve().parent / "tasks.json"`.
- This ensures the data file is stored in the same directory as the script.

### Input Validation
- `add_task`: Validates that `title` is not empty or whitespace. Raises `ValueError` if invalid.
- `finish_task`: Validates that `task_id` exists in the tasks list. Raises `ValueError` if not found.

### Observation-Hypothesis-Plan-Execution-Verification Workflow

**Observation**:
- A simple CLI task manager with persistent storage.

**Hypothesis**:
- `add`, `list`, `done` operations work correctly with input validation.

**Plan**:
1. Implement core operations in `task_manager.py`.
2. Write unit tests in `test_task_manager.py`.
3. Verify all operations via test cases.

**Execution**:
- Implemented `add_task`, `finish_task`, and `list` in `task_manager.py`.
- Wrote tests in `test_task_manager.py` with assertions and error handling.

**Verification**:
- All tests in `test_task_manager.py` pass, confirming correct behavior of add, finish, and missing task validation.

### Notes
- All data is stored in `tasks.json` in the directory of the script.
- Uses JSON for persistence with minimal overhead.