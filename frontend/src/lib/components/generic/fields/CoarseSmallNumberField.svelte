<script lang="ts">
	import Button from "$lib/components/ui/button/button.svelte";
	import Input from "$lib/components/ui/input/input.svelte";
	import { Minus, Plus } from "phosphor-svelte";
	import BaseField from "./BaseField.svelte";

    export let field: any;
    export let editable: boolean = false;
    export let getFields: () => void = () => {};
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
                <Plus weight="bold" /> 1
            </Button>
            <Button
                class="touch-manipulation"
                type="button"
                size="lg"
                onclick={() => {
                    const input = document.querySelector(`input[name="${field.uuid}"]`) as HTMLInputElement | null;
                    input?.stepUp(5);
                }}>
                <Plus weight="bold" /> 5
            </Button>
            <Button
                class="touch-manipulation"
                type="button"
                size="lg"
                onclick={() => {
                    const input = document.querySelector(`input[name="${field.uuid}"]`) as HTMLInputElement | null;
                    input?.stepUp(10);
                }}>
                <Plus weight="bold" /> 10
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
                <Minus weight="bold" /> 1
            </Button>
            <Button
                class="touch-manipulation"
                type="button"
                variant="outline"
                onclick={() => {
                    const input = document.querySelector(`input[name="${field.uuid}"]`) as HTMLInputElement | null;
                    input?.stepDown(5);
                }}>
                <Minus weight="bold" /> 5
            </Button>
            <Button
                class="touch-manipulation"
                type="button"
                variant="outline"
                onclick={() => {
                    const input = document.querySelector(`input[name="${field.uuid}"]`) as HTMLInputElement | null;
                    input?.stepDown(10);
                }}>
                <Minus weight="bold" /> 10
            </Button>
        </div>
    </div>
</BaseField>
