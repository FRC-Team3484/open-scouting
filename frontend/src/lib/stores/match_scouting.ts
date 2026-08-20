import { writable, type Writable } from "svelte/store";

export const matchScoutingTeamNumber: Writable<number> | Writable<null> = writable(null);
export const matchScoutingMatchNumber: Writable<number> | Writable<null> = writable(null);
export const matchScoutingTeamPosition: Writable<string> | Writable<null> = writable(null);