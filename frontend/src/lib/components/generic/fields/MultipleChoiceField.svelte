<script lang="ts">
    import * as Select from "$lib/components/ui/select/index.js";
    import BaseField from "./BaseField.svelte";

    export let field: any;
    export let editable: boolean = false;
    export let getFields: () => void = () => {};
</script>

<BaseField field={field} editable={editable} getFields={getFields}>
    <p>TODO</p>
    <!-- <Select.Root type="single" name={field.id} required={field.required}>
        <Select.Trigger>
            {field.options[0].id}
        </Select.Trigger>
        <Select.Content>
            <Select.Label>Options</Select.Label>
            {#each field.options as option}
                <Select.Item value={option.id} label={option.label} />
            {/each}
        </Select.Content>
    </Select.Root> -->
</BaseField>
