<script lang="ts">
    import * as Card from "$lib/components/ui/card/index.js";
	import { CaretDown, CaretUp } from "phosphor-svelte";
	import Button from "../ui/button/button.svelte";
	import { slide } from "svelte/transition";
	import TeamScores from "./TeamScores.svelte";
	import TeamCapabilities from "./TeamCapabilities.svelte";
	import TeamOthers from "./TeamOthers.svelte";

    let { team } = $props();

    let expanded = $state(false);
</script>

<Card.Root>
    <Card.Content>
        <div class="flex flex-col gap-2">
            <div class="flex flex-row gap-2 justify-between">
                <div class="flex flex-row gap-2 items-center">
                    <p class="font-bold">{team.team_number}</p>
                    <p class="text-muted-foreground">{team.nickname}</p>
                </div>

                <Button size="icon-sm" variant="ghost" onclick={() => expanded = !expanded}>
                    {#if expanded}
                        <CaretDown weight="bold" />
                    {:else}
                        <CaretUp weight="bold" />
                    {/if}
                </Button>
            </div>

            {#if expanded}
                <div class="flex flex-col gap-4" transition:slide>
                    <!-- Autonomous -->
                    <TeamScores title="Autonomous" gamePieces={team.auton} />

                    <!-- Teleoperated -->
                    <TeamScores title="Teleoperated" gamePieces={team.teleop} />
                    
                    <!-- Capabilities -->
                    <TeamCapabilities capabilities={team.capability} />

                    <!-- Other -->
                    <TeamOthers others={team.other} />
                </div>
            {/if}
        </div>
    </Card.Content>
</Card.Root>