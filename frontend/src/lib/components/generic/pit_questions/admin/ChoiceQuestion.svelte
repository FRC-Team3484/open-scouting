<script lang="ts">
	import * as Select from "$lib/components/ui/select/index.js";
	import BaseQuestion from "./BaseQuestion.svelte";

    let { question, editable = false, getQuestions = () => {} } = $props();

	let value = $state("na");

	let selectedOption = $derived(
		question.options.find((o) => o.id === value) ?? { id: "na", name: "N/A" }
	);
</script>

<BaseQuestion question={question} editable={editable} getQuestions={getQuestions}>
	<Select.Root type="single" name={question.uuid} required={question.required} bind:value>
		<Select.Trigger>
			{selectedOption.name ?? "Select an option"}
		</Select.Trigger>

		<Select.Content>
			<Select.Label>Options</Select.Label>
			<Select.Item value="na">N/A</Select.Item>
			{#each question.options as option}
				<Select.Item value={option.id}>
					{option.name}
				</Select.Item>
			{/each}
		</Select.Content>
	</Select.Root>
</BaseQuestion>
