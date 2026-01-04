from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "pitscoutinganswer" ADD "username" VARCHAR(255);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "pitscoutinganswer" DROP COLUMN "username";"""


MODELS_STATE = (
    "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"
)
