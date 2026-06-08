import type { LayoutServerLoad } from "./$types";
import { meAuthMeGet } from "$lib/api/auth/auth";

export const load: LayoutServerLoad = async ({ cookies }) => {
    // TODO: What happens if one of these is missing
    // Forward cookies from the client to the server
    const forwardCookies = `session_id=${cookies.get("session_id")};access_token=${cookies.get("access_token")}`;

    const response = await meAuthMeGet({
        headers: {
            cookie: forwardCookies
        }
    });

    if (response.status === 200) {
        return {
            user: response.data,
        };
    }

    return {
        user: null,
    };
};