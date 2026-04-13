<script lang="ts">
	import EventDisplay from "$lib/components/events/EventDisplay.svelte";
	import Header from "$lib/components/events/Header.svelte";
	import EventList from "$lib/components/generic/event_list/EventList.svelte";

    let selectedEvent = $state([]);
</script>

<div class="flex flex-col gap-4 items-center">
    <div class="flex flex-row gap-4 justify-center">
        <div class="w-[40vw]">
            <EventList bind:value={selectedEvent} />
        </div>
    
        <div class="flex flex-col gap-4 w-[50vw]">
            <Header />
            <EventDisplay selectedEvent={selectedEvent} />
        </div>
    </div>
</div>