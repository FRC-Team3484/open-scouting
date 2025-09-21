import os
from fastapi import FastAPI, Depends
from sqlmodel import SQLModel, Session, create_engine, Field, select, Column, String

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./dev.db")

# Engine creation
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(DATABASE_URL)

# Models
# ...

app = FastAPI()

# @app.on_event("startup")
# def on_startup():

# Dependency for DB session
def get_session():
    with Session(engine) as session:
        yield session

@app.get("/")
def read_root():
    return {"msg": "Hello World"}