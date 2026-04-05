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
	import { slide } from "svelte/transition";

    // Props
    interface Props {
        year?: number | null // If year is null, show all events across all years
        value?: any
    }

    interface ViewOptions {
        view: "alphabetical" | "week",
        showNearby: boolean,
        favoritesOnTop: boolean
    }
    interface Filters {
        showPast: boolean
        showFavorites: boolean
        showCustom: boolean
        eventType: string[]
    }

    let { year = null, value = $bindable(null) }: Props = $props();

    // Variables
    let events = liveQuery(() => db.event.toArray());
    let filteredEvents = $derived.by(() => {
        if ($events) {
            let eventsToFilter = $events;
            if (year) {
                eventsToFilter = eventsToFilter.filter(
                    e => e.year === year 
                );
            }

            if (search) {
                eventsToFilter = eventsToFilter.filter(e =>
                    e.name.toLowerCase().includes(search.toLowerCase()) || 
                    e.event_code.toLowerCase().includes(search.toLowerCase()) || 
                    e.city.toLowerCase().includes(search.toLowerCase()) ||
                    e.country.toLowerCase().includes(search.toLowerCase())
                )
            }

            if (!filters.showPast) {
                const today = new Date();

                eventsToFilter = eventsToFilter.filter(e => {
                    const endDate = new Date(e.end_date);
                    
                    endDate.setDate(endDate.getDate() + 1);

                    return endDate > today;
                });
            }

            if (filters.showFavorites) {
                eventsToFilter = eventsToFilter.filter(e => favoriteEvents.includes(`${e.year}_${e.event_code}`));
            }

            if (filters.showCustom) {
                eventsToFilter = eventsToFilter.filter(e => e.custom === true);
            }

            return eventsToFilter;
        } else {
            return [];
        }
    });
    let user = $state(null);
    let favoriteEvents: [] = $state([]);

    let search = $state("");
    let viewOptions: ViewOptions = $state({
        view: "alphabetical",
        showNearby: false,
        favoritesOnTop: false
    });
    let filters: Filters = $state({
        showPast: false,
        showFavorites: false,
        showCustom: false,
        eventType: []
    });

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
                        <DropdownMenu.RadioGroup bind:value={viewOptions.view}>
                            <DropdownMenu.RadioItem value="week">By Week</DropdownMenu.RadioItem>
                            <DropdownMenu.RadioItem value="alphabetical">Alphabetically</DropdownMenu.RadioItem>
                        </DropdownMenu.RadioGroup>

                        <DropdownMenu.Label>Options</DropdownMenu.Label>
                        <DropdownMenu.CheckboxGroup>
                            <DropdownMenu.CheckboxItem bind:checked={viewOptions.showNearby}>Nearby Events</DropdownMenu.CheckboxItem>
                            <DropdownMenu.CheckboxItem bind:checked={viewOptions.favoritesOnTop}>Favorite Events First</DropdownMenu.CheckboxItem>
                        </DropdownMenu.CheckboxGroup>
                    </DropdownMenu.Content>
                </DropdownMenu.Root>

                <DropdownMenu.Root>
                    <DropdownMenu.Trigger>
                        {#snippet child({ props })}
                            <Button {...props} class="transition-colors" variant={filters.showPast === true || filters.showFavorites === true || filters.showCustom === true || filters.eventType.length > 0 ? "default" : "outline"}>
                                <FadersIcon weight="bold" />
                                {#if filters.showPast === true || filters.showFavorites === true || filters.showCustom  === true || filters.eventType.length > 0}
                                    <p transition:slide={{ axis: "x" }}>
                                        {
                                        (filters.showPast === true ? 1 : 0) + 
                                        (filters.showFavorites === true ? 1 : 0) + 
                                        (filters.showCustom === true ? 1 : 0) + 
                                        filters.eventType.length
                                        }
                                    </p>
                                {/if}
                            </Button>
                        {/snippet}
                    </DropdownMenu.Trigger>

                    <DropdownMenu.Content>
                        <DropdownMenu.Label>Filter</DropdownMenu.Label>
                        <DropdownMenu.CheckboxItem bind:checked={filters.showPast}>Include Past Events</DropdownMenu.CheckboxItem>
                        <DropdownMenu.CheckboxItem bind:checked={filters.showFavorites}>Only Favorite Events</DropdownMenu.CheckboxItem>
                        <DropdownMenu.CheckboxItem bind:checked={filters.showCustom}>Only Custom Events</DropdownMenu.CheckboxItem>

                        <DropdownMenu.Label>Event Type</DropdownMenu.Label>
                        <DropdownMenu.CheckboxGroup bind:value={filters.eventType}>
                            <!-- TODO: Dynamically fill based on loaded events -->
                            <DropdownMenu.CheckboxItem value="qualification">Qualification</DropdownMenu.CheckboxItem>
                            <DropdownMenu.CheckboxItem value="playoff">Playoff</DropdownMenu.CheckboxItem>
                        </DropdownMenu.CheckboxGroup>

                    </DropdownMenu.Content>
                </DropdownMenu.Root>
            </div>

            <p class="text-sm text-muted-foreground text-left">Showing {filteredEvents.length} events</p>

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