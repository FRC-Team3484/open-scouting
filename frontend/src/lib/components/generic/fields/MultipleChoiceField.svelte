<!-- 
@component
Match scouting field with a multiple choice input from a given list of choices

TODO: Get a proper response schema for field.options.choices

Props:
    - `field` (`MatchScoutingFieldResponse`) - Data for this field
    - `editable` (`boolean`) - If this field is editable or not
    - `getFields` (`() => void`) - Function for fetching field data
-->
<script lang="ts">
	import * as Select from "$lib/components/ui/select/index.js";

	import type { MatchScoutingFieldResponse } from "$lib/api/model";
	import BaseField from "./BaseField.svelte";

	
	interface Props {
        field: MatchScoutingFieldResponse
        editable: boolean
        getFields: () => void
    }
	let { field, editable, getFields }: Props = $props();

	let options = field.options.choices

	// Store selected values as an array of IDs
	let value = $state<string[]>(["na"]);

	// Compute selected option objects from the IDs
	// TODO: Use when basing options on a UUID
	// let selectedOptions = $derived(
	// 	value.map((id) => options.find((o) => o.id === id) ?? { id, name: "N/A" })
	// );
	let selectedOptions = $derived(
		value.map((id) => options.find((o) => o.name === id) ?? { id, name: "N/A" })
	)
	let displayLabel = $derived(
		selectedOptions.length
			? selectedOptions.map((o) => o.name).join(", ")
			: "Select option(s)"
	);

	/**
	 * If "na" is selected with others, clear "na"
	 */
	$effect(() => {
		if (value.length > 1 && value.includes("na")) {
			value = value.filter((v) => v !== "na");
		}
	});


	/**
	 * When the form resets, change the value back to "na"
	 */
	$effect(() => {
		const form = document.querySelector("#match-scouting-form");

		const reset = () => {
			value = ["na"];
		};

		form?.addEventListener("reset", reset);
		return () => form?.removeEventListener("reset", reset);
	});
</script>

<BaseField field={field} editable={editable} getFields={getFields}>
	<Select.Root
		type="multiple"
		name={field.uuid}
		required={field.required}
		bind:value
	>
		<Select.Trigger class="whitespace-normal wrap-text">
			{displayLabel}
		</Select.Trigger>

		<Select.Content>
			<Select.Label>Options</Select.Label>

			<Select.Item value="na">N/A</Select.Item>

			{#each options as option}
				<!-- TODO: Currently forcing the value to be the plain text name instead of the ID. Later use the ID to allow for translations -->
				<Select.Item value={option.name}>
					{option.name}
				</Select.Item>
			{/each}
		</Select.Content>
	</Select.Root>
</BaseField>

