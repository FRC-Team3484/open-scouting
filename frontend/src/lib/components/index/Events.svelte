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
	import { getUserSetting, setUserSetting } from "$lib/utils/user";
	import EventList from "./events/EventList.svelte";
	import { db } from "$lib/utils/db";
	import { Button } from "../ui/button";
    import * as Dialog from "../ui/dialog/index.js";
	import { fetchEventData } from "$lib/utils/sync";
	import { toast } from "svelte-sonner";

    let { handleNavigate, year, setEvent } = $props();

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
        events = await db.event.toArray();
    }

    onMount(async () => {
        getEvents();

        favorite_events = await getUserSetting("favorite_events") ?? [];
    });
</script>

<Card.Root class="mt-4">
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
                        <Tabs.Trigger value="favorite"><Star weight="bold" /> Favorite Events</Tabs.Trigger>
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
                    <EventList events={filteredEvents} favorite_events={favorite_events} handleNavigate={handleNavigate} setEvent={setEvent} favoriteEvent={favoriteEvent} favorites={false} />
                </Tabs.Content>
                <Tabs.Content value="favorite">
                    <EventList events={filteredEvents} favorite_events={favorite_events} handleNavigate={handleNavigate} setEvent={setEvent} favoriteEvent={favoriteEvent} favorites={true} />
                </Tabs.Content>
            </Tabs.Root>
        </div>
    </Card.Content>
</Card.Root>
