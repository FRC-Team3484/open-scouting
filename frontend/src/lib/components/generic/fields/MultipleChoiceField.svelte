<script lang="ts">
	import * as Select from "$lib/components/ui/select/index.js";
	import BaseField from "./BaseField.svelte";

	let { field, editable, getFields } = $props();

	let options = field.options.choices

	// Store selected values as an array of IDs
	let value = $state<string[]>(["na"]);

	$inspect(value);

	// Compute selected option objects from the IDs
	// TODO: Use when basing options on a UUID
	// let selectedOptions = $derived(
	// 	value.map((id) => options.find((o) => o.id === id) ?? { id, name: "N/A" })
	// );
	let selectedOptions = $derived(
		value.map((id) => options.find((o) => o.name === id) ?? { id, name: "N/A" })
	)

	// Enforce selection rules
	$effect(() => {
		// If "na" is selected alongside others, clear "na"
		if (value.length > 1 && value.includes("na")) {
			value = value.filter((v) => v !== "na");
		}
	});

	// Derived display label
	let displayLabel = $derived(
		selectedOptions.length
			? selectedOptions.map((o) => o.name).join(", ")
			: "Select option(s)"
	);
</script>

<BaseField field={field} editable={editable} getFields={getFields}>
	<Select.Root
		type="multiple"
		name={field.uuid}
		required={field.required}
		bind:value
	>
		<Select.Trigger>
			{displayLabel}
		</Select.Trigger>

		<Select.Content>
			<Select.Label>Options</Select.Label>

			<!-- "N/A" option -->
			<Select.Item value="na">N/A</Select.Item>

			<!-- All field options -->
			{#each options as option}
				<!-- TODO: Currently forcing the value to be the plain text name instead of the ID. Later use the ID to allow for translations -->
				<Select.Item value={option.name}>
					{option.name}
				</Select.Item>
			{/each}
		</Select.Content>
	</Select.Root>
</BaseField>

