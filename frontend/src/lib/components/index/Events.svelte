<script lang="ts">
	import { theBlueAllianceApiFetch } from "$lib/utls/api";
	import { onMount } from "svelte";

    import * as Card from "$lib/components/ui/card/index.js";
    import * as Tabs from "$lib/components/ui/tabs";
	import Input from "../ui/input/input.svelte";
	import Checkbox from "../ui/checkbox/checkbox.svelte";
	import Label from "../ui/label/label.svelte";
	import Separator from "../ui/separator/separator.svelte";
	import { ArrowSquareOut, SquaresFour, Star } from "phosphor-svelte";
	import Badge from "../ui/badge/badge.svelte";
	import Skeleton from "../ui/skeleton/skeleton.svelte";
	import ScrollArea from "../ui/scroll-area/scroll-area.svelte";

    export let handleNavigate: (nextPage: string) => void;
    export let year: number;

    let events: any = null;

    onMount(async () => {
        try {
            const response = await theBlueAllianceApiFetch("/events/" + year);
            events = response;
        } catch (error) {
            console.error(error);
        }
    });

</script>

<Card.Root class="w-auto min-w-64">
    <Card.Header>
        <Card.Title>Events</Card.Title>
        <Card.Description>Choose an event to scout or view data for</Card.Description>
    </Card.Header>

    <Card.Content>
        <div class="flex flex-col gap-2">
            <Label for="search">Search for an event</Label>
            <Input id="search" type="text" placeholder="Search"/>
            
            <div class="flex flex-row gap-2">
                <Checkbox id="show_past_events" />
                <Label for="show_past_events">Include past events</Label>
            </div>

            <Separator orientation="horizontal" />

            <Tabs.Root value="all">
                <Tabs.List>
                    <Tabs.Trigger value="all"><SquaresFour weight="bold" /> All Events</Tabs.Trigger>
                    <Tabs.Trigger value="favorite"><Star weight="bold" /> Favorite Events</Tabs.Trigger>
                </Tabs.List>
                <Tabs.Content value="all">
                    <ScrollArea class="flex flex-col overflow-y-scroll max-h-[calc(100vh-32rem)]">
                        {#if events == null}
                            {#each [0, 1, 2] as _}
                                <div class="flex flex-col gap-2 my-2">
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

                        {:else if events.length == 0}
                            <p>No events found</p>
                        {:else}
                            {#each events as event}
                                <Card.Root class="max-w-128 p-4 min-w-64 my-2">
                                    <Card.Content>
                                        <div class="flex flex-col gap-2">
                                            <div class="flex flex-row gap-2">
                                                <Badge variant="secondary" class="max-h-5"><ArrowSquareOut weight="bold" />TBA</Badge>
                                                <p class="font-bold">{event.name}</p>
                                                <p class="font-mono text-muted-foreground">{event.event_code}</p>
                                            </div>

                                            <div class="flex flex-row gap-2">
                                                <p>{event.event_type_string}</p>
                                                <p>-</p>
                                                <p>{event.city},</p>
                                                <p>{event.country}</p>
                                            </div>

                                            <div class="flex flex-row gap-2">
                                                <p class="text-sm">{event.start_date}</p>
                                                <p class="text-sm">-</p>
                                                <p class="text-sm">{event.end_date}</p>
                                            </div>
                                        </div>
                                    </Card.Content>
                                </Card.Root>
                            {/each}
                        {/if}
                    </ScrollArea>
                </Tabs.Content>
                <Tabs.Content value="favorite">
                
                </Tabs.Content>
            </Tabs.Root>
        </div>
    </Card.Content>

    <Card.Footer>
    </Card.Footer>
</Card.Root>
