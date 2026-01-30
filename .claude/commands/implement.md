# /implement - Execute Approved Plan

Implement an approved plan from `.claude/plans/`.

## Instructions

1. **Find the Plan**: Look in `.claude/plans/` for the specified plan
2. **Verify Status**: Only implement plans with status `APPROVED`
3. **Execute Tasks**: Work through implementation tasks in order
4. **Update Status**: Mark plan as `IN_PROGRESS` while working
5. **Test**: Run tests after each significant change
6. **Complete**: Mark plan as `COMPLETED` when done

## Workflow

```
1. Read plan file
2. Update status to IN_PROGRESS
3. For each task:
   a. Implement the change
   b. Run relevant tests
   c. Mark task as done in plan
4. Run full test suite
5. Update status to COMPLETED
```

## Commands to Run

```bash
# After changes
uv run pytest tests/ -v

# Before marking complete
uv run ruff check src tests
uv run ruff format src tests
uv run mypy src
uv run pytest --cov
```

## Usage

```
/implement [plan-name]
```

If no plan name given, list available approved plans.
