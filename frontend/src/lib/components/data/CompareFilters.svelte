<script lang="ts">
    import * as Card from "$lib/components/ui/card/index.js";
    import * as Select from "$lib/components/ui/select/index.js";
    import * as AlertDialog from "$lib/components/ui/alert-dialog/index.js";
	import { Buildings, Calendar, Faders, Info, Selection, Users } from "phosphor-svelte";
	import { onMount } from "svelte";
	import FilterList from "./FilterList.svelte";
	import Button from "../ui/button/button.svelte";
	import { getSeasonsSeasonsGet } from "$lib/api/seasons/seasons";
	import type { GetDataFiltersDataFiltersGetParams, SeasonResponse } from "$lib/api/model";
	import { getDataFiltersDataFiltersGet } from "$lib/api/data/data";
	import { toast } from "svelte-sonner";
	import Separator from "../ui/separator/separator.svelte";
    
    let { filters = $bindable() } = $props();

    let seasons: SeasonResponse[] = $state([]);
    let seasons_label = $derived(seasons.find((s) => s.year === filters.year)?.name ?? "Select Year");
    let events = $state([]);
    let teams = $state([]);

    async function loadSeasons() {
        seasons = (await getSeasonsSeasonsGet()).data;

        if (!filters.year && seasons.length > 0) {
            const activeSeason = seasons.find((s) => s.active);
            filters.year = activeSeason ? activeSeason.year : seasons[0]?.year;
        }
    }

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

    $effect(() => {
        filters.year;
        filters.event_codes;
        filters.team_numbers;

        loadFilters();
    });
</script>

<Card.Root class="mt-4 min-w-64">
    <Card.Content>
        <div class="flex flex-col gap-2">
            <div class="flex flex-row gap-2 items-center">
                <Faders weight="bold" size={24} />
                <p class="text-lg font-bold"> Compare</p>

                <AlertDialog.Root>
                    <AlertDialog.Trigger>
                        <Button size="icon-sm" variant="outline"><Info weight="bold" /></Button>
                    </AlertDialog.Trigger>

                    <AlertDialog.Content>
                        <AlertDialog.Title>Compare</AlertDialog.Title>
                        <AlertDialog.Description>
                            Filter match scouting data by year, events, and teams, and compare the results
                        </AlertDialog.Description>
                        <AlertDialog.Description>
                            Avaliable filters are based on the other filters. For example, if two events are selected, you can only filter for teams that have data at both of those events.
                        </AlertDialog.Description>
                        <AlertDialog.Description>
                            You can select an event and match, and the teams that are in that match will be automatically selected.
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
                        <Calendar weight="bold" size={16} />
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

                    <div class="flex flex-row gap-2 items-center flex-wrap">
                        <FilterList filterTitle="Add Team Filter" values={teams.map((t) => t.team_number.toString())} labels={teams.map((t) => t.team_number.toString())} bind:selected={filters.team_numbers} />
                        <Button variant="outline"><Selection weight="bold" /> Select Match</Button>
                    </div>
                </div>

                <Separator orientation="horizontal" />

                <div class="flex flex-col gap-2">
                    <div class="flex flex-row gap-1 items-center">
                        <Users weight="bold" size={16} />
                        <p>Fields</p>
                    </div> 

                    <!-- <FilterList filterTitle="Add Field Filter" values={teams.map((t) => t.team_number.toString())} labels={teams.map((t) => t.team_number.toString())} bind:selected={filters.team_numbers} /> -->
                </div>
            </div>
        </div>
    </Card.Content>
</Card.Root>