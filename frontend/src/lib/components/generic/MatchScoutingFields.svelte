<script lang="ts">
	import { apiFetch } from "$lib/utls/api";
	import { onMount } from "svelte";
	import Skeleton from "../ui/skeleton/skeleton.svelte";
	import { FolderPlus, PlusCircle } from "phosphor-svelte";
    import * as Card from "$lib/components/ui/card/index.js";
    import * as Dialog from "$lib/components/ui/dialog/index.js";
	import Button from "../ui/button/button.svelte";
	import Separator from "../ui/separator/separator.svelte";

    let fields = [];

    export let season_uuid: string = "";
    export let editable: boolean = false;

    async function get_fields() {
        if (!season_uuid) return;
        fields = await apiFetch(`/fields/season/${season_uuid}`);
    }

    onMount(async () => {
        get_fields();
    });
</script>

<div class="flex flex-col gap-4">
    {#if season_uuid === ""}
        <Skeleton class="w-128 h-32" />
        <Skeleton class="w-128 h-32" />
        <Skeleton class="w-128 h-32" />
    {:else}
        <Separator />

        <Card.Root class="w-auto min-w-64">
            <Card.Content>
                <div class="flex flex-col gap-4">
                    <Dialog.Root>
                        <Dialog.Trigger>
                            <Button><PlusCircle weight="bold" /> Add Field</Button>
                        </Dialog.Trigger>

                        <Dialog.Content>
                            <Dialog.Header>
                                <Dialog.Title>Add Field</Dialog.Title>
                                <Dialog.Description>Create a new field</Dialog.Description>
                            </Dialog.Header>

                            <Dialog.Footer>
                                <Button type="submit">Create</Button>
                            </Dialog.Footer>
                        </Dialog.Content>
                    </Dialog.Root>

                    <Dialog.Root>
                        <Dialog.Trigger>
                            <Button><FolderPlus weight="bold" /> Add Section</Button>
                        </Dialog.Trigger>

                        <Dialog.Content>
                            <Dialog.Header>
                                <Dialog.Title>Add Section</Dialog.Title>
                                <Dialog.Description>Create a new section</Dialog.Description>
                            </Dialog.Header>

                            <Dialog.Footer>
                                <Button type="submit">Create</Button>
                            </Dialog.Footer>
                        </Dialog.Content>
                    </Dialog.Root>
                </div>
            </Card.Content>
        </Card.Root>

        {#each fields as field}
            <p>field</p>
        {/each}
    {/if}
</div>