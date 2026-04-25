<script lang="ts">
	import { onMount, tick } from "svelte";
	import { flip } from "svelte/animate";
	import { liveQuery } from "dexie";
	import { toast } from "svelte-sonner";

	import Button from "$lib/components/ui/button/button.svelte";
    import * as Card from "$lib/components/ui/card/index.js";
    import * as DropdownMenu from "$lib/components/ui/dropdown-menu/index.js";
	import Input from "$lib/components/ui/input/input.svelte";
    import * as Dialog from "$lib/components/ui/dialog/index.js";
	import { FadersIcon, InfoIcon, PlusCircleIcon, PlusIcon, TreeViewIcon } from "phosphor-svelte";
	import Separator from "$lib/components/ui/separator/separator.svelte";

	import { db } from "$lib/utils/db";
	import { getUserSetting, setUserSetting, validateTokenOnline } from "$lib/utils/user";
	import { fetchEventData } from "$lib/utils/sync";
	import Event from "./Event.svelte";
	import { slide } from "svelte/transition";
	import CreateCustomEventDialog from "../dialogs/CreateCustomEventDialog.svelte";

    // Props
    interface Props {
        year?: number | null // If year is null, show all events across all years
        value?: [] // Allows for selecting multiple events
        multiple?: boolean,
        limits?: [] // Given a list of event_codes, limit to only showing those events, used for the data page
        defaultViewOptions?: ViewOptions | null,
        defaultFilters?: Filters | null
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
        showSelected: boolean
        eventType: string[]
    }

    let { 
        year = null, 
        value = $bindable([]), 
        multiple = false, 
        limits = [],
        defaultViewOptions = null,
        defaultFilters = null
    }: Props = $props();

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

            if (filters.showSelected) {
                eventsToFilter = eventsToFilter.filter(e => value.some(selectedEvent => selectedEvent.year === e.year && selectedEvent.event_code === e.event_code));
            }

            if (filters.eventType.length > 0) {
                eventsToFilter = eventsToFilter.filter(e => filters.eventType.includes(e.type));
            }

            if (limits.length > 0) {
                eventsToFilter = eventsToFilter.filter(e => limits.includes(e.event_code));
            }

            if (viewOptions.view === "alphabetical") {
                eventsToFilter = eventsToFilter.sort((a, b) => a.name.localeCompare(b.name));
                if (viewOptions.favoritesOnTop) {
                    eventsToFilter = eventsToFilter.sort((a, b) => {
                        if (favoriteEvents.includes(`${a.year}_${a.event_code}`) && !favoriteEvents.includes(`${b.year}_${b.event_code}`)) {
                            return -1;
                        } else if (!favoriteEvents.includes(`${a.year}_${a.event_code}`) && favoriteEvents.includes(`${b.year}_${b.event_code}`)) {
                            return 1;
                        } else {
                            return 0;
                        }
                    });
                }

                return eventsToFilter;
            } else {
                // return an list of objects with a label and values param
                // the label should be the event.week if it exists, otherwise the event.type
                // all events in the week should be in the same list for that label
                // include a type param that's either "week" or "other"
                // sort by label, with the weeks first, then the others in alphabetical order
                // sort events in each section alphabetically by name

                const groups = new Map();

                for (const e of eventsToFilter) {
                    const isWeek = e.week !== undefined && e.week !== null;

                    const label = isWeek ? `Week ${e.week}` : e.type;
                    const type = isWeek ? "week" : "other";

                    if (!groups.has(label)) {
                        groups.set(label, {
                            label,
                            type,
                            events: []
                        });
                    }

                    groups.get(label).events.push(e);
                }

                const favoriteSet = new Set(favoriteEvents);

                for (const group of groups.values()) {
                    group.events = group.events.sort((a, b) => {
                        if (viewOptions.favoritesOnTop) {
                            const aFav = favoriteSet.has(`${a.year}_${a.event_code}`);
                            const bFav = favoriteSet.has(`${b.year}_${b.event_code}`);

                            if (aFav !== bFav) {
                                return aFav ? -1 : 1;
                            }
                        }

                        return a.name.localeCompare(b.name);
                    });
                }

                eventsToFilter = Array.from(groups.values()).sort((a, b) => {
                    // Weeks first
                    if (a.type !== b.type) {
                        return a.type === "week" ? -1 : 1;
                    }

                    // If both are weeks → sort numerically
                    if (a.type === "week") {
                        const weekA = parseInt(a.label.replace("Week ", ""));
                        const weekB = parseInt(b.label.replace("Week ", ""));
                        return weekA - weekB;
                    }

                    // Otherwise alphabetical
                    return a.label.localeCompare(b.label);
                });

                return eventsToFilter;
            }
        } else {
            return [];
        }
    });
    let eventTypes = $derived.by(() => {
        if ($events) {
            return Array.from(new Set($events.map(e => e.type)));
        } else {
            return [];
        }
    })
    let user = $state(null);
    let favoriteEvents: [] = $state([]);

    let search = $state("");
    let viewOptions: ViewOptions = $state({
        view: "week",
        showNearby: false,
        favoritesOnTop: true
    });
    let filters: Filters = $state({
        showPast: false,
        showFavorites: false,
        showCustom: false,
        showSelected: false,
        eventType: []
    });

    let eventCount = $derived.by(() => {
        if (filteredEvents) {
            if (viewOptions.view === "alphabetical") {
                return filteredEvents.length;
            } else {
                return filteredEvents.reduce((total, section) => total + section.events.length, 0);
            }
        } else {
            return 0;
        }
    });
    let createCustomEventOpen = $state(false);

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
        if (multiple) {
            value.push(event);
        } else {
            value = [event];
        }
    }

    function deselectEvent(event) {
        value = value.filter(e => e.year !== event.year || e.event_code !== event.event_code);
    }

    async function rebuildEventData() {
        await fetchEventData().then(() => {
            toast.success("Event cache rebuilt");
        }).catch((error) => {
            console.warn("Failed to rebuild event cache", error);
            toast.error("Failed to rebuild event cache");
        })
    }

    // Init
    onMount(async () => {
        user = await validateTokenOnline();
        if (user) {
            favoriteEvents = await getUserSetting("favorite_events") ?? [];
        }

        if (defaultViewOptions != null) {
            viewOptions = defaultViewOptions;
        }

        if (defaultFilters != null) {
            filters = defaultFilters;
        }
    });
