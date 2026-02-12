<script lang="ts">
	import { getSeasonsSeasonsGet } from "$lib/api/seasons/seasons";
	import MatchScoutingFields from "$lib/components/generic/MatchScoutingFields.svelte";
	import PageContainer from "$lib/components/layout/PageContainer.svelte";
	import Header from "$lib/components/match_scouting/Header.svelte";
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

    async function get_season_uuid(year: string) {
        await getSeasonsSeasonsGet().then((response) => {
            season_uuid = response.data.find((season) => season.year == year).uuid
        })
    }

    onMount(async () => {
        let url = new URL(window.location.href);
        year = url.searchParams.get("year");
        if (!year) {
            throw new Error("season_uuid is required as a URL parameter");
        }

        await get_season_uuid(year);
    });
</script>

<PageContainer>
    <Header bind:event_data={event_data}/>
    {#if year && season_uuid && event_data.year !== 0}
        <MatchScoutingFields season_uuid={season_uuid} year={year} event_data={event_data} editable={false} />
    {:else}
        <CircleNotch weight="bold" class="animate-spin md:!w-6 md:!h-6 !w-4 !h-4" />
    {/if}
</PageContainer>
