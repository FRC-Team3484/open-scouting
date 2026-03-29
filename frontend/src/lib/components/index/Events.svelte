<script lang="ts">
	import { onMount } from "svelte";

    import * as Card from "$lib/components/ui/card/index.js";

	import { getUserSetting, setUserSetting, validateTokenOnline } from "$lib/utils/user";
	import { db } from "$lib/utils/db";

	import CreateCustomEventDialog from "../generic/dialogs/CreateCustomEventDialog.svelte";
	import EventList from "../generic/event_list/EventList.svelte";

    let { handleNavigate, year, setEvent } = $props();

    let events = $state<any | null>(null);
    let favorite_events: [] = $state([]);

    let search = $state("");
    let showPastEvents = $derived(year != new Date().getFullYear());

    let user = $state(null);

    let filteredEvents = $derived(events?.filter(event => {
        const searchValue = search.toLowerCase();
        const eventName = event.name.toLowerCase();
        const eventCode = event.event_code.toLowerCase();

        const today = new Date().toISOString().split("T")[0]; // "YYYY-MM-DD"
        const endDate = event.end_date.split("T")[0];

        return (
            (eventName.includes(searchValue) || eventCode.includes(searchValue)) &&
            (showPastEvents || endDate >= today)
        );
    }));

    async function favoriteEvent(e: MouseEvent, eventData) {
        const key = `${eventData.year}_${eventData.event_code}`;

        if (favorite_events.includes(key)) {
            favorite_events = favorite_events.filter(k => k !== key); // reassignment
        } else {
            favorite_events = [...favorite_events, key]; // reassignment
        }

        await setUserSetting("favorite_events", favorite_events);
    }

    async function getEvents() {
        events = await db.event.where("year").equals(year).toArray();
    }

    onMount(async () => {
        getEvents();

        user = await validateTokenOnline();
        if (user) {
            favorite_events = await getUserSetting("favorite_events") ?? [];
        }
    });
</script>

<Card.Root class="my-4">
    <Card.Header>
        <Card.Title>Events</Card.Title>
        <Card.Description>Choose an event to scout or view data for</Card.Description>
    </Card.Header>

    <Card.Content>
        <EventList year={year} />
    </Card.Content>
</Card.Root>

<CreateCustomEventDialog getEvents={getEvents} />