from tortoise import BaseDBAsyncClient


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
