import { PUBLIC_FAST_API_URL } from "$env/static/public";
import { apiFetch } from "./api";

async function validateTokenOnline() {
    const token = localStorage.getItem("access_token");
    if (!token) {
        console.log("No token found");
        return;
    };

    const res = await fetch(PUBLIC_FAST_API_URL + "/auth/validate", {
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
    return await apiFetch("/users/me/get_settings", {
        token: localStorage.getItem("access_token")
    })
}

async function setUserSettings(settings) {
    await apiFetch("/users/me/update_settings", {
        method: "POST",
        data: settings,
        token: await localStorage.getItem("access_token")
    });
}

async function getUserSetting(key) {
    const settings = await getUserSettings();
    return settings[key];
}

async function setUserSetting(key, value) {
    let settings = await getUserSettings();
    console.log(settings);
    settings[key] = value;
    console.log(settings);
    await setUserSettings(settings);
}

export { validateTokenOnline, signOut, getUserSettings, setUserSettings, getUserSetting, setUserSetting };