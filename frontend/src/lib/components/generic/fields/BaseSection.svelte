<script lang="ts">
	import Button from "$lib/components/ui/button/button.svelte";
    import * as Card from "$lib/components/ui/card/index.js";
	import { addFieldDialogOpen, addFieldParentUuid, addSectionDialogOpen, addSectionParentUuid } from "$lib/stores/dialog";
	import { apiFetch } from "$lib/utls/api";
	import { FolderPlus, Pencil, PlusCircle, Trash } from "phosphor-svelte";

    let { field: section, editable = false, getFields = () => {}, children } = $props();

    async function editSection() {}

    async function deleteSection() {
        await apiFetch(`/fields/delete/${section.uuid}`, {
            method: "DELETE",
            token: localStorage.getItem("access_token")
        })

        await getFields();
    }

    function addField() {}

    async function addSection() {}
</script>


<Card.Root class="w-auto min-w-64">
    <Card.Header>
        <div class="flex flex-row gap-2 items-center justify-between flex-wrap">
            <div class="flex flex-row gap-2 items-center">
                <p>{section.name}</p>
                {#if editable}
                    <p class="text-sm opacity-80">{section.field_type}</p>
                {/if}
            </div>

            {#if editable}
                <div class="flex flex-row gap-2 items-center">
                    <Button size="icon" variant="outline"><Pencil weight="bold" /></Button>
                    <Button size="icon" variant="destructive" onclick={deleteSection}><Trash weight="bold" /></Button>
                    <Button size="icon" variant="default" onclick={() => {addFieldDialogOpen.set(true); addFieldParentUuid.set(section.uuid)}}><PlusCircle weight="bold" /></Button>
                    <Button size="icon" variant="default" onclick={() => {addSectionDialogOpen.set(true); addSectionParentUuid.set(section.uuid)}}><FolderPlus weight="bold" /></Button>
                </div>
            {/if}
        </div>
    </Card.Header>

    <Card.Content>
        {@render children()}
    </Card.Content>
</Card.Root>