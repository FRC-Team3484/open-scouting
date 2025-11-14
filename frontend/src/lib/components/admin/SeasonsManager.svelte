<script lang="ts">
    import * as Card from "$lib/components/ui/card/index.js";
	import { apiFetch } from "$lib/utls/api";
	import { CheckCircle, PlusCircle, X } from "phosphor-svelte";
	import { onMount } from "svelte";
	import Separator from "../ui/separator/separator.svelte";
    import Button from "../ui/button/button.svelte";
    import * as Dialog from "../ui/dialog/index.js";
    import * as Field from "../ui/field/index.js";
    import Input from "../ui/input/input.svelte";

    import CustomDialog from "../generic/Dialog.svelte";
	import Checkbox from "../ui/checkbox/checkbox.svelte";
	import { toast } from "svelte-sonner";

    let seasons = [];

    let showDeleteDialog = false;
    let selectedSeason = null;

    async function deleteSeason() {
        showDeleteDialog = false;
        try {
            await apiFetch(`/seasons/delete/${selectedSeason.uuid}`, {
                method: "DELETE",
                token: localStorage.getItem("access_token")
            });

            toast.success("Season deleted", { duration: 5000 });
            await fetchSeasons();
        } catch (error) {
            console.error(error);
        }
        
    }

    async function addSeason(event: Event) {
        event.preventDefault();

        const form = event.currentTarget as HTMLFormElement;
        const formData = new FormData(form);

        // Convert checkbox and ensure everything is a string
        const body = new FormData();
        body.append("year", formData.get("year")!.toString());
        body.append("name", formData.get("name")!.toString());
        body.append("active", formData.get("active") ? "true" : "false");

        try {
            await apiFetch(`/seasons/create`, {
                method: "POST",
                data: body,
                token: localStorage.getItem("access_token")
            });

            toast.success("Season created", { duration: 5000 });
            await fetchSeasons();
        } catch (error) {
            console.error(error);
        }
    }

    async function fetchSeasons() {
        seasons = await apiFetch(`/seasons`);
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
                        <div class="flex flex-row gap-2 items-center">
                            {#if season.active}
                                <CheckCircle weight="bold" />
                            {/if}
                            <p>{season.year}</p>
                            <p>{season.label}</p>
                            <Separator orientation="vertical" />
                            <Button size="icon" variant="destructive" onclick={() => {showDeleteDialog = true; selectedSeason = season}}><X weight="bold"/></Button>
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

                    <form method="post" on:submit={addSeason}>
                        <Field.Group>
                            <Field.Set>
                                <Field.Field>
                                    <Field.Label>Year</Field.Label>
                                    <Input type="number" name="year" defaultValue={new Date().getFullYear()} required />
                                </Field.Field>
                                <Field.Field>
                                    <Field.Label>Name</Field.Label>
                                    <Input type="text" name="name" required />
                                </Field.Field>

                                <Field.Field orientation="horizontal">
                                    <Checkbox id="active" checked name="active"/>
                                    <Field.Content>
                                        <Field.Label for="active">
                                            Make active season
                                        </Field.Label>
                                        <Field.Description>
                                            Make this season the active (default) season. The other seasons will be deactivated.
                                        </Field.Description>
                                    </Field.Content>
                                </Field.Field>
                            </Field.Set>
                        </Field.Group>

                        <Dialog.Footer>
                            <Dialog.Close>
                                <Button type="submit">Submit</Button>
                            </Dialog.Close>
                        </Dialog.Footer>
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