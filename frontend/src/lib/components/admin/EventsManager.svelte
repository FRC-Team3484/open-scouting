<script lang="ts">
	import { deleteUserUsersDeleteUuidDelete, removeSuperuserUsersRemoveSuperuserUuidPost, setSuperuserUsersSetSuperuserUuidPost } from "$lib/api/auth/auth";
	import type { AdminEventResponse, EventResponse } from "$lib/api/model";
    import * as Card from "$lib/components/ui/card";
	import { onMount } from "svelte";
	import Badge from "../ui/badge/badge.svelte";
	import Button from "../ui/button/button.svelte";
	import Separator from "../ui/separator/separator.svelte";
    import * as AlertDialog from "$lib/components/ui/alert-dialog";
	import { toast } from "svelte-sonner";
	import { validateTokenOnline } from "$lib/utils/user";
	import { deleteEventEventsDeleteEventUuidDelete, deleteMatchScoutingSubmissionsEventsDeleteEventUuidMatchScoutingSubmissionsDelete, deleteTeamPitsEventsDeleteEventUuidTeamPitsDelete, getAllEventsEventsGetGet } from "$lib/api/events/events";
	import { Calendar, List, MapPin, PlusCircle } from "phosphor-svelte";

    let events: AdminEventResponse[] = $state([]);
    let selected: string[] = $state([]);

    async function getEvents() {
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

    async function deleteEvent(uuid: string, once: boolean = true) {
        await deleteEventEventsDeleteEventUuidDelete(uuid).then((res) => {
            if (res.status !== 200) {
                console.error(res)
                toast.error("Failed to delete event", { duration: 5000 });
                return
            } else {
                if (once) { toast.success("Event deleted", { duration: 5000 }); getEvents(); }
            }
        })
    }

    async function deleteSelectedEvents() {
        for (let uuid of selected) {
            await deleteEvent(uuid, false);
        }

        toast.success("Events deleted", { duration: 5000 });
        getEvents();
    }

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

    async function deleteSelectedEventMatchScoutingSubmissions() {
        for (let uuid of selected) {
            await deleteEventMatchScoutingSubmissions(uuid, false);
        }

        toast.success("Match scouting submissions deleted", { duration: 5000 });
        getEvents();
    }

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
                                <List weight="bold" />
                                <p class="wrap-anywhere">{event.type}</p>
                                <MapPin weight="bold" />
                                <p class="wrap-anywhere">{event.country} - {event.city}</p>
                                <Calendar weight="bold" />
                                <p class="wrap-anywhere">{event.start_date} - {event.end_date}</p>
                            </div>

                            <div class="flex flex-row gap-2 items-center flex-wrap">
                                <p>{event.match_scouting_submissions} <span class="text-muted-foreground">Match Scouting Submissions</span>, {event.pits} <span class="text-muted-foreground">Pits</span></p>
                            </div>

                            <div class="flex flex-row gap-2 items-center flex-wrap text-sm text-muted-foreground">
                                <PlusCircle weight="bold" />
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