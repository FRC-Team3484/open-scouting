<!-- 
@component
Component for managing and creating seasons on the admin page

Allows a superuser to create a new season, make a season the active one, and delete seasons
-->
<script lang="ts">
	import { onMount } from "svelte";
	import { toast } from "svelte-sonner";
	import { CheckCircleIcon, PlusCircleIcon, TrashIcon } from "phosphor-svelte";
	import { zod4Client } from "sveltekit-superforms/adapters";
	import { superForm } from "sveltekit-superforms";

	import Separator from "../ui/separator/separator.svelte";
    import Button from "../ui/button/button.svelte";
    import * as Dialog from "../ui/dialog/index.js";
    import Input from "../ui/input/input.svelte";
    import * as Form from "../ui/form/index.js";
    import * as Card from "$lib/components/ui/card/index.js";
	import Checkbox from "../ui/checkbox/checkbox.svelte";
	import Label from "../ui/label/label.svelte";
	import Badge from "../ui/badge/badge.svelte";
    import * as AlertDialog from "../ui/alert-dialog/index.js";

	import { CreateSeasonSeasonsCreatePostBody } from "$lib/zod/seasons/seasons";
	import { activateSeasonSeasonsActivateSeasonUuidPost, createSeasonSeasonsCreatePost, deleteSeasonSeasonsDeleteSeasonUuidDelete, getSeasonsSeasonsGet } from "$lib/api/seasons/seasons";
	import type { SeasonResponse } from "$lib/api/model";


    let seasons: SeasonResponse[] = [];

    const createSeasonDefaultValues = {
        year: new Date().getFullYear(),
        name: "",
        active: false
    }
    const createSeasonForm = superForm(createSeasonDefaultValues, {
        SPA: true,
        validators: zod4Client(CreateSeasonSeasonsCreatePostBody),
        async onUpdate({ form }) {
            if (form.valid) {
                await createSeasonSeasonsCreatePost(form.data).then((request) => {
                    if (request.status === 200) {
                        toast.success("Season created", { duration: 5000 });
                        fetchSeasons();
                    } else {
                        toast.error("Failed to create season", { duration: 5000 });
                    }
                })
            }
        }
    })
    const { form: formData, enhance } = createSeasonForm

    /**
     * Delete a season from the server
     * 
     * @param season The season to delete
     */
    async function deleteSeason(season: SeasonResponse) {
        try {
            await deleteSeasonSeasonsDeleteSeasonUuidDelete(season.uuid);

            toast.success("Season deleted", { duration: 5000 });
            await fetchSeasons();
        } catch (error) {
            console.error(error);
        }
        
    }

    /**
     * Mark a season as active on the server
     * @param seasonUuid
     */
    async function activateSeason(season: SeasonResponse) {
        await activateSeasonSeasonsActivateSeasonUuidPost(season.uuid).then((response) => {
            if (response.status !== 200) {
                toast.error("Failed to activate season", { duration: 5000 });
            } else {
                toast.success("Season activated", { duration: 5000 });
                fetchSeasons();
            }
        });
    }

    /**
     * Fetch all seasons from the server
     */
    async function fetchSeasons() {
        seasons = (await getSeasonsSeasonsGet()).data;
    }

    onMount(async () => {
        await fetchSeasons();
    });
</script>


<Card.Root class="w-auto min-w-64">
    <Card.Header>
        <Card.Title>Seasons</Card.Title>
        <Card.Description>Manage seasons</Card.Description>
    </Card.Header>

    <Card.Content>
        <div class="flex flex-col gap-4">
            {#each seasons as season}
                <Card.Root>
                    <Card.Content>
                        <div class="flex flex-row gap-2 items-center justify-between">
                            <div class="flex flex-row gap-2 items-center">
                                {#if season.active}
                                    <Badge><CheckCircleIcon weight="bold" /> Active</Badge>
                                {/if}
                                <p>{season.year}</p>
                                <p class="font-bold">{season.name}</p>
                                <Separator orientation="vertical" />
                            </div>
                            {#if !season.active}
                                <Button size="sm" variant="outline" onclick={() => {activateSeason(season)}}><CheckCircleIcon weight="bold"/> Activate</Button>
                            {/if}
                            <AlertDialog.Root>
                                <AlertDialog.Trigger>
                                    <Button variant="destructive"><TrashIcon weight="bold"/> Delete</Button>
                                </AlertDialog.Trigger>

                                <AlertDialog.Content>
                                    <AlertDialog.Title>Delete Season</AlertDialog.Title>
                                    <p>Are you sure you want to delete this season?</p>
                                    <ul class="list-disc list-inside">
                                        <li>This action cannot be undone</li>
                                        <li>Deleting a season will break database references for match scouting fields, pit scouting questions, and all user submitted data for that season</li>
                                        <li>Manual database intervention is required to restore this data</li>
                                    </ul>
                                    <p>Please ensure you know what you're doing before proceeding.</p>

                                    <AlertDialog.Footer>
                                        <AlertDialog.Cancel>Close</AlertDialog.Cancel>
                                        <AlertDialog.Action onclick={() => {deleteSeason(season)}}>Delete</AlertDialog.Action>
                                    </AlertDialog.Footer>
                                </AlertDialog.Content>
                            </AlertDialog.Root>
                        </div>
                    </Card.Content>
                </Card.Root>
            {/each}

            <Dialog.Root>
                <Dialog.Trigger>
                    <Button><PlusCircleIcon weight="bold" />Add Season</Button>
                </Dialog.Trigger>

                <Dialog.Content>
                    <Dialog.Title>Add Season</Dialog.Title>
                    <Dialog.Description>Create a new season</Dialog.Description>

                    <form method="post" use:enhance>
                        <Form.Field form={createSeasonForm} name="year">
                            <Form.Control>
                                {#snippet children({ props })}
                                    <Label>Year</Label>
                                    <Input {...props} bind:value={$formData.year} type="number" />
                                {/snippet}
                            </Form.Control>
                            <Form.Description>The year of the season</Form.Description>
                            <Form.FieldErrors />
                        </Form.Field>

                        <Form.Field form={createSeasonForm} name="name">
                            <Form.Control>
                                {#snippet children({ props })}
                                    <Label>Name</Label>
                                    <Input {...props} bind:value={$formData.name} />
                                {/snippet}
                            </Form.Control>
                            <Form.Description>The name of the season</Form.Description>
                            <Form.FieldErrors />
                        </Form.Field>

                        <Form.Field form={createSeasonForm} name="active">
                            <Form.Control>
                                {#snippet children({ props })}
                                    <Label>Active</Label>
                                    <Checkbox {...props} bind:checked={$formData.active} />
                                {/snippet}
                            </Form.Control>
                            <Form.Description>Make this season the active (default) season. The other seasons will be deactivated.</Form.Description>
                            <Form.FieldErrors />
                        </Form.Field>

                        <Dialog.Close>
                            <Form.Button type="submit">Create Season</Form.Button>
                        </Dialog.Close>
                    </form>
                </Dialog.Content>
            </Dialog.Root>
        </div>
    </Card.Content>
</Card.Root>