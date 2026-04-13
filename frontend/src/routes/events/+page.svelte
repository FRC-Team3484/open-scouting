<script lang="ts">
	import EventDisplay from "$lib/components/events/EventDisplay.svelte";
	import Header from "$lib/components/events/Header.svelte";
	import BaseDialog from "$lib/components/generic/dialogs/BaseDialog.svelte";
	import EventList from "$lib/components/generic/event_list/EventList.svelte";
	import Button from "$lib/components/ui/button/button.svelte";
	import { ListIcon } from "phosphor-svelte";
	import { onMount } from "svelte";

    let selectedEvent = $state([]);
    let dialogOpen = $state(false);

    $effect(() => {
        if (selectedEvent.length > 0) {
            dialogOpen = false;
        }
    });

    onMount(async () => {
        if (window.innerWidth < 768) {
            setTimeout(() => {
                dialogOpen = true
            }, 1000);
        }
    })
</script>

<div class="flex flex-col gap-4 items-center">
    <div class="flex flex-row gap-4 justify-center">
        <div class="w-[40vw] hidden md:flex">
            <EventList bind:value={selectedEvent} />
        </div>
    
        <div class="flex flex-col gap-4 w-[95vw] md:w-[50vw]">
            <Header />
            <EventDisplay selectedEvent={selectedEvent} />
        </div>
    </div>
</div>

<Button class="absolute md:hidden bottom-4 left-[50%] translate-x-[-50%]" variant="default" size="lg" onclick={() => dialogOpen = true}><ListIcon weight="bold" /> Select Event</Button>

<BaseDialog title="Event Filters" description="Filter the displayed data by event" bind:open={dialogOpen}>
    <EventList bind:value={selectedEvent} />
</BaseDialog>