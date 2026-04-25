<script lang="ts">
    import * as Card from "$lib/components/ui/card/index.js";
	import { db } from "$lib/utils/db";
	import { onMount } from "svelte";
	import { scale, slide } from "svelte/transition";
	import Button from "../ui/button/button.svelte";
	import { CircleIcon } from "phosphor-svelte";
	import { getEventInfoEventInfoYearEventCodeGet } from "$lib/api/events/events";
	import { liveQuery } from "dexie";

    let events = liveQuery(() => db.event.filter(e => {
            const now = new Date();
            const startDate = new Date(e.start_date);
            const endDate = new Date(e.end_date);

            endDate.setDate(endDate.getDate() + 1);

            return startDate <= now && now <= endDate
        }).toArray()
    );

    let visibleEvent = $state(null);
    let container = null;
    let stopAutoScroll = $state(false);

    async function getEventDetails() {
        for (let event of $events) {
            const request = await getEventInfoEventInfoYearEventCodeGet(event.year, event.event_code);

            if (request.status === 200) {
                eventDetails.push(
                    {
                        year: event.year,
                        event_code: event.event_code,
                        ...request.data
                    }
                );
            }
        }
    }

    function updateVisible() {
        const children = Array.from(container.children);
        const containerRect = container.getBoundingClientRect();
        const center = containerRect.left + containerRect.width / 2;

        let closest = null;
        let closestDist = Infinity;

        for (const child of children) {
            const rect = child.getBoundingClientRect();
            const childCenter = rect.left + rect.width / 2;
            const dist = Math.abs(center - childCenter);

            if (dist < closestDist) {
                closestDist = dist;
                closest = child;
            }
        }

        const index = children.indexOf(closest);
        visibleEvent = $events[index];
    }

    function scrollToEvent(event) {
        const element = document.getElementById(event.event_code);
        if (element) {
            element.scrollIntoView({ behavior: "smooth" });
        }
    }

    function scrollToNext() {
        const index = $events.indexOf(visibleEvent);
        let nextIndex = (index + 1) % $events.length;

        if (nextIndex > $events.length - 1) {
            nextIndex = 0;
        }

        scrollToEvent($events[nextIndex]);
    }

    onMount(() => {
        const interval = setInterval(() => {
            if (!stopAutoScroll) {
                scrollToNext();
            }
        }, 5000);

        return () => clearInterval(interval);
    });

    $effect(() => {
        if ($events && $events.length > 0) {
            visibleEvent = $events[0];
        }
    });
</script>

{#if $events && $events.length > 0}
    <div transition:slide class="mb-4 md:mb-8">
        <div transition:scale>
            <Card.Root class="hidden min-[250px]:flex p-2">
                <Card.Content class="p-2" onclick={() => stopAutoScroll = true} onmouseover={() => stopAutoScroll = true}>
                    <div class="flex flex-col gap-2 items-center">
                        <div class="flex flex-row gap-2 items-center self-start">
                            <span class="relative flex size-3">
                                <span class="absolute inline-flex h-full w-full animate-ping rounded-full bg-blue-500 opacity-75"></span>
                                <span class="relative inline-flex size-3 rounded-full bg-blue-500"></span>
                            </span>
                            <p class="text-sm text-muted-foreground">{$events.length} {$events.length == 1 ? "event" : "events"} now</p>
                            {#if stopAutoScroll}
                                <div transition:slide={{axis: 'x'}}>
                                    <p class="text-xs text-muted-foreground whitespace-nowrap">Scrolling paused</p>
                                </div>
                            {/if}
                        </div>

                        <div class="flex flex-row overflow-y-hidden w-full max-w-[80vw] md:max-w-sm mx-auto snap-x snap-mandatory" bind:this={container} on:scroll={updateVisible}>
                            {#each $events as event}
                                <div class="flex flex-col gap-2 w-full shrink-0 snap-center border rounded-lg p-2">
                                    <div class="flex flex-row gap-2  justify-between " id={event.event_code}>
                                        <div class="flex flex-col items-start">
                                            <p class="text-sm font-bold line-clamp-1">{event.name}</p>
                                            <p class="text-xs text-muted-foreground">{event.start_date.split("T")[0]} - {event.end_date.split("T")[0]}</p>
                                    
                                        </div>
                                        <Button variant="outline" size="sm" href={`/events/?year=${event.year}&event_code=${event.event_code}`}>View Event</Button>
                                    </div>
                                </div>
                            {/each}
                        </div>

                        <div class="flex flex-row gap-2 items-center">
                            {#each $events as event}
                                {#if event == visibleEvent}
                                    <CircleIcon weight="fill" size={8} class="opacity-100" onclick={() => scrollToEvent(event)} />
                                {:else}
                                    <CircleIcon weight="fill" size={8} class="opacity-50 hover:opacity-100 transition-opacity" onclick={() => scrollToEvent(event)} />
                                {/if}
                            {/each}
                        </div>
                    </div>
                </Card.Content>
            </Card.Root>
        </div>
    </div>
{/if}