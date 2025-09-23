import { PUBLIC_FAST_API_URL } from "$env/static/public";

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

export { validateTokenOnline };