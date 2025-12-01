<script lang="ts">
    import * as Card from "$lib/components/ui/card/index.js";
	import { apiFetch } from "$lib/utils/api";
	import { onMount } from "svelte";
	import Button from "../ui/button/button.svelte";
	import { PlusCircle, X } from "phosphor-svelte";
    import * as Dialog from "$lib/components/ui/dialog/index.js";
    import * as Field from "$lib/components/ui/field/index.js";
	import Separator from "../ui/separator/separator.svelte";
	import Input from "../ui/input/input.svelte";
    import * as AlertDialog from "$lib/components/ui/alert-dialog/index.js";

    export let season_uuid: string = "";

    let game_pieces = [];

    async function getGamePieces() {
        game_pieces = await apiFetch(`/gamepieces/season/${season_uuid}`);
    }

    async function createGamePiece(event: Event) {
        event.preventDefault();

        const form = event.currentTarget as HTMLFormElement;
        const formData = new FormData(form);

        const body = new FormData();
        body.append("name", formData.get("name")!.toString());
        body.append("season_uuid", season_uuid);

        await apiFetch(`/gamepieces/create`, {
            method: "POST",
            data: body,
            token: localStorage.getItem("access_token")
        });
        getGamePieces();
    }

    async function deleteGamePiece(uuid: string) {
        await apiFetch(`/gamepieces/delete/${uuid}`, {
            method: "DELETE",
            token: localStorage.getItem("access_token")
        });
        getGamePieces();
    }

    onMount(async () => {
        while (!season_uuid) {
            await new Promise(resolve => setTimeout(resolve, 100));
        }
        getGamePieces();
    })
</script>

<Card.Root>
    <Card.Header>
        <Card.Title>Game Pieces</Card.Title>
        <Card.Description>A game piece should be created for each game piece that will be used in the fields for a season</Card.Description>
    </Card.Header>

    <Card.Content>
        <div class="flex flex-col gap-4">
            {#if game_pieces.length == 0}
                <p class="text-sm opacity-80">No game pieces found</p>
            {:else}
                {#each game_pieces as game_piece}
                    <Card.Root class="w-auto min-w-64">

                        <Card.Content>
                            <div class="flex flex-row gap-2 items-center justify-between">
                                <p>{game_piece.name}</p>
                                <AlertDialog.Root>
                                    <AlertDialog.Trigger>
                                        <Button variant="destructive" size="icon"><X weight="bold" /></Button>
                                    </AlertDialog.Trigger>
                                    <AlertDialog.Content>
                                        <AlertDialog.Header>
                                            <AlertDialog.Title>Are you sure?</AlertDialog.Title>
                                            <AlertDialog.Description>This will permanently delete the game piece, and is not reversible. This may temporarially break fields that rely on this game piece.</AlertDialog.Description>
                                        </AlertDialog.Header>
                                        <AlertDialog.Footer>
                                            <AlertDialog.Cancel type="button">Cancel</AlertDialog.Cancel>
                                            <AlertDialog.Action type="button" onclick={() => deleteGamePiece(game_piece.uuid)}>Delete</AlertDialog.Action>
                                        </AlertDialog.Footer>
                                    </AlertDialog.Content>
                                </AlertDialog.Root>
                            </div>
                        </Card.Content>
                    </Card.Root>
                {/each}
            {/if}
            
            <Dialog.Root>
                <Dialog.Trigger>
                    <Button><PlusCircle weight="bold" /> Add Game Piece</Button>
                </Dialog.Trigger>

                <Dialog.Content class="overflow-y-scroll max-h-[calc(100vh-2rem)]">
                    <Dialog.Header>
                        <Dialog.Title>Add Game Piece</Dialog.Title>
                        <Dialog.Description>Create a new game piece</Dialog.Description>
                    </Dialog.Header>

                    <form method="post" on:submit={createGamePiece} class="flex flex-col gap-4">
                        <Field.Group class="gap-4">
                            <Field.Set class="flex flex-col gap-2">
                                <Field.Label>Name</Field.Label>
                                <Input type="text" name="name" label="Name" required />
                                <Field.Description>The name of the game piece</Field.Description>
                            </Field.Set>
                        </Field.Group>

                        <Dialog.Footer>
                            <Dialog.Close>
                                <Button type="submit">Create</Button>
                            </Dialog.Close>
                        </Dialog.Footer>
                    </form>
                </Dialog.Content>
            </Dialog.Root>
        </div>
    </Card.Content>
</Card.Root>