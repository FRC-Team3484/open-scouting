from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "event" (
    "uuid" CHAR(36) NOT NULL PRIMARY KEY,
    "event_code" VARCHAR(255) NOT NULL,
    "name" VARCHAR(255) NOT NULL,
    "type" VARCHAR(255) NOT NULL,
    "city" VARCHAR(255) NOT NULL,
    "country" VARCHAR(255) NOT NULL,
    "start_date" TIMESTAMP NOT NULL,
    "end_date" TIMESTAMP NOT NULL,
    "created_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "season_id" CHAR(36) NOT NULL REFERENCES "season" ("uuid") ON DELETE CASCADE
);
        CREATE TABLE IF NOT EXISTS "matchscoutinganswer" (
    "uuid" CHAR(36) NOT NULL PRIMARY KEY,
    "value" VARCHAR(255),
    "created_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "event_id" CHAR(36) NOT NULL REFERENCES "event" ("uuid") ON DELETE CASCADE,
    "field_id" CHAR(36) NOT NULL REFERENCES "matchscoutingfield" ("uuid") ON DELETE CASCADE,
    "user_id" CHAR(36) NOT NULL REFERENCES "user" ("uuid") ON DELETE CASCADE
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "event";
        DROP TABLE IF EXISTS "matchscoutinganswer";"""
