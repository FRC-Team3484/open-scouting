<script lang="ts">
	import { deleteFieldFieldsDeleteFieldUuidDelete } from "$lib/api/match-scouting-fields/match-scouting-fields";
	import Button from "$lib/components/ui/button/button.svelte";
    import * as Card from "$lib/components/ui/card/index.js";
    import * as DropdownMenu from "$lib/components/ui/dropdown-menu/index.js";
	import { addFieldDialogOpen, addFieldParentUuid, addSectionDialogOpen, addSectionEditData, addSectionParentUuid } from "$lib/stores/dialog";
	import { CaretDown, CaretUp, DotsSixVertical, DotsThree, FolderPlus, Pencil, PlusCircle, Trash } from "phosphor-svelte";
	import { dragHandle } from "svelte-dnd-action";
	import { toast } from "svelte-sonner";
	import { slide } from "svelte/transition";

    let { field: section, editable = false, getFields = () => {}, children } = $props();

    let expanded = $state(true);

    function editSection() {
        addSectionDialogOpen.set(true);
        addSectionEditData.set(section);
    }

    async function deleteSection() {
        await deleteFieldFieldsDeleteFieldUuidDelete(section.uuid).catch((error) => {
            console.log("Failed to delete section", error)
            toast.error("Failed to delete section", { duration: 5000 });
        }).then(async () => {
            await getFields(); 
        });
    }

    function addField() {}

    async function addSection() {}
</script>


<Card.Root class="w-auto min-w-64">
    <Card.Header>
        <div class="flex flex-col gap-2 text-left">
            <div class="flex flex-row gap-2 items-center justify-between flex-wrap">
                <div class="flex flex-row gap-2 items-center">
                    {#if editable}
                        <div class="text-muted-foreground" use:dragHandle>
                            <DotsSixVertical weight="bold" />
                        </div>
                    {/if}
                    <p>{section.name}</p>
                    {#if editable}
                        <p class="text-sm opacity-80">{section.field_type}</p>
                    {/if}
                </div>
                <div class="flex flex-row gap-2 items-center">
                    {#if editable}
                        <DropdownMenu.Root>
                            <DropdownMenu.Trigger>
                                <Button size="icon" variant="outline"><DotsThree weight="bold" /></Button>
                            </DropdownMenu.Trigger>
                            <DropdownMenu.Content class="w-56" align="start">
                                <DropdownMenu.Label>Section Options</DropdownMenu.Label>
                                <DropdownMenu.Group>
                                    <DropdownMenu.Item onclick={editSection}><Pencil weight="bold" /> Edit</DropdownMenu.Item>
                                    <DropdownMenu.Item onclick={deleteSection}><Trash weight="bold" /> Delete</DropdownMenu.Item>
                                </DropdownMenu.Group>
                                <DropdownMenu.Separator />
                                <DropdownMenu.Group>
                                    <DropdownMenu.Item onclick={() => {addFieldDialogOpen.set(true); addFieldParentUuid.set(section.uuid)}}><PlusCircle weight="bold" /> Add Field</DropdownMenu.Item>
                                    <DropdownMenu.Item onclick={() => {addSectionDialogOpen.set(true); addSectionParentUuid.set(section.uuid)}}><FolderPlus weight="bold" /> Add Section</DropdownMenu.Item>
                                </DropdownMenu.Group>
                            </DropdownMenu.Content>
                        </DropdownMenu.Root>
                    {/if}
                    <Button size="icon" variant="ghost" onclick={() => expanded = !expanded}>
                        {#if expanded}
                            <CaretDown weight="bold" />
                        {:else}
                            <CaretUp weight="bold" />
                        {/if}
                    </Button>
                </div>
            </div>

            {#if section.description}
                <p class="text-sm text-muted-foreground">{section.description}</p>
            {/if}
        </div>
    </Card.Header>

    <Card.Content>
        {#if expanded}
            <div transition:slide>
                {@render children()}
            </div>
        {/if}
    </Card.Content>
</Card.Root>