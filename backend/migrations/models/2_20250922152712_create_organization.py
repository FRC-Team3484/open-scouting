from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "organization" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "name" VARCHAR(255) NOT NULL,
    "label" VARCHAR(512) NOT NULL,
    "description" TEXT
);
        CREATE TABLE "organization_user" (
    "organization_id" INT NOT NULL REFERENCES "organization" ("id") ON DELETE CASCADE,
    "user_id" INT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "organization_user";
        DROP TABLE IF EXISTS "organization";"""
