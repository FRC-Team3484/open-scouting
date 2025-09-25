from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "organization_user";
        CREATE TABLE IF NOT EXISTS "organizationmember" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "role" VARCHAR(255) NOT NULL,
    "organization_id" INT NOT NULL REFERENCES "organization" ("id") ON DELETE CASCADE,
    "user_id" INT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
);
        CREATE TABLE "organization_organizationmember" (
    "organizationmember_id" INT NOT NULL REFERENCES "organizationmember" ("id") ON DELETE CASCADE,
    "organization_id" INT NOT NULL REFERENCES "organization" ("id") ON DELETE CASCADE
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "organizationmember";
        CREATE TABLE "organization_user" (
    "user_id" INT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE,
    "organization_id" INT NOT NULL REFERENCES "organization" ("id") ON DELETE CASCADE
);"""
