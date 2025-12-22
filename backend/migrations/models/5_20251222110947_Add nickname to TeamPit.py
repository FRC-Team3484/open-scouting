from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "teampit" ADD "nickname" VARCHAR(255) NOT NULL;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "teampit" DROP COLUMN "nickname";"""


MODELS_STATE = (
    "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"
)
