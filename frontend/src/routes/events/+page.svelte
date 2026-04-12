<script lang="ts">
	import EventDisplay from "$lib/components/events/EventDisplay.svelte";
	import EventList from "$lib/components/generic/event_list/EventList.svelte";

    let selectedEvent = $state([]);
</script>

<div class="flex flex-row gap-4 items-center justify-center">
    <div class="w-[40vw]">
        <EventList bind:value={selectedEvent} />
    </div>

    <div class="w-[50vw]">
        <EventDisplay selectedEvent={selectedEvent} />
    </div>
</div>