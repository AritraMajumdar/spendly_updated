---
name: reset-db
description: Drop and recreate the local Spendly SQLite database (expense_tracker.db) with a fresh schema and seed data. Use when the dev database is in a bad state or schema changes need a clean slate.
disable-model-invocation: true
---

Reset the local Spendly development database:

1. Delete `expense_tracker.db` from the project root if it exists.
2. Run a short Python snippet (using the project's venv) that imports `init_db` and `seed_db` from `database.db` and calls both, e.g.:

```bash
python -c "from database.db import init_db, seed_db; init_db(); seed_db()"
```

3. Confirm the file was recreated and report what schema/seed data was applied.

If `database/db.py` does not yet implement `init_db()`/`seed_db()`, tell the user the DB layer hasn't been built yet instead of guessing at a schema.
