<script lang="ts">
	import type { AdminPitResponse, SubmissionResponse } from "$lib/api/model";
    import * as Card from "$lib/components/ui/card";
	import { onMount } from "svelte";
	import Button from "../ui/button/button.svelte";
	import Separator from "../ui/separator/separator.svelte";
    import * as AlertDialog from "$lib/components/ui/alert-dialog";
	import { toast } from "svelte-sonner";
	import { deleteMatchScoutingSubmissionScoutingSubmissionsDeleteSubmissionUuidDelete, getMatchScoutingSubmissionsScoutingSubmissionsGet } from "$lib/api/match-scouting/match-scouting";
	import { deletePitPitsDeletePitUuidDelete, getAllPitsPitsGetGet } from "$lib/api/pit-scouting/pit-scouting";

    let pits: AdminPitResponse[] = $state([]);
    let selected: string[] = $state([]);

    async function getPits() {
        selected = [];

        await getAllPitsPitsGetGet().then((res) => {
            if (res.status !== 200) {
                console.error(res)
                return
            } else {
                pits = res.data
            }
        })
    }

    async function deletePit(uuid: string, once: boolean = true) {
        await deletePitPitsDeletePitUuidDelete(uuid).then((res) => {
            if (res.status !== 200) {
                console.error(res)
                toast.error("Failed to delete pit", { duration: 5000 });
                return
            } else {
                if (once) {toast.success("Pit deleted", { duration: 5000 }); getPits();}
            }
        })
    }

    async function deleteSelected() {
        for (const uuid of selected) {
            await deletePit(uuid, false);
        }

        toast.success("Pits deleted", { duration: 5000 });
        getPits();
    }

    onMount(async () => {
        await getPits();
    })
</script>

<div class="flex flex-col gap-4">
    <Card.Root class="w-auto">
        <Card.Header>
            <Card.Title>Pit Scouting Data</Card.Title>
            <Card.Description>Manage pit data</Card.Description>
        </Card.Header>

        <Card.Content>
            <p>Found {pits.length} pits with a total of {pits.reduce((sum, user) => sum + user.answers, 0)} answers</p>
        </Card.Content>
    </Card.Root>

    <Card.Root>
        <Card.Content class="flex flex-col gap-2">
            <div class="flex flex-row gap-2 items-center flex-wrap">
                <p>Selected {selected.length} pits</p>
                <Button variant="outline" onclick={() => selected = pits.map((user) => user.uuid)} disabled={selected.length == pits.length}>Select All</Button>
                <Button variant="outline" onclick={() => selected = []} disabled={selected.length == 0}>Select None</Button>
                <Separator orientation="vertical" />
                <AlertDialog.Root>
                    <AlertDialog.Trigger>
                        <Button variant="destructive" disabled={selected.length == 0}>Delete {selected.length} pits</Button>
                    </AlertDialog.Trigger>

                    <AlertDialog.Content>
                        <AlertDialog.Title>Delete {selected.length} pits</AlertDialog.Title>
                        <AlertDialog.Description>
                            Are you sure you want to delete {selected.length} pits? This action cannot be undone.
                        </AlertDialog.Description>
                        <AlertDialog.Footer>
                            <AlertDialog.Cancel type="button">Cancel</AlertDialog.Cancel>
                            <AlertDialog.Action type="button" onclick={deleteSelected}>Delete</AlertDialog.Action>
                        </AlertDialog.Footer>
                    </AlertDialog.Content>
                </AlertDialog.Root>
            </div>

            <Separator orientation="horizontal" />
            
            {#each pits as submission}
                <Card.Root>
                    <Card.Content>
                        <div class="flex flex-col gap-2">
                            <div class="flex flex-row gap-2 items-center flex-wrap">
                                <input type="checkbox" bind:group={selected} value={submission.uuid} />
                                <p class="wrap-anywhere font-bold">{submission.team_number}<span class="text-muted-foreground">'s pit at </span> {submission.event_name} <span class="text-muted-foreground font-mono text-sm">{submission.event_code}</span></p>
                            </div>

                            <div class="flex flex-col gap-2 text-left flex-wrap">
                                <p class="wrap-anywhere">{submission.answers} answers</p>
                                <p class="text-sm text-muted-foreground">Created: {submission.created_at}</p>
                            </div>

                            <div class="flex flex-row gap-2 items-center flex-wrap">
                                <AlertDialog.Root>
                                    <AlertDialog.Trigger>
                                        <Button variant="destructive" size="sm">Delete</Button>
                                    </AlertDialog.Trigger>

                                    <AlertDialog.Content>
                                        <AlertDialog.Title>Delete Pit "{submission.uuid}"</AlertDialog.Title>
                                        <AlertDialog.Description>Are you sure you want to delete this pit? This action cannot be undone.</AlertDialog.Description>
                                        <AlertDialog.Footer>
                                            <AlertDialog.Cancel type="button">Cancel</AlertDialog.Cancel>
                                            <AlertDialog.Action type="button" onclick={() => deletePit(submission.uuid)}>Delete</AlertDialog.Action>
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