<!-- 
@component
The dialog for selecting teams based on a certain match number at a competition

Props:
    - `open` (`boolean`) - If the dialog should be open or not
    - `year` (`number`) - The year of the event
    - `selectMatch` (`(teams: string[]) => void`) - Given a list of team numbers, add those team numbers to the filters
-->
<script lang="ts" module>
    interface Alliance {
        dq_team_keys: string[]
        score: number
        surrogate_team_keys: string[]
        team_keys: string[]
    }
    export interface Match {
        actual_time: number
        alliances: {
            blue: Alliance
            red: Alliance
        }
        comp_level: string
        event_key: string
        key: string
        match_number: number
        predicted_time: number
        set_number: number
        time: number
        winning_alliance: string | null
    }
</script>

<script lang="ts">
	import { slide } from "svelte/transition";
	import { BuildingsIcon, CaretUpDownIcon, CircleNotchIcon, ListIcon } from "phosphor-svelte";

    import * as Alert from "$lib/components/ui/alert/index.js";
    import * as Collapsible from "$lib/components/ui/collapsible/index.js";
	import { buttonVariants } from "../../../ui/button";

	import { db, type Event } from "$lib/utils/db";
	import { theBlueAllianceApiFetch } from "$lib/utils/api";
	import FilterList from "../../FilterList.svelte";
	import BaseDialog from "../../../generic/dialogs/BaseDialog.svelte";
	import MatchItem from "./MatchItem.svelte";


    interface Props {
        open: boolean
        year: number
        selectMatch: (teams: string[]) => void
    }
    let { open = $bindable(false), year, selectMatch }: Props = $props();

    let events: Event[] = $state([]);
    let selectedEvents: string[] | undefined = $state([]);
    let matches: Match[] = $state([]);
    let closestMatches: Match[] = $derived.by(() => {
        const now = Date.now() / 1000;
        return matches.toSorted((a, b) => Math.abs(a.predicted_time - now) - Math.abs(b.predicted_time - now)).slice(0, 5);
    });

    let matchType: string = $state("qm");
    let matchNumber: number = $state(1);

    let matchesState: "selectEvent" | "loading" | "invalidEvent" | "ready" | "noMatches" = $state("selectEvent");

    /**
     * Get all events from the local database
     */
    async function getEvents(): Promise<void> {
        events = await db.event.filter(e => e.year === year && e.custom === false).toArray();
    }

    /**
     * Given a selected event, get the matches for that event from TBA
     * 
     * @param eventCode The event code for this event
     */
    async function getMatches(eventCode: string): Promise<void> {
        matchesState = "loading";

        matches = await theBlueAllianceApiFetch(`/event/${year + eventCode}/matches/simple`);

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

    /**
     * If selectedEvents is updated, get the matches for that event. If no event is selected, set the state to be ready to select an event
     */
    $effect(() => {
        if (selectedEvents.length > 0) {
            getMatches(selectedEvents[0]);
        } else if (selectedEvents.length === 0) {
            matchesState = "selectEvent";
        }
    });

    /**
     * When the match type is updated, set the match number to 1
     */
    $effect(() => {
        matchType;
        matchNumber = 1;
    });

    /**
     * When the year is updated, fetch events again
     */
    $effect(() => {
        year;

        getEvents();
    });
</script>

<BaseDialog title="Select a Match" description="Select a match at an event to automatically select the teams that played in that match." bind:open> 
    <div class="flex flex-col gap-2">
        <div class="flex flex-row gap-2 flex-wrap items-center">
            <BuildingsIcon weight="bold" size={16} />
            <p>Event</p>
            <FilterList filterTitle="Add Event Filter" values={events.map((e) => e.event_code)} labels={events.map((e) => e.name)} bind:selected={selectedEvents} onlyOne />
        </div>

        <div class="flex flex-row gap-2 flex-wrap items-center">
            {#if matchesState === "selectEvent"}
                <p class="text-muted-foreground">Select an event</p>
            {:else if matchesState === "loading"}
                <CircleNotchIcon class="animate-spin" size={16} />
                <p class="text-muted-foreground">Getting matches...</p>
            {:else if matchesState === "invalidEvent"}
                <p class="text-muted-foreground">Invalid event</p>
            {:else if matchesState === "ready"}
            
                <div class="flex flex-col gap-2 w-full">
                    <div class="flex flex-row gap-2 flex-wrap items-center">
                        <ListIcon weight="bold" size={16} />
                        <p>Match</p>
                    </div>

                    <Collapsible.Root open={new Date(events.find((e) => e.event_code === selectedEvents[0] && e.year === year)?.end_date) < new Date(`${year}-${('0' + (new Date().getMonth() + 1)).slice(-2) + '-' + ('0' + new Date().getDate()).slice(-2)}`)}>
                        <Collapsible.Trigger class={buttonVariants({ variant: "outline", class: "w-full" })}>Matches Soon <CaretUpDownIcon weight="bold" size={16} /></Collapsible.Trigger>

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
                        <Collapsible.Trigger class={buttonVariants({ variant: "outline", class: "w-full" })}>All Matches <CaretUpDownIcon weight="bold" size={16} /></Collapsible.Trigger>

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