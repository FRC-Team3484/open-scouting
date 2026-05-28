<!-- 
The pit scouting page. Loads the pits from the local database, then renders a Pit component for each pit.

Allows for creating new pits, and includes a section for viewing the progress of each pit.

TODO: Add a proper interface for user
-->
<script lang="ts">
    import { onMount } from "svelte";
	import { liveQuery } from "dexie";
	import { CircleNotchIcon } from "phosphor-svelte";

	import { db, type Event, type SeasonPitScoutingQuestion } from "$lib/utils/db";
	import { validateTokenOnline } from "$lib/utils/user";
	import PageContainer from "$lib/components/layout/PageContainer.svelte";
	import AddPit from "$lib/components/pit_scouting/AddPit.svelte";
	import Header from "$lib/components/pit_scouting/Header.svelte";
	import Pit from "$lib/components/pit_scouting/Pit.svelte";
	import SyncManager from "$lib/components/pit_scouting/SyncManager.svelte";
	import PitStatus from "$lib/components/pit_scouting/PitStatus.svelte";
	import { getSeasonsSeasonsGet } from "$lib/api/seasons/seasons";

    let season_uuid: string = $state("");
    let year: string | null = $state(null);

    let event_data: Event | null = $state(null);

    let pit_questions: SeasonPitScoutingQuestion[] = $state([]);

    let user: unknown = $state(null);

    let pits = liveQuery(
        () => db.pit_scouting
            .filter(pit => pit.year === event_data.year && pit.event_code === event_data.event_code)
            .sortBy("team_number")
    );

    /**
     * Get the season uuid for the given year
     * 
     * TODO: Fetch seasons from the local database instead
     * 
     * @param year The year to get the season uuid for
     */
    async function get_season_uuid(year: string): Promise<void> {
        await getSeasonsSeasonsGet().then((response) => {
            if (response.status === 200) {
                const season = response.data.find((season) => season.year.toString() == year);
                if (season) {
                    season_uuid = season.uuid;
                }
            } else {
                console.warn("Failed to get seasons");
            }
        })
    }

    /**
     * Get pit questions for the season from the local database
     */
    async function get_pit_questions(): Promise<void> {
        const season = await db.season_data.get(season_uuid);
        pit_questions = season?.pit_scouting_questions.sort((a, b) => a.order - b.order) ?? [];
    }

    /**
     * Load the year from the URL and find it's UUID
     * 
     * Then get the pit questions and user data.
     */
    onMount(async () => {
        let url = new URL(window.location.href);
        year = url.searchParams.get("year");
        if (!year) {
            throw new Error("season_uuid is required as a URL parameter");
        }

        await get_season_uuid(year);
        await get_pit_questions();

        user = await validateTokenOnline();
    });
</script>

<PageContainer disableSleep>
    <Header bind:event_data={event_data}/>
    {#if year && season_uuid && event_data && event_data.year !== 0}
        <div class="flex flex-col gap-4 items-center">
            <PitStatus pits={$pits} pit_questions={pit_questions} />

            {#each ($pits || []) as pit}
                <Pit pit={pit} pit_questions={pit_questions} user={user} show_avatar={false} />
            {/each}

            <AddPit event_data={event_data} />
        </div>

        <SyncManager eventData={event_data} seasonUuid={season_uuid} />
    {:else}
        <CircleNotchIcon weight="bold" class="animate-spin md:w-6! md:h-6! w-4! h-4!" />
    {/if}
</PageContainer>
