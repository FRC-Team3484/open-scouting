# Managing the Database

## Adding or editing models
Modify `/backend/app/main.py` to add new models

Then, use Alembic to migrate the database

First, create your migrations

```bash
alembic revision --autogenerate -m "What changes you made"
```

Confirm that the auto generated files look right. Then, run the migrations.

```bash
alembic upgrade head
```