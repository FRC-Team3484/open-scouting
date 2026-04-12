<script lang="ts">
    import * as Card from "$lib/components/ui/card/index.js";
	import { ArrowSquareOutIcon, CalendarBlankIcon, DatabaseIcon, PlusCircleIcon, WrenchIcon } from "phosphor-svelte";
	import Badge from "../ui/badge/badge.svelte";
	import Separator from "../ui/separator/separator.svelte";
	import Button from "../ui/button/button.svelte";
	import NumberStat from "./NumberStat.svelte";
	import { slide } from "svelte/transition";
	import { getEventInfoEventInfoYearEventCodeGet } from "$lib/api/events/events";
	import { toast } from "svelte-sonner";
	import type { EventInfoResponse } from "$lib/api/model";

    let { selectedEvent } = $props();

    let scoutingInfo: EventInfoResponse | null = $state(null);

    let event = $derived.by(() => {
        if (selectedEvent.length == 0) return null
        return selectedEvent[0]
    });

    async function getScoutingInfo() {
        scoutingInfo = null;

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
            <div class="flex flex-row flex-wrap items-center gap-2 mb-4">
                <p class="text-2xl font-bold">{event.name}</p>
                {#if event.custom}
                    <Badge class="bg-rose-500"><WrenchIcon weight="bold"/> Custom</Badge>
                {/if}
        
                {#if event.week}
                    <Badge class="bg-blue-500 transition-colors"><CalendarBlankIcon weight="bold"/> Week {event.week}</Badge>
                {/if}
            </div>

            <p class="text-md">{event.type} - {event.city}, {event.country}</p>
            <p class="text-md">{event.start_date} - {event.end_date}</p>

            {#if !event.custom}
                <Separator class="my-2"/>

                <Button variant="outline" class="w-full" href="https://thebluealliance.com/event/{event.year}{event.event_code}"><ArrowSquareOutIcon weight="bold" /> View on the Blue Alliance</Button>
            {/if}

            <Separator class="my-2"/>

            <div class={"grid grid-cols-2 gap-2 transition-all" + (scoutingInfo == null ? " opacity-50" : "")} transition:slide>
                <NumberStat value={scoutingInfo?.match_scouting_submissions || 0} label="Match Scouting Submissions" />
                <NumberStat value={scoutingInfo?.match_scouting_answers || 0} label="Match Scouting Answers" />
                <NumberStat value={scoutingInfo?.pits || 0} label="Pits" />
                <NumberStat value={scoutingInfo?.pit_answers || 0} label="Pit Scouting Answers" />
            </div>

            <div class="flex flex-row gap-2 items-center justify-center mt-2">
                <Button href="/data?year={event.year}&event_codes={event.event_code}"><DatabaseIcon weight="bold" /> View Data</Button>
                <Button variant="outline" href=""><PlusCircleIcon weight="bold" /> Add Scouting Data</Button>
            </div>

            <Separator class="my-2"/>
        {:else}
            <p class="text-muted-foreground text-center">Select an event from the event list</p>
        {/if}
    </Card.Content>
</Card.Root>