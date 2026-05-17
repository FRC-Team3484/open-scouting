<!-- 
@component
Match scouting field with a single choice input from a given list of choices

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

	let value = $state("na");

	let selectedChoice = $derived(
		field.options.choices?.find((o) => o.name === value) ?? { id: "na", name: "N/A" }
	);
</script>

<BaseField field={field} editable={editable} getFields={getFields}>
	<Select.Root type="single" name={field.uuid} required={field.required} bind:value>
		<Select.Trigger>
			{selectedChoice.name ?? "Select an option"}
		</Select.Trigger>

		<Select.Content>
			<Select.Label>Options</Select.Label>
			<Select.Item value="na">N/A</Select.Item>
			{#each field.options.choices as choice}
				<!-- TODO: Currently forcing the value to be the plain text name instead of the ID. Later use the ID to allow for translations -->
				<Select.Item value={choice.name}>
					{choice.name}
				</Select.Item>
			{/each}
		</Select.Content>
	</Select.Root>
</BaseField>
