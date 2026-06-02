<!-- 
@component
Renders info for each event on the event list

TODO: Get a proper interface for user

Props:
    - `event` (`Event`) - The event that is displayed
    - `favoriteEvents` (`string[]`) - The user's favorite events, from the parent
    - `user` (`unknown`) - The user from the parent
    - `favoriteEvent` (`(event: Event) => Promise<void>`) - The function to favorite an event
    - `selectEvent` (`(event: Event) => void`) - The function to select an event
    - `deselectEvent` (`(event: Event) => void`) - The function to deselect an event
    - `selectedEvents` (`Event[]`) - All selected events from the parent
-->
<script lang="ts">
	import { scale, slide } from "svelte/transition";
	import { ArrowSquareOutIcon, CalendarIcon, CheckSquareIcon, InfoIcon, MapPinIcon, SquareIcon, StarIcon, WrenchIcon } from "phosphor-svelte";

	import Badge from "$lib/components/ui/badge/badge.svelte";
	import Button from "$lib/components/ui/button/button.svelte";
    import * as Card from "$lib/components/ui/card/index.js";
	import Skeleton from "$lib/components/ui/skeleton/skeleton.svelte";
	import type { Event } from "$lib/utils/db";

    
    interface Props {
        event: Event
        favoriteEvents: string[]
        user: unknown
        favoriteEvent: (event: Event) => Promise<void>
        selectEvent: (event: Event) => void
        deselectEvent: (event: Event) => void
        selectedEvents: Event[]
    }
    let { 
        event, 
        favoriteEvents, 
        user, 
        favoriteEvent, 
        selectEvent, 
        deselectEvent, 
        selectedEvents, 
    }: Props = $props();
    
    let selected = $derived.by(() => {
        if (!selectedEvents) return false;

        return selectedEvents.some(e =>
            e.year === event.year &&
            e.event_code === event.event_code
        );
    });
</script>

<Card.Root>
    <Card.Content class="px-4 lg:px-6">
        <div class="flex flex-col lg:flex-row gap-2 lg:items-center lg:justify-between">
            <div class="flex flex-col gap-1">
                <div class="flex flex-row gap-1 items-center">
                    {#if event.custom}
                        <Badge class="bg-rose-500"><WrenchIcon weight="bold"/> Custom</Badge>
                    {:else}
                        <Badge class="bg-blue-500 transition-colors" href="https://thebluealliance.com/event/{event.year}{event.event_code}"><ArrowSquareOutIcon weight="bold"/> TBA</Badge>
                    {/if}

                    {#if favoriteEvents.includes(`${event.year}_${event.event_code}`)}

                        <div transition:slide={{axis: 'x'}}>
                            <div transition:scale>
                                <Badge class="bg-yellow-500 h-5 hover:bg-destructive transition-colors" onclick={(e) => favoriteEvent(e, event)}><StarIcon weight="fill" /></Badge>
                            </div>
                        </div>
                    {/if}

                    <p class="font-bold line-clamp-2 lg:line-clamp-1 text-left text-sm lg:text-md">{event.name}</p>
                </div>
                <div class="flex flex-row gap-1 items-center flex-wrap">
                    <InfoIcon weight="bold" />
                    <p class="text-sm">{event.type}</p>
                    <p class="text-sm">-</p>
                    <MapPinIcon weight="bold" />
                    <p class="text-sm">{event.city}, {event.country}</p>
                </div>
                <div class="flex flex-row gap-1 items-center flex-wrap">
                    <CalendarIcon weight="bold" />
                    <p class="text-sm">{event.start_date}</p>
                    <p class="text-sm">-</p>
                    <p class="text-sm">{event.end_date}</p>
                </div>
            </div>

            <div class="flex flex-row gap-2">
                {#if user}
                    <Button variant="outline" onclick={(e) => favoriteEvent(e, event)}>
                        {#if favoriteEvents.includes(`${event.year}_${event.event_code}`)}
                            <StarIcon weight="fill" />
                        {:else}
                            <StarIcon weight="bold" />
                        {/if}
                    </Button>
                {:else}
                    <Skeleton class="h-8 w-8 rounded-full" />
                {/if}
                
                {#if selected}
                    <Button variant="outline" onclick={() => deselectEvent(event)}><SquareIcon weight="bold" /> Deselect</Button>
                {:else}
                    <Button onclick={() => selectEvent(event)}><CheckSquareIcon weight="bold" /> Select</Button>
                {/if}
            </div>
        </div>
    </Card.Content>
</Card.Root>