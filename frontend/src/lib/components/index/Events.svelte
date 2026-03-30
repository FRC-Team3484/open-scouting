<script lang="ts">
    import * as Card from "$lib/components/ui/card/index.js";

	import CreateCustomEventDialog from "../generic/dialogs/CreateCustomEventDialog.svelte";
	import EventList from "../generic/event_list/EventList.svelte";

    let { handleNavigate, year, setEvent } = $props();

    let selectedEvent = $state(null);

    $effect(() => {
        if (selectedEvent) {
            setEvent(selectedEvent.event_code, selectedEvent.year, selectedEvent.name);
            handleNavigate("action");
        }
    });
</script>

<Card.Root class="my-4">
    <Card.Header>
        <Card.Title>Events</Card.Title>
        <Card.Description>Choose an event to scout or view data for</Card.Description>
    </Card.Header>

    <Card.Content class="px-4 lg:px-6">
        <EventList year={year} bind:value={selectedEvent} />
    </Card.Content>
</Card.Root>

<!-- <CreateCustomEventDialog getEvents={getEvents} /> -->