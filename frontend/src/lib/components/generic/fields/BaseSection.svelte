<!-- 
@component
Wrapper component for managing an individual section

If editable, allows for editing and deleting the section, and adding child fields or sections.
Renders the name, description, and lets the user collapse the section.
Any child components are assumed to be a child fields for the section

Props:
    - `field` (`MatchScoutingFieldResponse`) - This field's data
    - `editable` (`boolean`) - If the field is editable or not
    - `getFields` (`() => void`) - Function for fetching fields again
    - `children` (`Snippet`) - Child components
-->
<script lang="ts">
	import { toast } from "svelte-sonner";
	import { slide } from "svelte/transition";
	import { dragHandle } from "svelte-dnd-action";
	import { CaretDownIcon, CaretUpIcon, DotsSixVerticalIcon, DotsThreeIcon, FolderPlusIcon, PencilIcon, PlusCircleIcon, TrashIcon } from "phosphor-svelte";

	import Button from "$lib/components/ui/button/button.svelte";
    import * as Card from "$lib/components/ui/card/index.js";
    import * as DropdownMenu from "$lib/components/ui/dropdown-menu/index.js";

	import { addFieldDialogOpen, addFieldParentUuid, addSectionDialogOpen, addSectionEditData, addSectionParentUuid } from "$lib/stores/dialog";
	import { deleteFieldFieldsDeleteFieldUuidDelete } from "$lib/api/match-scouting-fields/match-scouting-fields";
	import type { MatchScoutingFieldResponse } from "$lib/api/model";
	import type { Snippet } from "svelte";

    interface Props {
        field: MatchScoutingFieldResponse
        editable: boolean
        getFields: () => void
        children: Snippet
    }
    let { field: section, editable = false, getFields = () => {}, children }: Props = $props();

    let expanded = $state(true);

    /**
     * Edit this section
     */
    function editSection() {
        addSectionDialogOpen.set(true);
        addSectionEditData.set(section);
    }

    /**
     * Delete this section
     */
    async function deleteSection() {
        if (!section.uuid) {
            console.warn("Failed to delete section. No uuid.");
            toast.error("Failed to delete section", { duration: 5000 });
            return;
        }

        await deleteFieldFieldsDeleteFieldUuidDelete(section.uuid).catch((error) => {
            console.log("Failed to delete section", error)
            toast.error("Failed to delete section", { duration: 5000 });
        }).then(async () => {
            await getFields(); 
        });
    }

    /**
     * Open the dialog for adding a child field to this section
     */
    function addField() {
        if (!section.uuid) {
            console.warn("Failed to add child field to section. No uuid.");
            toast.error("Failed to add child field to section", { duration: 5000 });
            return;
        }

        addFieldDialogOpen.set(true); 
        addFieldParentUuid.set(section.uuid);
    }

    /**
     * Open the dialog for adding a child section to this section
     */
    function addSection() {
        if (!section.uuid) {
            console.warn("Failed to add child section to section. No uuid.");
            toast.error("Failed to add child section to section", { duration: 5000 });
            return;
        }

        addSectionDialogOpen.set(true);
        addSectionParentUuid.set(section.uuid);
    }
</script>


<Card.Root class="w-auto min-w-64">
    <Card.Header>
        <div class="flex flex-col gap-2 text-left">
            <div class="flex flex-row gap-2 items-center justify-between flex-wrap">
                <div class="flex flex-row gap-2 items-center">
                    {#if editable}
                        <div class="text-muted-foreground" use:dragHandle>
                            <DotsSixVerticalIcon weight="bold" />
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
                                <Button size="icon" variant="outline"><DotsThreeIcon weight="bold" /></Button>
                            </DropdownMenu.Trigger>
                            <DropdownMenu.Content class="w-56" align="start">
                                <DropdownMenu.Label>Section Options</DropdownMenu.Label>
                                <DropdownMenu.Group>
                                    <DropdownMenu.Item onclick={editSection}><PencilIcon weight="bold" /> Edit</DropdownMenu.Item>
                                    <DropdownMenu.Item onclick={deleteSection}><TrashIcon weight="bold" /> Delete</DropdownMenu.Item>
                                </DropdownMenu.Group>
                                <DropdownMenu.Separator />
                                <DropdownMenu.Group>
                                    <DropdownMenu.Item onclick={addField}><PlusCircleIcon weight="bold" /> Add Field</DropdownMenu.Item>
                                    <DropdownMenu.Item onclick={addSection}><FolderPlusIcon weight="bold" /> Add Section</DropdownMenu.Item>
                                </DropdownMenu.Group>
                            </DropdownMenu.Content>
                        </DropdownMenu.Root>
                    {/if}
                    <Button size="icon" variant="ghost" onclick={() => expanded = !expanded}>
                        {#if expanded}
                            <CaretDownIcon weight="bold" />
                        {:else}
                            <CaretUpIcon weight="bold" />
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