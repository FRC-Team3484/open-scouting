<script lang="ts">
	import { onMount } from "svelte";
	import { toast } from "svelte-sonner";
	import { CheckCircle, PlusCircle, Trash } from "phosphor-svelte";
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

    import CustomDialog from "../generic/Dialog.svelte";

	import { CreateSeasonSeasonsCreatePostBody } from "$lib/zod/seasons/seasons";
	import { activateSeasonSeasonsActivateSeasonUuidPost, createSeasonSeasonsCreatePost, deleteSeasonSeasonsDeleteSeasonUuidDelete, getSeasonsSeasonsGet } from "$lib/api/seasons/seasons";
	import type { SeasonResponse } from "$lib/api/model";

    let seasons: SeasonResponse[] = [];

    let showDeleteDialog: boolean = false;
    let selectedSeason: SeasonResponse | null = null;

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

    async function deleteSeason() {
        showDeleteDialog = false;
        if (!selectedSeason) {
            return;
        }

        try {
            await deleteSeasonSeasonsDeleteSeasonUuidDelete(selectedSeason.uuid);

            toast.success("Season deleted", { duration: 5000 });
            await fetchSeasons();
        } catch (error) {
            console.error(error);
        }
        
    }

    async function activateSeason(seasonUuid: string) {
        await activateSeasonSeasonsActivateSeasonUuidPost(seasonUuid).then((response) => {
            if (response.status !== 200) {
                toast.error("Failed to activate season", { duration: 5000 });
            } else {
                toast.success("Season activated", { duration: 5000 });
                fetchSeasons();
            }
        });
    }

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
                                    <Badge><CheckCircle weight="bold" /> Active</Badge>
                                {/if}
                                <p>{season.year}</p>
                                <p class="font-bold">{season.name}</p>
                                <Separator orientation="vertical" />
                            </div>
                            {#if !season.active}
                                <Button size="sm" variant="outline" onclick={() => {activateSeason(season.uuid)}}><CheckCircle weight="bold"/> Activate</Button>
                            {/if}
                            <Button size="sm" variant="destructive" onclick={() => {showDeleteDialog = true; selectedSeason = season}}><Trash weight="bold"/> Delete</Button>
                        </div>
                    </Card.Content>
                </Card.Root>
            {/each}

            <Dialog.Root>
                <Dialog.Trigger>
                    <Button><PlusCircle weight="bold" />Add Season</Button>
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

<CustomDialog
    bind:open={showDeleteDialog}
    title="Delete Season"
    description="Are you sure you want to delete this season? This action cannot be undone, and may break things and cause data loss for match and pit scouting fields, and collected data relating to this season. Ensure you know what you're doing before proceeding."
    cancel_text="Cancel"
    submit_text="Delete"
    onSubmit={deleteSeason}
>
</CustomDialog>