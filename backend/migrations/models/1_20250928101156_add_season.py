from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "season" (
    "uuid" CHAR(36) NOT NULL PRIMARY KEY,
    "year" INT NOT NULL,
    "label" VARCHAR(255) NOT NULL,
    "active" INT NOT NULL DEFAULT 1,
    "created_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "season";"""
