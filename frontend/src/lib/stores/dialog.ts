import { writable } from "svelte/store";

export const addFieldDialogOpen = writable(false);
export const addFieldParentUuid = writable("");
export const addFieldEditData = writable({});

export const addSectionDialogOpen = writable(false);
export const addSectionParentUuid = writable("");
