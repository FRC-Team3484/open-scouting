import os
from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

app = FastAPI()

@app.get("/")
def read_root():
    return {"msg": "Hello World"}

# Register Tortoise ORM
register_tortoise(
    app,
    db_url=os.getenv("DATABASE_URL", "sqlite://dev.db"),
    modules={"models": ["app.models"]},
    generate_schemas=False,
    add_exception_handlers=True,
)

TORTOISE_ORM = {
    "connections": {"default": os.getenv("DATABASE_URL", "sqlite://dev.db")},
    "apps": {
        "models": {
            "models": ["app.models", "aerich.models"],
            "default_connection": "default",
        },
    },
}
