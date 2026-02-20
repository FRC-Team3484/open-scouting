<script lang="ts">
	import { flip } from "svelte/animate";
	import BaseSection from "./BaseSection.svelte";

	import StringField from "./StringField.svelte";
	import LargeNumberField from "./LargeNumberField.svelte";
	import SmallNumberField from "./SmallNumberField.svelte";
	import BooleanField from "./BooleanField.svelte";
	import ChoiceField from "./ChoiceField.svelte";
	import MultipleChoiceField from "./MultipleChoiceField.svelte";
	import Section from "./Section.svelte";
	import CoarseSmallNumberField from "./CoarseSmallNumberField.svelte";
	import { dragHandleZone } from "svelte-dnd-action";

	let { field = $bindable(), editable, getFields, updateOrders } = $props();

	function normalizeOrders(items) {
        return items.map((item, index) => ({
            ...item,
            order: index,
            fields: Array.isArray(item.fields)
                ? normalizeOrders(item.fields)
                : item.fields
        }));
    }

	function onConsider(e: any) {
		field.fields = e.detail.items;
	}

	async function onFinalize(e: any) {
		field.fields = normalizeOrders(e.detail.items);
		await updateOrders();
	}
</script>

<BaseSection field={field} editable={editable} getFields={getFields}>
	<div class="flex flex-col gap-4" use:dragHandleZone={{items: field.fields, flipDurationMs: 100}} onconsider={onConsider} onfinalize={onFinalize}>
		{#each field.fields as child (child.uuid)}
			<div animate:flip={{duration: 100}}>
				{#if child.field_type === "string"}
					<StringField field={child} editable={editable} getFields={getFields} />
				{:else if child.field_type === "large_number"}
					<LargeNumberField field={child} editable={editable} getFields={getFields} />
				{:else if child.field_type === "small_number"}
					<SmallNumberField field={child} editable={editable} getFields={getFields} />
				{:else if child.field_type === "coarse_small_number"}
					<CoarseSmallNumberField field={child} editable={editable} getFields={getFields} />
				{:else if child.field_type === "boolean"}
					<BooleanField field={child} editable={editable} getFields={getFields} />
				{:else if child.field_type === "choice"}
					<ChoiceField field={child} editable={editable} getFields={getFields} />
				{:else if child.field_type === "multiple_choice"}
					<MultipleChoiceField field={child} editable={editable} getFields={getFields} />
				{:else if child.field_type === "section"}
					<Section field={child} editable={editable} getFields={getFields} updateOrders={updateOrders} />
				{/if}
			</div>
		{/each}

		{#if field.fields.length === 0 && editable}
			<div class="flex flex-col items-center justify-center py-16 px-16 border-2 border-dashed border-muted-foreground rounded-md">
				<p class="text-muted-foreground">No fields</p>
				<p class="text-muted-foreground text-sm">Drag and drop fields here</p>
			</div>
		{/if}
	</div>
</BaseSection>
