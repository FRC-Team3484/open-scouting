<script lang="ts">
	import Input from "$lib/components/ui/input/input.svelte";
	import BaseField from "./BaseField.svelte";

    export let field: any;
    export let editable: boolean = false;
    export let getFields: () => void = () => {};
</script>

<BaseField field={field} editable={editable} getFields={getFields}>
    <Input type="number" name={field.uuid} placeholder={field.name} required={field.required} />
</BaseField>
