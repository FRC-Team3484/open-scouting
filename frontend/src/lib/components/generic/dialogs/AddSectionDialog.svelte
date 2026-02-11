<script lang="ts">
    import { addSectionDialogOpen, addSectionEditData, addSectionParentUuid } from "$lib/stores/dialog";
	import { apiFetch } from "$lib/utils/api";
    
    import * as Field from "$lib/components/ui/field";
    import * as Dialog from "$lib/components/ui/dialog";
	import { Input } from "$lib/components/ui/input";
	import Button from "$lib/components/ui/button/button.svelte";
    import * as Form from "$lib/components/ui/form";

    import BaseDialog from "./BaseDialog.svelte";
	import { zod4Client } from "sveltekit-superforms/adapters";
	import { createSeasonFieldFieldsSeasonSeasonUuidCreatePost, editSeasonFieldFieldsSeasonSeasonUuidEditFieldUuidPost } from "$lib/api/match-scouting-fields/match-scouting-fields";
	import { CreateSeasonFieldFieldsSeasonSeasonUuidCreatePostBody } from "$lib/zod/match-scouting-fields/match-scouting-fields";
	import { superForm } from "sveltekit-superforms";
	import Label from "$lib/components/ui/label/label.svelte";
	import { toast } from "svelte-sonner";
	import { untrack } from "svelte";

    let { open = $bindable(), season_uuid, getStructure } = $props();
    
    let dialogTitle = $state("Add Section");
    let dialogDescription = $state("Create a new section");

    const defaultValues = {
        name: "",
        season_uuid: season_uuid,
        field_type: "section",
        stat_type: "section",
        required: false,
        order: 0,
        organization_uuid: null as string | null,
        parent_uuid: null as string | null,
        options: {
            choices: [],
            minimum: 0,
            maximum: 0,
            default: 0
        },
        choices: [] as any[],
        game_piece_uuid: null as string | null,
    }

    const form = superForm(defaultValues, {
        SPA: true,
        dataType: "json",
        validators: zod4Client(CreateSeasonFieldFieldsSeasonSeasonUuidCreatePostBody),
        async onUpdate({ form }) {
            if (form.valid) {
                if ($addSectionParentUuid) {
                    form.data.parent_uuid = $addSectionParentUuid;
                }

                if (Object.keys($addSectionEditData).length > 0) {
                    await editSeasonFieldFieldsSeasonSeasonUuidEditFieldUuidPost(season_uuid, $addSectionEditData.uuid, form.data).then((response) => {
                        if (response.status !== 200) {
                            toast.error("Failed to update field", { duration: 5000 });
                        }
                    });
                } else {
                    await createSeasonFieldFieldsSeasonSeasonUuidCreatePost(season_uuid, form.data).then((response) => {
                        if (response.status !== 200) {
                            toast.error("Failed to create field", { duration: 5000 });
                        }
                    })
                }

                addSectionParentUuid.set("");
                addSectionDialogOpen.set(false);
                getStructure();
            } else {
                console.log(form.errors);
            }
        }
    })

    const { form: formData, enhance } = form

    $effect(() => {
        if ($addSectionDialogOpen === false) {
            addSectionParentUuid.set("");
            addSectionEditData.set({});

            form.reset();
            untrack(() => {
                $formData.season_uuid = season_uuid;
            });
            dialogTitle = "Add Section";
            dialogDescription = "Create a new section";
        } else if (Object.keys($addSectionEditData).length > 0) {
            const data = $addSectionEditData;
            
            if (data && Object.keys(data).length > 0) {
                untrack(() => {
                    $formData = data;
                    $formData.season_uuid = season_uuid;
                    dialogTitle = "Edit Section";
                    dialogDescription = `Editing section '${$formData.name}'`;
                })
            }
        }
    })

    $effect(() => {
        $formData.season_uuid = season_uuid;
        defaultValues.season_uuid = season_uuid;
    })
</script>

<BaseDialog title={dialogTitle} description={dialogDescription} bind:open={$addSectionDialogOpen}>
    <form method="post" use:enhance class="flex flex-col gap-4">
        <Form.Field {form} name="name">
            <Form.Control>
                {#snippet children({ props })}
                    <Label>Name</Label>
                    <Input {...props} bind:value={$formData.name} />
                {/snippet}
            </Form.Control>
            <Form.Description>The name of the section</Form.Description>
            <Form.FieldErrors />
        </Form.Field>

        <Dialog.Footer>
            {#if Object.keys($addSectionEditData).length > 0}
            <Form.Button type="submit">Edit</Form.Button>
            {:else}
            <Form.Button type="submit">Create</Form.Button>
            {/if}
            <Dialog.Close>
                <Form.Button type="button" variant="outline">Cancel</Form.Button>
            </Dialog.Close>
        </Dialog.Footer>
    </form>
</BaseDialog>