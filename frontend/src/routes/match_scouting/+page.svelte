<!-- 
The match scouting page. Renders the match scouting fields for a single season.

TODO: Fetch season uuid from the local database instead
-->
<script lang="ts">
	import { onMount } from "svelte";
	import { CircleNotchIcon } from "phosphor-svelte";

	import { getSeasonsSeasonsGet } from "$lib/api/seasons/seasons";
	import type { Event } from "$lib/utils/db";
	import MatchScoutingFields from "$lib/components/generic/MatchScoutingFields.svelte";
	import PageContainer from "$lib/components/layout/PageContainer.svelte";
	import Header from "$lib/components/match_scouting/Header.svelte";


    let season_uuid: string = $state("");
    let year: string | null = $state(null);

    let event_data: Event | null = $state(null);

    /**
     * Get the season uuid for the given year
     * 
     * TODO: Fetch seasons from the local database instead
     * 
     * @param year The year to get the season uuid for
     */
    async function get_season_uuid(year: string) {
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
     * Load the year from the URL and find it's UUID
     */
    onMount(async () => {
        let url = new URL(window.location.href);
        year = url.searchParams.get("year");
        if (!year) {
            throw new Error("season_uuid is required as a URL parameter");
        }

        await get_season_uuid(year);
    });
</script>

<PageContainer disableSleep>
    <Header bind:event_data={event_data}/>
    {#if year && season_uuid && event_data && event_data.year !== 0}
        <MatchScoutingFields season_uuid={season_uuid} year={parseInt(year)} event_data={event_data} editable={false} />
    {:else}
        <CircleNotchIcon weight="bold" class="animate-spin md:w-6! md:h-6! w-4! h-4!" />
    {/if}
</PageContainer>
