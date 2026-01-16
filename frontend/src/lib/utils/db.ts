import Dexie from 'dexie';

export class OpenScoutingDB extends Dexie {
  match_scouting! : Dexie.Table<{uuid: string, data: any, user_uuid: string, year: number, team_number: number, match_number: number, match_type: string, event_code: string, event_name: string, event_type: string, event_city: string, event_country: string, event_start_date: string, event_end_date: string, synced: boolean}, string>;
  season_data! : Dexie.Table<{year: number, fields: any, game_pieces: any, pit_scouting_questions: any, fetch_time: Date}, number>;
  event! : Dexie.Table<{uuid: string, year: number, event_code: string, name: string, type: string, city: string, country: string, start_date: string, end_date: string, custom: boolean, fetch_time: Date}, string>;
  pit_scouting! : Dexie.Table<{uuid: string, answers: any, nickname: string, team_number: number, year: number, event_code: string, event_name: string, event_type: string, event_city: string, event_country: string, event_start_date: string, event_end_date: string, synced: boolean}, string>;

  constructor() {
    super('open-scouting');
    
    this.version(1).stores({
      match_scouting: "&uuid, data, user_uuid, year, team_number, match_number, match_type, event_code, event_name, event_type, event_city, event_country, event_start_date, event_end_date, synced",
      season_data: "&year, fields, game_pieces, pit_scouting_questions, fetch_time",
      event: "&uuid, year, event_code, name, type, city, country, start_date, end_date, custom, fetch_time",
      pit_scouting: "&uuid, answers, nickname, team_number, year, event_code, event_name, event_type, event_city, event_country, event_start_date, event_end_date, synced"
    });

    this.match_scouting = this.table('match_scouting');
    this.season_data = this.table('season_data');
    this.event = this.table('event');
    this.pit_scouting = this.table('pit_scouting');
  }
}

export const db = new OpenScoutingDB();