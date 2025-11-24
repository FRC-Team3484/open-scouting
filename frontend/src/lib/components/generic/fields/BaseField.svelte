<script lang="ts">
	import { apiFetch } from "$lib/utls/api";
	import { DotsThree, Pencil, Trash } from "phosphor-svelte";
    
	import Button from "$lib/components/ui/button/button.svelte";
    import * as Card from "$lib/components/ui/card/index.js";
    import * as DropdownMenu from "$lib/components/ui/dropdown-menu/index.js";
	import { addFieldDialogOpen, addFieldEditData, addFieldParentUuid } from "$lib/stores/dialog";

    let { field, editable = false, getFields = () => {}, children } = $props();

    async function deleteField() {
        await apiFetch(`/fields/delete/${field.uuid}`, {
            method: "DELETE",
            token: localStorage.getItem("access_token")
        })

        await getFields();
    }

    function editField() {
        addFieldDialogOpen.set(true);
        addFieldEditData.set(field);
    }
</script>


<Card.Root class="w-auto min-w-64">
    <Card.Header>
        <div class="flex flex-row gap-2 items-center justify-between flex-wrap">
            <div class="flex flex-row gap-2 items-center">
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
                        <Button size="icon" variant="outline"><DotsThree weight="bold" /></Button>
                    </DropdownMenu.Trigger>

                    <DropdownMenu.Content class="w-56" align="start">
                        <DropdownMenu.Label>Field Options</DropdownMenu.Label>
                        <DropdownMenu.Group>
                            <DropdownMenu.Item onclick={editField}><Pencil weight="bold" /> Edit</DropdownMenu.Item>
                            <DropdownMenu.Item onclick={deleteField}><Trash weight="bold" /> Delete</DropdownMenu.Item>
                        </DropdownMenu.Group>
                    </DropdownMenu.Content>
                </DropdownMenu.Root>
            {/if}
        </div>
    </Card.Header>

    <Card.Content>
        {@render children()}
    </Card.Content>
</Card.Root>