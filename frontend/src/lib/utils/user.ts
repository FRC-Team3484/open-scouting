import { browser } from "$app/environment";
import { page } from "$app/state";
import { getUserSettingsUsersMeGetSettingsGet, updateUserSettingsUsersMeUpdateSettingsPost } from "$lib/api/auth/auth";
import type { UserResponse } from "$lib/api/model";

function getUser() : UserResponse | null {
    // Remove legacy token from local storage
    if (browser && localStorage.getItem("access_token")) {
        localStorage.removeItem("access_token");
    }

    return page.data.user.user;
}

function getAuthenticationStatus(): boolean {
    return page.data.user.authenticated;
}

// TODO: Improve
async function signOut() {
    localStorage.removeItem("access_token");
}

async function getUserSettings() {
    return (await getUserSettingsUsersMeGetSettingsGet()).data;
}

async function setUserSettings(settings) {
    await updateUserSettingsUsersMeUpdateSettingsPost(settings);
}

async function getUserSetting(key) {
    const settings = await getUserSettings();
    return settings[key];
}

async function setUserSetting(key, value) {
    let settings = await getUserSettings();
    settings[key] = value;
    await setUserSettings(settings);
}

export { getUser, getAuthenticationStatus, signOut, getUserSettings, setUserSettings, getUserSetting, setUserSetting };