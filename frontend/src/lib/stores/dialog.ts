import { VERSION } from "$lib/utils/constants";
import { writable } from "svelte/store";

export const addFieldDialogOpen = writable(false);
export const addFieldParentUuid = writable("");
export const addFieldEditData = writable({});

export const addSectionDialogOpen = writable(false);
export const addSectionParentUuid = writable("");
export const addSectionEditData = writable({});

export const addPitScoutingQuestionDialogOpen = writable(false);
export const addPitScoutingQuestionData = writable({});

export const changelogDialogOpen = writable(false);
export const changelogDialogVersion = writable(VERSION)