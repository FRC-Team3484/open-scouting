import { compare } from "semver-ts";
import { menuState } from "$lib/stores/menu";
import { changelogDialogOpen, changelogDialogVersion } from "$lib/stores/dialog"
import { theBlueAllianceApiFetch } from "./api";
import { db } from "./db";

import { getSeasonsSeasonsGet } from "$lib/api/seasons/seasons";
import { getSeasonFieldsFieldsSeasonSeasonUuidGet } from "$lib/api/match-scouting-fields/match-scouting-fields"
import { getSeasonGamepiecesGamepiecesSeasonSeasonUuidGet } from "$lib/api/gamepieces/gamepieces"
import { getPitFieldsPitsFieldsSeasonUuidGet, submitPitPitsSubmitSeasonUuidTeamNumberPost, getPitsPitsGetSeasonUuidPost } from "$lib/api/pit-scouting/pit-scouting"
import { getCustomEventsEventCustomSeasonUuidGet } from "$lib/api/events/events"
import { submitMatchScoutingScoutingSubmitPost } from "$lib/api/match-scouting/match-scouting";
import type { SeasonResponse, GamepieceResponse, PitFieldResponse, EventResponse, MatchScoutingRequest, SubmitPitFieldAnswerRequest, GetPitsForSeasonRequest, BodyUploadImageUploadImagePost, UploadImageUploadImagePostParams } from "$lib/api/model";
import { getServerStatusStatusGet } from "$lib/api/generic/generic";
import { browser } from "$app/environment";
import { VERSION } from "./constants";
import { uploadImageUploadImagePost } from "$lib/api/uploads/uploads";
import { get } from "svelte/store";

/**
 * Checks if syncing is enabled by the user
 * 
 * @returns True if syncing is enabled
 */
function isSyncingEnabled(): boolean {
    if (get(syncStatus) === false) {
        console.warn("Syncing is disabled by user");
        return false;
    } else {
        return true;
    }
}

/**
 * Fetches season data and stores it locally
 * 
 * For each season, fetch the match scouting fields and game pieces, 
 *    and store them using Dexie for later use
 */
