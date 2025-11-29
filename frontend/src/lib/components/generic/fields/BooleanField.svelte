<script lang="ts">
	import Checkbox from "$lib/components/ui/checkbox/checkbox.svelte";
	import BaseField from "./BaseField.svelte";

    let { field, editable, getFields } = $props();

    let checked = $state(false);
</script>

<BaseField field={field} editable={editable} getFields={getFields}>
    <!-- Use a hidden input to return a boolean value always, instead of only when checked if using a checkbox -->
    <input type="hidden" name={field.uuid} value={checked ? "true" : "false"} />
    <Checkbox placeholder={field.name} required={field.required} bind:checked />
</BaseField>
