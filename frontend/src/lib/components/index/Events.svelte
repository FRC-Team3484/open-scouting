<script lang="ts">
	import { theBlueAllianceApiFetch } from "$lib/utils/api";
	import { onMount } from "svelte";

    import * as Card from "$lib/components/ui/card/index.js";
    import * as Tabs from "$lib/components/ui/tabs";
	import Input from "../ui/input/input.svelte";
	import Checkbox from "../ui/checkbox/checkbox.svelte";
	import Label from "../ui/label/label.svelte";
	import Separator from "../ui/separator/separator.svelte";
	import { CloudSlash, SquaresFour, Star } from "phosphor-svelte";
	import { getUserSetting, setUserSetting, validateTokenOnline } from "$lib/utils/user";
	import EventList from "./events/EventList.svelte";
	import { db } from "$lib/utils/db";
	import { Button } from "../ui/button";
    import * as Dialog from "../ui/dialog/index.js";
	import { fetchEventData } from "$lib/utils/sync";
	import { toast } from "svelte-sonner";
	import CreateCustomEventDialog from "../generic/dialogs/CreateCustomEventDialog.svelte";

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
        <div class="flex flex-col gap-2">
            <Label for="search">Search for an event</Label>
            <Input id="search" type="text" placeholder="Search" bind:value={search}/>
            
            <div class="flex flex-row gap-2">
                <Checkbox id="show_past_events" bind:checked={showPastEvents}/>
                <Label for="show_past_events">Include past events</Label>
            </div>

            <Separator orientation="horizontal" />

            <Tabs.Root value="all">
                <div class="flex flex-row gap-2 items-center justify-between">
                    <Tabs.List>
                        <Tabs.Trigger value="all"><SquaresFour weight="bold" /> All Events</Tabs.Trigger>
                        {#if user}
                            <Tabs.Trigger value="favorite"><Star weight="bold" /> Favorite Events</Tabs.Trigger>
                        {/if}
                    </Tabs.List>
                    
                    <Dialog.Root>
                        <Dialog.Trigger>
                            <Button variant="outline" size="icon"><CloudSlash weight="bold" /></Button>
                        </Dialog.Trigger>
                        <Dialog.Content>
                            <Dialog.Title>Using Offline Data</Dialog.Title>
                            <Dialog.Description>Open Scouting caches events from The Blue Alliance to work with no or poor connection. If an event seems to be missing, you can rebuild the event cache here.</Dialog.Description>

                            <Dialog.Footer>
                                <Dialog.Close>
                                    <Button variant="outline">Cancel</Button>
                                    <Button onclick={async () => {await fetchEventData(); await getEvents(); await toast.success("Event cache rebuilt");}}>Rebuild Event Cache</Button>
                                </Dialog.Close>
                            </Dialog.Footer>
                        </Dialog.Content>
                    </Dialog.Root>
                </div>

                <Tabs.Content value="all">
                    <EventList events={filteredEvents} favorite_events={favorite_events} handleNavigate={handleNavigate} setEvent={setEvent} favoriteEvent={favoriteEvent} favorites={false} signed_in={user ? true : false} />
                </Tabs.Content>

                {#if user}
                    <Tabs.Content value="favorite">
                        <EventList events={filteredEvents} favorite_events={favorite_events} handleNavigate={handleNavigate} setEvent={setEvent} favoriteEvent={favoriteEvent} favorites={true} signed_in={user ? true : false} />
                    </Tabs.Content>
                {/if}
            </Tabs.Root>
        </div>
    </Card.Content>
</Card.Root>

<CreateCustomEventDialog getEvents={getEvents} />