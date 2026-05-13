<!-- 
@component
Container component for each team on the default data view page

Props:
    - `team` (`unknown`) - The team information from the server
-->
<script lang="ts">
	import { slide } from "svelte/transition";
	import { CaretDownIcon, CaretUpIcon } from "phosphor-svelte";

    import * as Card from "$lib/components/ui/card/index.js";

	import Button from "../../ui/button/button.svelte";
	import TeamScores from "./TeamScores.svelte";
	import TeamCapabilities from "./TeamCapabilities.svelte";
	import TeamOthers from "./TeamOthers.svelte";
	import TeamSummary from "./TeamSummary.svelte";


    // TODO: `data` from DataManager needs a proper response schema
    interface Props {
        team: unknown
    }
    let { team }: Props = $props();

    let expanded: boolean = $state(false);
</script>

<Card.Root class="py-2 md:py-6">
    <Card.Content>
        <div class="flex flex-col gap-2 lg:min-w-lg max-w-[80vw]">
            <div class="flex flex-row gap-2 justify-between">
                <div class="flex flex-row gap-2 items-center">
                    <p class="font-bold">{team.team_number}</p>
                    <p class="text-muted-foreground">{team.nickname}</p>
                </div>

                <Button size="icon-sm" variant="ghost" onclick={() => expanded = !expanded}>
                    {#if expanded}
                        <CaretDownIcon weight="bold" />
                    {:else}
                        <CaretUpIcon weight="bold" />
                    {/if}
                </Button>
            </div>

            {#if expanded}
                <div class="flex flex-col gap-1 md:gap-4" transition:slide>
                    <!-- Summary -->
                    <TeamSummary fields={team.summary} />

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