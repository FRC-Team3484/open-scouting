<script lang="ts">
    import * as Card from "$lib/components/ui/card/index.js";
	import { ArrowSquareOutIcon, CalendarBlankIcon, ChartBarIcon, DatabaseIcon, PlusCircleIcon, WrenchIcon } from "phosphor-svelte";
	import Badge from "../ui/badge/badge.svelte";
	import Separator from "../ui/separator/separator.svelte";
	import Button from "../ui/button/button.svelte";
	import NumberStat from "./NumberStat.svelte";
	import { getEventInfoEventInfoYearEventCodeGet } from "$lib/api/events/events";
	import { toast } from "svelte-sonner";
	import type { EventInfoResponse } from "$lib/api/model";
	import { slide } from "svelte/transition";

    let { selectedEvent } = $props();

    let scoutingInfo: EventInfoResponse | null = $state(null);

    let event = $derived.by(() => {
        if (selectedEvent.length == 0) return null
        return selectedEvent[0]
    });

    async function getScoutingInfo() {
        scoutingInfo = null;

        if (event == null) return;

        await getEventInfoEventInfoYearEventCodeGet(event.year, event.event_code).then((response) => {
            if (response.status === 200) {
                scoutingInfo = response.data;
            } else {
                toast.error("Failed to load scouting info", { duration: 5000 });
            }
        })
    }

    $effect(() => {
        event;

        getScoutingInfo();
    })
</script>

<Card.Root>
    <Card.Content>
        {#if event}
            <div transition:slide>
                <div class="flex flex-row flex-wrap items-center gap-2 mb-4">
                    <p class="text-2xl font-bold">{event.name}</p>
                    {#if event.custom}
                        <Badge class="bg-rose-500"><WrenchIcon weight="bold"/> Custom</Badge>
                    {/if}
                    {#if event.week != null}
                        <Badge class="bg-blue-500 transition-colors"><CalendarBlankIcon weight="bold"/> Week {event.week}</Badge>
                    {/if}
                </div>
                <p class="text-md">{event.type} - {event.city}, {event.country}</p>
                <p class="text-md">{event.start_date} - {event.end_date}</p>
                {#if !event.custom}
                    <Separator class="my-2"/>
                    <Button variant="outline" class="w-full" href="https://thebluealliance.com/event/{event.year}{event.event_code}"><ArrowSquareOutIcon weight="bold" /> View on The Blue Alliance</Button>
                {/if}
                <Separator class="my-2"/>
                
                <p class="font-bold mb-1">Match Scouting Information</p>
                <div class={"grid grid-cols-2 gap-2 transition-all" + (scoutingInfo == null ? " opacity-50" : "")}>
                    <NumberStat value={scoutingInfo?.match_scouting_submissions || 0} label="Match Scouting Submissions" />
                    <NumberStat value={scoutingInfo?.match_scouting_answers || 0} label="Match Scouting Answers" />
                    <Button href="/data?year={event.year}&event_codes={event.event_code}"><DatabaseIcon weight="bold" /> View Data</Button>
                    <Button variant="outline" href="/start?year={event.year}&event_code={event.event_code}&event_name={event.name}&action=match_scouting"><PlusCircleIcon weight="bold" /> Add Scouting Data</Button>
                </div>
                <p class="font-bold mb-1 mt-4">Pit Scouting Information</p>
                <div class={"grid grid-cols-2 gap-2 transition-all" + (scoutingInfo == null ? " opacity-50" : "")}>
                    <NumberStat value={scoutingInfo?.pits || 0} label="Pits" />
                    <NumberStat value={scoutingInfo?.pit_answers || 0} label="Pit Scouting Answers" />
                </div>
                <div class={"grid grid-cols-3 gap-2 transition-all mt-2 mb-2" + (scoutingInfo == null ? " opacity-50" : "")}>
                    <NumberStat value={scoutingInfo?.pits_complete} label="Complete Pits" color="green" />
                    <NumberStat value={scoutingInfo?.pits_incomplete} label="Incomplete Pits" color="orange" />
                    <NumberStat value={scoutingInfo?.pits_not_started} label="Pits Not Started" color="red" />
                </div>
                <Button class="w-full" href="/start?year=2026&event_code={event.event_code}&event_name={event.name}&action=pit_scouting"><ChartBarIcon weight="bold" /> View Pit Scouting Data</Button>
            </div>
        {:else}
            <p class="text-muted-foreground text-center">Select an event from the event list</p>
        {/if}
    </Card.Content>
</Card.Root>