<script lang="ts">
    import * as Card from "$lib/components/ui/card/index.js";
    import * as Select from "$lib/components/ui/select/index.js";
	import { apiFetch } from "$lib/utils/api";
	import { Buildings, Calendar, Faders, Users } from "phosphor-svelte";
	import { onMount } from "svelte";
	import FilterList from "./FilterList.svelte";
    
    let { filters = $bindable() } = $props();

    let seasons = $state([]);
    let seasons_label = $derived(seasons.find((s) => s.value === filters.season)?.label ?? "Select Year");
    let events = $state([]);
    let teams = $state([]);

    async function getFilterOptions() {
        const seasonsRequest = await apiFetch(`/seasons`);

        seasons = seasonsRequest.map((season) => ({
            label: `${season.year} - ${season.name}`,
            value: season.year
        }));

        filters.season = seasons[0].value;

        let filterQueryParams = new URLSearchParams(window.location.search);

        filterQueryParams.set("year", filters.season);
        if (filters.event_codes.length > 0) {
            filterQueryParams.set("event_codes", filters.event_codes.join(","));
        }
        if (filters.team_numbers.length > 0) {
            filterQueryParams.set("team_numbers", filters.team_numbers.join(","));
        }

        const filtersRequest = await apiFetch(`/data/filters?${filterQueryParams.toString()}`);
        console.log(filtersRequest);

        events = filtersRequest.events;
        teams = filtersRequest.teams;
    }

    onMount(async () => {
        getFilterOptions();
    })
</script>

<Card.Root class="mt-4">
    <Card.Content>
        <div class="flex flex-col gap-2">
            <div class="flex flex-row gap-2 items-center">
                <Faders weight="bold" size={24} />
                <p class="text-lg font-bold"> Filters</p>
            </div>

            <p class="text-muted-foreground text-left">Filter the loaded match scouting data by year, events, and teams.</p>

            <div class="flex flex-col gap-2">
                <div class="flex flex-col gap-2">
                    <div class="flex flex-row gap-1 items-center">
                        <Calendar weight="bold" size={16} />
                        <p>Year</p>
                    </div>
                    <Select.Root type="single" bind:value={filters.season}>
                        <Select.Trigger>{seasons_label}</Select.Trigger>

                        <Select.Content>
                            <Select.Label>Seasons</Select.Label>
                            {#each seasons as season}
                                <Select.Item value={season.value} label={season.label} />
                            {/each}
                        </Select.Content>
                    </Select.Root>
                </div>

                <div class="flex flex-col gap-2">
                    <div class="flex flex-row gap-1 items-center">
                        <Buildings weight="bold" size={16} />
                        <p>Events</p>
                    </div>

                    <FilterList filterTitle="Add Event Filter" values={events.map((e) => e.event_code)} labels={events.map((e) => e.event_name)} bind:selected={filters.event_codes} />
                </div>

                <div class="flex flex-col gap-2">
                    <div class="flex flex-row gap-1 items-center">
                        <Users weight="bold" size={16} />
                        <p>Teams</p>
                    </div> 

                    <FilterList filterTitle="Add Team Filter" values={teams.map((t) => t.team_number.toString())} labels={teams.map((t) => t.team_number.toString())} bind:selected={filters.team_numbers} />
                </div>
            </div>
        </div>
    </Card.Content>
</Card.Root>