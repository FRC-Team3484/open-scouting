<!-- 
@component
Wrapper component for all match scouting fields

If editable, allows for editing and deleting the field. 
Renders the name, description, and if the field is required or not.
Any child components are assumed to be a part of the field specific data.

Props:
    - `field` (`MatchScoutingFieldResponse`) - This field's data
    - `editable` (`boolean`) - If the field is editable or not
    - `getFields` (`() => void`) - Function for fetching fields again
    - `children` (`Snippet`) - Child components
-->
<script lang="ts">
	import { toast } from "svelte-sonner";
	import { DotsSixVerticalIcon, DotsThreeIcon, PencilIcon, TrashIcon } from "phosphor-svelte";
	import { dragHandle } from "svelte-dnd-action";
	import type { Snippet } from "svelte";
    
	import Button from "$lib/components/ui/button/button.svelte";
    import * as Card from "$lib/components/ui/card/index.js";
    import * as DropdownMenu from "$lib/components/ui/dropdown-menu/index.js";

	import { addFieldDialogOpen, addFieldEditData } from "$lib/stores/dialog";
	import { deleteFieldFieldsDeleteFieldUuidDelete } from "$lib/api/match-scouting-fields/match-scouting-fields";
	import type { MatchScoutingFieldResponse } from "$lib/api/model";


    interface Props {
        field: MatchScoutingFieldResponse
        editable: boolean
        getFields: () => void
        children: Snippet
    }
    let { field, editable = false, getFields = () => {}, children }: Props = $props();

    /**
     * Delete this field
     */
    async function deleteField() {
        if (!field.uuid) {
            console.warn("Failed to delete field. No uuid.");
            toast.error("Failed to delete field", { duration: 5000 });
            return;
        }

        await deleteFieldFieldsDeleteFieldUuidDelete(field.uuid).catch((error) => {
            console.warn("Failed to delete field", error);
            toast.error("Failed to delete field", { duration: 5000 });
        }).then(async () => {
            await getFields(); 
        });
    }

    /**
     * Edit this field
     */
    function editField() {
        addFieldDialogOpen.set(true);
        addFieldEditData.set(field);
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
                    <p>
                        {field.name}
                        {#if field.required}
                            <span class="text-red-500">*</span>
                        {/if}
                    </p>
                    {#if editable}
                        <p class="text-sm opacity-80">{field.field_type}</p>
                    {/if}
                </div>
                {#if editable}
                    <DropdownMenu.Root>
                        <DropdownMenu.Trigger>
                            <Button size="icon" variant="outline"><DotsThreeIcon weight="bold" /></Button>
                        </DropdownMenu.Trigger>
                        <DropdownMenu.Content class="w-56" align="start">
                            <DropdownMenu.Label>Field Options</DropdownMenu.Label>
                            <DropdownMenu.Group>
                                <DropdownMenu.Item onclick={editField}><PencilIcon weight="bold" /> Edit</DropdownMenu.Item>
                                <DropdownMenu.Item onclick={deleteField}><TrashIcon weight="bold" /> Delete</DropdownMenu.Item>
                            </DropdownMenu.Group>
                        </DropdownMenu.Content>
                    </DropdownMenu.Root>
                {/if}
            </div>

            {#if field.description}
                <p class="text-sm text-muted-foreground">{field.description}</p>
            {/if}
        </div>
    </Card.Header>

    <Card.Content>
        {@render children()}
    </Card.Content>
</Card.Root>