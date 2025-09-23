import { PUBLIC_FAST_API_URL } from "$env/static/public";

async function validateTokenOnline() {
    const token = localStorage.getItem("auth_token");
    if (!token) {
        console.log("No token found");
        return;
    };

    const res = await fetch(PUBLIC_FAST_API_URL + "/auth/validate", {
        headers: { Authorization: `Bearer ${token}` },
    });

    if (res.ok) {
        const data = await res.json();
        console.log("Validated:", data);
    } else {
        console.log("error");
    }
}

export { validateTokenOnline };