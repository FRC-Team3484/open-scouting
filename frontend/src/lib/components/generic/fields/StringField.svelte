<!-- 
@component
Match scouting field with a string input

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
    <Input type="text" name={field.uuid} placeholder={field.name} required={field.required} />
</BaseField>
