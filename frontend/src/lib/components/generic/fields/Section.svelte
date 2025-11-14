<script lang="ts">
	import BaseSection from "./BaseSection.svelte";

	import StringField from "./StringField.svelte";
	import LargeNumberField from "./LargeNumberField.svelte";
	import SmallNumberField from "./SmallNumberField.svelte";
	import BooleanField from "./BooleanField.svelte";
	import ChoiceField from "./ChoiceField.svelte";
	import MultipleChoiceField from "./MultipleChoiceField.svelte";
	import Section from "./Section.svelte";

	let { field, editable, getFields } = $props();
</script>

<BaseSection field={field} editable={editable} getFields={getFields}>
	<div class="flex flex-col gap-4">
		{#each field.fields as child (child.uuid)}
			{#if child.field_type === "string"}
				<StringField field={child} editable={editable} getFields={getFields} />
			{:else if child.field_type === "large_number"}
				<LargeNumberField field={child} editable={editable} getFields={getFields} />
			{:else if child.field_type === "small_number"}
				<SmallNumberField field={child} editable={editable} getFields={getFields} />
			{:else if child.field_type === "boolean"}
				<BooleanField field={child} editable={editable} getFields={getFields} />
			{:else if child.field_type === "choice"}
				<ChoiceField field={child} editable={editable} getFields={getFields} />
			{:else if child.field_type === "multiple_choice"}
				<MultipleChoiceField field={child} editable={editable} getFields={getFields} />
			{:else if child.field_type === "section"}
				<Section field={child} editable={editable} getFields={getFields} />
			{/if}
		{/each}
	</div>
</BaseSection>
