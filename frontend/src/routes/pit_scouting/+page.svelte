<!-- 
The pit scouting page. Loads the pits from the local database, then renders a Pit component for each pit.

Allows for creating new pits, and includes a section for viewing the progress of each pit.
-->
<script lang="ts">
    import { onMount } from "svelte";
	import { liveQuery, type Observable } from "dexie";
	import { CircleNotchIcon } from "phosphor-svelte";
	import { page } from "$app/state";
	import { replaceState } from "$app/navigation";

	import { db, type Event, type PitScoutingData, type SeasonPitScoutingQuestion } from "$lib/utils/db";
	import { getUser } from "$lib/utils/user";
	import PageContainer from "$lib/components/layout/PageContainer.svelte";
	import AddPit from "$lib/components/pit_scouting/AddPit.svelte";
	import Header from "$lib/components/pit_scouting/Header.svelte";
	import Pit from "$lib/components/pit_scouting/Pit.svelte";
	import SyncManager from "$lib/components/pit_scouting/SyncManager.svelte";
	import PitStatus from "$lib/components/pit_scouting/PitStatus.svelte";
	import { type UserResponse } from "$lib/api/model";


    let season_uuid: string = $state("");
    let year: string | null = $state(null);

    let event_data: Event | null = $state(null);

    let pit_questions: SeasonPitScoutingQuestion[] = $state([]);

    let user: UserResponse | null = getUser();

    let scrolledFromUrl: boolean = $state(false);
    let scrolledFromUrlTeam: number | null = $state(null);

    let pits: Observable<PitScoutingData[]> = $derived.by(() => {
        if (!event_data) {
            return liveQuery(() => Promise.resolve([]));
        }

        return liveQuery(() =>
            db.pit_scouting
                .filter(
                    pit =>
                        pit.year === event_data.year &&
                        pit.event_code === event_data.event_code
                )
                .sortBy("team_number")
        );
    });

    /**
     * Get the season uuid for the given year
     *       
     * @param year The year to get the season uuid for
     */
    async function get_season_uuid(year: string) {
        await db.season_data.toArray().then((seasons) => {
            const season = seasons.find((season) => season.year.toString() == year);
            if (season) {
                season_uuid = season.uuid;
            } else {
                console.warn("Failed to get season");
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
     * Scroll to the team with the given team number, or the add pit section
     * 
     * @param team_number The team number to scroll to, or "addPit"
     */
    function scrollToTeam(team_number: number | "addPit") {
        const element = document.querySelector(`[data-teamNumber="${team_number}"]`);
        if (element) {
            element.scrollIntoView({ behavior: "smooth" });

            const params = new URLSearchParams(page.url.search);
            if (params.get("pit") === team_number) return;

            // Wait a bit before updating the URL, so that the interaction observer doesn't overwrite it
            setTimeout(() => {
                params.set("pit", team_number.toString());
                replaceState(`?${params}`, {});
            }, 500);

        }
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
    }); 

    /**
     * Scroll to the team with the given team number stored in the URL params, 
     * either from the interaction observer, or by clicking a team in the PitStatus component
     */
    $effect(() => {
        if (!$pits?.length || scrolledFromUrl) return;

        queueMicrotask(() => {
            const team = page.url.searchParams.get("pit");
            if (!team || team === "addPit") return;

            scrollToTeam(parseInt(team));

            scrolledFromUrl = true;
            scrolledFromUrlTeam = parseInt(team);
        });
    });
</script>

<PageContainer disableSleep>
    <Header bind:event_data={event_data}/>
    {#if year && season_uuid && event_data && event_data.year !== 0}
        <div class="flex flex-col gap-4 items-center">
            <PitStatus pits={$pits} pit_questions={pit_questions} scrollToTeam={scrollToTeam} />

            {#if $pits && $pits.length > 0}
                {#each ($pits) as pit}
                    <Pit pit={pit} pit_questions={pit_questions} user={user} show_avatar={false} expanded={scrolledFromUrl && scrolledFromUrlTeam === pit.team_number} />
                {/each}
            {:else}
                <p>No pits found</p>
            {/if}

            <AddPit event_data={event_data} />
        </div>

        <SyncManager eventData={event_data} seasonUuid={season_uuid} />
    {:else}
        <CircleNotchIcon weight="bold" class="animate-spin md:w-6! md:h-6! w-4! h-4!" />
    {/if}
</PageContainer>
