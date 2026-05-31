<!-- 
@component
Component for each section, handling drag and drop and rendering child components

Handles dragging and dropping, and updating the orders for each field after a drag
	and drop has completed

TODO: MatchScoutingFieldResponse has no property "fields"

Props:
    - `field` (`MatchScoutingFieldResponse[]`) - This section's data
    - `editable` (`boolean`) - If the field is editable or not
    - `getFields` (`() => void`) - Function for fetching fields again
    - `updateOrders` (`() => Promise<void>`) - Function for updating the orders of child components
-->
<script lang="ts">
	import { flip } from "svelte/animate";
	import BaseSection from "./BaseSection.svelte";
	import { dragHandleZone } from "svelte-dnd-action";

	import type { MatchScoutingFieldResponse } from "$lib/api/model";
	import StringField from "./StringField.svelte";
	import LargeNumberField from "./LargeNumberField.svelte";
	import SmallNumberField from "./SmallNumberField.svelte";
	import BooleanField from "./BooleanField.svelte";
	import ChoiceField from "./ChoiceField.svelte";
	import MultipleChoiceField from "./MultipleChoiceField.svelte";
	import Section from "./Section.svelte";
	import CoarseSmallNumberField from "./CoarseSmallNumberField.svelte";

	interface Props {
        field: MatchScoutingFieldResponse
        editable: boolean
        getFields: () => void
        updateOrders: () => Promise<void>
    }
	let { field = $bindable(), editable, getFields, updateOrders }: Props = $props();

	/**
	 * Given a list of fields, adjust their internal orders to match their position in the list
	 * 
	 * @param fields The fields to normalize
	 */
	function normalizeOrders(fields: MatchScoutingFieldResponse[]): MatchScoutingFieldResponse[] {
        return fields.map((item, index) => ({
            ...item,
            order: index,
            fields: Array.isArray(item.fields)
                ? normalizeOrders(item.fields)
                : item.fields
        }));
    }

	/**
	 * What to do when the user is hovering a field in the drag and drop zone
	 * 
	 * @param e
	 */
	function onConsider(e: any): void {
		field.fields = e.detail.items;
	}

	/**
	 * What to do when the user has released a field into the drag and drop zone
	 * 
	 * @param e
	 */
	async function onFinalize(e: any): Promise<void> {
		field.fields = normalizeOrders(e.detail.items);
		await updateOrders();
	}
</script>

{#snippet fieldsBlock()}
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
{/snippet}

<BaseSection field={field} editable={editable} getFields={getFields}>
	{#if editable}
		<div class="flex flex-col gap-4" use:dragHandleZone={{items: field.fields, flipDurationMs: 100, dropTargetStyle: {outline: 'var(--primary) dashed 2px', borderRadius: 'var(--radius)'}}} onconsider={onConsider} onfinalize={onFinalize}>
			{@render fieldsBlock()}

			{#if field.fields.length === 0 && editable}
				<div class="flex flex-col items-center justify-center py-16 px-16 border-2 border-dashed border-muted-foreground rounded-md">
					<p class="text-muted-foreground">No fields</p>
					<p class="text-muted-foreground text-sm">Drag and drop fields here</p>
				</div>
			{/if}
		</div>
	{:else}
		<div class="flex flex-col gap-4">
			{@render fieldsBlock()}
		</div>
	{/if}
</BaseSection>
