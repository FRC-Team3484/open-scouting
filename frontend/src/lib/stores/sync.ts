import { browser } from "$app/environment";
import { writable } from "svelte/store";

function localStorageStore(key: string, defaultValue: boolean) {
    if (!browser) return null;
    
	const stored =
		typeof localStorage !== "undefined"
			? localStorage.getItem(key)
			: null;

	const initial = stored !== null ? stored === "true" : defaultValue;

	const store = writable(initial);

	store.subscribe((value) => {
		localStorage.setItem(key, value ? "true" : "false");
	});

    if (typeof window !== "undefined") {
        window.addEventListener("storage", (e) => {
            if (e.key === key) {
                store.set(e.newValue === "true");
            }
        });
    }

	return store;
}

export const syncStatus = localStorageStore("syncing", true);