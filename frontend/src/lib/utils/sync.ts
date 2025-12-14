import { menuState } from "$lib/stores/menu";
import { apiFetch, theBlueAllianceApiFetch } from "./api";
import { db } from "./db";

/**
 * Fetches season data and stores it locally
 * 
 * For each season, fetch the match scouting fields and game pieces, 
 *    and store them using Dexie for later use
 */
async function fetchSeasonData() {
    const seasonsResponse = await apiFetch("/seasons");

    for (const season in seasonsResponse) {
        const fieldData = await apiFetch(`/fields/season/${seasonsResponse[season].uuid}`);
        const gamePieceData = await apiFetch(`/gamepieces/season/${seasonsResponse[season].uuid}`);

        await db.season_data.put({
            year: seasonsResponse[season].year,
            fields: fieldData,
            game_pieces: gamePieceData,
            fetch_time: new Date()
        });
    }
}

/**
 * Fetches event data and stores it locally
 * 
 * For each avaliable season, fetch event data from TBA
 *    and store them locally using Dexie for later use
 */
async function fetchEventData() {
    const seasonsResponse = await apiFetch("/seasons");

    for (const season in seasonsResponse) {
        const eventsResponse = await theBlueAllianceApiFetch(`/events/${seasonsResponse[season].year}`);

        for (const event in eventsResponse) {
            await db.event.put({
                uuid: eventsResponse[event].key,
                year: seasonsResponse[season].year,
                event_code: eventsResponse[event].event_code,
                name: eventsResponse[event].name,
                type: eventsResponse[event].type,
                city: eventsResponse[event].city,
                country: eventsResponse[event].country,
                start_date: eventsResponse[event].start_date,
                end_date: eventsResponse[event].end_date,
                fetch_time: new Date()
            });
        }
    }
}

/**
 * Checks if the data stored locally is out of date
 * 
 * If there's no data for either season or event data, return true
 * If stored data is older than three days, return true
 * Otherwise, return false
 * 
 * @returns boolean
 */
async function isOldData() {
    if (db.table("season_data") && db.table("event")) {
        const seasonData = await db.season_data.toArray();
        const eventData = await db.event.toArray();

        if (seasonData.length === 0 || eventData.length === 0) {
            return true;
        }

        const now = new Date();
        const threeDaysAgo = new Date(now.getTime() - 3 * 24 * 60 * 60 * 1000);

        return seasonData[0].fetch_time < threeDaysAgo || eventData[0].fetch_time < threeDaysAgo;
    } else {
        return true;
    }
}

/**
 * Pushes unsynced match scouting data to the backend
 * 
 * 
 */
async function pushMatchScoutingData() {
    const unsynced = await db.match_scouting.filter(m => m.synced === false).toArray();

    if (unsynced.length > 0) {
        menuState.set({
            state: "loading",
            status: "Uploading match scouting data...",
            close: false
        });

        for (const match of unsynced) {
            const body = new FormData();
            body.append("submission_uuid", match.uuid);
            body.append("fields", JSON.stringify(match.data));
            body.append("user_uuid", match.user_uuid);
            body.append("year", match.year);
            body.append("team_number", match.team_number);
            body.append("match_number", match.match_number);
            body.append("match_type", match.match_type);
            body.append("event_code", match.event_code);
            body.append("event_name", match.event_name);
            body.append("event_type", match.event_type);
            body.append("event_city", match.event_city);
            body.append("event_country", match.event_country);
            body.append("event_start_date", match.event_start_date);
            body.append("event_end_date", match.event_end_date);

            await apiFetch("/scouting/submit", {
                method: "POST",
                data: body
            }).then(() => {
                db.match_scouting.update(match.uuid, { synced: true });
            });
        }

        menuState.set({
            state: "ready",
            status: "Match scouting data uploaded!",
            close: true
        });
    } else {
        console.log("No unsynced data");
    }
}

/**
 * If the locally stored data is out of date, download it and ask the menu to show that status
 */
async function main() {
    if (await isOldData()) {
        console.log("Data is out of date. Fetching...");
        menuState.set({
            state: "loading",
            status: "Fetching season data...",
            close: false
        });

        await fetchSeasonData();
        console.log("Fetched season data");
        menuState.set({
            state: "loading",
            status: "Fetching event data...",
            close: false
        });

        await fetchEventData();
        console.log("Fetched event data");
        menuState.set({
            state: "ready",
            status: "Data is up to date!",
            close: true
        });
    }

    await pushMatchScoutingData();
}

main().catch((error) => console.error(error));

export { fetchSeasonData, fetchEventData, isOldData, pushMatchScoutingData }