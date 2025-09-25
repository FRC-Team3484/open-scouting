from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "organization_organizationmember";
        ALTER TABLE "organization" ADD "created_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP;
        ALTER TABLE "organizationmember" ADD "created_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "organization" DROP COLUMN "created_at";
        ALTER TABLE "organizationmember" DROP COLUMN "created_at";
        CREATE TABLE "organization_organizationmember" (
    "organization_id" INT NOT NULL REFERENCES "organization" ("id") ON DELETE CASCADE,
    "organizationmember_id" INT NOT NULL REFERENCES "organizationmember" ("id") ON DELETE CASCADE
);"""
