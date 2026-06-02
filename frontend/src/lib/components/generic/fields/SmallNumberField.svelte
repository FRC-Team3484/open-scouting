<!-- 
@component
Match scouting field for a small number

Uses the default browser "number" input, with -1 / +1 controls for quicker editing.
Should be used for score or miss number inputs.
LargeNumberField should be used for things like team and match numbers.

Props:
    - `field` (`MatchScoutingFieldResponse`) - Data for this field
    - `editable` (`boolean`) - If this field is editable or not
    - `getFields` (`() => void`) - Function for fetching field data
-->
<script lang="ts">
	import { MinusIcon, PlusIcon } from "phosphor-svelte";

	import Button from "$lib/components/ui/button/button.svelte";
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
    <div class="flex flex-row gap-2 items-center">
        <Input
            type="number"
            name={field.uuid}
            placeholder={field.name}
            required={field.required}
            min={field.options?.minimum ?? 0}
            max={field.options?.maximum ?? undefined}
            value={field.options?.default ?? 0}
            defaultValue={field.options?.default ?? 0}
        />

        <!-- Decrease button -->
        <Button
            class="touch-manipulation"
            type="button"
            onclick={() => {
                const input = document.querySelector(`input[name="${field.uuid}"]`) as HTMLInputElement | null;
                input?.stepDown();
            }}>
            <MinusIcon weight="bold" />
        </Button>

        <!-- Increase button -->
        <Button
            class="touch-manipulation"
            type="button"
            onclick={() => {
                const input = document.querySelector(`input[name="${field.uuid}"]`) as HTMLInputElement | null;
                input?.stepUp();
            }}>
            <PlusIcon weight="bold" />
        </Button>
    </div>
</BaseField>
