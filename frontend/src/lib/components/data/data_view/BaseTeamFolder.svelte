<!-- 
@component
The base folder for each team section (TeamSummary, TeamScores, TeamCapabilities and TeamOthers)

Allows for collapsing the section, and shows an error if there's no avaliable data

Props:
    - `title` (`string`) - The title of the section
    - `children` (`children`) - The child components of the section
    - `expanded` (`boolean`) - If the section is expanded by default or not
-->
<script lang="ts">
	import { slide } from "svelte/transition";
	import type { Snippet } from "svelte";
	import { CaretDownIcon, CaretUpIcon } from "phosphor-svelte";

    import * as Card from "$lib/components/ui/card/index.js";
	import Button from "../../ui/button/button.svelte";


    interface Props {
        title: string
        children: Snippet
        expanded?: boolean
    }
    let { title, children, expanded = false }: Props = $props();
</script>

<Card.Root>
    <Card.Content>
        <div class="flex flex-row gap-2 items-center justify-between">
            <p class="font-bold text-lg">{title}</p>

            <Button size="icon-sm" variant="ghost" onclick={() => expanded = !expanded}>
                {#if expanded}
                    <CaretDownIcon weight="bold" />
                {:else}
                    <CaretUpIcon weight="bold" />
                {/if}
            </Button>
        </div>

        {#if expanded}
            <div class="flex flex-col gap-2 mt-4" transition:slide>
                {#if children}
                    {@render children()}
                {:else}
                    <p class="text-muted-foreground">No data found</p>
                {/if}
            </div>
        {/if}
    </Card.Content>
</Card.Root>