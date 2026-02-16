import { env } from "$env/dynamic/public";
import { writable } from "svelte/store";

export const addFieldDialogOpen = writable(false);
export const addFieldParentUuid = writable("");
export const addFieldEditData = writable({});

export const addSectionDialogOpen = writable(false);
export const addSectionParentUuid = writable("");
export const addSectionEditData = writable({});

export const addPitScoutingQuestionDialogOpen = writable(false);
export const addPitScoutingQuestionData = writable({});

export const createCustomEventDialogOpen = writable(false);

export const changelogDialogOpen = writable(false);
export const changelogDialogVersion = writable(env.PUBLIC_VERSION)