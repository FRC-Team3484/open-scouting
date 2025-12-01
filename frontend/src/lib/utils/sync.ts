import { error } from "@sveltejs/kit";
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
                uuid: crypto.randomUUID(),
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
 * If the locally stored data is out of date, download it and ask the menu to show that status
 */
async function main() {
    if (await isOldData()) {
        console.log("Data is out of date. Fetching...");
        await fetchSeasonData();
        console.log("Fetched season data");
        await fetchEventData();
        console.log("Fetched event data");
    }
}

main().catch((error) => console.error(error));

export { fetchSeasonData, fetchEventData, isOldData }