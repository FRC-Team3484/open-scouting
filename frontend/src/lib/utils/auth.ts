import { browser } from "$app/environment";
import { meAuthMeGet } from "$lib/api/auth/auth";
import type { UserMeResponse } from "$lib/api/model";
import { writable, type Writable } from "svelte/store";

interface UserData extends UserMeResponse {
    loading: boolean
}

let user: Writable<UserData> = writable({
    authenticated: false,
    user: null,
    settings: null,
    loading: true
});

/**
 * Authenticates the user and updates the user store
 */
async function authenticate() {
    // Remove legacy token from local storage
    if (browser && localStorage.getItem("access_token")) {
        localStorage.removeItem("access_token");
    }
    
    await meAuthMeGet().then((response) => {
        if (response.status === 200) {
            user.set({
                authenticated: response.data.authenticated,
                user: response.data.user,
                settings: response.data.settings,
                loading: false
            })
        } else {
            user.set({
                authenticated: false,
                user: null,
                settings: null,
                loading: false
            })
        }
    }).catch(() => {
        user.set({
            authenticated: false,
            user: null,
            settings: null,
            loading: false
        })
    });
}

export { type UserData, user, authenticate }