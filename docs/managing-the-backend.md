# Managing the Backend
- [Adding or editing models](#adding-or-editing-models)
- [Updating orval types](#updating-orval-types)

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

## Updating orval types
When backend routes are edited, the typed frontend API request functions and zod schemas should be generated. This improves data validation and makes it easier to correctly perform requests to the backend. These can be generated using `orval`.

```bash
cd frontend
npx orval
```

You can also use the VSCode task `Generate orval types`