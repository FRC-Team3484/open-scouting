<!-- 
@component
Displays a single row of teams for a given match in the select match dialog

Props:
    - `match` (`Match`) - The information from the parent about that match
    - `compLevel` (`string`) - The competition level of that match
    - `selectMatch` (`(teams: string[]) => void`) - Given a list of team numbers, add those team numbers to the filters
    - `showCompLevel?` (`boolean`) - If the competition level should be shown or not
-->
<script lang="ts">
	import { Badge } from "../../../ui/badge";
	import Button from "../../../ui/button/button.svelte";

	import { type Match } from "./SelectMatchDialog.svelte";

    
    interface Props {
        match: Match
        compLevel: string
        selectMatch: (teams: string[]) => void
        showCompLevel?: boolean
    }
    let { match, compLevel, selectMatch, showCompLevel = false }: Props = $props();

    let compLevelLabel: string = $derived.by(() => {
        if (showCompLevel == false) {
            return ""
        }

        if (compLevel == "sf") {
            return "Semifinals"
        } else if (compLevel == "f") {
            return "Finals"
        } else {
            return "Qualification"
        }
    });

    /**
     * Get the team numbers from the match information
     */
    function getTeams(): string[] {
        return [...match.alliances.red.team_keys, ...match.alliances.blue.team_keys].map(team => team.replace("frc", ""));
    }
</script>

{#snippet teams()}
    <div class="flex flex-row gap-1 items-center flex-wrap">
        <div class="flex flex-row gap-1 flex-wrap">
            {#each match?.alliances.blue.team_keys as team}
                <Badge class="bg-blue-500">{team.replace("frc", "")}</Badge>
            {/each}
        </div>
        <div class="flex flex-row gap-1 flex-wrap">
            {#each match?.alliances.red.team_keys as team}
                <Badge class="bg-red-500">{team.replace("frc", "")}</Badge>
            {/each}
        </div>
    </div>
{/snippet}

<div class="flex flex-col lg:flex-row gap-2 lg:items-center flex-wrap">
    {#if compLevel == "sf"}
        <Button variant="outline" class="flex! h-auto! min-h-9! flex-wrap! whitespace-normal! wrap-break-word! items-start! shrink! justify-start! text-left" onclick={() => selectMatch(getTeams())}>{compLevelLabel} Match {match?.set_number} {@render teams()}</Button>
    {:else}
        <Button variant="outline" class="flex! h-auto! min-h-9! flex-wrap! whitespace-normal! wrap-break-word! items-start! shrink! justify-start! text-left" onclick={() => selectMatch(getTeams())}>{compLevelLabel} Match {match?.match_number} {@render teams()}</Button>
    {/if}
</div>