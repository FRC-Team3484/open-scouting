<script lang="ts">
	import { apiFetch } from "$lib/utls/api";
	import { onMount } from "svelte";
	import Skeleton from "../ui/skeleton/skeleton.svelte";
	import { FolderPlus, PlusCircle } from "phosphor-svelte";
    import * as Card from "$lib/components/ui/card/index.js";
    import * as Dialog from "$lib/components/ui/dialog/index.js";
	import Button from "../ui/button/button.svelte";
	import Separator from "../ui/separator/separator.svelte";
    import * as Field from "$lib/components/ui/field/index.js";
	import Input from "../ui/input/input.svelte";
	import * as Select from "$lib/components/ui/select/index.js";
	import Checkbox from "../ui/checkbox/checkbox.svelte";

    let fields = [];
    let field_type_value = {"name": "string", "label": "String"};
    let stat_type_value = {"name": "auton_score", "label": "Auton Score"};

    export let season_uuid: string = "";
    export let editable: boolean = false;

    async function get_fields() {
        if (!season_uuid) return;
        fields = await apiFetch(`/fields/season/${season_uuid}`);
    }

    onMount(async () => {
        get_fields();
    });
</script>

<div class="flex flex-col gap-4">
    {#if season_uuid === ""}
        <Skeleton class="w-128 h-32" />
        <Skeleton class="w-128 h-32" />
        <Skeleton class="w-128 h-32" />
    {:else}
        <Separator />

        <Card.Root class="w-auto min-w-64">
            <Card.Content>
                <div class="flex flex-col gap-4">
                    <Dialog.Root>
                        <Dialog.Trigger>
                            <Button><PlusCircle weight="bold" /> Add Field</Button>
                        </Dialog.Trigger>

                        <Dialog.Content>
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
                                            <Select.Root type="single" name="field_type" label="Field Type" required>
                                                <Select.Trigger>
                                                    {field_type_value.label}
                                                </Select.Trigger>
                                                <Select.Content>
                                                    <Select.Label>Field Type</Select.Label>
                                                    <Select.Item value={{"name":"string", "label":"String"}} label="String" />
                                                    <Select.Item value={{"name":"large_number", "label":"Large Number"}} label="Large Number" />
                                                    <Select.Item value={{"name":"small_number", "label":"Small Number"}} label="Small Number" />
                                                    <Select.Item value={{"name":"boolean", "label":"Boolean"}} label="Boolean" />
                                                    <Select.Item value={{"name":"choice", "label":"Choice"}} label="Choice" />
                                                    <Select.Item value={{"name":"multiple_choice", "label":"Multiple Choice"}} label="Multiple Choice" />
                                                </Select.Content>
                                            </Select.Root>
                                        <Field.Description>Define the type of field</Field.Description>
                                    </Field.Set>

                                    <Field.Set class="flex flex-col gap-2">
                                        <Field.Label>Stat Type</Field.Label>
                                            <Select.Root type="single" name="stat_type" label="Stat Type" required>
                                                <Select.Trigger>
                                                    {stat_type_value.label}
                                                </Select.Trigger>
                                                <Select.Content>
                                                    <Select.Label>Stat Type</Select.Label>
                                                    <Select.Item value={{"name":"auton_score", "label":"Auton Score"}} label="Auton Score" />
                                                    <Select.Item value={{"name":"auton_miss", "label":"Auton Miss"}} label="Auton Miss" />
                                                    <Select.Item value={{"name":"teleop_score", "label":"Teleop Score"}} label="Teleop Score" />
                                                    <Select.Item value={{"name":"teleop_miss", "label":"Teleop Miss"}} label="Teleop Miss" />
                                                    <Select.Item value={{"name":"capability", "label":"Capability"}} label="Capability" />
                                                    <Select.Item value={{"name":"other", "label":"Other"}} label="Other" />
                                                    <Select.Item value={{"name":"ignore", "label":"Ignore"}} label="Ignore" />
                                                </Select.Content>
                                            </Select.Root>
                                        <Field.Description>Define the type of field</Field.Description>
                                    </Field.Set>

                                    <Field.Set class="flex flex-col gap-2">
                                        <Field.Label>Game Piece</Field.Label>
                                        <Input type="text" name="game_piece" label="Game Piece" required />
                                        <Field.Description>Used when stat_type is a score or a miss, represents the game piece used for that stat</Field.Description>
                                    </Field.Set>

                                    <Field.Set class="flex flex-col gap-2">
                                        <Field.Label>Required</Field.Label>
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

                                <Separator />

                                <Field.Group class="gap-4">
                                    <Field.Set class="flex flex-col gap-2">
                                        <Field.Label>Options</Field.Label>
                                        <Input type="text" name="options" label="Options" required />
                                        <Field.Description>Used for choice, multiple_choice, and small_number fields. Used to specify various options, like the choices for a choice field, or the minimum and maximum value for a small_number field</Field.Description>
                                    </Field.Set>
                                </Field.Group>
                            </form>

                            <Dialog.Footer>
                                <Button type="submit">Create</Button>
                            </Dialog.Footer>
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
            <p>field</p>
        {/each}
    {/if}
</div>