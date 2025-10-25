<script lang="ts">
	import Button from "$lib/components/ui/button/button.svelte";
    import * as Card from "$lib/components/ui/card/index.js";
	import { apiFetch } from "$lib/utls/api";
	import { Pencil, Trash } from "phosphor-svelte";

    let { field, editable = false, getFields = () => {}, children } = $props();

    async function deleteField() {
        await apiFetch(`/fields/delete/${field.uuid}`, {
            method: "DELETE",
            token: localStorage.getItem("access_token")
        })

        await getFields();
    }
</script>


<Card.Root class="w-auto min-w-64">
    <Card.Header>
        <div class="flex flex-row gap-2 items-center justify-between">
            <div class="flex flex-row gap-2 items-center">
                <p>{field.name}</p>
                {#if editable}
                    <p class="text-sm opacity-80">{field.field_type}</p>
                {/if}
            </div>

            {#if editable}
                <div class="flex flex-row gap-2 items-center">
                    <Button size="icon" variant="outline"><Pencil weight="bold" /></Button>
                    <Button size="icon" variant="destructive" onclick={deleteField}><Trash weight="bold" /></Button>
                </div>
            {/if}
        </div>
    </Card.Header>

    <Card.Content>
        {@render children()}
    </Card.Content>
</Card.Root>