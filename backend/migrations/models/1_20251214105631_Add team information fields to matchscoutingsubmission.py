from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "matchscoutingsubmission" ADD "team_number" INT NOT NULL DEFAULT 0;
        ALTER TABLE "matchscoutingsubmission" ADD "match_number" INT NOT NULL DEFAULT 0;
        ALTER TABLE "matchscoutingsubmission" ADD "match_type" VARCHAR(255) NOT NULL DEFAULT '';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "matchscoutingsubmission" DROP COLUMN "team_number";
        ALTER TABLE "matchscoutingsubmission" DROP COLUMN "match_number";
        ALTER TABLE "matchscoutingsubmission" DROP COLUMN "match_type";"""


MODELS_STATE = (
    "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"
    "cUJ64zJhUkrOuVP60sN60gTqt3L7/+B2KXgX8="
)
