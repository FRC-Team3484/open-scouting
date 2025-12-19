<script lang="ts">
	import { apiFetch } from "$lib/utils/api";

	import BaseDialog from "./BaseDialog.svelte";
	import * as Field from "$lib/components/ui/field";
	import Input from "$lib/components/ui/input/input.svelte";
	import * as Select from "$lib/components/ui/select";
	import * as Dialog from "$lib/components/ui/dialog";
	import Button from "$lib/components/ui/button/button.svelte";
	import Separator from "$lib/components/ui/separator/separator.svelte";

	import { addPitScoutingQuestionDialogOpen } from "$lib/stores/dialog";

	let { getQuestions, seasonUuid } = $props();

	const questionTypes = [
		{ value: "text", label: "Text" },
		{ value: "number", label: "Number" },
		{ value: "boolean", label: "Boolean" },
		{ value: "choice", label: "Choice" },
	];
	let selectedQuestionType = $state("text");
	const selectedQuestionTypeLabel = $derived(
		questionTypes.find((qt) => qt.value === selectedQuestionType)?.label ?? "Select Question Type"
	);

	async function createPitQuestion(event: Event) {
		event.preventDefault();

		const form = event.currentTarget as HTMLFormElement;
		const formData = new FormData(form);

		console.log(formData);

		const body = new FormData();
		body.append("name", formData.get("name")!.toString());
		body.append("field_type", selectedQuestionType);
		body.append("order", "0"); // TODO: Implement reordering
		body.append("organization_uuid", "");

		if (selectedQuestionType == "choice") {
			body.append("options", JSON.stringify(formData.get("options")?.toString().split(",")));
		} else {
			body.append("options", "[]");
		}

		console.log(body);

		try {
			await apiFetch(`/pits/fields/${seasonUuid}/create`, {
				method: "POST",
				data: body,
				token: localStorage.getItem("access_token")
			});
			getQuestions();
		} catch (error) {
			console.error(error);
		}
	}
</script>

<BaseDialog title={"Add Pit Scouting Question"} description={"Create a new pit scouting question"} bind:open={$addPitScoutingQuestionDialogOpen}>
    <form method="post" on:submit={createPitQuestion} class="flex flex-col gap-4">
		<Field.Group class="gap-4">
			<Field.Set class="flex flex-col gap-2">
				<Field.Label>Name</Field.Label>
				<Input type="text" name="name" required />
				<Field.Description>The name of the question</Field.Description>
			</Field.Set>

			<Field.Set class="flex flex-col gap-2">
				<Field.Label>Question Type</Field.Label>
				<Select.Root type="single" bind:value={selectedQuestionType} name="field_type">
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

		{#if selectedQuestionType === "choice"}
			<Separator />

			<Field.Group class="gap-4">
				<Field.Set class="flex flex-col gap-2">
					<Field.Label>Choices</Field.Label>
					<Input type="text" name="options" required />
					<Field.Description>Comma separated list of choices</Field.Description>
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