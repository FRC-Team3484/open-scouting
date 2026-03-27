<script lang="ts">
	import BaseDialog from "../generic/dialogs/BaseDialog.svelte";
	import { db } from "$lib/utils/db";
	import { onMount } from "svelte";
	import FilterList from "./FilterList.svelte";
	import { Buildings, CaretUpDown, CircleNotch, List } from "phosphor-svelte";
	import { theBlueAllianceApiFetch } from "$lib/utils/api";
    import * as Alert from "$lib/components/ui/alert/index.js";
	import { slide } from "svelte/transition";
	import MatchItem from "./MatchItem.svelte";
    import * as Collapsible from "$lib/components/ui/collapsible/index.js";
	import { buttonVariants } from "../ui/button";
	import { get } from "svelte/store";

    let { open = $bindable(false), year, selectMatch } = $props();

    let events = $state([]);
    let selectedEvents = $state([]);
    let matches = $state([]);
    let closestMatches = $derived.by(() => {
        const now = Date.now() / 1000;
        return matches.toSorted((a, b) => Math.abs(a.predicted_time - now) - Math.abs(b.predicted_time - now)).slice(0, 5);
    });

    let matchType = $state("qm");
    let matchNumber = $state(1);

    let matchesState: "selectEvent" | "loading" | "invalidEvent" | "ready" | "noMatches" = $state("selectEvent");

    async function getEvents() {
        events = await db.event.filter(e => e.year === year && e.custom === false).toArray();
    }

    async function getMatches(event) {
        matchesState = "loading";

        matches = await theBlueAllianceApiFetch(`/event/${year + event}/matches/simple`);

        if (matches?.Error) {
            matchesState = "invalidEvent";
        } else if (matches.length > 0) {
            matchesState = "ready";
        } else if (matches.length === 0) {
            matchesState = "noMatches";
        } else {
            matchesState = "invalidEvent";
        }
    }

    $effect(() => {
        if (selectedEvents.length > 0) {
            getMatches(selectedEvents[0]);
        }
    });

    $effect(() => {
        if (selectedEvents.length === 0) {
            matchesState = "selectEvent";
        }
    });

    $effect(() => {
        matchType;
        matchNumber = 1;
    });

    $effect(() => {
        year;

        getEvents();
    });
</script>

<BaseDialog title="Select a Match" description="Select a match at an event to automatically select the teams that played in that match." bind:open> 
    <div class="flex flex-col gap-2">
        <div class="flex flex-row gap-2 flex-wrap items-center">
            <Buildings weight="bold" size={16} />
            <p>Event</p>
            <FilterList filterTitle="Add Event Filter" values={events.map((e) => e.event_code)} labels={events.map((e) => e.name)} bind:selected={selectedEvents} onlyOne />
        </div>

        <div class="flex flex-row gap-2 flex-wrap items-center">
            {#if matchesState === "selectEvent"}
                <p class="text-muted-foreground">Select an event</p>
            {:else if matchesState === "loading"}
                <CircleNotch class="animate-spin" size={16} />
                <p class="text-muted-foreground">Getting matches...</p>
            {:else if matchesState === "invalidEvent"}
                <p class="text-muted-foreground">Invalid event</p>
            {:else if matchesState === "ready"}
            
                <div class="flex flex-col gap-2 w-full">
                    <div class="flex flex-row gap-2 flex-wrap items-center">
                        <List weight="bold" size={16} />
                        <p>Match</p>
                    </div>

                    <Collapsible.Root open={new Date(events.find((e) => e.event_code === selectedEvents[0] && e.year === year)?.end_date) < new Date(`${year}-${('0' + (new Date().getMonth() + 1)).slice(-2) + '-' + ('0' + new Date().getDate()).slice(-2)}`)}>
                        <Collapsible.Trigger class={buttonVariants({ variant: "outline", class: "w-full" })}>Matches Soon <CaretUpDown weight="bold" size={16} /></Collapsible.Trigger>

                        <Collapsible.Content>
                            <div class="flex flex-col gap-2">
                                <p class="text-sm text-muted-foreground mt-2">5 Closest Matches</p>
                                {#each closestMatches as match}
                                    <MatchItem match={match} compLevel={match.comp_level} selectMatch={selectMatch} showCompLevel />
                                {/each}
                            </div>
                        </Collapsible.Content>
                    </Collapsible.Root>

                    <Collapsible.Root open={new Date(events.find((e) => e.event_code === selectedEvents[0] && e.year === year)?.end_date) > new Date(`${year}-${('0' + (new Date().getMonth() + 1)).slice(-2) + '-' + ('0' + new Date().getDate()).slice(-2)}`)}>
                        <Collapsible.Trigger class={buttonVariants({ variant: "outline", class: "w-full" })}>All Matches <CaretUpDown weight="bold" size={16} /></Collapsible.Trigger>

                        <Collapsible.Content>
                            <div class="flex flex-col gap-2">
                                <p class="text-sm text-muted-foreground mt-2">Qualification Matches</p>
                                {#each matches.filter((m) => m.comp_level === "qm").toSorted((a, b) => a.match_number - b.match_number) as match}
                                    <MatchItem match={match} compLevel={match.comp_level} selectMatch={selectMatch} />
                                {/each}
                                <p class="text-sm text-muted-foreground mt-2">Semi-Finals Matches</p>
                                {#each matches.filter((m) => m.comp_level === "sf").toSorted((a, b) => a.set_number - b.set_number) as match}
                                    <MatchItem match={match} compLevel={match.comp_level} selectMatch={selectMatch} />
                                {/each}
                                <p class="text-sm text-muted-foreground mt-2">Finals Matches</p>
                                {#each matches.filter((m) => m.comp_level === "f").toSorted((a, b) => a.match_number - b.match_number) as match}
                                    <MatchItem match={match} compLevel={match.comp_level} selectMatch={selectMatch} />
                                {/each}
                            </div>
                        </Collapsible.Content>
                    </Collapsible.Root>
                </div>
            {:else if matchesState === "noMatches"}
                <p>No matches found for <span class="font-mono">{year + selectedEvents[0]}</span></p>
            {/if}
        </div>

        {#if matchesState === "invalidEvent" || matchesState === "noMatches"}
            <div transition:slide>
                <Alert.Root class="text-left">
                    <Alert.Title>Not all events have match information</Alert.Title>
                    <Alert.Description>
                        Some events may not have their match schedules released on TBA yet, and custom events in Open Scouting are not supported.
                    </Alert.Description>
                </Alert.Root>
            </div>
        {/if}
    </div>
</BaseDialog>