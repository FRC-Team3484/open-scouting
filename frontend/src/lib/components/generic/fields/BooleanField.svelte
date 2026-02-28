<script lang="ts">
    import Switch from "$lib/components/ui/switch/switch.svelte";
	import BaseField from "./BaseField.svelte";

    let { field, editable, getFields } = $props();

    let checked = $state(false);
</script>

<BaseField field={field} editable={editable} getFields={getFields}>
    <div class="flex flex-row gap-2 items-center">
        <input
            type="hidden"
            name={field.uuid}
            value="false"
            disabled={checked}
        />

        <input
            type="checkbox"
            class="sr-only"
            name={field.uuid}
            value="true"
            bind:checked
        />

        <Switch
            checked={checked}
            onCheckedChange={() => (checked = !checked)}
            class="touch-manipulation"
            required={field.required}
        />

        <p>{checked ? "True" : "False"}</p>
    </div>
</BaseField>