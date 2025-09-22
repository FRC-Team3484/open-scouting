from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "profile" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "display_name" VARCHAR(255) NOT NULL,
    "team_number" INT,
    "user_id" INT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
);
        ALTER TABLE "user" DROP COLUMN "display_name";"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "user" ADD "display_name" VARCHAR(255) NOT NULL;
        DROP TABLE IF EXISTS "profile";"""
