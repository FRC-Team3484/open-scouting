<script lang="ts">
	import { onMount } from "svelte";
	import { flip } from "svelte/animate";
	import { liveQuery } from "dexie";
	import { toast } from "svelte-sonner";

	import Button from "$lib/components/ui/button/button.svelte";
    import * as Card from "$lib/components/ui/card/index.js";
    import * as DropdownMenu from "$lib/components/ui/dropdown-menu/index.js";
	import Input from "$lib/components/ui/input/input.svelte";
    import * as Dialog from "$lib/components/ui/dialog/index.js";
	import { FadersIcon, InfoIcon, PlusIcon, TreeViewIcon } from "phosphor-svelte";
	import Separator from "$lib/components/ui/separator/separator.svelte";

	import { db } from "$lib/utils/db";
	import { getUserSetting, setUserSetting, validateTokenOnline } from "$lib/utils/user";
	import { fetchEventData } from "$lib/utils/sync";
	import Event from "./Event.svelte";

    // Props
    interface Props {
        year?: number | null // If year is null, show all events across all years
        value?: any
    }

    let { year = null, value = $bindable(null) }: Props = $props();

    // Variables
    let events = liveQuery(() => db.event.toArray());
    let filteredEvents = $derived.by(() => {
        if ($events) {
            if (year) {
                return $events.filter(e => e.year === year && e.name.includes(search));
            } else {
                return $events;
            }
        } else {
            return [];
        }
    });
    let user = $state(null);
    let favoriteEvents: [] = $state([]);

    let search = $state("");

    // Functions
    async function favoriteEvent(e: MouseEvent, eventData) {
        const key = `${eventData.year}_${eventData.event_code}`;

        if (favoriteEvents.includes(key)) {
            favoriteEvents = favoriteEvents.filter(k => k !== key); // reassignment
        } else {
            favoriteEvents = [...favoriteEvents, key]; // reassignment
        }

        await setUserSetting("favorite_events", favoriteEvents);
    }

    function selectEvent(event) {
        value = event;
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
                                <Button onclick={async () => {await fetchEventData(); await toast.success("Event cache rebuilt");}}>Rebuild Event Cache</Button>
                            </Dialog.Close>
                        </Dialog.Footer>
                    </Dialog.Content>
                </Dialog.Root>
            </div>
            <div class="flex flex-row gap-2">
                <Button><PlusIcon weight="bold" /></Button>

                <Input type="text" placeholder="Search for an event..." bind:value={search} />

                <DropdownMenu.Root>
                    <DropdownMenu.Trigger>
                        {#snippet child({ props })}
                            <Button {...props} variant="outline">
                                <TreeViewIcon weight="bold" />
                            </Button>
                        {/snippet}
                    </DropdownMenu.Trigger>

                    <DropdownMenu.Content>
                        <DropdownMenu.Label>View</DropdownMenu.Label>
                        <DropdownMenu.RadioGroup value="week">
                            <DropdownMenu.RadioItem value="week">By Week</DropdownMenu.RadioItem>
                            <DropdownMenu.RadioItem value="alphabetical">Alphabetically</DropdownMenu.RadioItem>
                        </DropdownMenu.RadioGroup>

                        <DropdownMenu.Label>Options</DropdownMenu.Label>
                        <DropdownMenu.CheckboxGroup>
                            <DropdownMenu.CheckboxItem>Nearby Events</DropdownMenu.CheckboxItem>
                            <DropdownMenu.CheckboxItem>Favorite Events First</DropdownMenu.CheckboxItem>
                        </DropdownMenu.CheckboxGroup>
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
                        <DropdownMenu.Label>Filter</DropdownMenu.Label>
                        <DropdownMenu.CheckboxItem>Favorite Events</DropdownMenu.CheckboxItem>
                        <DropdownMenu.CheckboxItem>Past Events</DropdownMenu.CheckboxItem>

                        <DropdownMenu.Label>Event Type</DropdownMenu.Label>
                        <DropdownMenu.CheckboxGroup>
                            <!-- TODO: Dynamically fill based on loaded events -->
                            <DropdownMenu.CheckboxItem>Qualification</DropdownMenu.CheckboxItem>
                            <DropdownMenu.CheckboxItem>Playoff</DropdownMenu.CheckboxItem>
                        </DropdownMenu.CheckboxGroup>

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
                {#each filteredEvents as event (event.year + event.event_code)}
                    <div animate:flip={{duration: 300}}>
                        <Event event={event} favoriteEvents={favoriteEvents} user={user} favoriteEvent={favoriteEvent} selectEvent={selectEvent} />
                    </div>
                {/each}
            {/if}
        </div>
    </Card.Content>
</Card.Root>