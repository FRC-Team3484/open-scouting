import { toast } from "svelte-sonner";

import { getUserSettingsUsersMeGetSettingsGet, logoutAuthLogoutPost, updateUserSettingsUsersMeUpdateSettingsPost } from "$lib/api/auth/auth";


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
 * TODO: Should this be removed?
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
 * TODO: Should this be removed?
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
 * TODO: Should this be removed?
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
 * TODO: Should this be removed?
 * 
 * @param key The key of the setting
 * @param value The value of the setting
 */
async function setUserSetting(key, value) {
    let settings = {};
    settings[key] = value;
    await setUserSettings(settings);
}

export { signOut, getUserSettings, setUserSettings, getUserSetting, setUserSetting };