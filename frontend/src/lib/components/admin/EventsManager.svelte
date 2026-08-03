<!-- 
@component
Handles the admin page for event management

This page lets superusers delete events, delete match scouting data for events, and delete pit scouting data for events.
Superusers can select more than one event at once to do actions on.
-->
<script lang="ts">
	import { onMount } from "svelte";
	import { toast } from "svelte-sonner";
	import { CalendarIcon, ListIcon, MapPinIcon, PlusCircleIcon } from "phosphor-svelte";

    import * as Card from "$lib/components/ui/card";
	import Badge from "../ui/badge/badge.svelte";
	import Button from "../ui/button/button.svelte";
	import Separator from "../ui/separator/separator.svelte";
    import * as AlertDialog from "$lib/components/ui/alert-dialog";

	import type { AdminEventResponse } from "$lib/api/model";
	import { deleteEventEventsDeleteEventUuidDelete, deleteMatchScoutingSubmissionsEventsDeleteEventUuidMatchScoutingSubmissionsDelete, deleteTeamPitsEventsDeleteEventUuidTeamPitsDelete, getAllEventsEventsGetGet } from "$lib/api/events/events";


    let events: AdminEventResponse[] = $state([]);
    let selected: string[] = $state([]);

    /**
     * Fetches all events from the server
     * 
     * Use this instead of the local event cache to ensure the data is up to date
     */
    async function getEvents(): Promise<void> {
        selected = [];

        await getAllEventsEventsGetGet().then((res) => {
            if (res.status !== 200) {
                console.error(res)
                return
            } else {
                events = res.data

            }
        })
    }

    /**
     * Delete an event from the server
     * 
     * @param uuid The uuid of the event to delete
     * @param once If false, log messages about the deletion state will be handled elsewhere
     */
    async function deleteEvent(uuid: string, once: boolean = true): Promise<void> {
        await deleteEventEventsDeleteEventUuidDelete(uuid).then((res) => {
            if (res.status !== 200) {
                console.error(res);
                toast.error("Failed to delete event", { duration: 5000 });
            } else {
                if (once) { toast.success("Event deleted", { duration: 5000 }); getEvents(); }
            }
        })
    }

    /**
     * Delete all selected events from the server
     */
    async function deleteSelectedEvents(): Promise<void> {
        for (let uuid of selected) {
            await deleteEvent(uuid, false);
        }

        toast.success("Events deleted", { duration: 5000 });
        getEvents();
    }

    /**
     * Deletes match scouting submissions for an event from the server
     * 
     * @param uuid What event to delete match scouting data for
     * @param once If false, log messages about the deletion state will be handled elsewhere
     */
    async function deleteEventMatchScoutingSubmissions(uuid: string, once: boolean = true) {
        await deleteMatchScoutingSubmissionsEventsDeleteEventUuidMatchScoutingSubmissionsDelete(uuid).then((res) => {
            if (res.status !== 200) {
                console.error(res)
                toast.error("Failed to delete match scouting submissions for event", { duration: 5000 });
                return
            } else {
                if (once) { toast.success("Match scouting submissions deleted", { duration: 5000 }); getEvents(); }
            }
        });
    }

    /**
     * Delete match scouting submissions for all selected events
     */
    async function deleteSelectedEventMatchScoutingSubmissions() {
        for (let uuid of selected) {
            await deleteEventMatchScoutingSubmissions(uuid, false);
        }

        toast.success("Match scouting submissions deleted", { duration: 5000 });
        getEvents();
    }

    /**
     * Delete pit scouting data for an event
     * 
     * @param uuid What event to delete pit scouting data for
     * @param once If false, log messages about the deletion state will be handled elsewhere
     */
    async function deleteEventPits(uuid: string, once: boolean = true) {
        await deleteTeamPitsEventsDeleteEventUuidTeamPitsDelete(uuid).then((res) => {
            if (res.status !== 200) {
                console.error(res)
                toast.error("Failed to delete pits for event", { duration: 5000 });
                return
            } else {
                if (once) {toast.success("Pits deleted", { duration: 5000 }); getEvents();}
            }
        })
    }

    /**
     * Delete pit scouting data for all selected events
     */
    async function deleteSelectedEventPitScoutingSubmissions() {
        for (let uuid of selected) {
            await deleteEventPits(uuid, false);
        }

        toast.success("Pits deleted", { duration: 5000 });
        getEvents();
    }

    onMount(async () => {
        await getEvents();
    })
