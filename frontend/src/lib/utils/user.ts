import { env } from "$env/dynamic/public";
import { getUserSettingsUsersMeGetSettingsGet, updateUserSettingsUsersMeUpdateSettingsPost } from "$lib/api/auth/auth";

async function validateTokenOnline() {
    const token = localStorage.getItem("access_token");
    if (!token) {
        console.log("No token found");
        return;
    };

    const res = await fetch(env.PUBLIC_FAST_API_URL + "/auth/validate", {
        headers: { Authorization: `Bearer ${token}` },
    });

    if (res.ok) {
        const data = await res.json();
        return data;
    } else {
        return;
    }
}

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

export { validateTokenOnline, signOut, getUserSettings, setUserSettings, getUserSetting, setUserSetting };