import { TBA_API_KEY } from "$env/static/private";
import type { RequestHandler } from "./$types";

export const GET: RequestHandler = async ({ params, url }) => {
    const pathSegments = Array.isArray(params.path) ? params.path : [params.path];
    const path = pathSegments.join("/");

    const query = url.searchParams.toString();
    const fullUrl = `https://www.thebluealliance.com/api/v3/${path}${query ? "?" + query : ""}`;

    const response = await fetch(fullUrl, {
        headers: {
            "X-TBA-Auth-Key": TBA_API_KEY,
        },
    });

    const data = await response.json();

    return new Response(JSON.stringify(data), {
        headers: { "Content-Type": "application/json" },
    });
};
