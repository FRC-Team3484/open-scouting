<script lang="ts">
	import MatchScoutingFields from "$lib/components/generic/MatchScoutingFields.svelte";
	import PageContainer from "$lib/components/layout/PageContainer.svelte";
	import Header from "$lib/components/match_scouting/Header.svelte";
	import { apiFetch } from "$lib/utils/api";
	import { CircleNotch } from "phosphor-svelte";
	import { onMount } from "svelte";

    let season_uuid: string = $state("");
    let year: string = $state("");

    function get_season_uuid(year: string) {
        apiFetch(`/seasons`).then((seasons) => {
            season_uuid = seasons.find((season) => season.year == year).uuid
        })
    }

    onMount(async () => {
        let url = new URL(window.location.href);
        year = url.searchParams.get("year");
        if (!year) {
            throw new Error("season_uuid is required as a URL parameter");
        }

        get_season_uuid(year);
    });
</script>

<PageContainer>
    <Header />
    {#if year && season_uuid}
        <MatchScoutingFields season_uuid={season_uuid} year={year} editable={false} />
    {:else}
        <CircleNotch weight="bold" class="animate-spin md:!w-6 md:!h-6 !w-4 !h-4" />
    {/if}
</PageContainer>
