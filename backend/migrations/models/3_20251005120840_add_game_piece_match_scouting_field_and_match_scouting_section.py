from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "gamepiece" (
    "uuid" CHAR(36) NOT NULL PRIMARY KEY,
    "name" VARCHAR(255) NOT NULL,
    "label" VARCHAR(255) NOT NULL,
    "created_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "season_id" CHAR(36) NOT NULL REFERENCES "season" ("uuid") ON DELETE CASCADE
);
        CREATE TABLE IF NOT EXISTS "matchscoutingfield" (
    "uuid" CHAR(36) NOT NULL PRIMARY KEY,
    "name" VARCHAR(255) NOT NULL,
    "label" VARCHAR(255) NOT NULL,
    "field_type" VARCHAR(255) NOT NULL,
    "stat_type" VARCHAR(255) NOT NULL,
    "required" INT NOT NULL DEFAULT 0,
    "options" JSON,
    "order" INT NOT NULL DEFAULT 0,
    "created_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "game_piece_id" CHAR(36) REFERENCES "gamepiece" ("uuid") ON DELETE CASCADE,
    "organization_id" CHAR(36) REFERENCES "organization" ("uuid") ON DELETE CASCADE,
    "season_id" CHAR(36) NOT NULL REFERENCES "season" ("uuid") ON DELETE CASCADE
);
        CREATE TABLE IF NOT EXISTS "matchscoutingsection" (
    "uuid" CHAR(36) NOT NULL PRIMARY KEY,
    "name" VARCHAR(255) NOT NULL,
    "label" VARCHAR(255) NOT NULL,
    "order" INT NOT NULL DEFAULT 0,
    "created_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "organization_id" CHAR(36) REFERENCES "organization" ("uuid") ON DELETE CASCADE,
    "season_id" CHAR(36) NOT NULL REFERENCES "season" ("uuid") ON DELETE CASCADE
);
        CREATE TABLE "matchscoutingsection_matchscoutingfield" (
    "matchscoutingfield_id" CHAR(36) NOT NULL REFERENCES "matchscoutingfield" ("uuid") ON DELETE CASCADE,
    "matchscoutingsection_id" CHAR(36) NOT NULL REFERENCES "matchscoutingsection" ("uuid") ON DELETE CASCADE
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "matchscoutingsection";
        DROP TABLE IF EXISTS "matchscoutingfield";
        DROP TABLE IF EXISTS "gamepiece";"""
