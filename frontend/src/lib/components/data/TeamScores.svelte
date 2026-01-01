<script lang="ts">
	import ScoreDisplay from "./ScoreDisplay.svelte";
	import BaseTeamFolder from "./BaseTeamFolder.svelte";

    let { title, gamePieces } = $props();
</script>

<BaseTeamFolder title={title}>
    <div class="flex flex-col gap-2 text-left">
        {#each Object.entries(gamePieces) as [key, value]}
            <div class="flex flex-col gap-2 text-left border-l-border border-l-2 pl-2">
                <p class="font-bold">{key}</p>
                {#each value as field}
                    <ScoreDisplay field={field} />
                {/each}
            </div>
        {/each}
    </div>
</BaseTeamFolder>
