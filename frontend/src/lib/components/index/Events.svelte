<script lang="ts">
    import * as Card from "$lib/components/ui/card/index.js";

	import EventList from "../generic/event_list/EventList.svelte";

    let { handleNavigate, year, setEvent } = $props();

    let selectedEvent = $state([]);

    $effect(() => {
        if (selectedEvent.length > 0) {
            setEvent(selectedEvent[0].event_code, selectedEvent[0].year, selectedEvent[0].name);
            handleNavigate("action");
        }
    });
</script>

<Card.Root class="my-4">
    <Card.Header>
        <Card.Title>Events</Card.Title>
        <Card.Description>Choose an event to scout or view data for</Card.Description>
    </Card.Header>

    <Card.Content class="px-4 lg:px-6 max-w-unset lg:max-w-[50vw]">
        <EventList year={year} bind:value={selectedEvent} />
    </Card.Content>
</Card.Root>