</script>

<Card.Root class="">
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
                                <Button onclick={rebuildEventData}>Rebuild Event Cache</Button>
                            </Dialog.Close>
                        </Dialog.Footer>
                    </Dialog.Content>
                </Dialog.Root>
            </div>
            <div class="flex flex-row gap-2">
                <Button onclick={() => createCustomEventOpen = true}><PlusIcon weight="bold" /></Button>

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
                        <!-- <DropdownMenu.CheckboxItem bind:checked={viewOptions.showNearby}>Nearby Events</DropdownMenu.CheckboxItem> -->
                        <DropdownMenu.CheckboxItem bind:checked={viewOptions.favoritesOnTop}>Favorite Events First</DropdownMenu.CheckboxItem>
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
                        {#if multiple}
                            <DropdownMenu.CheckboxItem bind:checked={filters.showSelected}>Only Selected Events</DropdownMenu.CheckboxItem>
                        {/if}

                        <DropdownMenu.Label>Event Type</DropdownMenu.Label>
                        <DropdownMenu.CheckboxGroup bind:value={filters.eventType}>
                            {#each eventTypes as type}
                                <DropdownMenu.CheckboxItem value={type}>{type.charAt(0).toUpperCase() + type.slice(1)}</DropdownMenu.CheckboxItem>
                            {/each}
                        </DropdownMenu.CheckboxGroup>

                    </DropdownMenu.Content>
                </DropdownMenu.Root>
            </div>

            {#if multiple}
                <p class="text-sm text-muted-foreground text-left">Showing {eventCount} events with {value.length} selected</p>
            {:else}
                <p class="text-sm text-muted-foreground text-left">Showing {eventCount} events</p>
            {/if}

            {#if limits.length > 0}
                <p class="text-sm text-muted-foreground text-left">Avaliable events have been limited to {limits.length} events</p>
            {/if}

            <Separator class="mb-4" />
        </div>

        <!-- Events -->
        <div class="flex flex-col gap-2 max-h-[75vh] overflow-y-scroll [content-visiblity:auto]">
            {#if filteredEvents.length === 0}
                <div class="flex flex-col gap-2">
                    <p class="text-muted-foreground">No events found</p>
                    <p class="text-muted-foreground text-sm">Try changing or removing filters</p>
                    <Separator />
                    <p class="text-muted-foreground text-sm">Or, create a custom event if it's missing on TBA</p>
                    <Button onclick={() => createCustomEventOpen = true}><PlusCircleIcon weight="bold" />Create Custom Event</Button>
                </div>
            {:else}
                {#if viewOptions.view === "alphabetical"}
                    {#each filteredEvents as event (event.year + event.event_code)}
                        <div animate:flip={{duration: 300}}>
                            <Event 
                                event={event} 
                                favoriteEvents={favoriteEvents} 
                                user={user} 
                                favoriteEvent={favoriteEvent} 
                                selectEvent={selectEvent} 
                                deselectEvent={deselectEvent} 
                                selectedEvents={value} 
                                multiple={multiple} 
                            />
                        </div>
                    {/each}
                {:else if viewOptions.view === "week"}
                    {#each filteredEvents as section}
                        <p class="text-left text-sm text-muted-foreground sticky top-0 bg-card pb-2">{section.label.charAt(0).toUpperCase() + section.label.slice(1)}</p>

                        {#each section.events as event (event.year + event.event_code)}
                            <div animate:flip={{duration: 300}}>
                                <Event 
                                    event={event} 
                                    favoriteEvents={favoriteEvents} 
                                    user={user} 
                                    favoriteEvent={favoriteEvent} 
                                    selectEvent={selectEvent} 
                                    deselectEvent={deselectEvent} 
                                    selectedEvents={value} 
                                    multiple={multiple} 
                                />
                            </div>
                        {/each}
                    {/each}
                {/if}
            {/if}
        </div>
    </Card.Content>
</Card.Root>

<CreateCustomEventDialog bind:open={createCustomEventOpen} />