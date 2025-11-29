import Dexie from 'dexie';

export class OpenScoutingDB extends Dexie {
  match_scouting! : Dexie.Table<{uuid: string, data: any, synced: boolean}, string>;

  constructor() {
    super('open-scouting');
    
    this.version(1).stores({
      match_scouting: "&uuid, data, synced"
    });

    this.match_scouting = this.table('match_scouting');
  }
}

export const db = new OpenScoutingDB();