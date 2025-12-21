<script lang="ts">
	import { apiFetch } from "$lib/utils/api";

	import BaseDialog from "./BaseDialog.svelte";
	import * as Field from "$lib/components/ui/field";
	import Input from "$lib/components/ui/input/input.svelte";
	import * as Select from "$lib/components/ui/select";
	import * as Dialog from "$lib/components/ui/dialog";
	import Button from "$lib/components/ui/button/button.svelte";
	import Separator from "$lib/components/ui/separator/separator.svelte";

	import { addFieldDialogOpen, addPitScoutingQuestionData, addPitScoutingQuestionDialogOpen } from "$lib/stores/dialog";
	import { PlusCircle, X } from "phosphor-svelte";
	import { add } from "dexie";

	let { getQuestions, seasonUuid } = $props();

	let addQuestionAnswers = $state({
		name: "",
		field_type: "text",
		options: [],
	});

	const questionTypes = [
		{ value: "text", label: "Text" },
		{ value: "number", label: "Number" },
		{ value: "boolean", label: "Boolean" },
		{ value: "choice", label: "Choice" },
	];
	const selectedQuestionTypeLabel = $derived(
		questionTypes.find((qt) => qt.value === addQuestionAnswers.field_type)?.label ?? "Select Question Type"
	);

	let dialogTitle = $state("Add Pit Scouting Question");
	let dialogDescription = $state("Create a new pit scouting question");

	async function createPitQuestion(event: Event) {
		event.preventDefault();

		const form = event.currentTarget as HTMLFormElement;
		const formData = new FormData(form);

		console.log(formData, addQuestionAnswers.options);

		const body = new FormData();
		body.append("name", formData.get("name")!.toString());
		body.append("field_type", addQuestionAnswers.field_type);
		body.append("order", "0"); // TODO: Implement reordering
		body.append("organization_uuid", "");

		if (addQuestionAnswers.field_type == "choice") {
			body.append("options", JSON.stringify(addQuestionAnswers.options));
		} else {
			body.append("options", "[]");
		}

		console.log(body);

		try {
			if (Object.keys($addPitScoutingQuestionData).length > 0) {
				await apiFetch(`/pits/fields/${seasonUuid}/edit/${$addPitScoutingQuestionData.uuid}`, {
					method: "PATCH",
					data: body,
					token: localStorage.getItem("access_token")
				});
			} else {
				await apiFetch(`/pits/fields/${seasonUuid}/create`, {
					method: "POST",
					data: body,
					token: localStorage.getItem("access_token")
				});
			}
			
			addFieldDialogOpen.set(false);
			getQuestions();
		} catch (error) {
			console.error(error);
		}
	}

	function onOpenChange() {
		if ($addPitScoutingQuestionDialogOpen === false) {
			addPitScoutingQuestionData.set({});

			addQuestionAnswers = {
				name: "",
				field_type: "text",
				options: [],
			};

			dialogTitle = "Add Pit Scouting Question";
			dialogDescription = "Create a new pit scouting question";
		} else {
			const data = $addPitScoutingQuestionData;
			if (data && Object.keys(data).length > 0) {
				addQuestionAnswers.name = data.name ?? "";
				addQuestionAnswers.field_type = data.field_type ?? "text";
				addQuestionAnswers.options = data.options ?? [];

				dialogTitle = "Edit Pit Scouting Question";
				dialogDescription = `Editing pit scouting question '${addQuestionAnswers.name}'`;
			}
		}
	}
</script>

<BaseDialog title={dialogTitle} description={dialogDescription} bind:open={$addPitScoutingQuestionDialogOpen} bind:onOpenChange={onOpenChange}>
    <form method="post" on:submit={createPitQuestion} class="flex flex-col gap-4">
		<Field.Group class="gap-4">
			<Field.Set class="flex flex-col gap-2">
				<Field.Label>Name</Field.Label>
				<Input type="text" name="name" required bind:value={addQuestionAnswers.name} />
				<Field.Description>The name of the question</Field.Description>
			</Field.Set>

			<Field.Set class="flex flex-col gap-2">
				<Field.Label>Question Type</Field.Label>
				<Select.Root type="single" bind:value={addQuestionAnswers.field_type} name="field_type">
                    <Select.Trigger>{selectedQuestionTypeLabel}</Select.Trigger>
                    <Select.Content>
                        <Select.Label>Match Types</Select.Label>
                        {#each questionTypes as questionType}
                            <Select.Item value={questionType.value} label={questionType.label} />
                        {/each}
                    </Select.Content>
                </Select.Root>
				<Field.Description>The type of question</Field.Description>
			</Field.Set>
		</Field.Group>

		{#if addQuestionAnswers.field_type === "choice"}
			<Separator />
            <Field.Group class="gap-4">
                <Field.Set class="flex flex-col gap-2">
                    <Field.Label>Choices</Field.Label>
                    <div class="flex flex-row gap-2 items-center">
                        <Input id="choice_name" type="text" placeholder="Choice Name" />
                    </div>

                    <Button type="button" onclick={() => {
                        addQuestionAnswers.options = [...addQuestionAnswers.options, {id: crypto.randomUUID(), name: document.getElementById("choice_name").value}]
                        ; document.getElementById("choice_name").value = ""
                        }}>
                        <PlusCircle weight="bold" />Add Choice
                    </Button>

                    {#each addQuestionAnswers.options as option, i (option.id)}
                        <div class="flex flex-row gap-2 items-center justify-between">
                            <p>{option.name}</p>
                            <Button variant="destructive" type="button" onclick={() => addQuestionAnswers.options = addQuestionAnswers.options.filter((_, j) => j !== i)}>
                                <X weight="bold" />
                            </Button>
                        </div>
                    {/each}
                </Field.Set>
            </Field.Group>
		{/if}

		<Dialog.Footer>
			<Dialog.Close>
				<Button type="button" variant="outline">Cancel</Button>
				<Button type="submit">Create</Button>
			</Dialog.Close>
		</Dialog.Footer>
	</form>
</BaseDialog>