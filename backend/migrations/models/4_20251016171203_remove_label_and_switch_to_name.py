from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "gamepiece" DROP COLUMN "label";
        ALTER TABLE "matchscoutingfield" DROP COLUMN "label";
        ALTER TABLE "matchscoutingsection" DROP COLUMN "label";
        ALTER TABLE "organization" DROP COLUMN "label";
        ALTER TABLE "season" RENAME COLUMN "label" TO "name";"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "gamepiece" ADD "label" VARCHAR(255) NOT NULL;
        ALTER TABLE "matchscoutingfield" ADD "label" VARCHAR(255) NOT NULL;
        ALTER TABLE "matchscoutingsection" ADD "label" VARCHAR(255) NOT NULL;
        ALTER TABLE "organization" ADD "label" VARCHAR(512) NOT NULL;
        ALTER TABLE "season" RENAME COLUMN "name" TO "label";"""
