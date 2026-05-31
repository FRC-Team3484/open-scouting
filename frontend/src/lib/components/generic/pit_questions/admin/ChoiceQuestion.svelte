<!-- 
@component
Admin preview for the single choice pit scouting question

TODO: Create an interface for question.option.choices

Props:
    - `question` (`PitFieldResponse`) - The data for this question
    - `editable` (`boolean`) - If this question is editable or not
    - `getQuestions` (`() => void`) - The function for fetching the questions
-->
<script lang="ts">
	import * as Select from "$lib/components/ui/select/index.js";

	import type { PitFieldResponse } from "$lib/api/model";
	import BaseQuestion from "./BaseQuestion.svelte";


	interface Props {
        question: PitFieldResponse
        editable: boolean
        getQuestions: () => void
    }
    let { question, editable = false, getQuestions = () => {} }: Props = $props();
	
	let value = $state("na");
	
	let selectedOption = $derived(
		question.options.choices.find((o) => o.id === value) ?? { id: "na", name: "N/A" }
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
			{#each question.options.choices as option}
				<Select.Item value={option.id}>
					{option.name}
				</Select.Item>
			{/each}
		</Select.Content>
	</Select.Root>
</BaseQuestion>
