<script lang="ts">
	import { replaceState } from "$app/navigation";
	import CompareFilters from "$lib/components/data/CompareFilters.svelte";
	import CompareManager from "$lib/components/data/CompareManager.svelte";
	import DataManager from "$lib/components/data/DataManager.svelte";
	import Filters from "$lib/components/data/Filters.svelte";
	import Header from "$lib/components/data/Header.svelte";
	import PageContainer from "$lib/components/layout/PageContainer.svelte";
	import { onMount, tick, untrack } from "svelte";

    // Page should be loaded like 
    // /?mode=all&year=2025&event_codes=paca,ohcl&team_numbers=1234,3484
    // /?mode=compare&year=2025&event_codes=paca,ohcl&team_numbers=1234,3484&fields=uuid,uuid

    let filters = $state({year: 0, event_codes: [], team_numbers: []});
    let compareFilters = $state({year: 0, event_codes: [], team_numbers: [], fields: []});
    let mode: "all" | "compare" = $state("all");

    let lastYear: number | null = $state(null);
    let lastCompareYear: number | null = $state(null);

    let fields: Array<{ name: string; value: string }> = $state([]); // [{ name: "", value: "" }, ...]

    function setUrlParams() {
        const url = new URL(window.location.href);

        url.searchParams.set("mode", mode);

        if (mode == "all") {
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
        } else {
            if (compareFilters.year > 0) {
                url.searchParams.set("year", String(compareFilters.year));
            } else {
                url.searchParams.delete("year");
            }

            if (compareFilters.event_codes.length > 0) {
                url.searchParams.set("event_codes", compareFilters.event_codes.join(","));
            } else {
                url.searchParams.delete("event_codes");
            }
    
            if (compareFilters.team_numbers.length > 0) {
                url.searchParams.set("team_numbers", compareFilters.team_numbers.join(","));
            } else {
                url.searchParams.delete("team_numbers");
            }
    
            if (compareFilters.fields.length > 0) {
                url.searchParams.set("fields", compareFilters.fields.join(","));
            } else {
                url.searchParams.delete("fields");
            }
        }

        tick().then(() => {
            replaceState(url, {});
        });
    }

    function loadUrlParams() {
        const url = new URL(window.location.href);

        // Only allow good values, default to all if changed by user
        if (url.searchParams.get("mode") == "all") {
            mode = "all";
        } else if (url.searchParams.get("mode") == "compare") {
            mode = "compare";
        } else {
            mode = "all";
        }

        if (mode == "all") {
            const year = url.searchParams.get("year");
            if (year) filters.year = Number(year);
    
            const events = url.searchParams.get("event_codes");
            if (events) filters.event_codes = events.split(",");
    
            const teams = url.searchParams.get("team_numbers");
            if (teams) filters.team_numbers = teams.split(",");
        } else {
            const year = url.searchParams.get("year");
            if (year) compareFilters.year = Number(year);

            const events = url.searchParams.get("event_codes");
            if (events) compareFilters.event_codes = events.split(",");
    
            const teams = url.searchParams.get("team_numbers");
            if (teams) compareFilters.team_numbers = teams.split(",");
    
            const fields = url.searchParams.get("fields");
            if (fields) compareFilters.fields = fields.split(",");
        }
    }

    onMount(() => {
        loadUrlParams();
    });
    
    $effect(() => {
        filters.year;
        filters.event_codes;
        filters.team_numbers;

        compareFilters.year;
        compareFilters.event_codes;
        compareFilters.team_numbers;
        compareFilters.fields;
        
        mode;
        
        setUrlParams();
    });

    $effect(() => {
        const year = filters.year;

        if (year === 0) return;

        if (lastYear !== null && year !== lastYear) {
            untrack(() => {
                filters.event_codes = [];
                filters.team_numbers = [];
            });
        }

        lastYear = year;
    });

    $effect(() => {
        const year = compareFilters.year;

        if (year === 0) return;

        if (lastCompareYear !== null && year !== lastCompareYear) {
            untrack(() => {
                compareFilters.event_codes = [];
                compareFilters.team_numbers = [];
                compareFilters.fields = [];
            });
        }

        lastCompareYear = year;
    });
</script>

<PageContainer>
    <Header bind:mode />
    {#if mode === "all"}
        <div class="lg:flex lg:flex-col lg:overflow-y-scroll">
            <div class="flex flex-col lg:flex-row lg:gap-4 lg:items-start">
                <Filters bind:filters={filters} />

                <DataManager filters={filters} />
            </div>
        </div>
    {:else if mode === "compare"}
        <div class="lg:flex lg:flex-col lg:overflow-y-scroll">
            <div class="flex flex-col lg:flex-row lg:gap-4 lg:items-start">
                <CompareFilters bind:filters={compareFilters} fields={fields} />

                <CompareManager filters={compareFilters} bind:fields={fields} />
            </div>
        </div>
    {/if}
</PageContainer>
