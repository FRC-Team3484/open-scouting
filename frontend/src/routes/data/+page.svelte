<!-- 
The data page, which shows match scouting data in both all and compare view modes.

Page should be loaded like 
    /?mode=all&year=2025&event_codes=paca,ohcl&team_numbers=1234,3484
    /?mode=compare&year=2025&event_codes=paca,ohcl&team_numbers=1234,3484&fields=uuid,uuid
-->
<script module lang="ts">
    export interface Field {
        value: string
        name: string
        stat_type: string
    }
    export interface Filters {
        year: number
        event_codes: string[]
        team_numbers: string[]
    }
    export interface CompareFilters {
        year: number
        event_codes: string[]
        team_numbers: string[]
        fields: string[]
    }
</script>

<script lang="ts">
	import { onMount, tick, untrack } from "svelte";
	import { replaceState } from "$app/navigation";

	import CompareViewFilters from "$lib/components/data/compare_view/CompareFilters.svelte";
	import CompareManager from "$lib/components/data/compare_view/CompareManager.svelte";
	import DataManager from "$lib/components/data/data_view/DataManager.svelte";
	import DataViewFilters from "$lib/components/data/data_view/Filters.svelte";
	import Header from "$lib/components/data/Header.svelte";
	import PageContainer from "$lib/components/layout/PageContainer.svelte";


    let filters: Filters = $state({year: 0, event_codes: [], team_numbers: []});
    let compareFilters: CompareFilters = $state({year: 0, event_codes: [], team_numbers: [], fields: []});
    let mode: "all" | "compare" = $state("all");

    let lastYear: number | null = $state(null);
    let lastCompareYear: number | null = $state(null);

    let fields: Field[] = $state([]); // [{ name: "", value: "", stat_type: "" }, ...] from CompareManager

    /**
     * Set the URL params from the currently selected filters
     */
    function setUrlParams(): void {
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

    /**
     * Set the current filters from the URL params
     */
    function loadUrlParams(): void {
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

    /**
     * Load URL params when the component renders
     */
    onMount(() => {
        loadUrlParams();
    });
    
    /**
     * When any filters change, update the URL params
     */
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

    /**
     * Only clear data view filters when changing years if not loading the year from the URL params
     */
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

    /**
     * Only clear compare view filters when changing years if not loading the year from the URL params
     */
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
                <DataViewFilters bind:filters={filters} />

                <DataManager filters={filters} />
            </div>
        </div>
    {:else if mode === "compare"}
        <div class="lg:flex lg:flex-col lg:overflow-y-scroll">
            <div class="flex flex-col lg:flex-row lg:gap-4 lg:items-start">
                <CompareViewFilters bind:filters={compareFilters} fields={fields} />

                <CompareManager filters={compareFilters} bind:fields={fields} />
            </div>
        </div>
    {/if}
</PageContainer>
