<!-- 
@component
Generic filter list component, given a list of values and labels, used for filters on the data page

Provides an "Add" button, and a list of the selected values

@deprecated Should soon be replaced with a better equivalent.
Similar to EventList, create a dedicated list for team filtering.
Create a better list for field filtering.

Props:
    - `filterTitle` (`string`) - The title of the filter list
    - `values` (`any[]`) - The list of values
    - `labels` (`string[]`) - The corresponding list of labels
    - `selected` (`any[]`) - The selected values
    - `onlyOne` (`boolean`) - If only one value should be able to be selected at once
-->
<script lang="ts">
	import { PlusCircleIcon, TrashIcon, XIcon } from "phosphor-svelte";

	import Button from "../ui/button/button.svelte";
	import Input from "../ui/input/input.svelte";
	import Separator from "../ui/separator/separator.svelte";
	import BaseDialog from "../generic/dialogs/BaseDialog.svelte";


    interface Props {
        filterTitle: string
        values: any[]
        labels: string[]
        selected: any[]
        onlyOne: boolean
    }
    let { filterTitle, values, labels, selected = $bindable([]), onlyOne = false }: Props = $props();

    let open: boolean = $state(false);
    let search: string = $state("");

    let filteredValues = $derived(
        values.filter((value) => !selected.includes(value))
            .filter((value) => labels[values.indexOf(value)].toLowerCase().includes(search.toLowerCase()) || value.toLowerCase().includes(search.toLowerCase()))
    )

    /**
     * Select an item and close the menu
     * 
     * @param value The value to select
     */
    function addItem(value) {
        selected = [...selected, value];
        open = false;
        search = "";
    }

    /**
     * Delete an item from the list of selected values
     * 
     * @param value The value to delete from the selected values
     */
    function deleteItem(value) {
        selected = selected.filter((item) => item !== value);
        open = false;
        search = "";
    }
</script>

<div class="flex flex-row gap-2 max-h-screen max-w-screen flex-wrap items-center">
    {#if !onlyOne}
        <Button variant="outline" onclick={() => open = true}><PlusCircleIcon weight="bold" /> Add</Button>
    {:else}
        <Button variant="outline" onclick={() => open = true} disabled={selected.length > 0}><PlusCircleIcon weight="bold" />Set</Button>
    {/if}

    <BaseDialog bind:open={open} title={filterTitle} description="Select an item to add">
        <div class="flex flex-col gap-2 overflow-y-scroll">
            <div class="flex flex-row gap-2">
                <Input type="text" placeholder="Search..." bind:value={search} />
                <Button size="icon-sm" variant="outline" onclick={() => search = ""} ><TrashIcon weight="bold" /></Button>
            </div>

            <Separator orientation="horizontal" />

            {#each filteredValues as value}
                <div class="flex flex-row gap-2 items-center">
                    <Button variant="ghost" onclick={() => addItem(value)}>{labels[values.indexOf(value)]}</Button>
                </div>
            {/each}

            {#if filteredValues.length <= 0}
                <p class="text-muted-foreground text-sm text-center mt-2">No matches found</p>
            {/if}
        </div>
    </BaseDialog>
    
    {#each selected as value}
        <Button variant="outline" size="sm" onclick={() => deleteItem(value)} ><XIcon weight="bold" /> {labels[values.indexOf(value)] || value}</Button>
    {/each}
</div>

