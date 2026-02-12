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
    <div class="flex flex-row gap-2 items-center">
        <Input
            type="number"
            name={field.uuid}
            placeholder={field.name}
            required={field.required}
            min={field.options?.minimum ?? 0}
            max={field.options?.maximum ?? undefined}
            value={field.options?.default ?? 0}
        />

        <!-- Decrease button -->
        <Button
            type="button"
            onclick={() => {
                const input = document.querySelector(`input[name="${field.uuid}"]`) as HTMLInputElement | null;
                console.log(input)
                input?.stepDown();
            }}>
            <Minus weight="bold" />
        </Button>

        <!-- Increase button -->
        <Button
            type="button"
            onclick={() => {
                const input = document.querySelector(`input[name="${field.uuid}"]`) as HTMLInputElement | null;
                input?.stepUp();
            }}>
            <Plus weight="bold" />
        </Button>
    </div>
</BaseField>
