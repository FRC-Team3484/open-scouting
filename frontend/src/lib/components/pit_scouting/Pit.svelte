<script lang="ts">
    import * as Card from "$lib/components/ui/card/index.js";
	import { CaretDown, CaretUp } from "phosphor-svelte";
	import Button from "../ui/button/button.svelte";
	import { slide } from "svelte/transition";

    let { pit, show_avatar = false } = $props();

    let expanded = $state(false);
    let avatar_loaded = $state(true);
</script>

<Card.Root class="w-auto md:min-w-128">
    <Card.Content>
        <div class="flex flex-col gap-4">
            <div class="flex flex-row gap-2 items-center justify-between">
                <div class="flex flex-row gap-2 items-center flex-wrap">
                    {#if show_avatar && avatar_loaded}
                        <img src={`https://www.thebluealliance.com/avatar/2026/frc${pit.team_number}.png`} class="w-10 h-10 aspect-square rounded-md bg-accent p-1" onerror={() => avatar_loaded = false}>
                    {/if}
                    
                    <p class="font-bold">{pit.team_number}</p>
                    <p class="text-sm text-muted-foreground">{pit.nickname}</p>
                </div>

                <Button size="icon" variant="ghost" onclick={() => expanded = !expanded}>
                    {#if expanded}
                        <CaretDown weight="bold" />
                    {:else}
                        <CaretUp weight="bold" />
                    {/if}
                </Button>
            </div>

            {#if expanded}
                <div class="flex flex-col gap-2 items-start" transition:slide>
                    <p>expanded</p>
                </div>
            {/if}
        </div>
    </Card.Content>
</Card.Root>