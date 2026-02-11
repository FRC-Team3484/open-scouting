<script lang="ts">
	import BaseDialog from "./BaseDialog.svelte";
	import Input from "$lib/components/ui/input/input.svelte";
	import * as Select from "$lib/components/ui/select";
	import * as Dialog from "$lib/components/ui/dialog";
	import Button from "$lib/components/ui/button/button.svelte";
	import * as Form from "$lib/components/ui/form";
	import Label from "$lib/components/ui/label/label.svelte";

	import { addPitScoutingQuestionData, addPitScoutingQuestionDialogOpen } from "$lib/stores/dialog";
	import { PlusCircle, X } from "phosphor-svelte";
	import { superForm } from "sveltekit-superforms";
	import { zod4Client } from "sveltekit-superforms/adapters";
	import { CreatePitFieldPitsFieldsSeasonUuidCreatePostBody } from "$lib/zod/pit-scouting/pit-scouting";
	import { createPitFieldPitsFieldsSeasonUuidCreatePost, editPitFieldPitsFieldsSeasonUuidEditFieldUuidPatch } from "$lib/api/pit-scouting/pit-scouting";
	import { toast } from "svelte-sonner";
	import { untrack } from "svelte";

	let { getQuestions, seasonUuid } = $props();

	const questionTypes = [
		{ value: "text", label: "Text" },
		{ value: "number", label: "Number" },
		{ value: "boolean", label: "Boolean" },
		{ value: "choice", label: "Choice" },
	];
	const selectedQuestionTypeLabel = $derived(
		questionTypes.find((qt) => qt.value === $formData.field_type)?.label ?? "Select Question Type"
	);

	let dialogTitle = $state("Add Pit Scouting Question");
	let dialogDescription = $state("Create a new pit scouting question");

	const defaultValues = {
		season_uuid: seasonUuid,
		name: "",
		field_type: "",
		options: {
			choices: [],
		},
		order: 0,
		organization_uuid: null as string | null,
	}

	const form = superForm(defaultValues, {
		SPA: true,
		dataType: "json",
		validators: zod4Client(CreatePitFieldPitsFieldsSeasonUuidCreatePostBody),
		async onUpdate({ form }) {
			if (form.valid) {
				if (Object.keys($addPitScoutingQuestionData).length > 0) {
					await editPitFieldPitsFieldsSeasonUuidEditFieldUuidPatch(seasonUuid, $addPitScoutingQuestionData.uuid, form.data).then((response) => {
						if (response.status !== 200) {
							toast.error("Failed to update question", { duration: 5000 });
						}
					});
				} else {
					await createPitFieldPitsFieldsSeasonUuidCreatePost(seasonUuid, form.data).then((response) => {
						if (response.status !== 200) {
							toast.error("Failed to create question", { duration: 5000 });
						}
					})
				}

				addPitScoutingQuestionDialogOpen.set(false);
				getQuestions();
			} else {
				console.log(form.errors);
			}
		},
	});

	const { form: formData, enhance } = form;

	$effect(() => {
		if ($addPitScoutingQuestionDialogOpen === false) {
			addPitScoutingQuestionData.set({});

			form.reset();
			untrack(() => {
				$formData.season_uuid = seasonUuid;
				dialogTitle = "Add Pit Scouting Question";
				dialogDescription = "Create a new pit scouting question";
			})
		} else {
			const data = $addPitScoutingQuestionData;
			if (data && Object.keys(data).length > 0) {
				untrack(() => {
					$formData = data;
					$formData.season_uuid = seasonUuid;
					dialogTitle = "Edit Pit Scouting Question";
					dialogDescription = `Editing pit scouting question '${$formData.name}'`;
				})
			}
		}
	})
</script>

<BaseDialog title={dialogTitle} description={dialogDescription} bind:open={$addPitScoutingQuestionDialogOpen}>
	<form method="post" use:enhance class="flex flex-col gap-4">
		<Form.Field {form} name="name">
			<Form.Control>
				{#snippet children({ props })}
					<Label>Name</Label>
					<Input {...props} bind:value={$formData.name} />
				{/snippet}
			</Form.Control>
			<Form.Description>The name of the question</Form.Description>
			<Form.FieldErrors />
		</Form.Field>

		<Form.Field {form} name="field_type">
			<Form.Control>
				{#snippet children({ props })}
					<Label>Question Type</Label>
					<Select.Root type="single" bind:value={$formData.field_type} name="field_type">
						<Select.Trigger>{selectedQuestionTypeLabel}</Select.Trigger>
						<Select.Content>
							<Select.Label>Match Types</Select.Label>
							{#each questionTypes as questionType}
								<Select.Item value={questionType.value} label={questionType.label} />
							{/each}
						</Select.Content>
					</Select.Root>
				{/snippet}
			</Form.Control>
			<Form.Description>The type of question</Form.Description>
			<Form.FieldErrors />
		</Form.Field>

		{#if $formData.field_type === "choice"}
			<Form.Field {form} name="options.choices">
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

						{#each $formData.options.choices as option, i (option.id)}
							<div class="flex flex-row gap-2 items-center justify-between">
								<p>{option.name}</p>
								<Button variant="destructive" type="button" onclick={() => $formData.options.choices = $formData.options.choices.filter((_, j) => j !== i)}>
									<X weight="bold" />
								</Button>
							</div>
						{/each}
					{/snippet}
				</Form.Control>
				<Form.Description>The choices for a choice question</Form.Description>
				<Form.FieldErrors />
			</Form.Field>
		{/if}

		<Dialog.Footer>
			{#if Object.keys($addPitScoutingQuestionData).length > 0}
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