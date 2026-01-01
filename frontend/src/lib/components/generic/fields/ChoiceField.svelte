<script lang="ts">
	import * as Select from "$lib/components/ui/select/index.js";
	import BaseField from "./BaseField.svelte";

	let { field, editable, getFields } = $props();

	let value = $state("na");

	let selectedOption = $derived(
		field.options.find((o) => o.id === value) ?? { id: "na", name: "N/A" }
	);
</script>

<BaseField field={field} editable={editable} getFields={getFields}>
	<Select.Root type="single" name={field.uuid} required={field.required} bind:value>
		<Select.Trigger>
			{selectedOption.name ?? "Select an option"}
		</Select.Trigger>

		<Select.Content>
			<Select.Label>Options</Select.Label>
			<Select.Item value="na">N/A</Select.Item>
			{#each field.options as option}
				<!-- TODO: Currently forcing the value to be the plain text name instead of the ID. Later use the ID to allow for translations -->
				<Select.Item value={option.name}>
					{option.name}
				</Select.Item>
			{/each}
		</Select.Content>
	</Select.Root>
</BaseField>
