from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "pitscoutingfield" (
    "uuid" CHAR(36) NOT NULL PRIMARY KEY,
    "name" VARCHAR(255) NOT NULL,
    "field_type" VARCHAR(255) NOT NULL,
    "options" JSON,
    "order" INT NOT NULL DEFAULT 0,
    "created_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "organization_id" CHAR(36) REFERENCES "organization" ("uuid") ON DELETE CASCADE,
    "season_id" CHAR(36) NOT NULL REFERENCES "season" ("uuid") ON DELETE CASCADE
);
        CREATE TABLE IF NOT EXISTS "teampit" (
    "uuid" CHAR(36) NOT NULL PRIMARY KEY,
    "team_number" INT NOT NULL,
    "created_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "event_id" CHAR(36) NOT NULL REFERENCES "event" ("uuid") ON DELETE CASCADE,
    "season_id" CHAR(36) NOT NULL REFERENCES "season" ("uuid") ON DELETE CASCADE
);
        CREATE TABLE IF NOT EXISTS "pitscoutinganswer" (
    "uuid" CHAR(36) NOT NULL PRIMARY KEY,
    "value" VARCHAR(255),
    "field_id" CHAR(36) NOT NULL REFERENCES "pitscoutingfield" ("uuid") ON DELETE CASCADE,
    "team_id" CHAR(36) NOT NULL REFERENCES "teampit" ("uuid") ON DELETE CASCADE
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "teampit";
        DROP TABLE IF EXISTS "pitscoutinganswer";
        DROP TABLE IF EXISTS "pitscoutingfield";"""


MODELS_STATE = (
    "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"
)
