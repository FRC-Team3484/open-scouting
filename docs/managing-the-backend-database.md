# Managing the Backend Database

## Adding or editing models
Modify `/backend/app/models.py` to add new models

Then, use Aerich to migrate the database

First, create your migrations

```bash
aerich migrate --name "add_display_name"
```

Confirm that the auto generated files look right. Then, run the migrations.

```bash
aerich upgrade
```