<!-- 
@component
Handles the filters for the regular data view page

Props:
    - `filters` (`Filters`) - The current filters from the parent
-->
<script lang="ts">
	import { onMount } from "svelte";
	import { BuildingsIcon, CalendarIcon, FadersIcon, InfoIcon, PlusCircleIcon, UserIcon, XIcon } from "phosphor-svelte";
	import { toast } from "svelte-sonner";

    import * as Card from "$lib/components/ui/card/index.js";
    import * as Select from "$lib/components/ui/select/index.js";
    import * as AlertDialog from "$lib/components/ui/alert-dialog/index.js";
	import Button from "$lib/components/ui/button/button.svelte";

	import { db } from "$lib/utils/db";
	import type { Filters as EventListFilters } from "$lib/components/generic/event_list/EventList.svelte";
	import { getSeasonsSeasonsGet } from "$lib/api/seasons/seasons";
	import type { GetDataFiltersDataFiltersGetParams, SeasonResponse } from "$lib/api/model";
	import { getDataFiltersDataFiltersGet } from "$lib/api/data/data";
	import BaseDialog from "$lib/components/generic/dialogs/BaseDialog.svelte";
	import FilterList from "../FilterList.svelte";
	import EventList from "$lib/components/generic/event_list/EventList.svelte";
	import type { Filters } from "../../../../routes/data/+page.svelte";
    

    interface Props {
        filters: Filters
    }
    let { filters = $bindable() }: Props = $props();

    let seasons: SeasonResponse[] = $state([]);
    let seasons_label = $derived(seasons.find((s) => s.year === filters.year)?.name ?? "Select Year");
    let events = $state([]);
    let teams = $state([]);
    let selectedEvents = $state([]);
    let eventListOpen = $state(false);
    let hydratedFromUrl = $state(false);

    const eventListDefaultFilters: EventListFilters = { showPast: true, showFavorites: false, showCustom: false, showSelected: false, eventType: [] };

    /**
     * Load all seasons from the server
     * 
     * TODO: Should this fetch the local seasons instead?
     */
    async function loadSeasons() {
        seasons = (await getSeasonsSeasonsGet()).data;

        if (!filters.year && seasons.length > 0) {
            const activeSeason = seasons.find((s) => s.active);
            filters.year = activeSeason ? activeSeason.year : seasons[0]?.year;
        }
    }

    /**
     * Based on the current filters, load what other filters are allowed
     */
    async function loadFilters() {
        if (!filters.year) return;

        const params: GetDataFiltersDataFiltersGetParams = {
            year: filters.year,
            event_codes: "",
            team_numbers: ""
        }

        if (filters.event_codes.length) {
            params.event_codes = filters.event_codes.join(",");
        }

        if (filters.team_numbers.length) {
            params.team_numbers = filters.team_numbers.join(",");
        }

        // TODO: This needs a proper response schema
        await getDataFiltersDataFiltersGet(params).then((response) => {
            if (response.status === 200) {
                events = response.data.events;
                teams = response.data.teams;
            } else {
                toast.error("Error loading filters", { duration: 5000 });
            }
        }).catch(() => {
            toast.error("Error loading filters", { duration: 5000 });
        });
    }

    onMount(async () => {
        await loadSeasons();
    });

    /**
     * When filters change, get the new list of allowed filters
     */
    $effect(() => {
        filters.year;
        filters.event_codes;
        filters.team_numbers;

        loadFilters();
    });

    /**
     * Hydrate the event list with the correctly selected event when the page loads
     */
    $effect(() => {
        const year = filters.year;
        const codes = filters.event_codes;

        if (!events.length || !codes.length) return;
        if (hydratedFromUrl) return;

        (async () => {
            const results = await db.event
                .where("year")
                .equals(year)
                .toArray();

            selectedEvents = results.filter(e =>
                codes.includes(e.event_code)
            );

            hydratedFromUrl = true;
        })();
    });

    /**
     * When an event is selected by the event list, update the event code filters accordingly
     */
    $effect(() => {
        filters.event_codes = selectedEvents.map(e => e.event_code);
    });
</script>

<Card.Root class="mt-4 min-w-64">
    <Card.Content>
        <div class="flex flex-col gap-2">
            <div class="flex flex-row gap-2 items-center">
                <FadersIcon weight="bold" size={24} />
                <p class="text-lg font-bold"> Filters</p>

                <AlertDialog.Root>
                    <AlertDialog.Trigger>
                        <Button size="icon-sm" variant="outline"><InfoIcon weight="bold" /></Button>
                    </AlertDialog.Trigger>

                    <AlertDialog.Content>
                        <AlertDialog.Title>Filters</AlertDialog.Title>
                        <AlertDialog.Description>Filter the loaded match scouting data by year, events, and teams</AlertDialog.Description>
                        <AlertDialog.Description>
                            Avaliable filters are based on the other filters. For example, if two events are selected, you can only filter for teams that have data at both of those events.
                        </AlertDialog.Description>

                        <AlertDialog.Footer>
                            <AlertDialog.Cancel type="button">Close</AlertDialog.Cancel>
                        </AlertDialog.Footer>
                    </AlertDialog.Content>
                </AlertDialog.Root>
            </div>

            <div class="flex flex-col gap-2">
                <div class="flex flex-col gap-2">
                    <div class="flex flex-row gap-1 items-center">
                        <CalendarIcon weight="bold" size={16} />
                        <p>Year</p>
                    </div>
                    <Select.Root type="single" bind:value={filters.year}>
                        <Select.Trigger>{seasons_label}</Select.Trigger>

                        <Select.Content>
                            <Select.Label>Seasons</Select.Label>
                            {#each seasons as season}
                                <Select.Item value={season.year} label={season.name} />
                            {/each}
                        </Select.Content>
                    </Select.Root>
                </div>

                <div class="flex flex-col gap-2">
                    <div class="flex flex-row gap-1 items-center">
                        <BuildingsIcon weight="bold" size={16} />
                        <p>Events</p>
                    </div>

                    <div class="flex flex-row gap-2 max-h-screen max-w-screen flex-wrap items-center">
                        {#each selectedEvents as event}
                            <div class="flex flex-row gap-1 items-center">
                                <Button variant="outline" onclick={() => selectedEvents = selectedEvents.filter((e) => e.event_code !== event.event_code)}><XIcon weight="bold" /> {event.name}</Button>
                            </div>
                        {/each}
                        <Button variant="outline" class="w-auto" onclick={() => eventListOpen = true}><PlusCircleIcon weight="bold" /> Add</Button>
                    </div>
                </div>

                <div class="flex flex-col gap-2">
                    <div class="flex flex-row gap-1 items-center">
                        <UserIcon weight="bold" size={16} />
                        <p>Teams</p>
                    </div> 

                    <FilterList filterTitle="Add Team Filter" values={teams.map((t) => t.team_number.toString())} labels={teams.map((t) => t.team_number.toString())} bind:selected={filters.team_numbers} />
                </div>
            </div>
        </div>
    </Card.Content>
</Card.Root>

<BaseDialog title="Event Filters" description="Filter the displayed data by event" bind:open={eventListOpen}>
    <EventList 
        year={filters.year} 
        bind:value={selectedEvents} 
        multiple={true} 
        limits={events.map((e) => e.event_code)} 
        defaultFilters={eventListDefaultFilters} 
    />
    
    <Button variant="outline" onclick={() => eventListOpen = false}>Close</Button>
</BaseDialog>