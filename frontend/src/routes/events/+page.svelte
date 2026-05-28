<!-- 
The event page. Shows detailed match and pit scouting information for a single event.

Provides quick links to the data, scouting, and pit scouting pages for the event. Also links to TBA, if applicable.
On smaller screens, the event list is moved into a dialog.
-->
<script lang="ts">
	import { onMount, tick } from "svelte";
	import { ListIcon } from "phosphor-svelte";
	import { replaceState } from "$app/navigation";

	import Button from "$lib/components/ui/button/button.svelte";

	import { db, type Event } from "$lib/utils/db";
	import EventDisplay from "$lib/components/events/EventDisplay.svelte";
	import Header from "$lib/components/events/Header.svelte";
	import BaseDialog from "$lib/components/generic/dialogs/BaseDialog.svelte";
	import EventList from "$lib/components/generic/event_list/EventList.svelte";


    let selectedEvent: Event[] = $state([]);
    let dialogOpen: boolean = $state(false);

    /**
     * Load the selected event from the URL
     */
    async function loadUrlParams() {
        const url = new URL(window.location.href);

        if (url.searchParams.has("year") && url.searchParams.has("event_code")) {
            const event = await db.event.filter((e) => e.year == url.searchParams.get("year") && e.event_code == url.searchParams.get("event_code")).first();

            if (event) {
                selectedEvent = [event];
            }
        }
    }

    /**
     * Update the URL with the selected event
     */
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

    /**
     * Update the URL when the selected event changes
     */
    $effect(() => {
        if (selectedEvent.length > 0) {
            dialogOpen = false;
        }

        setUrlParams();
    });

    /**
     * If on a smaller screen, and no event has been selected (after one second to allow the event list to load), open the dialog automatically
    */
    onMount(async () => {
        setTimeout(() => {
            if (window.innerWidth < 768 && selectedEvent.length == 0) {
                dialogOpen = true
            }
        }, 1000);

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