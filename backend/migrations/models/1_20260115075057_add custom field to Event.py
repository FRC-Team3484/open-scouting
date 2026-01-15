from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "event" ADD "custom" BOOL NOT NULL DEFAULT False;
        ALTER TABLE "matchscoutingfield" ALTER COLUMN "options" TYPE JSONB USING "options"::JSONB;
        ALTER TABLE "pitscoutingfield" ALTER COLUMN "options" TYPE JSONB USING "options"::JSONB;
        ALTER TABLE "settings" ALTER COLUMN "favorite_events" TYPE JSONB USING "favorite_events"::JSONB;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "event" DROP COLUMN "custom";
        ALTER TABLE "settings" ALTER COLUMN "favorite_events" TYPE JSONB USING "favorite_events"::JSONB;
        ALTER TABLE "pitscoutingfield" ALTER COLUMN "options" TYPE JSONB USING "options"::JSONB;
        ALTER TABLE "matchscoutingfield" ALTER COLUMN "options" TYPE JSONB USING "options"::JSONB;"""


MODELS_STATE = (
    "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"
)
