from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "event" ADD "end_date" DATE;
        ALTER TABLE "event" ADD "start_date" DATE;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "event" DROP COLUMN "end_date";
        ALTER TABLE "event" DROP COLUMN "start_date";"""


MODELS_STATE = (
    "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"
)