async function fetchSeasonData() {
    if (!isSyncingEnabled()) return;

    const seasonsResponse: Array<SeasonResponse> = (await getSeasonsSeasonsGet()).data;

    for (const season of seasonsResponse) {
        const fieldData = (await getSeasonFieldsFieldsSeasonSeasonUuidGet(season.uuid)).data;
        let gamePieceData: Array<GamepieceResponse> = [];
        let pitData: Array<PitFieldResponse> = [];

        const gamePieceRequest = await getSeasonGamepiecesGamepiecesSeasonSeasonUuidGet(season.uuid);
        if (gamePieceRequest.status !== 422) {
            gamePieceData = gamePieceRequest.data;
        }

        const pitRequest = await getPitFieldsPitsFieldsSeasonUuidGet(season.uuid);
        if (pitRequest.status !== 422) {
            pitData = pitRequest.data;
        }

        await db.season_data.put({
            uuid: season.uuid,
            year: season.year,
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
    if (!isSyncingEnabled()) return;

    const seasonsResponse: Array<SeasonResponse> = (await getSeasonsSeasonsGet()).data;

    for (const season of seasonsResponse) {
        const eventsResponse = await theBlueAllianceApiFetch(`/events/${season.year}`);

        for (const event of eventsResponse) {
            await db.event.put({
                uuid: event.key,
                year: season.year,
                event_code: event.event_code,
                name: event.name,
                type: event.event_type_string,
                city: event.city,
                country: event.country,
                start_date: event.start_date,
                end_date: event.end_date,
                week: event.week,
                custom: false,
                fetch_time: new Date()
            });
        }

        const customEventsRequest = await getCustomEventsEventCustomSeasonUuidGet(season.uuid);
        let customEventsData: Array<EventResponse> = [];
        if (customEventsRequest.status !== 422) {
            customEventsData = customEventsRequest.data;
        }

        for (const event of customEventsData) {
            await db.event.put({
                uuid: event.uuid,
                year: season.year,
                event_code: event.event_code,
                name: event.name,
                type: event.type,
                city: event.city,
                country: event.country,
                start_date: event.start_date,
                end_date: event.end_date,
                week: null,
                custom: true,
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
 * Checks if there are any unsynced files
 * 
 * @returns boolean
 */
async function isUnsyncedFiles() {
    return (await db.files.filter(m => m.synced === false).toArray()).length > 0;
}

/**
 * Pushes unsynced match scouting data to the backend
 * 
 * 
 */
async function pushMatchScoutingData() {
    if (!isSyncingEnabled()) return;

    const unsynced = await db.match_scouting.filter(m => m.synced === false).toArray();

    if (unsynced.length > 0) {
        menuState.set({
            state: "loading",
            status: "Uploading match scouting data...",
            close: false
        });

        for (const match of unsynced) {
            const body: MatchScoutingRequest = {
                submission_uuid: match.uuid,
                fields: match.data,
                user_uuid: match.user_uuid,
                year: match.year,
                team_number: match.team_number,
                match_number: match.match_number,
                match_type: match.match_type,
                event_code: match.event_code,
                event_name: match.event_name,
                event_type: match.event_type,
                event_city: match.event_city,
                event_country: match.event_country,
                event_start_date: match.event_start_date,
                event_end_date: match.event_end_date
            }

            await submitMatchScoutingScoutingSubmitPost(body).then((data) => {
                if (data.status === 200) {
                    db.match_scouting.update(match.uuid, { synced: true });
                }
            });
        }

        menuState.set({
            state: "ready",
            status: "Match scouting data uploaded!",
            close: true
        });
    } else {
        // console.log("No unsynced match scouting data");
    }
}

/**
 * Pushes unsynced pit scouting data to the backend, based on the event
 * 
 * @param event_data The event data
 */
async function pushPitScoutingData(event_data, season_uuid) {
    if (!isSyncingEnabled()) return;

    const unsyncedPits = await db.pit_scouting.filter(
        p => p.synced === false && 
        p.event_code === event_data.event_code && 
        p.year === parseInt(event_data.year)
    ).toArray();

    if (unsyncedPits.length > 0) {
        menuState.set({
            state: "loading",
            status: "Uploading pit scouting data...",
            close: false
        });

        for (const pit of unsyncedPits) {
            const body: SubmitPitFieldAnswerRequest = {
                uuid: pit.uuid,
                season_uuid: season_uuid,
                team_number: pit.team_number,
                event_code: event_data.event_code,
                event_name: event_data.event_name,
                event_type: event_data.event_type,
                event_city: event_data.event_city,
                event_country: event_data.event_country,
                event_start_date: event_data.event_start_date,
                event_end_date: event_data.event_end_date,
                answers: pit.answers || [],
                nickname: pit.nickname || ""
            }

            await submitPitPitsSubmitSeasonUuidTeamNumberPost(season_uuid, pit.team_number, body).then((data) => {
                if (data.status === 200) {
                    db.pit_scouting.update(pit.uuid, { synced: true });
                }
            });

            console.log("Pit scouting data uploaded", pit.uuid);
        }

        menuState.set({
            state: "ready",
            status: "Pit scouting data uploaded!",
            close: true
        });
    } else {
        // console.log("No unsynced pit scouting data");
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
    if (!isSyncingEnabled()) return;

    const body: GetPitsForSeasonRequest = {
        season_uuid: season_uuid,
        event_code: event_data.event_code,
        event_name: event_data.event_name,
        event_type: event_data.event_type,
        event_city: event_data.event_city,
        event_country: event_data.event_country,
        event_start_date: event_data.event_start_date,
        event_end_date: event_data.event_end_date,
        event_custom: event_data.event_custom
    }

    const pitDataRequest = (await getPitsPitsGetSeasonUuidPost(season_uuid, body)).data;

    for (const pit of pitDataRequest) {
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
 * Pushes files to the backend
 */
async function pushFiles() {
    if (!isSyncingEnabled()) return;

    let files = await db.files.filter(f => f.synced === false).toArray();

    for (const file of files) {
        const params: UploadImageUploadImagePostParams = {
            file_uuid: file.uuid
        }
        const body: BodyUploadImageUploadImagePost = {
            file: file.data
        }

        await uploadImageUploadImagePost(body, params).then(async (data) => {
            if (data.status === 200) {
                await db.files.delete(file.uuid);
            }
        });

    }
}

async function getServerStatus() {
    if (!browser) return;
    if (!isSyncingEnabled()) return;

    await getServerStatusStatusGet().then((response) => {
        if (response.data) {
            const server_version: string | null = response.data.version;

            if (server_version !== null) {
                if (compare(server_version, VERSION) === 0) {
                    console.info(`Open Scouting ${VERSION} is up to date`);

                } else if (compare(server_version, VERSION) === 1) {
                    console.warn(`Open Scouting Client ${VERSION} is out of date. Server version is ${server_version}`);

                } else if (compare(server_version, VERSION) === -1) {
                    console.warn(`Open Scouting Client ${VERSION} is incompatible with the server. Server version is ${server_version}`);
                }

                const lastOpenedVersion = localStorage.getItem("version");
                const showChangelogs = localStorage.getItem("showChangelogs");

                if (lastOpenedVersion === null || lastOpenedVersion != VERSION) {
                    localStorage.setItem("version", VERSION);
                    if (showChangelogs === "true" || showChangelogs === null) {
                        changelogDialogOpen.set(true);
                        changelogDialogVersion.set(VERSION);
                    }
                }

                if (showChangelogs === null) {
                    localStorage.setItem("showChangelogs", "true");
                }
            } else {
                console.error("Could not get server version");
                return false;
            }

            return true;
        }
        
    }).catch((error) => {
        console.error(error);
        return false;
    });
}

/**
 * If the locally stored data is out of date, download it and ask the menu to show that status
 */
async function main() {
    if (!isSyncingEnabled()) return;

    setTimeout(() => {
        getServerStatus();
    }, 500);

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

        if (await isUnsyncedFiles()) {
            menuState.set({
                state: "loading",
                status: "Syncing files...",
                close: false
            });

            await pushFiles();
            console.log("Synced files");
        }

        menuState.set({
            state: "ready",
            status: "Data is up to date!",
            close: true
        });
    }

    await pushMatchScoutingData();
}

main().catch((error) => console.error(error));

export { fetchSeasonData, fetchEventData, isOldData, pushMatchScoutingData, pushPitScoutingData, fetchPitScoutingData, pushFiles }