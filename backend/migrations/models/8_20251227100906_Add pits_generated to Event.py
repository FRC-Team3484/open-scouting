from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "event" ADD "pits_generated" INT NOT NULL DEFAULT 0;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "event" DROP COLUMN "pits_generated";"""


MODELS_STATE = (
    "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"
)
