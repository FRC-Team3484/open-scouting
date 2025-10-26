<script lang="ts">
	import { apiFetch } from "$lib/utls/api";
	import { onMount } from "svelte";
	import Skeleton from "../ui/skeleton/skeleton.svelte";
	import { ArrowLeft, ArrowRight, FolderPlus, Minus, Pencil, Plus, PlusCircle, Trash, X } from "phosphor-svelte";
    import * as Card from "$lib/components/ui/card/index.js";
    import * as Dialog from "$lib/components/ui/dialog/index.js";
	import Button from "../ui/button/button.svelte";
	import Separator from "../ui/separator/separator.svelte";
    import * as Field from "$lib/components/ui/field/index.js";
	import Input from "../ui/input/input.svelte";
	import * as Select from "$lib/components/ui/select/index.js";
	import Checkbox from "../ui/checkbox/checkbox.svelte";
	import { get } from "svelte/store";
	import { Root } from "../ui/alert";
	import { Trigger } from "../ui/alert-dialog";
	import { json } from "@sveltejs/kit";
	import StringField from "./fields/StringField.svelte";
	import LargeNumberField from "./fields/LargeNumberField.svelte";
	import SmallNumberField from "./fields/SmallNumberField.svelte";
	import BooleanField from "./fields/BooleanField.svelte";
	import ChoiceField from "./fields/ChoiceField.svelte";
	import MultipleChoiceField from "./fields/MultipleChoiceField.svelte";

    let fields = [];
    let gamePieces = [];
    let selectedGamePiece = null;

    const fieldTypes = [
        { name: "string", label: "String" },
        { name: "large_number", label: "Large Number" },
        { name: "small_number", label: "Small Number" },
        { name: "boolean", label: "Boolean" },
        { name: "choice", label: "Choice" },
        { name: "multiple_choice", label: "Multiple Choice" },
    ];
    let selectedFieldType = "string";
    const statTypes = [
        { name: "auton_score", label: "Auton Score" },
        { name: "auton_miss", label: "Auton Miss" },
        { name: "teleop_score", label: "Teleop Score" },
        { name: "teleop_miss", label: "Teleop Miss" },
        { name: "capability", label: "Cabability" },
        { name: "other", label: "Other" },
        { name: "ignore", label: "Ignore" },
    ];
    let selectedStatType = "auton_score";

    type ChoiceType = {id: string; name: string }[];
    let choices: ChoiceType[] = [];

    export let season_uuid: string = "";
    export let editable: boolean = false;

    async function getFields() {
        if (!season_uuid) return;
        fields = [];
        fields = await apiFetch(`/fields/season/${season_uuid}`);

        fields = fields.map(field => {
            if (field.field_type === "choice" || field.field_type === "multiple_choice" || field.field_type === "small_number") {
                const raw = field.options?.[0];
                try {
                    // Parse only if it's a valid JSON string
                    if (typeof raw === "string") {
                        field.options = JSON.parse(raw);
                    }
                } catch (err) {
                    console.error("Error parsing field options:", field.name, raw, err);
                    field.options = [];
                }
            }
            return field;
        });

        console.log(fields);
    }

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
        body.append("label", formData.get("name")!.toString());
        body.append("order", "0");
        body.append("organization_uuid", "");

        if (formData.get("field_type") === "choice" || formData.get("field_type") === "multiple_choice") {
            body.append("options", JSON.stringify(choices));
        } else if (formData.get("field_type") === "small_number") {
            const options = JSON.parse(formData.get("options") || "{}");
            options.minimum = formData.get("minimum")!.toString();
            options.maximum = formData.get("maximum")!.toString();
            options.default = formData.get("default")!.toString();
            body.append("options", JSON.stringify(options));
        }

        console.log(body)

        try {
            const response = await apiFetch(`/fields/season/${season_uuid}/create`, {
                method: "POST",
                data: body,
                token: localStorage.getItem("access_token")
            });

            getFields();
        } catch (error) {
            console.error(error);
        }
    }

    async function getGamePieces() {
        gamePieces = await apiFetch(`/gamepieces/season/${season_uuid}`);
        selectedGamePiece = gamePieces[0];
    }

    onMount(async () => {
        while (!season_uuid) {
            await new Promise(resolve => setTimeout(resolve, 100));
        }
        getFields();
        getGamePieces();
    });
</script>

