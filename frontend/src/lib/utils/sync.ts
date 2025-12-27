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
        const pitData = await apiFetch(`/pits/fields/${seasonsResponse[season].uuid}`);

        await db.season_data.put({
            year: seasonsResponse[season].year,
            fields: fieldData,
            game_pieces: gamePieceData,
            pit_scouting_questions: pitData,
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
        console.log("No unsynced match scouting data");
    }
}

/**
 * Pushes unsynced pit scouting data to the backend, based on the event
 * 
 * @param event_data The event data
 */
async function pushPitScoutingData(event_data, season_uuid) {
    const unsyncedPits = await db.pit_scouting.filter(
        p => p.synced === false && 
        p.event_code === event_data.event_code && 
        p.year === parseInt(event_data.year)
    ).toArray();

    console.log(unsyncedPits);

    if (unsyncedPits.length > 0) {
        menuState.set({
            state: "loading",
            status: "Uploading pit scouting data...",
            close: false
        });

        for (const pit of unsyncedPits) {
            const body = new FormData();
            body.append("event_code", event_data.event_code);
            body.append("event_name", event_data.event_name);
            body.append("event_type", event_data.event_type);
            body.append("event_city", event_data.event_city);
            body.append("event_country", event_data.event_country);
            body.append("event_start_date", event_data.event_start_date);
            body.append("event_end_date", event_data.event_end_date);

            body.append("answers", JSON.stringify(pit.answers));
            body.append("nickname", pit.nickname);

            await apiFetch(`/pits/submit/${season_uuid}/${pit.team_number}`, {
                method: "POST",
                data: body
            }).then(() => {
                db.pit_scouting.update(pit.uuid, { synced: true });
            });

            console.log("Pit scouting data uploaded", pit.uuid);
        }

        menuState.set({
            state: "ready",
            status: "Pit scouting data uploaded!",
            close: true
        });
    } else {
        console.log("No unsynced pit scouting data");
        return false;
    }
}

/**
 * Gets pit scouting data from the backend and stores it locally, based on the event
 * 
 * @param event_data The event data
 * @param season_uuid The season uuid
 */
async function fetchPitScoutingData(event_data, season_uuid) {
    const body = new FormData();
    body.append("event_code", event_data.event_code);
    body.append("event_name", event_data.event_name);
    body.append("event_type", event_data.event_type);
    body.append("event_city", event_data.event_city);
    body.append("event_country", event_data.event_country);
    body.append("event_start_date", event_data.event_start_date);
    body.append("event_end_date", event_data.event_end_date);

    const pit_data = await apiFetch(`/pits/get/${season_uuid}`, {
        method: "POST",
        data: body
    });

    console.log("Fetched pit scouting data", pit_data);

    for (const pit of pit_data) {
        const pit_in_db = await db.pit_scouting.get(pit.uuid);
        const synced = pit_in_db ? pit_in_db.synced : true;

        if (synced) {
            await db.pit_scouting.put({
                uuid: pit.uuid,
                answers: pit.answers,
                nickname: pit.nickname,
                team_number: pit.team_number,
                year: event_data.year,
                event_code: event_data.event_code,
                event_name: event_data.event_name,
                event_type: event_data.event_type,
                event_city: event_data.event_city,
                event_country: event_data.event_country,
                event_start_date: event_data.event_start_date,
                event_end_date: event_data.event_end_date,
                synced: true
            });
        } else {
            console.warn("Pit not synced: " + pit.uuid);
        }
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

export { fetchSeasonData, fetchEventData, isOldData, pushMatchScoutingData, pushPitScoutingData, fetchPitScoutingData }