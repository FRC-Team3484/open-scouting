<!-- 
@component
Match scouting field for a large number

Uses the default browser "number" input, without any special controls.
Should be used for regular number inputs, like team or match numbers. 
SmallNumberField should be used for game piece scores or misses.

Props:
    - `field` (`MatchScoutingFieldResponse`) - Data for this field
    - `editable` (`boolean`) - If this field is editable or not
    - `getFields` (`() => void`) - Function for fetching field data
-->
<script lang="ts">
	import Input from "$lib/components/ui/input/input.svelte";

	import type { MatchScoutingFieldResponse } from "$lib/api/model";
	import BaseField from "./BaseField.svelte";

    interface Props {
        field: MatchScoutingFieldResponse
        editable: boolean
        getFields: () => void
    }
    let { field, editable, getFields }: Props = $props();
</script>

<BaseField field={field} editable={editable} getFields={getFields}>
    <Input type="number" name={field.uuid} placeholder={field.name} required={field.required} />
</BaseField>
