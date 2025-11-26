<script lang="ts">
    import { addSectionDialogOpen, addSectionEditData, addSectionParentUuid } from "$lib/stores/dialog";
	import { apiFetch } from "$lib/utls/api";
    
    import * as Field from "$lib/components/ui/field";
    import * as Dialog from "$lib/components/ui/dialog";
	import { Input } from "$lib/components/ui/input";
	import Button from "$lib/components/ui/button/button.svelte";

    import BaseDialog from "./BaseDialog.svelte";

    let { open = $bindable(), season_uuid, getStructure } = $props();

    let addSectionAnswers = $state({
        name: "",
    });

    let dialogTitle = $state("Add Section");
    let dialogDescription = $state("Create a new section");

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
            if (Object.keys($addSectionEditData).length > 0) {
                await apiFetch(`/fields/season/${season_uuid}/edit/${$addSectionEditData.uuid}`, {
                    method: "POST",
                    data: body,
                    token: localStorage.getItem("access_token")
                });
            } else {
                await apiFetch(`/fields/season/${season_uuid}/create`, {
                    method: "POST",
                    data: body,
                    token: localStorage.getItem("access_token")
                });
            }

            addSectionParentUuid.set("");
            addSectionDialogOpen.set(false);
            getStructure();
        } catch (error) {
            console.error(error);
        }
    }

    function onOpenChange() {
        if ($addSectionDialogOpen === false) {
            addSectionParentUuid.set("");
            addSectionEditData.set({});

            addSectionAnswers = {
                name: "",
            }

            dialogTitle = "Add Section";
            dialogDescription = "Create a new section";
        } else {
            const data = $addSectionEditData;
            if (data && Object.keys(data).length > 0) {
                addSectionAnswers.name = data.name ?? "";
                dialogTitle = "Edit Section";
                dialogDescription = `Editing section '${addSectionAnswers.name}'`;

                addSectionParentUuid.set("")
            }
        }
    }
</script>

<BaseDialog title="Add Section" description="Create a new section" bind:open={$addSectionDialogOpen} onOpenChange={onOpenChange}>
    <form method="post" on:submit={createSection} class="flex flex-col gap-4">
        <Field.Group class="gap-4">
            <Field.Set class="flex flex-col gap-2">
                <Field.Label>Name</Field.Label>
                <Input type="text" name="name" required bind:value={addSectionAnswers.name} />
                <Field.Description>The name of the section</Field.Description>
            </Field.Set>
        </Field.Group>

        <Dialog.Footer>
            <Button type="submit">Create</Button>
        </Dialog.Footer>
    </form>
</BaseDialog>