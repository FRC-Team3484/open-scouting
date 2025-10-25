<script lang="ts">
	import Checkbox from "$lib/components/ui/checkbox/checkbox.svelte";
	import BaseField from "./BaseField.svelte";

    export let field: any;
    export let editable: boolean = false;
    export let getFields: () => void = () => {};
</script>

<BaseField field={field} editable={editable} getFields={getFields}>
    <Checkbox name={field.uuid} placeholder={field.name} required={field.required} />
</BaseField>
