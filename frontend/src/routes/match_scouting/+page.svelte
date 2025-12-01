<script lang="ts">
	import MatchScoutingFields from "$lib/components/generic/MatchScoutingFields.svelte";
	import PageContainer from "$lib/components/layout/PageContainer.svelte";
	import Header from "$lib/components/match_scouting/Header.svelte";
	import { apiFetch } from "$lib/utils/api";
	import { onMount } from "svelte";

    let season_uuid: string = "";

    

    function get_season_uuid(year: string) {
        apiFetch(`/seasons`).then((seasons) => {
            season_uuid = seasons.find((season) => season.year == year).uuid
        })
    }

    onMount(async () => {
        let url = new URL(window.location.href);
        let year = url.searchParams.get("year");
        if (!year) {
            throw new Error("season_uuid is required as a URL parameter");
        }

        get_season_uuid(year);
        
    })
</script>

<PageContainer>
    <Header />
    <MatchScoutingFields season_uuid={season_uuid} editable={false} />
</PageContainer>
