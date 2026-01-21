<script lang="ts">
	import ScrollArea from "$lib/components/ui/scroll-area/scroll-area.svelte";
	import Skeleton from "$lib/components/ui/skeleton/skeleton.svelte";
    import * as Card from "$lib/components/ui/card/index.js";
	import { ArrowRight, ArrowSquareOut, Star, Wrench } from "phosphor-svelte";
	import { Badge } from "$lib/components/ui/badge";
	import Button from "$lib/components/ui/button/button.svelte";
	import CreateCustomEventButton from "./CreateCustomEventButton.svelte";

    export let events: any = null;
    export let favorite_events: [] = [];
    export let handleNavigate: (nextPage: string) => void;
    export let setEvent: (event_code: string, year: number, name: string) => void;
    export let favoriteEvent: (e: MouseEvent, eventData) => void;
    export let favorites = false;
    export let signed_in = false;

    $: filteredEvents = favorites
        ? (events ?? []).filter(event => favorite_events.includes(`${event.year}_${event.event_code}`))
        : events;
</script>

<ScrollArea>
    <div class="flex flex-col overflow-y-scroll max-h-128 md:max-h-256 bg-secondary p-4 rounded-md border-2 border-accent">
        {#if filteredEvents == null}
            {#each [0, 1, 2] as _}
                <div class="flex flex-col gap-2 my-4">
                    <div class="flex flex-row gap-2">
                        <Skeleton class="h-5 w-8" />
                        <Skeleton class="h-5 w-48" />
                        <Skeleton class="h-5 w-8" />
                    </div>
                    <div class="flex flex-row gap-2">
                        <Skeleton class="h-5 w-16" />
                        <Skeleton class="h-5 w-16" />
                        <Skeleton class="h-5 w-8" />
                    </div>
                    <div class="flex flex-row gap-2">
                        <Skeleton class="h-5 w-16" />
                        <Skeleton class="h-5 w-16" />
                    </div>
                </div>
            {/each}
        {:else if filteredEvents.length == 0}
            <CreateCustomEventButton />
                
            <p>No events found</p>
        {:else}
            <CreateCustomEventButton />

            {#each filteredEvents as event}
                <Card.Root class="w-full max-w-128 min-w-64 my-2">
                    <Card.Content>
                        <div class="flex flex-row gap-2 justify-between">
                            <div class="flex flex-col gap-2">
                                <div class="flex flex-row gap-2">
                                    {#if favorite_events.includes(`${event.year}_${event.event_code}`)}
                                        <Badge variant="default" class="max-h-5 bg-yellow-500"><Star weight="fill" /></Badge>
                                    {/if}

                                    {#if event.custom == true}
                                        <Badge variant="secondary" class="max-h-5 !bg-rose-500"><Wrench weight="fill" /> Custom</Badge>
                                    {:else}
                                        <Badge variant="secondary" class="max-h-5 !bg-blue-500"><ArrowSquareOut weight="bold" />TBA</Badge>
                                    {/if}

                                    <p class="font-bold">{event.name}</p>
                                    {#if event.custom == false}
                                        <p class="font-mono text-muted-foreground overflow-hidden">{event.event_code}</p>
                                    {/if}
                                </div>
                                <div class="flex flex-row gap-2">
                                    <p>{event.type.charAt(0).toUpperCase() + event.type.slice(1)}</p>
                                    <p>-</p>
                                    <p>{event.city},</p>
                                    <p>{event.country}</p>
                                </div>
                                <div class="flex flex-row gap-2">
                                    <p class="text-sm">{event.start_date}</p>
                                    <p class="text-sm">-</p>
                                    <p class="text-sm">{event.end_date}</p>
                                </div>
                                <div class="flex flex-row gap-2">
                                    {#if signed_in}
                                        {#if favorite_events.includes(`${event.year}_${event.event_code}`)}
                                            <Button variant="ghost" size="icon" onclick={(e) => favoriteEvent(e, event)}><Star weight="fill" /></Button>
                                        {:else}
                                            <Button variant="ghost" size="icon" onclick={(e) => favoriteEvent(e, event)}><Star weight="bold" /></Button>
                                        {/if}
                                    {/if}
                                    <Button variant="outline" onclick={(e) => {setEvent(event.event_code, event.year, event.name); handleNavigate("action")}}><ArrowRight weight="bold" /> Continue</Button>
                                </div>
                            </div>
                        </div>
                    </Card.Content>
                </Card.Root>
            {/each}
        {/if}
    </div>
</ScrollArea>