<!-- 
@component
Match scouting field with a boolean input

Uses a "fake" checkbox to ensure there's always either a true or false value added to the form

Props:
    - `field` (`MatchScoutingFieldResponse`) - Data for this field
    - `editable` (`boolean`) - If this field is editable or not
    - `getFields` (`() => void`) - Function for fetching field data
-->
<script lang="ts">
    import Switch from "$lib/components/ui/switch/switch.svelte";

	import type { MatchScoutingFieldResponse } from "$lib/api/model";
	import BaseField from "./BaseField.svelte";


    interface Props {
        field: MatchScoutingFieldResponse
        editable: boolean
        getFields: () => void
    }
    let { field, editable, getFields }: Props = $props();

    let checked: boolean = $state(false);
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