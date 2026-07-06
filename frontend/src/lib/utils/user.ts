import { browser } from "$app/environment";
import { page } from "$app/state";
import { getUserSettingsUsersMeGetSettingsGet, logoutAuthLogoutPost, updateUserSettingsUsersMeUpdateSettingsPost } from "$lib/api/auth/auth";
import type { UserResponse } from "$lib/api/model";
import { toast } from "svelte-sonner";

/**
 * Get user data from the page
 * 
 * Also removes legacy token from local storage
 * 
 * @returns The user data
 */
function getUser() : UserResponse | null {
    // Remove legacy token from local storage
    if (browser && localStorage.getItem("access_token")) {
        localStorage.removeItem("access_token");
    }

    return page.data.user.user;
}

/**
 * Get the user's authentication status
 * 
 * @returns True if the user is authenticated
 */
function getAuthenticationStatus(): boolean {
    return page.data.user.authenticated;
}

/**
 * Get the user's settings
 * 
 * @returns The user's settings
 */
function getSettings() {
    return page.data.user.settings;
}

/**
 * Sign the user out
 */
async function signOut() {
    await logoutAuthLogoutPost().then(async (response) => {
        if (response.status === 200) {
            toast.success("Logged out successfully.");
            window.location.href = "/";
        } else {
            toast.error("Failed to log out.");
            console.error(response);
        }
    });
}

/**
 * Get the user's settings
 * 
 * @returns The user's settings
 */
async function getUserSettings() {
    return (await getUserSettingsUsersMeGetSettingsGet()).data;
}

/**
 * Set the user's settings
 * 
 * TODO: Add types
 * 
 * @param settings The user's settings
 */
async function setUserSettings(settings) {
    await updateUserSettingsUsersMeUpdateSettingsPost(settings);
}

/**
 * Get a user setting
 * 
 * TODO: Add types
 * 
 * @param key The key of the setting
 * @returns The value of the setting
 */
async function getUserSetting(key) {
    const settings = await getUserSettings();
    return settings[key];
}

/**
 * Set a single user setting
 * 
 * TODO: Add types
 * 
 * @param key The key of the setting
 * @param value The value of the setting
 */
async function setUserSetting(key, value) {
    let settings = {};
    settings[key] = value;
    await setUserSettings(settings);
}

export { getUser, getAuthenticationStatus, getSettings, signOut, getUserSettings, setUserSettings, getUserSetting, setUserSetting };