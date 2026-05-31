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
	import { BuildingsIcon, CaretUpDownIcon, CircleNotchIcon, ListIcon, PlusCircleIcon } from "phosphor-svelte";

    import * as Alert from "$lib/components/ui/alert/index.js";
    import * as Collapsible from "$lib/components/ui/collapsible/index.js";
	import Button from "$lib/components/ui/button/button.svelte";
	import { buttonVariants } from "../../../ui/button";

	import { db, type Event } from "$lib/utils/db";
	import { theBlueAllianceApiFetch } from "$lib/utils/api";
	import BaseDialog from "../../../generic/dialogs/BaseDialog.svelte";
	import MatchItem from "./MatchItem.svelte";
	import EventList from "$lib/components/generic/event_list/EventList.svelte";


    interface Props {
        open: boolean
        year: number
        selectMatch: (teams: string[]) => void
    }
    let { open = $bindable(false), year, selectMatch }: Props = $props();

    let selectedEvents: Event[] = $state([]);
    let selectedEvent: Event | null = $derived.by(() => {
        if (selectedEvents.length === 1) {
            return selectedEvents[0] ?? null;
        } else {
            return null;
        }
    });
    const eventUpcoming: boolean = $derived.by(() => {
        if (!selectedEvent) return false;
        const today = new Date();
        today.setHours(0, 0, 0, 0);

        return new Date(selectedEvent.end_date) > today;
    });

    let matches: Match[] = $state([]);
    let closestMatches: Match[] = $derived.by(() => {
        const now = Date.now() / 1000;
        return matches.toSorted((a, b) => Math.abs(a.predicted_time - now) - Math.abs(b.predicted_time - now)).slice(0, 5);
    });

    let matchesState: "selectEvent" | "loading" | "invalidEvent" | "ready" | "noMatches" = $state("selectEvent");
    let selectEventOpen: boolean = $state(false);

    /**
     * Given a selected event, get the matches for that event from TBA
     * 
     * @param eventCode The event code for this event
     */
    async function getMatches(eventCode: string): Promise<void> {
        matchesState = "loading";

        matches = await theBlueAllianceApiFetch(`/event/${year + eventCode}/matches/simple`)

        if (matches?.error) {
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
        if (selectedEvent) {
            selectEventOpen = false;
            getMatches(selectedEvent.event_code);
        } else if (selectedEvents.length === 0) {
            matchesState = "selectEvent";
        }
    });
</script>

<BaseDialog title="Select a Match" description="Select a match at an event to automatically select the teams that played in that match." bind:open> 
    <div class="flex flex-col gap-2">
        <div class="flex flex-row gap-2 flex-wrap items-center">
            <BuildingsIcon weight="bold" size={16} />
            <p>Event</p>
            <Button variant="outline" onclick={() => {selectEventOpen = true}}><PlusCircleIcon weight="bold" /> Set</Button>
        </div>

        <div class="flex flex-row gap-2 flex-wrap items-center">
            {#if matchesState === "selectEvent"}
                <p class="text-muted-foreground">Select an event</p>
            {:else if matchesState === "loading"}
                <CircleNotchIcon class="animate-spin" size={16} />
                <p class="text-muted-foreground">Getting matches...</p>
            {:else if matchesState === "invalidEvent"}
                <p class="text-muted-foreground">Invalid event</p>
            {:else if matchesState === "ready" && selectedEvent}
            
                <div class="flex flex-col gap-2 w-full">
                    <div class="flex flex-row gap-2 flex-wrap items-center">
                        <ListIcon weight="bold" size={16} />
                        <p>Match</p>
                    </div>

                    <Collapsible.Root open={eventUpcoming}>
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

                    <Collapsible.Root open={!eventUpcoming}>
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
            {:else if matchesState === "noMatches" && selectedEvent}
                <p>No matches found for <span class="font-mono">{year + selectedEvent.event_code}</span></p>
            {:else}
                <p class="text-muted-foreground">There was a problem displaying matches</p>
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

<BaseDialog title="Select Event" description="Select an event to show matches for" bind:open={selectEventOpen}>
    <EventList year={year} bind:value={selectedEvents} multiple={false} />
</BaseDialog>