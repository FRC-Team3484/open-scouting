import Dexie from 'dexie';

export class OpenScoutingDB extends Dexie {
  match_scouting! : Dexie.Table<{uuid: string, data: any, synced: boolean}, string>;
  season_data! : Dexie.Table<{year: number, fields: any, game_pieces: any}, number>;
  event! : Dexie.Table<{uuid: string, year: number, event_code: string, name: string, type: string, city: string, country: string, start_date: string, end_date: string}, string>;

  constructor() {
    super('open-scouting');
    
    this.version(1).stores({
      match_scouting: "&uuid, data, synced",
      season_data: "&year, fields, game_pieces",
      event: "&uuid, year, event_code, name, type, city, country, start_date, end_date"
    });

    this.match_scouting = this.table('match_scouting');
    this.season_data = this.table('season_data');
    this.event = this.table('event');
  }
}

export const db = new OpenScoutingDB();