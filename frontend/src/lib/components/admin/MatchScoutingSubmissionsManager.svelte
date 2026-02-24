<script lang="ts">
	import { deleteUserUsersDeleteUuidDelete, getUsersUsersGet, removeSuperuserUsersRemoveSuperuserUuidPost, setSuperuserUsersSetSuperuserUuidPost } from "$lib/api/auth/auth";
	import type { SubmissionResponse, UserResponse } from "$lib/api/model";
    import * as Card from "$lib/components/ui/card";
	import { onMount } from "svelte";
	import Badge from "../ui/badge/badge.svelte";
	import Button from "../ui/button/button.svelte";
	import Separator from "../ui/separator/separator.svelte";
    import * as AlertDialog from "$lib/components/ui/alert-dialog";
	import { toast } from "svelte-sonner";
	import { validateTokenOnline } from "$lib/utils/user";
	import { deleteMatchScoutingSubmissionScoutingSubmissionsDeleteSubmissionUuidDelete, getMatchScoutingSubmissionsScoutingSubmissionsGet } from "$lib/api/match-scouting/match-scouting";

    let submissions: SubmissionResponse[] = $state([]);
    let selected: string[] = $state([]);
    let user_self = $state(null);

    async function getSubmissions() {
        selected = [];

        await getMatchScoutingSubmissionsScoutingSubmissionsGet().then((res) => {
            if (res.status !== 200) {
                console.error(res)
                return
            } else {
                submissions = res.data

            }
        })
    }

    async function deleteSubmission(uuid: string, once: boolean = true) {
        await deleteMatchScoutingSubmissionScoutingSubmissionsDeleteSubmissionUuidDelete(uuid).then((res) => {
            if (res.status !== 200) {
                console.error(res)
                toast.error("Failed to delete submission", { duration: 5000 });
                return
            } else {
                if (once) {toast.success("Submission deleted", { duration: 5000 }); getSubmissions();}
            }
        })
    }

    async function deleteSelected() {
        for (const uuid of selected) {
            await deleteSubmission(uuid, false);
        }

        toast.success("Submissions deleted", { duration: 5000 });
        getSubmissions();
    }

    onMount(async () => {
        await getSubmissions();
    })
</script>

<div class="flex flex-col gap-4">
    <Card.Root class="w-auto">
        <Card.Header>
            <Card.Title>Match Scouting Submissions</Card.Title>
            <Card.Description>Manage match scouting submissions</Card.Description>
        </Card.Header>

        <Card.Content>
            <p>Found {submissions.length} submissions with a total of {submissions.reduce((sum, user) => sum + user.answers, 0)} answers</p>
        </Card.Content>
    </Card.Root>

    <Card.Root>
        <Card.Content class="flex flex-col gap-2">
            <div class="flex flex-row gap-2 items-center flex-wrap">
                <p>Selected {selected.length} submissions</p>
                <Button variant="outline" onclick={() => selected = submissions.map((user) => user.uuid)} disabled={selected.length == submissions.length}>Select All</Button>
                <Button variant="outline" onclick={() => selected = []} disabled={selected.length == 0}>Select None</Button>
                <Separator orientation="vertical" />
                <AlertDialog.Root>
                    <AlertDialog.Trigger>
                        <Button variant="destructive" disabled={selected.length == 0}>Delete {selected.length} submissions</Button>
                    </AlertDialog.Trigger>

                    <AlertDialog.Content>
                        <AlertDialog.Title>Delete {selected.length} submissions</AlertDialog.Title>
                        <AlertDialog.Description>
                            Are you sure you want to delete {selected.length} submissions? This action cannot be undone.
                        </AlertDialog.Description>
                        <AlertDialog.Footer>
                            <AlertDialog.Cancel type="button">Cancel</AlertDialog.Cancel>
                            <AlertDialog.Action type="button" onclick={deleteSelected}>Delete</AlertDialog.Action>
                        </AlertDialog.Footer>
                    </AlertDialog.Content>
                </AlertDialog.Root>
            </div>

            <Separator orientation="horizontal" />
            
            {#each submissions as submission}
                <Card.Root>
                    <Card.Content>
                        <div class="flex flex-col gap-2">
                            <div class="flex flex-row gap-2 items-center flex-wrap">
                                <input type="checkbox" bind:group={selected} value={submission.uuid} />
                                <p class="wrap-anywhere font-bold">{submission.answers} <span class="text-muted-foreground">answers for submission at</span> {submission.event_name} <span class="text-muted-foreground font-mono text-sm">{submission.event_code}</span></p>
                            </div>

                            <div class="flex flex-col gap-2 text-left flex-wrap">
                                <p class="wrap-anywhere"><span class="text-muted-foreground">Team:</span> {submission.team_number} <span class="text-muted-foreground">Match:</span> {submission.match_number}</p>
                                <p class="wrap-anywhere">{submission.match_type.charAt(0).toUpperCase() + submission.match_type.slice(1)} match</p>
                                <p class="text-sm text-muted-foreground">Created: {submission.created_at}</p>
                            </div>

                            <div class="flex flex-row gap-2 items-center flex-wrap">
                                <AlertDialog.Root>
                                    <AlertDialog.Trigger>
                                        <Button variant="destructive" size="sm">Delete</Button>
                                    </AlertDialog.Trigger>

                                    <AlertDialog.Content>
                                        <AlertDialog.Title>Delete Submission "{submission.uuid}"</AlertDialog.Title>
                                        <AlertDialog.Description>Are you sure you want to delete this submission? This action cannot be undone.</AlertDialog.Description>
                                        <AlertDialog.Footer>
                                            <AlertDialog.Cancel type="button">Cancel</AlertDialog.Cancel>
                                            <AlertDialog.Action type="button" onclick={() => deleteSubmission(submission.uuid)}>Delete</AlertDialog.Action>
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