import Dexie from 'dexie';

// Interfaces for tables
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
    event_name: string
    event_type: string
    event_city: string
    event_country: string
    event_start_date: string
    event_end_date: string
    synced: boolean
}
export interface SeasonMatchScoutingField {
    uuid: string
    name: string
    description: string
    field_type: string
    stat_type: string
    game_piece_uuid: string | null
    required: boolean
    options: {
        choices: {
            id: string
            name: string
        }[]        
        default: number
        maximum: number
        minimum: number
    }
    order: number
    organization_id: string
    fields: SeasonMatchScoutingField[]
}
export interface SeasonGamePiece {
    uuid: string
    season: string // uuid
    name: string
    created_at: Date
}
export interface SeasonPitScoutingQuestion {
    uuid: string
    season: string // uuid
    name: string
    description: string
    required: boolean
    field_type: string
    options: {
        choices: {
            id: string
            name: string
        }[]
    }
    order: number
    organization: string | null // uuid
    created_at: Date
}
export interface Season {
    uuid: string
    year: number
    fields: SeasonMatchScoutingField[]
    game_pieces: SeasonGamePiece[]
    pit_scouting_questions: SeasonPitScoutingQuestion[]
    fetch_time: Date
}
// Create a version of Season without recursive fields to keep dexie from being unhappy
export interface SeasonStored
    extends Omit<Season, "fields"> {
    fields: any[];
}
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
    nickname: string
    team_number: number
    year: number
    event_code: string
    event_name: string
    event_type: string
    event_city: string
    event_country: string
    event_start_date: string
    event_end_date: string
    synced: boolean
}
export interface File {
    uuid: string
    data: File
    url: string
    synced: boolean
}

// Create DB
export class OpenScoutingDB extends Dexie {
    match_scouting!: Dexie.Table<MatchScoutingData>;
    season_data!: Dexie.Table<SeasonStored>;
    event!: Dexie.Table<Event>;
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

        this.match_scouting = this.table('match_scouting');
        this.season_data = this.table('season_data');
        this.event = this.table('event');
        this.pit_scouting = this.table('pit_scouting');
    }
}

export const db = new OpenScoutingDB();