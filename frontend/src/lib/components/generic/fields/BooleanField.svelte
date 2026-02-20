<script lang="ts">
    import Switch from "$lib/components/ui/switch/switch.svelte";
	import BaseField from "./BaseField.svelte";

    let { field, editable, getFields } = $props();

    let checked = $state(false);
</script>

<BaseField field={field} editable={editable} getFields={getFields}>
    <!-- Use a hidden input to return a boolean value always, instead of only when checked if using a checkbox -->
    <input type="hidden" name={field.uuid} value={checked ? "true" : "false"} />
    <div class="flex flex-row gap-2 items-center">
        <Switch class="touch-manipulation" placeholder={field.name} required={field.required} bind:checked />
        <p>{checked.toString().charAt(0).toUpperCase() + checked.toString().slice(1)}</p>
    </div>
</BaseField>
