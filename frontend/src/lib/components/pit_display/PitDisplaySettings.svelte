<script lang="ts">
	import { FadersIcon } from "phosphor-svelte";
	import BaseDialog from "../generic/dialogs/BaseDialog.svelte";
	import Button from "../ui/button/button.svelte";
    import * as Select from "../ui/select/index.js";
	import Separator from "../ui/separator/separator.svelte";
    import * as Card from "../ui/card/index.js";
	import BaseSection from "./widget_settings/BaseSection.svelte";


    let { widgets = $bindable() } = $props();


    let settingsOpen: boolean = $state(false);

    let selectedViewOption: "horizontal" | "vertical" = $state("horizontal");
    let viewOptions = [
        { name: "Horizontally", value: "horizontal" },
        { name: "Vertically", value: "vertical" }
    ]
    let viewOptionLabel = $derived(
        viewOptions.find((option) => option.value === selectedViewOption)?.name
    )
</script>

<Button onclick={() => settingsOpen = true} class="fixed bottom-4 left-[50%] translate-x-[-50%]"><FadersIcon weight="bold" /> Settings</Button>

<BaseDialog title="Pit Display Settings" description="Customize the appearance of the pit display" bind:open={settingsOpen}>
    <div class="flex flex-col gap-2">
        <p class="text-muted-foreground mb-2">The pit display is broken into two sections. Customize which widget goes in each section here.</p>
        <p>View widgets:</p>
        <Select.Root bind:value={selectedViewOption} type="single">
            <Select.Trigger>{viewOptionLabel}</Select.Trigger>
            <Select.Content>
                <Select.Label>View Options</Select.Label>
                {#each viewOptions as option}
                    <Select.Item value={option.value} label={option.name} />
                {/each}
            </Select.Content>
        </Select.Root>
        <Separator orientation="horizontal" />

        <BaseSection section="one" orientation={selectedViewOption} bind:widgets={widgets} />
        <BaseSection section="two" orientation={selectedViewOption} bind:widgets={widgets} />

        
    </div>
</BaseDialog>