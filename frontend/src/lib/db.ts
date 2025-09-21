import Dexie from 'dexie';

export class OpenScoutingDB extends Dexie {
  constructor() {
    super('open-scouting');
    // TODO: Add tables later
  }
}

export const db = new OpenScoutingDB();