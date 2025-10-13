<script lang="ts">
    import * as Card from "$lib/components/ui/card/index.js";
	import { apiFetch } from "$lib/utls/api";
	import { CheckCircle, PlusCircle, X } from "phosphor-svelte";
	import { onMount } from "svelte";
	import Separator from "../ui/separator/separator.svelte";
    import Button from "../ui/button/button.svelte";
    import * as Dialog from "../ui/dialog/index.js";

    import CustomDialog from "../generic/Dialog.svelte";

    let seasons = [];

    let showDeleteDialog = false;
    let selectedSeason = null;

    function deleteSeason() {
        showDeleteDialog = false;
        console.log("ACTION")
        console.log(selectedSeason)
    }

    onMount(async () => {
        seasons = await apiFetch(`/seasons`);
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

                    <form method="post">
                        <Dialog.Footer>
                            <Button>Submit</Button>
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