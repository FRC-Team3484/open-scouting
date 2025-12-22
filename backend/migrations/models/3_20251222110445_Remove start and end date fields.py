from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "event" DROP COLUMN "start_date";
        ALTER TABLE "event" DROP COLUMN "end_date";"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "event" ADD "start_date" TIMESTAMP NOT NULL;
        ALTER TABLE "event" ADD "end_date" TIMESTAMP NOT NULL;"""


MODELS_STATE = (
    "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"
)
