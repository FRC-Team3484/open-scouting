<script lang="ts">
	import { liveQuery } from "dexie";
	import { onMount } from "svelte";

	import Button from "$lib/components/ui/button/button.svelte";
    import * as Card from "$lib/components/ui/card/index.js";
    import * as DropdownMenu from "$lib/components/ui/dropdown-menu/index.js";
	import Input from "$lib/components/ui/input/input.svelte";
    import * as Dialog from "$lib/components/ui/dialog/index.js";
	import { FadersIcon, InfoIcon, PlusIcon, TreeViewIcon } from "phosphor-svelte";
	import Separator from "$lib/components/ui/separator/separator.svelte";

	import { db } from "$lib/utils/db";
	import { getUserSetting, setUserSetting, validateTokenOnline } from "$lib/utils/user";
	import Event from "./Event.svelte";

    // Props
    interface Props {
        year?: number | null // If year is null, show all events across all years
    }

    let { year = null }: Props = $props();

    // Variables
    let events = liveQuery(() => db.event.toArray());
    let filteredEvents = $derived.by(() => {
        if ($events) {
            if (year) {
                return $events.filter(e => e.year === year);
            } else {
                return $events;
            }
        } else {
            return [];
        }
    });
    let user = $state(null);
    let favoriteEvents: [] = $state([]);

    // Functions
    async function favoriteEvent(e: MouseEvent, eventData) {
        const key = `${eventData.year}_${eventData.event_code}`;

        if (favoriteEvents.includes(key)) {
            favoriteEvents = favoriteEvents.filter(k => k !== key); // reassignment
        } else {
            favoriteEvents = [...favoriteEvents, key]; // reassignment
        }

        await setUserSetting("favorite_events", favoriteEvents);

        console.log(favoriteEvents);
    }

    // Init
    onMount(async () => {
        user = await validateTokenOnline();
        if (user) {
            favoriteEvents = await getUserSetting("favorite_events") ?? [];
        }
    });

</script>

<Card.Root class="max-w-[90vw] lg:max-w-[50vw]">
    <Card.Content class="px-4 lg:px-6">
        <!-- Header -->
        <div class="flex flex-col gap-2">
            <div class="flex flex-row gap-2 items-center">
                <p class="font-bold">Events</p>
                <Dialog.Root>
                    <Dialog.Trigger>
                        <Button variant="outline" size="icon-sm"><InfoIcon weight="bold" /></Button>
                    </Dialog.Trigger>
                    <Dialog.Content>
                        <Dialog.Title>Using Offline Events</Dialog.Title>
                        <Dialog.Description>Open Scouting caches events from The Blue Alliance (and custom ones from the sever) to work with no or poor connection. If an event seems to be missing, you can rebuild the event cache here.</Dialog.Description>

                        <Dialog.Footer>
                            <Dialog.Close>
                                <Button variant="outline">Cancel</Button>
                                <Button onclick={async () => {await fetchEventData(); await getEvents(); await toast.success("Event cache rebuilt");}}>Rebuild Event Cache</Button>
                            </Dialog.Close>
                        </Dialog.Footer>
                    </Dialog.Content>
                </Dialog.Root>
            </div>
            <div class="flex flex-row gap-2">
                <Button><PlusIcon weight="bold" /></Button>

                <Input type="text" placeholder="Search for an event..." />

                <DropdownMenu.Root>
                    <DropdownMenu.Trigger>
                        {#snippet child({ props })}
                            <Button {...props} variant="outline">
                                <TreeViewIcon weight="bold" />
                            </Button>
                        {/snippet}
                    </DropdownMenu.Trigger>

                    <DropdownMenu.Content>
                        <DropdownMenu.Label>View As</DropdownMenu.Label>
                    </DropdownMenu.Content>
                </DropdownMenu.Root>

                <DropdownMenu.Root>
                    <DropdownMenu.Trigger>
                        {#snippet child({ props })}
                            <Button {...props} variant="outline">
                                <FadersIcon weight="bold" />
                            </Button>
                        {/snippet}
                    </DropdownMenu.Trigger>

                    <DropdownMenu.Content>
                        <DropdownMenu.Label>Filter By</DropdownMenu.Label>
                    </DropdownMenu.Content>
                </DropdownMenu.Root>
            </div>

            <p class="text-sm text-muted-foreground text-left">Showing x events with x filters</p>

            <Separator class="mb-4" />
        </div>

        <!-- Events -->
        <div class="flex flex-col gap-2 max-h-[75vh] overflow-y-scroll">
            {#if filteredEvents.length === 0}
                <p>No events found</p>
            {:else}
                {#each filteredEvents as event}
                    <Event event={event} favoriteEvents={favoriteEvents} {favoriteEvent} />
                {/each}
            {/if}
        </div>
    </Card.Content>
</Card.Root>