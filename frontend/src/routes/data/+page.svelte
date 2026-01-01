<script lang="ts">
	import { pushState, replaceState } from "$app/navigation";
	import DataManager from "$lib/components/data/DataManager.svelte";
	import Filters from "$lib/components/data/Filters.svelte";
	import Header from "$lib/components/data/Header.svelte";
	import PageContainer from "$lib/components/layout/PageContainer.svelte";
	import { onMount, tick } from "svelte";

    // Page should be loaded like /?year=2025&event_codes=paca,ohcl&team_numbers=1234,3484
    let filters = $state({year: 0, event_codes: [], team_numbers: []})

    function setUrlParams() {
        const url = new URL(window.location.href);

        if (filters.year > 0) {
            url.searchParams.set("year", String(filters.year));
        } else {
            url.searchParams.delete("year");
        }

        if (filters.event_codes.length > 0) {
            url.searchParams.set("event_codes", filters.event_codes.join(","));
        } else {
            url.searchParams.delete("event_codes");
        }

        if (filters.team_numbers.length > 0) {
            url.searchParams.set("team_numbers", filters.team_numbers.join(","));
        } else {
            url.searchParams.delete("team_numbers");
        }

        tick().then(() => {
            replaceState(url, {});
        });
    }

    function loadUrlParams() {
        const url = new URL(window.location.href);

        const year = url.searchParams.get("year");
        if (year) filters.year = Number(year);

        const events = url.searchParams.get("event_codes");
        if (events) filters.event_codes = events.split(",");

        const teams = url.searchParams.get("team_numbers");
        if (teams) filters.team_numbers = teams.split(",");
    }

    onMount(() => {
        loadUrlParams();
    });
    
    $effect(() => {
        filters.year;
        filters.event_codes;
        filters.team_numbers;
        
        setUrlParams();
    });
</script>

<PageContainer>
    <Header />
    <Filters bind:filters={filters} />
    <DataManager filters={filters} />
</PageContainer>
