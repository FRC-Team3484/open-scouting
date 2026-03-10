<script lang="ts">
    import { onMount } from "svelte";
	import { toast } from "svelte-sonner";

	import { PlusCircle, X } from "phosphor-svelte";
    import * as Card from "$lib/components/ui/card/index.js";
    import * as Dialog from "$lib/components/ui/dialog/index.js";
	import Button from "../ui/button/button.svelte";
	import Input from "../ui/input/input.svelte";
    import * as AlertDialog from "$lib/components/ui/alert-dialog/index.js";
    import * as Form from "$lib/components/ui/form/index.js";

    import { getSeasonGamepiecesGamepiecesSeasonSeasonUuidGet, createGamepieceGamepiecesCreatePost, deleteGamepieceGamepiecesDeleteGamepieceUuidDelete } from "$lib/api/gamepieces/gamepieces"
    import { type GamepieceResponse } from "$lib/api/model";
    import { CreateGamepieceGamepiecesCreatePostBody } from "$lib/zod/gamepieces/gamepieces";
	import { superForm } from "sveltekit-superforms";
	import { zod4Client } from "sveltekit-superforms/adapters";
	import Label from "../ui/label/label.svelte";

    let { season_uuid } = $props();

    let game_pieces: GamepieceResponse[] = $state([]);

    const form = superForm(
        {
            season_uuid: season_uuid,
            name: ""
        },
        {   
            SPA: true,
            validators: zod4Client(CreateGamepieceGamepiecesCreatePostBody),
            async onUpdate({ form }) {
                if (form.valid) {
                    await createGamepieceGamepiecesCreatePost($formData).then((request) => {
                        if (request.status === 200) {
                            console.log("ah")
                            getGamePieces();
                        } else {
                            toast.error("Failed to create game piece", { duration: 5000 });
                        }
                    });
                }
            }
        }
    )
    const { form: formData, enhance } = form

    async function getGamePieces() {
        const response = await getSeasonGamepiecesGamepiecesSeasonSeasonUuidGet(season_uuid);
        if (response.status === 200) {
            game_pieces = response.data;
        } else {
            toast.error("Failed to get game pieces", { duration: 5000 });
        }
    }

    async function deleteGamePiece(uuid: string) {
        await deleteGamepieceGamepiecesDeleteGamepieceUuidDelete(uuid).then((request) => {
            if (request.status === 200) {
                getGamePieces();
            } else {
                toast.error("Failed to delete game piece", { duration: 5000 });
            }
        });
    }

    onMount(async () => {
        while (!season_uuid) {
            await new Promise(resolve => setTimeout(resolve, 100));
        }
        getGamePieces();
    });

    $effect(() => {
        season_uuid;
        getGamePieces();
    });
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

                    <form use:enhance class="flex flex-col gap-4">
                        <Form.Field {form} name="name">
                            <Form.Control>
                                {#snippet children({ props })}
                                    <Label>Name</Label>
                                    <Input {...props} bind:value={$formData.name} />
                                {/snippet}
                            </Form.Control>
                            <Form.Description>The name of the game piece</Form.Description>
                            <Form.FieldErrors />
                        </Form.Field>

                        <Dialog.Close>
                            <Button type="submit">Create</Button>
                        </Dialog.Close>
                    </form>
                </Dialog.Content>
            </Dialog.Root>
        </div>
    </Card.Content>
</Card.Root>