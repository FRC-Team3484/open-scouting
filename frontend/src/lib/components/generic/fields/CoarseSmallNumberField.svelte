<!-- 
@component
Match scouting field with a coarse integer input

"Coarse" referrs to a integer value that does not need to be exact. 
This field provides -10 / -5 / -1 / +1 / +5 / +10 buttons.
Initally introduced for scouting Fuel in 2026.

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
    <div class="flex flex-col gap-4 items-center">
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

        <div class="flex flex-row gap-2 items-center">
            <Button
                class="touch-manipulation"
                type="button"
                size="lg"
                onclick={() => {
                    const input = document.querySelector(`input[name="${field.uuid}"]`) as HTMLInputElement | null;
                    input?.stepUp(1);
                }}>
                <PlusIcon weight="bold" /> 1
            </Button>
            <Button
                class="touch-manipulation"
                type="button"
                size="lg"
                onclick={() => {
                    const input = document.querySelector(`input[name="${field.uuid}"]`) as HTMLInputElement | null;
                    input?.stepUp(5);
                }}>
                <PlusIcon weight="bold" /> 5
            </Button>
            <Button
                class="touch-manipulation"
                type="button"
                size="lg"
                onclick={() => {
                    const input = document.querySelector(`input[name="${field.uuid}"]`) as HTMLInputElement | null;
                    input?.stepUp(10);
                }}>
                <PlusIcon weight="bold" /> 10
            </Button>
        </div>

        <div class="flex flex-row gap-2 items-center">
            <Button
                class="touch-manipulation"
                type="button"
                variant="outline"
                onclick={() => {
                    const input = document.querySelector(`input[name="${field.uuid}"]`) as HTMLInputElement | null;
                    input?.stepDown(1);
                }}>
                <MinusIcon weight="bold" /> 1
            </Button>
            <Button
                class="touch-manipulation"
                type="button"
                variant="outline"
                onclick={() => {
                    const input = document.querySelector(`input[name="${field.uuid}"]`) as HTMLInputElement | null;
                    input?.stepDown(5);
                }}>
                <MinusIcon weight="bold" /> 5
            </Button>
            <Button
                class="touch-manipulation"
                type="button"
                variant="outline"
                onclick={() => {
                    const input = document.querySelector(`input[name="${field.uuid}"]`) as HTMLInputElement | null;
                    input?.stepDown(10);
                }}>
                <MinusIcon weight="bold" /> 10
            </Button>
        </div>
    </div>
</BaseField>
