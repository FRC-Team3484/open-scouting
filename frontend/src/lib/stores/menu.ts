import { writable } from "svelte/store";

export const menuState = writable({
    state: "ready",
    status: "",
    close: false
})