</script>

<div class="flex flex-col gap-4">
    <Card.Root class="w-auto">
        <Card.Header>
            <Card.Title>Events</Card.Title>
            <Card.Description>Manage events</Card.Description>
        </Card.Header>

        <Card.Content>
            <p>Found {events.length} events</p>
        </Card.Content>
    </Card.Root>

    <Card.Root>
        <Card.Content class="flex flex-col gap-2">
            <div class="flex flex-row gap-2 items-center flex-wrap">
                <p>Selected {selected.length} events</p>
                <Button variant="outline" onclick={() => selected = events.map((event) => event.uuid)} disabled={selected.length == events.length}>Select All</Button>
                <Button variant="outline" onclick={() => selected = []} disabled={selected.length == 0}>Select None</Button>
                <Separator orientation="vertical" />
                <AlertDialog.Root>
                    <AlertDialog.Trigger>
                        <Button variant="destructive" size="sm" disabled={selected.length == 0}>Delete {selected.length} events</Button>
                    </AlertDialog.Trigger>

                    <AlertDialog.Content>
                        <AlertDialog.Title>Delete {selected.length} events</AlertDialog.Title>
                        <AlertDialog.Description>
                            Are you sure you want to delete {selected.length} events? This action cannot be undone.
                        </AlertDialog.Description>
                        <AlertDialog.Footer>
                            <AlertDialog.Cancel type="button">Cancel</AlertDialog.Cancel>
                            <AlertDialog.Action type="button" onclick={deleteSelectedEvents}>Delete</AlertDialog.Action>
                        </AlertDialog.Footer>
                    </AlertDialog.Content>
                </AlertDialog.Root>

                <Separator orientation="vertical" />

                <AlertDialog.Root>
                    <AlertDialog.Trigger>
                        <Button variant="destructive" size="sm" disabled={selected.length == 0}>Delete Match Scouting Submissions</Button>
                    </AlertDialog.Trigger>

                    <AlertDialog.Content>
                        <AlertDialog.Title>Delete match scouting submissions for {selected.length} events</AlertDialog.Title>
                        <AlertDialog.Description>
                            Are you sure you want to delete match scouting submission data for {selected.length} events? This action cannot be undone.
                        </AlertDialog.Description>
                        <AlertDialog.Footer>
                            <AlertDialog.Cancel type="button">Cancel</AlertDialog.Cancel>
                            <AlertDialog.Action type="button" onclick={deleteSelectedEventMatchScoutingSubmissions}>Delete</AlertDialog.Action>
                        </AlertDialog.Footer>
                    </AlertDialog.Content>
                </AlertDialog.Root>

                <AlertDialog.Root>
                    <AlertDialog.Trigger>
                        <Button variant="destructive" size="sm" disabled={selected.length == 0}>Delete Pits</Button>
                    </AlertDialog.Trigger>

                    <AlertDialog.Content>
                        <AlertDialog.Title>Delete pits for {selected.length} events</AlertDialog.Title>
                        <AlertDialog.Description>
                            Are you sure you want to delete pit data for {selected.length} events? This action cannot be undone.
                        </AlertDialog.Description>
                        <AlertDialog.Footer>
                            <AlertDialog.Cancel type="button">Cancel</AlertDialog.Cancel>
                            <AlertDialog.Action type="button" onclick={deleteSelectedEventPitScoutingSubmissions}>Delete</AlertDialog.Action>
                        </AlertDialog.Footer>
                    </AlertDialog.Content>
                </AlertDialog.Root>
            </div>

            <Separator orientation="horizontal" />
            
            {#each events as event}
                <Card.Root>
                    <Card.Content>
                        <div class="flex flex-col gap-2">
                            <div class="flex flex-row gap-2 items-center flex-wrap">
                                <input type="checkbox" bind:group={selected} value={event.uuid} />
                                <p class="wrap-anywhere font-bold">{event.name}</p>
                                {#if event.custom}
                                    <Badge>Custom</Badge>
                                {/if}
                            </div>

                            <div class="flex flex-row gap-2 items-center flex-wrap">
                                <ListIcon weight="bold" />
                                <p class="wrap-anywhere">{event.type}</p>
                                <MapPinIcon weight="bold" />
                                <p class="wrap-anywhere">{event.country} - {event.city}</p>
                                <CalendarIcon weight="bold" />
                                <p class="wrap-anywhere">{event.start_date} - {event.end_date}</p>
                            </div>

                            <div class="flex flex-row gap-2 items-center flex-wrap">
                                <p>{event.match_scouting_submissions} <span class="text-muted-foreground">Match Scouting Submissions</span>, {event.pits} <span class="text-muted-foreground">Pits</span></p>
                            </div>

                            <div class="flex flex-row gap-2 items-center flex-wrap text-sm text-muted-foreground">
                                <PlusCircleIcon weight="bold" />
                                <p>Created: {event.created_at}</p>
                            </div>

                            <div class="flex flex-row gap-2 items-center flex-wrap">
                                <AlertDialog.Root>
                                    <AlertDialog.Trigger>
                                        <Button variant="destructive" size="sm">Delete</Button>
                                    </AlertDialog.Trigger>

                                    <AlertDialog.Content>
                                        <AlertDialog.Title>Delete event "{event.name}"</AlertDialog.Title>
                                        <AlertDialog.Description>Are you sure you want to delete this event? This action cannot be undone.</AlertDialog.Description>
                                        <AlertDialog.Footer>
                                            <AlertDialog.Cancel type="button">Cancel</AlertDialog.Cancel>
                                            <AlertDialog.Action type="button" onclick={() => deleteEvent(event.uuid)}>Delete</AlertDialog.Action>
                                        </AlertDialog.Footer>
                                    </AlertDialog.Content>
                                </AlertDialog.Root>

                                <AlertDialog.Root>
                                    <AlertDialog.Trigger>
                                        <Button variant="outline" size="sm" disabled={event.match_scouting_submissions == 0}>Delete Match Scouting Submissions</Button>
                                    </AlertDialog.Trigger>

                                    <AlertDialog.Content>
                                        <AlertDialog.Title>Delete match scouting data under "{event.name}"</AlertDialog.Title>
                                        <AlertDialog.Description>Are you sure you want to delete match scouting submissions under this event? This action cannot be undone.</AlertDialog.Description>
                                        <AlertDialog.Footer>
                                            <AlertDialog.Cancel type="button">Cancel</AlertDialog.Cancel>
                                            <AlertDialog.Action type="button" onclick={() => deleteEventMatchScoutingSubmissions(event.uuid)}>Delete</AlertDialog.Action>
                                        </AlertDialog.Footer>
                                    </AlertDialog.Content>
                                </AlertDialog.Root>

                                <AlertDialog.Root>
                                    <AlertDialog.Trigger>
                                        <Button variant="outline" size="sm" disabled={event.pits == 0}>Delete Pits</Button>
                                    </AlertDialog.Trigger>

                                    <AlertDialog.Content>
                                        <AlertDialog.Title>Delete pits "{event.name}"</AlertDialog.Title>
                                        <AlertDialog.Description>Are you sure you want to delete pits under this event? This action cannot be undone.</AlertDialog.Description>
                                        <AlertDialog.Footer>
                                            <AlertDialog.Cancel type="button">Cancel</AlertDialog.Cancel>
                                            <AlertDialog.Action type="button" onclick={() => deleteEventPits(event.uuid)}>Delete</AlertDialog.Action>
                                        </AlertDialog.Footer>
                                    </AlertDialog.Content>
                                </AlertDialog.Root>
                            </div>
                        </div>
                    </Card.Content>
                </Card.Root>
            {/each}
        </Card.Content>
    </Card.Root>
</div>