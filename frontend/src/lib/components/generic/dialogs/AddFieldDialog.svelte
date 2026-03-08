<script lang="ts">
    import { toast } from "svelte-sonner";
    import { untrack } from "svelte";
	import { PlusCircle, X } from "phosphor-svelte";

	import { addFieldDialogOpen, addFieldEditData, addFieldParentUuid } from "$lib/stores/dialog";

    import * as Dialog from "$lib/components/ui/dialog";
	import { Input } from "$lib/components/ui/input";
	import Button from "$lib/components/ui/button/button.svelte";
    import { Separator } from "$lib/components/ui/separator";
    import * as Select from "$lib/components/ui/select";
	import { Checkbox } from "$lib/components/ui/checkbox";
    import * as Form from "$lib/components/ui/form";
    
    import BaseDialog from "./BaseDialog.svelte";
	import { zod4Client } from "sveltekit-superforms/adapters";
	import { CreateSeasonFieldFieldsSeasonSeasonUuidCreatePostBody } from "$lib/zod/match-scouting-fields/match-scouting-fields";
	import { superForm } from "sveltekit-superforms";
	import Label from "$lib/components/ui/label/label.svelte";
	import { createSeasonFieldFieldsSeasonSeasonUuidCreatePost, editSeasonFieldFieldsSeasonSeasonUuidEditFieldUuidPost } from "$lib/api/match-scouting-fields/match-scouting-fields";

    let { season_uuid, gamePieces, getStructure } = $props();

    const fieldTypes = [
        { name: "string", label: "String" },
        { name: "large_number", label: "Large Number" },
        { name: "small_number", label: "Small Number" },
        { name: "coarse_small_number", label: "Coarse Small Number" },
        { name: "boolean", label: "Boolean" },
        { name: "choice", label: "Choice" },
        { name: "multiple_choice", label: "Multiple Choice" },
    ];
    const statTypes = [
        { name: "auton_score", label: "Auton Score" },
        { name: "auton_miss", label: "Auton Miss" },
        { name: "teleop_score", label: "Teleop Score" },
        { name: "teleop_miss", label: "Teleop Miss" },
        { name: "capability", label: "Cabability" },
        { name: "other", label: "Other" },
        { name: "ignore", label: "Ignore" },
    ];

    let dialogTitle = $state("Add Field");
    let dialogDescription = $state("Create a new field");
    
    const defaultValues = {
        name: "",
        description: "",
        season_uuid: season_uuid,
        field_type: "",
        stat_type: "",
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
            if ($addFieldParentUuid) {
                form.data.parent_uuid = $addFieldParentUuid;
            }

            if (form.valid) {
                if (Object.keys($addFieldEditData).length > 0) {
                    await editSeasonFieldFieldsSeasonSeasonUuidEditFieldUuidPost(season_uuid, $addFieldEditData.uuid, form.data).then((response) => {
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
    
                addFieldParentUuid.set("");
                addFieldDialogOpen.set(false);
                getStructure();
            } else {
                console.log(form.errors);
            }
        }
    })

    const { form: formData, enhance } = form

    $effect(() => {
        if ($addFieldDialogOpen === false) {
            addFieldParentUuid.set("");
            addFieldEditData.set({});

            form.reset();
            untrack(() => {
                $formData.season_uuid = season_uuid;
            });
            dialogTitle = "Add Field";
            dialogDescription = "Create a new field";
        } else if (Object.keys($addFieldEditData).length > 0) {
            const data = $addFieldEditData;

            if (data && Object.keys(data).length > 0) {
                untrack(() => {
                    $formData = data;
                    $formData.season_uuid = season_uuid;
                    dialogTitle = "Edit Field";
                    dialogDescription = `Editing field '${$formData.name}'`;
                })
            }
        }
    });

    $effect(() => {
        if (gamePieces && gamePieces.length > 0) {
            $formData.game_piece_uuid = gamePieces[0].uuid;
            defaultValues.game_piece_uuid = gamePieces[0].uuid;
        }
    });

    $effect(() => {
        $formData.season_uuid = season_uuid;
        defaultValues.season_uuid = season_uuid;
    })
</script>

<BaseDialog title={dialogTitle} description={dialogDescription} bind:open={$addFieldDialogOpen}>
    <form method="post" use:enhance class="flex flex-col gap-4">
        <Form.Field {form} name="name">
            <Form.Control>
                {#snippet children({ props })}
                    <Label>Name</Label>
                    <Input {...props} bind:value={$formData.name} />
                {/snippet}
            </Form.Control>
            <Form.Description>The name of the field</Form.Description>
            <Form.FieldErrors />
        </Form.Field>

        <Form.Field {form} name="description">
            <Form.Control>
                {#snippet children({ props })}
                    <Label>Description</Label>
                    <Input {...props} bind:value={$formData.description} />
                {/snippet}
            </Form.Control>
            <Form.Description>The description for the field</Form.Description>
            <Form.FieldErrors />
        </Form.Field>

        <Separator />

        <Form.Field {form} name="field_type">
            <Form.Control>
                {#snippet children({ props })}
                    <Label>Field Type</Label>
                    <Select.Root type="single" name="field_type" required bind:value={$formData.field_type}>
                            <Select.Trigger>
                            {fieldTypes.find(t => t.name === $formData.field_type)?.label}
                        </Select.Trigger>
                        <Select.Content>
                            <Select.Label>Field Type</Select.Label>
                            {#each fieldTypes as type}
                                <Select.Item value={type.name} label={type.label} />
                            {/each}
                        </Select.Content>
                    </Select.Root>
                {/snippet}
            </Form.Control>
            <Form.Description>Define the type of field</Form.Description>
            <Form.FieldErrors />
        </Form.Field>

        <Form.Field {form} name="stat_type">
            <Form.Control>
                {#snippet children({ props })}
                    <Label>Stat Type</Label>
                    <Select.Root type="single" name="stat_type" required bind:value={$formData.stat_type}>
                        <Select.Trigger>
                            {statTypes.find(t => t.name === $formData.stat_type)?.label}
                        </Select.Trigger>
                        <Select.Content>
                            <Select.Label>Stat Type</Select.Label>
                            {#each statTypes as type}
                                <Select.Item value={type.name} label={type.label} />
                            {/each}
                        </Select.Content>
                    </Select.Root>
                {/snippet}
            </Form.Control>
            <Form.Description>Define which kind of data this field will store for the data view</Form.Description>
            <Form.FieldErrors />
        </Form.Field>

        {#if $formData.stat_type === "auton_score" || $formData.stat_type === "auton_miss" || $formData.stat_type === "teleop_score" || $formData.stat_type === "teleop_miss"}
            <Form.Field {form} name="game_piece_uuid">
                <Form.Control>
                    {#snippet children({ props })}
                        <Label>Game Piece</Label>
                        <Select.Root type="single" name="game_piece" required bind:value={$formData.game_piece_uuid}>
                        {#if gamePieces && gamePieces.length > 0}
                            <Select.Trigger>
                                {gamePieces.find(t => t.uuid === $formData.game_piece_uuid)?.name}
                            </Select.Trigger>
                        {/if}
                        <Select.Content>
                            <Select.Label>Game Piece</Select.Label>
                            {#each gamePieces as game_piece}
                                <Select.Item value={game_piece.uuid} label={game_piece.name} />
                            {/each}
                        </Select.Content>
                    </Select.Root>
                    {/snippet}
                </Form.Control>
                <Form.Description>Used when stat_type is a score or a miss, represents the game piece used for that stat</Form.Description>
                <Form.FieldErrors />
            </Form.Field>
        {/if}

        <Form.Field {form} name="required">
            <Form.Control>
                {#snippet children({ props })}
                    <Label>Required</Label>
                    <Checkbox id="required" name="required" bind:checked={$formData.required} />
                {/snippet}
            </Form.Control>
            <Form.Description>Make this field required when scouts are filling it out. Use this sparingly, to simplify the scouting experience for the scouts</Form.Description>
            <Form.FieldErrors />
        </Form.Field>
        
        {#if $formData.field_type === "choice" || $formData.field_type === "multiple_choice"}
            <Separator />

            <Form.Field {form} name="choices">
                <Form.Control>
                    {#snippet children({ props })}
                        <Label>Choices</Label>
                        <div class="flex flex-row gap-2 items-center">
                            <Input id="choice_name" type="text" placeholder="Choice Name" />
                        </div>

                        <Button type="button" onclick={() => {
                            $formData.options.choices = [...$formData.options.choices, {id: crypto.randomUUID(), name: document.getElementById("choice_name").value}]
                            ; document.getElementById("choice_name").value = ""
                            }}>
                            <PlusCircle weight="bold" />Add Choice
                        </Button>

                        {#each $formData.options.choices as choice, i (choice.id)}
                            <div class="flex flex-row gap-2 items-center justify-between">
                                <p>{choice.name}</p>
                                <Button variant="destructive" type="button" onclick={() => $formData.options.choices = $formData.options.choices.filter((_, j) => j !== i)}>
                                    <X weight="bold" />
                                </Button>
                            </div>
                        {/each}
                    {/snippet}
                </Form.Control>
                <Form.Description>The choices for a choice or multiple_choice field</Form.Description>
                <Form.FieldErrors />
            </Form.Field>

        {:else if $formData.field_type === "small_number" || $formData.field_type === "coarse_small_number"}
            <Separator />

            <Form.Field {form} name="options.default">
                <Form.Control>
                    {#snippet children({ props })}
                        <Label>Default</Label>
                        <Input type="number" name="default" bind:value={$formData.options.default} required />
                    {/snippet}
                </Form.Control>
                <Form.Description>Used for small_number fields. The default value for the field</Form.Description>
                <Form.FieldErrors />
            </Form.Field>

            <Form.Field {form} name="options.minimum">
                <Form.Control>
                    {#snippet children({ props })}
                        <Label>Minimum</Label>
                        <Input type="number" name="minimum" bind:value={$formData.options.minimum} required />
                    {/snippet}
                </Form.Control>
                <Form.Description>Used for small_number fields. The minimum value for the field</Form.Description>
                <Form.FieldErrors />
            </Form.Field>

            <Form.Field {form} name="options.maximum">
                <Form.Control>
                    {#snippet children({ props })}
                        <Label>Maximum</Label>
                        <Input type="number" name="maximum" bind:value={$formData.options.maximum} required />
                    {/snippet}
                </Form.Control>
                <Form.Description>Used for small_number fields. The maximum value for the field</Form.Description>
                <Form.FieldErrors />
            </Form.Field>
        {/if}

        <Dialog.Footer>
            {#if Object.keys($addFieldEditData).length > 0}
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