<script lang="ts">
    import { addSectionDialogOpen, addSectionParentUuid } from "$lib/stores/dialog";
	import { apiFetch } from "$lib/utls/api";
    
    import * as Field from "$lib/components/ui/field";
    import * as Dialog from "$lib/components/ui/dialog";
	import { Input } from "$lib/components/ui/input";
	import Button from "$lib/components/ui/button/button.svelte";

    import BaseDialog from "./BaseDialog.svelte";

    let { open = $bindable(), season_uuid, getStructure } = $props();

    async function createSection(event: Event) {
        event.preventDefault();

        const form = event.currentTarget as HTMLFormElement;
        const formData = new FormData(form);

        const body = new FormData();
        body.append("name", formData.get("name")!.toString());
        body.append("field_type", "section")
        body.append("stat_type", "section")
        body.append("game_piece_uuid", "");
        body.append("required", "false");
        body.append("options", JSON.stringify([]));
        body.append("order", "0");
        body.append("organization_uuid", "");
        body.append("parent_uuid", $addSectionParentUuid);

        try {
            const response = await apiFetch(`/fields/season/${season_uuid}/create`, {
                method: "POST",
                data: body,
                token: localStorage.getItem("access_token")
            });

            addSectionParentUuid.set("");
            getStructure();
        } catch (error) {
            console.error(error);
        }
    }
</script>

<BaseDialog title="Add Section" description="Create a new section" bind:open={$addSectionDialogOpen}>
    <form method="post" on:submit={createSection} class="flex flex-col gap-4">
        <Field.Group class="gap-4">
            <Field.Set class="flex flex-col gap-2">
                <Field.Label>Name</Field.Label>
                <Input type="text" name="name" required />
                <Field.Description>The name of the section</Field.Description>
            </Field.Set>
        </Field.Group>

        <Dialog.Footer>
            <Button type="submit">Create</Button>
        </Dialog.Footer>
    </form>
</BaseDialog>