<div class="flex flex-col gap-4">
    {#if season_uuid === ""}
        <Skeleton class="w-128 h-32" />
        <Skeleton class="w-128 h-32" />
        <Skeleton class="w-128 h-32" />
    {:else}
        <Card.Root class="w-auto min-w-64">
            <Card.Content>
                <div class="flex flex-col gap-4">
                    <Dialog.Root>
                        <Dialog.Trigger>
                            <Button><PlusCircle weight="bold" /> Add Field</Button>
                        </Dialog.Trigger>

                        <Dialog.Content class="overflow-y-scroll max-h-[calc(100vh-2rem)]">
                            <Dialog.Header>
                                <Dialog.Title>Add Field</Dialog.Title>
                                <Dialog.Description>Create a new field</Dialog.Description>
                            </Dialog.Header>

                            <form method="post" on:submit={createField} class="flex flex-col gap-4">
                                <Field.Group class="gap-4">
                                    <Field.Set class="flex flex-col gap-2">
                                        <Field.Label>Name</Field.Label>
                                        <Input type="text" name="name" label="Name" required />
                                        <Field.Description>The name of the field</Field.Description>
                                    </Field.Set>
                                </Field.Group>

                                <Separator />

                                <Field.Group class="gap-4">
                                    <Field.Set class="flex flex-col gap-2">
                                        <Field.Label>Field Type</Field.Label>
                                            <Select.Root type="single" name="field_type" label="Field Type" required bind:value={selectedFieldType}>
                                                 <Select.Trigger>
                                                    {fieldTypes.find(t => t.name === selectedFieldType)?.label}
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
                                            <Select.Root type="single" name="stat_type" label="Stat Type" required bind:value={selectedStatType}>
                                                <Select.Trigger>
                                                    {statTypes.find(t => t.name === selectedStatType)?.label}
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

                                    <Field.Set class="flex flex-col gap-2">
                                        <Field.Label>Game Piece</Field.Label>
                                        <Select.Root type="single" name="game_piece" label="Game Piece" required bind:value={selectedGamePiece}>
                                            <Select.Trigger>
                                                {gamePieces.find(t => t.uuid === selectedGamePiece)?.name}
                                            </Select.Trigger>
                                            <Select.Content>
                                                <Select.Label>Game Piece</Select.Label>
                                                {#each gamePieces as game_piece}
                                                    <Select.Item value={game_piece.uuid} label={game_piece.name} />
                                                {/each}
                                            </Select.Content>
                                        </Select.Root>
                                        <Field.Description>Used when stat_type is a score or a miss, represents the game piece used for that stat</Field.Description>
                                    </Field.Set>

                                    <Field.Set class="flex flex-col gap-2">
                                        <Field.Field orientation="horizontal">
                                            <Checkbox id="required" name="required"/>
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

                                {#if selectedFieldType === "choice" || selectedFieldType === "multiple_choice"}
                                    <Separator />
                                    <!-- TODO: FIx this so it actually adds the name to the options list -->
                                    <Field.Group class="gap-4">
                                        <Field.Set class="flex flex-col gap-2">
                                            <Field.Label>Choices</Field.Label>
                                            <div class="flex flex-row gap-2 items-center">
                                                <Input id="choice_name" type="text" placeholder="Choice Name" />
                                            </div>

                                            <Button type="button" onclick={() => {
                                                choices = [...choices, {id: crypto.randomUUID(), name: document.getElementById("choice_name").value}]
                                                ; document.getElementById("choice_name").value = ""
                                                }}>
                                                <PlusCircle weight="bold" />Add Choice
                                            </Button>

                                            {#each choices as choice, i (choice.id)}
                                                <div class="flex flex-row gap-2 items-center justify-between">
                                                    <p>{choice.name}</p>
                                                    <Button variant="destructive" type="button" onclick={() => choices = choices.filter((_, j) => j !== i)}>
                                                        <X weight="bold" />
                                                    </Button>
                                                </div>
                                            {/each}
                                        </Field.Set>
                                    </Field.Group>

                                {:else if selectedFieldType === "small_number"}
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
                                    <Button type="submit">Create</Button>
                                </Dialog.Footer>
                            </form>
                        </Dialog.Content>
                    </Dialog.Root>

                    <Dialog.Root>
                        <Dialog.Trigger>
                            <Button><FolderPlus weight="bold" /> Add Section</Button>
                        </Dialog.Trigger>

                        <Dialog.Content>
                            <Dialog.Header>
                                <Dialog.Title>Add Section</Dialog.Title>
                                <Dialog.Description>Create a new section</Dialog.Description>
                            </Dialog.Header>

                            <Dialog.Footer>
                                <Button type="submit">Create</Button>
                            </Dialog.Footer>
                        </Dialog.Content>
                    </Dialog.Root>
                </div>
            </Card.Content>
        </Card.Root>

        {#each fields as field}
            {#if field.field_type === "string"}
                <StringField field={field} editable={editable} getFields={getFields}/>
            {:else if field.field_type === "large_number"}
                <LargeNumberField field={field} editable={editable} getFields={getFields}/>
            {:else if field.field_type === "small_number"}
                <SmallNumberField field={field} editable={editable} getFields={getFields}/>
            {:else if field.field_type === "boolean"}
                <BooleanField field={field} editable={editable} getFields={getFields}/>
            {:else if field.field_type === "choice"}
                <ChoiceField field={field} editable={editable} getFields={getFields}/>
            {:else if field.field_type === "multiple_choice"}
                <MultipleChoiceField field={field} editable={editable} getFields={getFields}/>
            {/if}
        {/each}
    {/if}
</div>