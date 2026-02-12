<script lang="ts">
    import { onMount } from "svelte";
	import { liveQuery } from "dexie";
	import { CircleNotch } from "phosphor-svelte";

	import { db } from "$lib/utils/db";
	import { validateTokenOnline } from "$lib/utils/user";
	import PageContainer from "$lib/components/layout/PageContainer.svelte";
	import AddPit from "$lib/components/pit_scouting/AddPit.svelte";
	import Header from "$lib/components/pit_scouting/Header.svelte";
	import Pit from "$lib/components/pit_scouting/Pit.svelte";
	import SyncManager from "$lib/components/pit_scouting/SyncManager.svelte";
	import PitStatus from "$lib/components/pit_scouting/PitStatus.svelte";
	import { getSeasonsSeasonsGet } from "$lib/api/seasons/seasons";

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

    async function get_season_uuid(year: string) {
        await getSeasonsSeasonsGet().then((response) => {
            season_uuid = response.data.find((season) => season.year == year).uuid
        })
    }

    let pits = liveQuery(
        () => db.pit_scouting
            .filter(pit => pit.year === event_data.year && pit.event_code === event_data.event_code)
            .sortBy("team_number")
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

        await get_season_uuid(year);
        get_pit_questions();

        user = await validateTokenOnline();
    });
</script>

<PageContainer>
    <Header bind:event_data={event_data}/>
    {#if year && season_uuid && event_data.year !== 0}
        <div class="flex flex-col gap-4 items-center">
            <PitStatus pits={$pits} pit_questions={pit_questions} />

            {#each ($pits || []) as pit}
                <Pit pit={pit} pit_questions={pit_questions} user={user} show_avatar={false} />
            {/each}

            <AddPit event_data={event_data} />
        </div>

    {:else}
        <CircleNotch weight="bold" class="animate-spin md:!w-6 md:!h-6 !w-4 !h-4" />
    {/if}

    <SyncManager eventData={event_data} seasonUuid={season_uuid} />
</PageContainer>
