import type { LayoutServerLoad } from "./$types";
import { meAuthMeGet } from "$lib/api/auth/auth";

export const load: LayoutServerLoad = async ({ cookies }) => {
    // Forward cookies from the client to the server
    let forwardCookies = "";
    if (cookies.get("session_id")) {
        forwardCookies = forwardCookies.concat(`session_id=${cookies.get("session_id")}`);
    }
    if (cookies.get("access_token")) {
        forwardCookies = forwardCookies.concat(`;access_token=${cookies.get("access_token")}`);
    }

    const response = await meAuthMeGet({
        headers: {
            cookie: forwardCookies
        }
    });

    if (response.status === 200) {
        cookies.set("session_id", response.headers.get("set-cookie")?.split(";")[0].split("=")[1], {
            path: "/",
            httpOnly: true,
            sameSite: "lax"
        });

        return {
            user: response.data,
        };
    }

    return {
        user: null,
    };
};