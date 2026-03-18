<script lang="ts">
	import { Badge } from "../ui/badge";
	import Button from "../ui/button/button.svelte";

    let { match, compLevel, selectMatch, showCompLevel = false } = $props();

    let compLevelLabel = $derived.by(() => {
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

    function getTeams() {
        return [...match.alliances.red.team_keys, ...match.alliances.blue.team_keys].map(team => team.replace("frc", ""));
    }

</script>

<div class="flex flex-col lg:flex-row gap-2 lg:items-center flex-wrap">
    {#if compLevel == "sf"}
        <Button variant="outline" onclick={() => selectMatch(getTeams())}>{compLevelLabel} Match {match?.set_number}</Button>
    {:else}
        <Button variant="outline" onclick={() => selectMatch(getTeams())}>{compLevelLabel} Match {match?.match_number}</Button>
    {/if}

    <div class="flex flex-row gap-1 items-center">
        {#each match?.alliances.blue.team_keys as team}
            <Badge class="bg-blue-500">{team.replace("frc", "")}</Badge>
        {/each}
        {#each match?.alliances.red.team_keys as team}
            <Badge class="bg-red-500">{team.replace("frc", "")}</Badge>
        {/each}
    </div>
    <div class="flex flex-row gap-1 items-center">
    </div>
</div>