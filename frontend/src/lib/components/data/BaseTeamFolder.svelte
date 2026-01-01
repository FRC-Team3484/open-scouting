<script lang="ts">
	import { slide } from "svelte/transition";
    import * as Card from "$lib/components/ui/card/index.js";
	import Button from "../ui/button/button.svelte";
	import { CaretDown, CaretUp } from "phosphor-svelte";

    let { title, children } = $props();

    let expanded = $state(false);
</script>

<Card.Root>
    <Card.Content>
        <div class="flex flex-row gap-2 items-center justify-between">
            <p class="font-bold text-lg">{title}</p>

            <Button size="icon-sm" variant="ghost" onclick={() => expanded = !expanded}>
                {#if expanded}
                    <CaretDown weight="bold" />
                {:else}
                    <CaretUp weight="bold" />
                {/if}
            </Button>
        </div>

        {#if expanded}
            <div class="flex flex-col gap-2 mt-4" transition:slide>
                {@render children()}
            </div>
        {/if}
    </Card.Content>
</Card.Root>