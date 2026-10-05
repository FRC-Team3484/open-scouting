import Dexie from 'dexie';

// Interfaces for tables
//     Season table
export interface Season {
    uuid: string
    year: number
    name: string
    active: boolean
    fetch_time: Date
}

//     Fields table
export interface ScoutingFieldChoice {
    uuid: string
    name: string
    simple_name: string
}
export interface ScoutingFieldOptions {
    uuid: string
    choices: ScoutingFieldChoice[] | null
    default: number | null
    minimum: number | null
    maximum: number | null
}
export interface MatchScoutingField {
    uuid: string
    season_uuid: string | null
    organization_uuid: string | null
    parent_uuid: string | null
    name: string
    description: string
    scouting_type: "match"
    field_type: "section" | "string" | "large_number" | "small_number" | "coarse_small_number" | "boolean" | "choice" | "multiple_choice"
    stat_type: "section" | "auton_score" | "auton_miss" | "teleop_score" | "teleop_miss" | "capability" | "other" | "ignore"
    game_piece_uuid: string | null
    required: boolean
    options: ScoutingFieldOptions | null
    order: number
    archived: boolean
}
export interface PitScoutingField {
    uuid: string
    season_uuid: string | null
    organization_uuid: string | null
    name: string
    description: string
    scouting_type: "pit"
    field_type: "string" | "boolean" | "choice" | "number" | "image"
    required: boolean
    options: ScoutingFieldOptions | null
    order: number
    archived: boolean
}
export type ScoutingField = MatchScoutingField | PitScoutingField

//     Game Pieces table
export interface GamePiece {
    uuid: string
    season_uuid: string
    name: string
    fetch_time: Date
}

//     Events table
export interface Event {
    uuid: string
    year: number
    event_code: string
    name: string
    type: string
    city: string
    country: string
    start_date: string
    end_date: string
    week: number | null
    custom: boolean
    fetch_time: Date
}

//     Match Scouting table
export interface MatchScoutingData {
    uuid: string
    data: { 
        [key: string]: string 
    }
    user_uuid: string
    year: number
    team_number: number
    match_number: number
    match_type: string
    event_code: string
    synced: boolean
}

//     Pit Scouting table
export interface PitScoutingAnswer {
    uuid: string
    field_uuid: string
    value: string | number | boolean
    username: string
    created_at: string
}
export interface PitScoutingData {
    uuid: string
    answers: PitScoutingAnswer[]
    nickname: string | null
    team_number: number
    year: number
    event_code: string
    synced: boolean
}

//     Files table
export interface File {
    uuid: string
    data: File
    url: string
    synced: boolean
}

// Create DB
export class OpenScoutingDB extends Dexie {
    season!: Dexie.Table<Season>;
    fields!: Dexie.Table<ScoutingField>;
    game_piece!: Dexie.Table<GamePiece>;
    event!: Dexie.Table<Event>;
    match_scouting!: Dexie.Table<MatchScoutingData>;
    pit_scouting!: Dexie.Table<PitScoutingData>;
    files!: Dexie.Table<File>;

    constructor() {
        super('open-scouting');

        this.version(1).stores({
            match_scouting: "&uuid, data, user_uuid, year, team_number, match_number, match_type, event_code, event_name, event_type, event_city, event_country, event_start_date, event_end_date, synced",
            season_data: "$year, fields, game_pieces, pit_scouting_questions, fetch_time",
            event: "&uuid, year, event_code, name, type, city, country, start_date, end_date, week, custom, fetch_time",
            pit_scouting: "&uuid, answers, nickname, team_number, year, event_code, event_name, event_type, event_city, event_country, event_start_date, event_end_date, synced",
            files: "&uuid, data, url, synced"
        });
        // Delete entire season_data table when changing to support uuid as primary key
        // Then sync will re-fetch the items from the server
        this.version(2).stores({
            season_data: null
        });
        this.version(3).stores({
            season_data: "&uuid, year, fields, game_pieces, pit_scouting_questions, fetch_time"
        });

        // Delete entire season_data when adding name and active field
        // Then sync will re-fetch the items from the server
        this.version(4).stores({
            season_data: null
        });
        this.version(5).stores({
            season_data: "&uuid, year, name, fields, game_pieces, pit_scouting_questions, active, fetch_time"
        });

        // v2.3.0
        // Remove event data from match_scouting and pit_scouting, to be replaced with event_code
        // The server will load event data itself as needed
        this.version(6).stores({
            match_scouting: "&uuid, data, user_uuid, year, team_number, match_number, match_type, event_code, synced",
            pit_scouting: "&uuid, answers, nickname, team_number, year, event_code, synced"
        }).upgrade(async (transaction) => {
            await transaction.table("match_scouting").toCollection().modify(item => {
                delete item.event_name;
                delete item.event_type;
                delete item.event_city;
                delete item.event_country;
                delete item.event_start_date;
                delete item.event_end_date;
            });
            await transaction.table("pit_scouting").toCollection().modify(item => {
                delete item.event_name;
                delete item.event_type;
                delete item.event_city;
                delete item.event_country;
                delete item.event_start_date;
                delete item.event_end_date;
            });
        });

        // v2.3.0
        // Remove season_data
        // Add season and fields
        this.version(7).stores({
            season_data: null,
            season: "&uuid, year, name, active, fetch_time",
            fields: "&uuid, season_uuid, organization_uuid, parent_uuid, name, description, scouting_type, field_type, stat_type, game_piece_uuid, required, options, order, archived",
            game_piece: "&uuid, season_uuid, name, fetch_time"
        });

        this.season = this.table('season');
        this.fields = this.table('fields');
        this.game_piece = this.table('game_piece');
        this.event = this.table('event');
        this.match_scouting = this.table('match_scouting');
        this.pit_scouting = this.table('pit_scouting');
        this.files = this.table('files');
    }
}

export const db = new OpenScoutingDB();