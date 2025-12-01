<script lang="ts">
	import { PlusCircle, X } from "phosphor-svelte";

	import { addFieldDialogOpen, addFieldEditData, addFieldParentUuid } from "$lib/stores/dialog";
	import { apiFetch } from "$lib/utils/api";

    import * as Field from "$lib/components/ui/field";
    import * as Dialog from "$lib/components/ui/dialog";
	import { Input } from "$lib/components/ui/input";
	import Button from "$lib/components/ui/button/button.svelte";
    import { Separator } from "$lib/components/ui/separator";
    import * as Select from "$lib/components/ui/select";
	import { Checkbox } from "$lib/components/ui/checkbox";
    
    import BaseDialog from "./BaseDialog.svelte";

    let { season_uuid, gamePieces, getStructure } = $props();

    const fieldTypes = [
        { name: "string", label: "String" },
        { name: "large_number", label: "Large Number" },
        { name: "small_number", label: "Small Number" },
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

    let addFieldAnswers = $state({
        name: "",
        field_type: "",
        stat_type: "",
        game_piece: "",
        required: false,
        options: [],
        minimum: "",
        maximum: "",
        default: "",
        choices: []
    });

    let dialogTitle = $state("Add Field");
    let dialogDescription = $state("Create a new field");
    
    async function createField(event: Event) {
        event.preventDefault();

        const form = event.currentTarget as HTMLFormElement;
        const formData = new FormData(form);

        const body = new FormData();
        body.append("name", formData.get("name")!.toString());
        body.append("field_type", formData.get("field_type")!.toString());
        body.append("stat_type", formData.get("stat_type")!.toString());
        body.append("game_piece_uuid", formData.get("game_piece")!.toString());
        body.append("required", formData.get("required") ? "true" : "false");
        body.append("order", "0");
        body.append("organization_uuid", "");
        body.append("parent_uuid", $addFieldParentUuid);

        if (formData.get("field_type") === "choice" || formData.get("field_type") === "multiple_choice") {
            body.append("options", JSON.stringify(addFieldAnswers.choices));
        } else if (formData.get("field_type") === "small_number") {
            const options = JSON.parse(formData.get("options") || "[]");
            options.minimum = formData.get("minimum")!.toString();
            options.maximum = formData.get("maximum")!.toString();
            options.default = formData.get("default")!.toString();
            body.append("options", JSON.stringify(options));
        } else {
            body.append("options", JSON.stringify([]));
        }

        try {
            if (Object.keys($addFieldEditData).length > 0) {
                await apiFetch(`/fields/season/${season_uuid}/edit/${$addFieldEditData.uuid}`, {
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

            addFieldParentUuid.set("");
            addFieldDialogOpen.set(false);
            getStructure();
        } catch (error) {
            console.error(error);
        }
    }

    function onOpenChange() {
        if ($addFieldDialogOpen === false) {
            addFieldParentUuid.set("");
            addFieldEditData.set({});
            addFieldAnswers = {
                name: "",
                field_type: "",
                stat_type: "",
                game_piece: "",
                required: false,
                options: [],
                minimum: "",
                maximum: "",
                default: "",
                choices: []
            };
            dialogTitle = "Add Field";
            dialogDescription = "Create a new field";
        } else {
            const data = $addFieldEditData;
            if (data && Object.keys(data).length > 0) {
                addFieldAnswers.name = data.name ?? "";
                addFieldAnswers.field_type = data.field_type ?? "";
                addFieldAnswers.stat_type = data.stat_type ?? "";
                addFieldAnswers.game_piece = data.game_piece_id ?? "";
                addFieldAnswers.required = data.required ?? false;
                addFieldAnswers.options = data.options ?? [];
                addFieldAnswers.minimum = data.minimum ?? "";
                addFieldAnswers.maximum = data.maximum ?? "";
                addFieldAnswers.default = data.default ?? "";
                addFieldAnswers.choices = data.choices ?? [];

                dialogTitle = "Edit Field";
                dialogDescription = `Editing field '${addFieldAnswers.name}'`;

                addFieldParentUuid.set("");
            }
        }
    }


    $effect(() => {
        if (gamePieces && gamePieces.length > 0) {
            addFieldAnswers.game_piece = gamePieces[0].uuid;
        }
    });
</script>

<BaseDialog title={dialogTitle} description={dialogDescription} bind:open={$addFieldDialogOpen} onOpenChange={onOpenChange}>
    <form method="post" on:submit={createField} class="flex flex-col gap-4">
        <Field.Group class="gap-4">
            <Field.Set class="flex flex-col gap-2">
                <Field.Label>Name</Field.Label>
                <Input type="text" name="name" label="Name" required bind:value={addFieldAnswers.name} />
                <Field.Description>The name of the field</Field.Description>
            </Field.Set>
        </Field.Group>

        <Separator />

        <Field.Group class="gap-4">
            <Field.Set class="flex flex-col gap-2">
                <Field.Label>Field Type</Field.Label>
                    <Select.Root type="single" name="field_type" label="Field Type" required bind:value={addFieldAnswers.field_type}>
                            <Select.Trigger>
                            {fieldTypes.find(t => t.name === addFieldAnswers.field_type)?.label}
                        </Select.Trigger>
                        <Select.Content>
                            <Select.Label>Field Type</Select.Label>
                            {#each fieldTypes as type}
                                <Select.Item value={type.name} label={type.label} />
                            {/each}
                        </Select.Content>
                    </Select.Root>
                <Field.Description>Define the type of field</Field.Description>
            </Field.Set>

            <Field.Set class="flex flex-col gap-2">
                <Field.Label>Stat Type</Field.Label>
                    <Select.Root type="single" name="stat_type" label="Stat Type" required bind:value={addFieldAnswers.stat_type}>
                        <Select.Trigger>
                            {statTypes.find(t => t.name === addFieldAnswers.stat_type)?.label}
                        </Select.Trigger>
                        <Select.Content>
                            <Select.Label>Stat Type</Select.Label>
                            {#each statTypes as type}
                                <Select.Item value={type.name} label={type.label} />
                            {/each}
                        </Select.Content>
                    </Select.Root>
                <Field.Description>Define the type of field</Field.Description>
            </Field.Set>

            {#if addFieldAnswers.stat_type === "auton_score" || addFieldAnswers.stat_type === "auton_miss" || addFieldAnswers.stat_type === "teleop_score" || addFieldAnswers.stat_type === "teleop_miss"}
                <Field.Set class="flex flex-col gap-2">
                    <Field.Label>Game Piece</Field.Label>
                    <Select.Root type="single" name="game_piece" label="Game Piece" required bind:value={addFieldAnswers.game_piece}>
                        {#if gamePieces && gamePieces.length > 0}
                            <Select.Trigger>
                                {gamePieces.find(t => t.uuid === addFieldAnswers.game_piece)?.name}
                            </Select.Trigger>
                        {/if}
                        <Select.Content>
                            <Select.Label>Game Piece</Select.Label>
                            {#each gamePieces as game_piece}
                                <Select.Item value={game_piece.uuid} label={game_piece.name} />
                            {/each}
                        </Select.Content>
                    </Select.Root>
                    <Field.Description>Used when stat_type is a score or a miss, represents the game piece used for that stat</Field.Description>
                </Field.Set>
            {/if}

            <Field.Set class="flex flex-col gap-2">
                <Field.Field orientation="horizontal">
                    <Checkbox id="required" name="required" bind:checked={addFieldAnswers.required} />
                    <Field.Content>
                        <Field.Label for="required">
                            Required Field
                        </Field.Label>
                        <Field.Description>
                            Make this field required when scouts are filling it out. Use this sparingly, to simplify the scouting experience for the scouts
                        </Field.Description>
                    </Field.Content>
                </Field.Field>
            </Field.Set>
        </Field.Group>

        {#if addFieldAnswers.field_type === "choice" || addFieldAnswers.field_type === "multiple_choice"}
            <Separator />
            <Field.Group class="gap-4">
                <Field.Set class="flex flex-col gap-2">
                    <Field.Label>Choices</Field.Label>
                    <div class="flex flex-row gap-2 items-center">
                        <Input id="choice_name" type="text" placeholder="Choice Name" />
                    </div>

                    <Button type="button" onclick={() => {
                        addFieldAnswers.choices = [...addFieldAnswers.choices, {id: crypto.randomUUID(), name: document.getElementById("choice_name").value}]
                        ; document.getElementById("choice_name").value = ""
                        }}>
                        <PlusCircle weight="bold" />Add Choice
                    </Button>

                    {#each addFieldAnswers.choices as choice, i (choice.id)}
                        <div class="flex flex-row gap-2 items-center justify-between">
                            <p>{choice.name}</p>
                            <Button variant="destructive" type="button" onclick={() => addFieldAnswers.choices = addFieldAnswers.choices.filter((_, j) => j !== i)}>
                                <X weight="bold" />
                            </Button>
                        </div>
                    {/each}
                </Field.Set>
            </Field.Group>

        {:else if addFieldAnswers.field_type === "small_number"}
            <Separator />

            <Field.Group class="gap-4">
                <Field.Set class="flex flex-col gap-2">
                    <Field.Label>Minimum</Field.Label>
                    <Input type="number" name="minimum" label="Minimum" required />
                    <Field.Description>Used for small_number fields. The minimum value for the field</Field.Description>
                </Field.Set>
                <Field.Set class="flex flex-col gap-2">
                    <Field.Label>Max</Field.Label>
                    <Input type="number" name="maximum" label="Maximum" required />
                    <Field.Description>Used for small_number fields. The maximum value for the field</Field.Description>
                </Field.Set>
                <Field.Set class="flex flex-col gap-2">
                    <Field.Label>Default</Field.Label>
                    <Input type="number" name="default" label="Default" required />
                    <Field.Description>Used for small_number fields. The default value for the field</Field.Description>
                </Field.Set>
            </Field.Group>

        {/if}

        <Dialog.Footer>
            <Dialog.Close>
                <Button type="button" variant="outline">Cancel</Button>
            </Dialog.Close>
            {#if Object.keys($addFieldEditData).length > 0}
                <Button type="submit">Edit</Button>
            {:else}
                <Button type="submit">Create</Button>
            {/if}
        </Dialog.Footer>
    </form>
</BaseDialog>