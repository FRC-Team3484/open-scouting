<script lang="ts">
	import { theBlueAllianceApiFetch } from "$lib/utls/api";
	import { onMount } from "svelte";

    import * as Card from "$lib/components/ui/card/index.js";
    import * as Tabs from "$lib/components/ui/tabs";
	import Input from "../ui/input/input.svelte";
	import Checkbox from "../ui/checkbox/checkbox.svelte";
	import Label from "../ui/label/label.svelte";
	import Separator from "../ui/separator/separator.svelte";
	import { ArrowRight, ArrowSquareOut, Mouse, SquaresFour, Star } from "phosphor-svelte";
	import Badge from "../ui/badge/badge.svelte";
	import Skeleton from "../ui/skeleton/skeleton.svelte";
	import ScrollArea from "../ui/scroll-area/scroll-area.svelte";
	import Button from "../ui/button/button.svelte";
	import { getUserSetting, getUserSettings, setUserSetting } from "$lib/utls/user";
	import { get } from "svelte/store";
	import EventList from "./events/EventList.svelte";

    export let handleNavigate: (nextPage: string) => void;
    export let year: number;

    let events: any = null;
    let favorite_events: [] = [];

    onMount(async () => {
        try {
            const response = await theBlueAllianceApiFetch("/events/" + year);
            events = response;
        } catch (error) {
            console.error(error);
        }

        favorite_events = await getUserSetting("favorite_events") ?? [];
    });

    function selectEvent(e: MouseEvent, eventData) {
        console.log("clicked", eventData);
    }

    async function favoriteEvent(e: MouseEvent, eventData) {
        const key = `${eventData.year}_${eventData.event_code}`;

        if (favorite_events.includes(key)) {
            favorite_events = favorite_events.filter(k => k !== key); // reassignment
        } else {
            favorite_events = [...favorite_events, key]; // reassignment
        }

        console.log(favorite_events);

        await setUserSetting("favorite_events", favorite_events);
    }
</script>

<Card.Root class="w-auto min-w-64">
    <Card.Header>
        <Card.Title>Events</Card.Title>
        <Card.Description>Choose an event to scout or view data for</Card.Description>
    </Card.Header>

    <Card.Content>
        <div class="flex flex-col gap-2">
            <Label for="search">Search for an event</Label>
            <Input id="search" type="text" placeholder="Search"/>
            
            <div class="flex flex-row gap-2">
                <Checkbox id="show_past_events" />
                <Label for="show_past_events">Include past events</Label>
            </div>

            <Separator orientation="horizontal" />

            <Tabs.Root value="all">
                <Tabs.List>
                    <Tabs.Trigger value="all"><SquaresFour weight="bold" /> All Events</Tabs.Trigger>
                    <Tabs.Trigger value="favorite"><Star weight="bold" /> Favorite Events</Tabs.Trigger>
                </Tabs.List>
                <Tabs.Content value="all">
                    <EventList events={events} favorite_events={favorite_events} selectEvent={selectEvent} favoriteEvent={favoriteEvent} />
                </Tabs.Content>
                <Tabs.Content value="favorite">
                    <EventList events={events} favorite_events={favorite_events} selectEvent={selectEvent} favoriteEvent={favoriteEvent} favorites={true} />
                </Tabs.Content>
            </Tabs.Root>
        </div>
    </Card.Content>

    <Card.Footer>
    </Card.Footer>
</Card.Root>
