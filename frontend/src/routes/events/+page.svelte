<script lang="ts">
	import { replaceState } from "$app/navigation";
	import EventDisplay from "$lib/components/events/EventDisplay.svelte";
	import Header from "$lib/components/events/Header.svelte";
	import BaseDialog from "$lib/components/generic/dialogs/BaseDialog.svelte";
	import EventList from "$lib/components/generic/event_list/EventList.svelte";
	import Button from "$lib/components/ui/button/button.svelte";
	import { db } from "$lib/utils/db";
	import { ListIcon } from "phosphor-svelte";
	import { onMount, tick } from "svelte";

    let selectedEvent = $state([]);
    let dialogOpen = $state(false);

    async function loadUrlParams() {
        const url = new URL(window.location.href);

        if (url.searchParams.has("year") && url.searchParams.has("event_code")) {
            const event = await db.event.filter((e) => e.year == url.searchParams.get("year") && e.event_code == url.searchParams.get("event_code")).first();

            if (event) {
                selectedEvent = [event];
            }
        }
    }

    function setUrlParams() {
        const url = new URL(window.location.href);

        if (selectedEvent.length == 0) {
            url.searchParams.delete("year");
            url.searchParams.delete("event_code");
        } else {
            url.searchParams.set("year", selectedEvent[0].year)
            url.searchParams.set("event_code", selectedEvent[0].event_code);
        };

        tick().then(() => {
            replaceState(url, {})
        });
    }

    $effect(() => {
        if (selectedEvent.length > 0) {
            dialogOpen = false;
        }


        setUrlParams();
    });

    onMount(async () => {
        if (window.innerWidth < 768) {
            setTimeout(() => {
                dialogOpen = true
            }, 1000);
        }

        loadUrlParams();
    })
</script>

<div class="flex flex-col gap-4 items-center">
    <div class="flex flex-row gap-4 justify-center">
        <div class="w-[40vw] hidden md:flex">
            <EventList bind:value={selectedEvent} />
        </div>
    
        <div class="flex flex-col gap-4 w-[95vw] md:w-[50vw] mb-18 md:mb-2">
            <Header />
            <EventDisplay selectedEvent={selectedEvent} />
        </div>
    </div>
</div>

<Button class="fixed md:hidden bottom-4 left-[50%] translate-x-[-50%]" variant="default" size="lg" onclick={() => dialogOpen = true}><ListIcon weight="bold" /> Select Event</Button>

<BaseDialog title="Event Filters" description="Filter the displayed data by event" bind:open={dialogOpen}>
    <EventList bind:value={selectedEvent} />
</BaseDialog>