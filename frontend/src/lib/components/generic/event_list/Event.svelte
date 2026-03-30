<script lang="ts">
	import Badge from "$lib/components/ui/badge/badge.svelte";
	import Button from "$lib/components/ui/button/button.svelte";
    import * as Card from "$lib/components/ui/card/index.js";
	import { ArrowRightIcon, ArrowSquareOutIcon, CalendarIcon, InfoIcon, MapPinIcon, StarIcon, WrenchIcon } from "phosphor-svelte";

    // Props
    let { event, favoriteEvents, user, favoriteEvent } = $props();

    // Functions
    
</script>

<Card.Root>
    <Card.Content class="px-4 lg:px-6">
        <div class="flex flex-col lg:flex-row gap-2 lg:items-center lg:justify-between">
            <div class="flex flex-col gap-1">
                <div class="flex flex-row gap-1 items-center">
                    {#if event.custom}
                        <Badge class="bg-rose-500"><WrenchIcon weight="bold"/> Custom</Badge>
                    {:else}
                        <Badge class="bg-blue-500" href="https://thebluealliance.com/event/{event.year}{event.event_code}"><ArrowSquareOutIcon weight="bold"/> TBA</Badge>
                    {/if}

                    {#if favoriteEvents.includes(`${event.year}_${event.event_code}`)}
                        <Badge class="bg-yellow-500 h-5"><StarIcon weight="fill" /></Badge>
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
                    {#if favoriteEvents.includes(`${event.year}_${event.event_code}`)}
                        <Button variant="outline" onclick={(e) => favoriteEvent(e, event)}><StarIcon weight="bold" /></Button>
                    {:else}
                        <Button variant="outline" onclick={(e) => favoriteEvent(e, event)}><StarIcon weight="fill" /></Button>
                    {/if}
                {/if}  
                <Button><ArrowRightIcon weight="bold" /> Select</Button>
            </div>
        </div>
    </Card.Content>
</Card.Root>