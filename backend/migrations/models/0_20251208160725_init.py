from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "organization" (
    "uuid" CHAR(36) NOT NULL PRIMARY KEY,
    "name" VARCHAR(255) NOT NULL,
    "description" TEXT,
    "created_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS "season" (
    "uuid" CHAR(36) NOT NULL PRIMARY KEY,
    "year" INT NOT NULL,
    "name" VARCHAR(255) NOT NULL,
    "active" INT NOT NULL DEFAULT 1,
    "created_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS "event" (
    "uuid" CHAR(36) NOT NULL PRIMARY KEY,
    "event_code" VARCHAR(255) NOT NULL,
    "name" VARCHAR(255) NOT NULL,
    "type" VARCHAR(255) NOT NULL,
    "city" VARCHAR(255) NOT NULL,
    "country" VARCHAR(255) NOT NULL,
    "start_date" TIMESTAMP NOT NULL,
    "end_date" TIMESTAMP NOT NULL,
    "created_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "season_id" CHAR(36) NOT NULL REFERENCES "season" ("uuid") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "gamepiece" (
    "uuid" CHAR(36) NOT NULL PRIMARY KEY,
    "name" VARCHAR(255) NOT NULL,
    "created_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "season_id" CHAR(36) NOT NULL REFERENCES "season" ("uuid") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "matchscoutingfield" (
    "uuid" CHAR(36) NOT NULL PRIMARY KEY,
    "name" VARCHAR(255) NOT NULL,
    "field_type" VARCHAR(255) NOT NULL,
    "stat_type" VARCHAR(255) NOT NULL,
    "required" INT NOT NULL DEFAULT 0,
    "options" JSON,
    "order" INT NOT NULL DEFAULT 0,
    "created_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "game_piece_id" CHAR(36) REFERENCES "gamepiece" ("uuid") ON DELETE CASCADE,
    "organization_id" CHAR(36) REFERENCES "organization" ("uuid") ON DELETE CASCADE,
    "parent_id" CHAR(36) REFERENCES "matchscoutingfield" ("uuid") ON DELETE CASCADE,
    "season_id" CHAR(36) NOT NULL REFERENCES "season" ("uuid") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "user" (
    "uuid" CHAR(36) NOT NULL PRIMARY KEY,
    "username" VARCHAR(255) NOT NULL UNIQUE,
    "email" VARCHAR(255) NOT NULL UNIQUE,
    "hashed_password" VARCHAR(255) NOT NULL,
    "is_superuser" INT NOT NULL DEFAULT 0,
    "created_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS "matchscoutingsubmission" (
    "uuid" CHAR(36) NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "event_id" CHAR(36) NOT NULL REFERENCES "event" ("uuid") ON DELETE CASCADE,
    "user_id" CHAR(36) NOT NULL REFERENCES "user" ("uuid") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "matchscoutinganswer" (
    "uuid" CHAR(36) NOT NULL PRIMARY KEY,
    "value" VARCHAR(255),
    "field_id" CHAR(36) NOT NULL REFERENCES "matchscoutingfield" ("uuid") ON DELETE CASCADE,
    "submission_id" CHAR(36) NOT NULL REFERENCES "matchscoutingsubmission" ("uuid") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "organizationmember" (
    "uuid" CHAR(36) NOT NULL PRIMARY KEY,
    "role" VARCHAR(255) NOT NULL,
    "created_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "organization_id" CHAR(36) NOT NULL REFERENCES "organization" ("uuid") ON DELETE CASCADE,
    "user_id" CHAR(36) NOT NULL REFERENCES "user" ("uuid") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "profile" (
    "uuid" CHAR(36) NOT NULL PRIMARY KEY,
    "display_name" VARCHAR(255) NOT NULL,
    "team_number" INT,
    "user_id" CHAR(36) NOT NULL REFERENCES "user" ("uuid") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "settings" (
    "uuid" CHAR(36) NOT NULL PRIMARY KEY,
    "favorite_events" JSON,
    "user_id" CHAR(36) NOT NULL REFERENCES "user" ("uuid") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSON NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """


MODELS_STATE = (
    "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"
    "c="
)
