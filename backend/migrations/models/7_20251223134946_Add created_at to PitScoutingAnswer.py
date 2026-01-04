from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "pitscoutinganswer" ADD "created_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "pitscoutinganswer" DROP COLUMN "created_at";"""


MODELS_STATE = (
    "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"
    "zjRkOcVr+8/PofnrG1Tg=="
)
