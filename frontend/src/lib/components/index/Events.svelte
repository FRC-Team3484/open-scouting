<script lang="ts">
	import { theBlueAllianceApiFetch } from "$lib/utls/api";
	import { onMount } from "svelte";

    import * as Card from "$lib/components/ui/card/index.js";
    import * as Tabs from "$lib/components/ui/tabs";
	import Input from "../ui/input/input.svelte";
	import Checkbox from "../ui/checkbox/checkbox.svelte";
	import Label from "../ui/label/label.svelte";
	import Separator from "../ui/separator/separator.svelte";
	import { SquaresFour, Star } from "phosphor-svelte";
	import { getUserSetting, setUserSetting } from "$lib/utls/user";
	import EventList from "./events/EventList.svelte";

    let { handleNavigate, year } = $props();

    let events = $state<any | null>(null);
    let favorite_events: [] = $state([]);

    let search = $state("");
    let showPastEvents = $state(false);

    let filteredEvents = $derived(events?.filter(event => {
        const searchValue = search.toLowerCase();
        const eventName = event.name.toLowerCase();
        const eventCode = event.event_code.toLowerCase();

        return (
            (eventName.includes(searchValue) || eventCode.includes(searchValue)) &&
            (showPastEvents || event.start_date >= new Date().toISOString())
        );
    }));

    onMount(async () => {
        try {
            const response = await theBlueAllianceApiFetch("/events/" + year);
            events = response;
        } catch (error) {
            console.error(error);
        }

        favorite_events = await getUserSetting("favorite_events") ?? [];
    });

    function selectEvent(e: MouseEvent, eventData) {
        console.log("clicked", eventData);
    }

    async function favoriteEvent(e: MouseEvent, eventData) {
        const key = `${eventData.year}_${eventData.event_code}`;

        if (favorite_events.includes(key)) {
            favorite_events = favorite_events.filter(k => k !== key); // reassignment
        } else {
            favorite_events = [...favorite_events, key]; // reassignment
        }

        await setUserSetting("favorite_events", favorite_events);
    }
</script>

<Card.Root class="w-auto min-w-64">
    <Card.Header>
        <Card.Title>Events</Card.Title>
        <Card.Description>Choose an event to scout or view data for</Card.Description>
    </Card.Header>

    <Card.Content>
        <div class="flex flex-col gap-2">
            <Label for="search">Search for an event</Label>
            <Input id="search" type="text" placeholder="Search" bind:value={search}/>
            
            <div class="flex flex-row gap-2">
                <Checkbox id="show_past_events" bind:checked={showPastEvents}/>
                <Label for="show_past_events">Include past events</Label>
            </div>

            <Separator orientation="horizontal" />

            <Tabs.Root value="all">
                <Tabs.List>
                    <Tabs.Trigger value="all"><SquaresFour weight="bold" /> All Events</Tabs.Trigger>
                    <Tabs.Trigger value="favorite"><Star weight="bold" /> Favorite Events</Tabs.Trigger>
                </Tabs.List>
                <Tabs.Content value="all">
                    <EventList events={filteredEvents} favorite_events={favorite_events} selectEvent={selectEvent} favoriteEvent={favoriteEvent} />
                </Tabs.Content>
                <Tabs.Content value="favorite">
                    <EventList events={filteredEvents} favorite_events={favorite_events} selectEvent={selectEvent} favoriteEvent={favoriteEvent} favorites={true} />
                </Tabs.Content>
            </Tabs.Root>
        </div>
    </Card.Content>

    <Card.Footer>
    </Card.Footer>
</Card.Root>
