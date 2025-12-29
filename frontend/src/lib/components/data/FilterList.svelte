<script lang="ts">
    import * as Popover from "$lib/components/ui/popover/index.js";
    import * as Drawer from "$lib/components/ui/drawer/index.js";
	import { onMount } from "svelte";
	import Button from "../ui/button/button.svelte";
	import { PlusCircle, Trash, X, XCircle } from "phosphor-svelte";
	import Input from "../ui/input/input.svelte";
	import Separator from "../ui/separator/separator.svelte";
	import { browser } from "$app/environment";

    let { filterTitle, values, labels, selected = $bindable([]) } = $props();

    let open = $state(false);
    let search = $state("");
    let isDesktop = $state(false);

    let filteredValues = $derived(
        values.filter((value) => !selected.includes(value))
            .filter((value) => labels[values.indexOf(value)].toLowerCase().includes(search.toLowerCase()) || value.toLowerCase().includes(search.toLowerCase()))
    )

    function addItem(value) {
        selected = [...selected, value];
        open = false;
        search = "";
    }

    function deleteItem(value) {
        selected = selected.filter((item) => item !== value);
        open = false;
        search = "";
    }

    function checkScreenSize() {
        // tailwind-css' md breakpoint is 768 pixels
        isDesktop = window.innerWidth >= 768;
    }

    onMount(() => {
        if (browser) {
            checkScreenSize();
            window.addEventListener("resize", checkScreenSize);
            return () => window.removeEventListener("resize", checkScreenSize);
        }
    })
</script>

{#snippet filters()}
    <div class="flex flex-col gap-2 overflow-y-scroll">
        <div class="flex flex-row gap-2 items-center justify-between">
            <p class="font-bold">{filterTitle}</p>
            <Button size="icon-sm" variant="outline" onclick={() => open = false}><XCircle weight="bold" /></Button>
        </div>

        <div class="flex flex-row gap-2">
            <Input type="text" placeholder="Search..." bind:value={search} />
            <Button size="icon-sm" variant="outline" onclick={() => search = ""} ><Trash weight="bold" /></Button>
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
{/snippet}

<div class="flex flex-row gap-2 max-h-screen max-w-screen flex-wrap items-center">
    {#if isDesktop}
        <Popover.Root bind:open>
            <Popover.Trigger>
                <Button variant="outline"><PlusCircle weight="bold" /> Add</Button>
            </Popover.Trigger>

            <Popover.Content>
                {@render filters()}
            </Popover.Content>
        </Popover.Root>
    {:else}
        <Drawer.Root bind:open>
            <Drawer.Trigger>
                <Button variant="outline"><PlusCircle weight="bold" /> Add</Button>
            </Drawer.Trigger>

            <Drawer.Content class="p-4">
                {@render filters()}
            </Drawer.Content>
        </Drawer.Root>
    {/if}
    
    {#each selected as value}
        <Button variant="outline" size="sm" onclick={() => deleteItem(value)} ><X weight="bold" /> {labels[values.indexOf(value)]}</Button>
    {/each}
</div>

