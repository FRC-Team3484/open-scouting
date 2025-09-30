from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "settings" (
    "uuid" CHAR(36) NOT NULL PRIMARY KEY,
    "favorite_events" JSON,
    "user_id" CHAR(36) NOT NULL REFERENCES "user" ("uuid") ON DELETE CASCADE
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "settings";"""
