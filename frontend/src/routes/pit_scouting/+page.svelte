<script lang="ts">
	import PitScoutingFields from "$lib/components/generic/PitScoutingFields.svelte";
	import PageContainer from "$lib/components/layout/PageContainer.svelte";
	import Header from "$lib/components/pit_scouting/Header.svelte";
	import Pit from "$lib/components/pit_scouting/Pit.svelte";
	import { apiFetch } from "$lib/utils/api";
	import { db } from "$lib/utils/db";
	import { validateTokenOnline } from "$lib/utils/user";
	import { liveQuery } from "dexie";
	import { CircleNotch } from "phosphor-svelte";
	import { onMount } from "svelte";

    let season_uuid: string = $state("");
    let year: string = $state("");

    let event_data = $state({
        year: 0,
        event_code: "",
        event_name: "",
        event_type: "",
        event_city: "",
        event_country: "",
        event_start_date: "",
        event_end_date: ""
    });

    let pit_questions = $state([]);

    let user = $state(null);

    function get_season_uuid(year: string) {
        apiFetch(`/seasons`).then((seasons) => {
            season_uuid = seasons.find((season) => season.year == year).uuid
        })
    }

    async function get_pits() {
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

    let pits = liveQuery(
        () => db.pit_scouting.filter(pit => pit.year === event_data.year && pit.event_code === event_data.event_code).toArray()
    );

    async function get_pit_questions() {
        const season = await db.season_data.get(parseInt(year));
        pit_questions = season?.pit_scouting_questions;
    }

    onMount(async () => {
        let url = new URL(window.location.href);
        year = url.searchParams.get("year");
        if (!year) {
            throw new Error("season_uuid is required as a URL parameter");
        }

        get_season_uuid(year);
        get_pit_questions();

        user = await validateTokenOnline();
    });

    $effect(async () => {
        if (season_uuid && event_data.year !== 0) {
            get_pits();
        }
    })
</script>

<PageContainer>
    <Header bind:event_data={event_data}/>
    {#if year && season_uuid && event_data.year !== 0 && user}
        <div class="flex flex-col gap-4 items-center">
            {#each ($pits || []) as pit}
                <Pit pit={pit} pit_questions={pit_questions} user={user} show_avatar={false} />
            {/each}
        </div>

    {:else}
        <CircleNotch weight="bold" class="animate-spin md:!w-6 md:!h-6 !w-4 !h-4" />
    {/if}
</PageContainer>
