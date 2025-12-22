<script lang="ts">
	import PitScoutingFields from "$lib/components/generic/PitScoutingFields.svelte";
	import PageContainer from "$lib/components/layout/PageContainer.svelte";
	import Header from "$lib/components/pit_scouting/Header.svelte";
	import { apiFetch } from "$lib/utils/api";
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

    let pits = $state([]);

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

        console.log(body);

        pits = await apiFetch(`/pits/get/${season_uuid}`, {
            method: "POST",
            data: body
        })

        console.log(pits);
    }

    onMount(async () => {
        let url = new URL(window.location.href);
        year = url.searchParams.get("year");
        if (!year) {
            throw new Error("season_uuid is required as a URL parameter");
        }

        get_season_uuid(year);
    });

    $effect(() => {
        if (season_uuid && event_data.year !== 0) {
            get_pits();
        }
    })
</script>

<PageContainer>
    <Header bind:event_data={event_data}/>
    {#if year && season_uuid && event_data.year !== 0}
        <PitScoutingFields season_uuid={season_uuid} year={year} event_data={event_data} editable={false} />
    {:else}
        <CircleNotch weight="bold" class="animate-spin md:!w-6 md:!h-6 !w-4 !h-4" />
    {/if}
</PageContainer>
