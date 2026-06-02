<!-- 
@component
The scores and miss section for each team on the default data view page

Props:
    - `title` (`string`) - The title of this section
    - `gamePieces` (`[key: string]: DataNumericStatEntry[]`) - The game piece information from the server
-->
<script lang="ts">
	import ScoreDisplay from "./displays/ScoreDisplay.svelte";
	import BaseTeamFolder from "./BaseTeamFolder.svelte";
	import type { DataNumericStatEntry } from "$lib/api/model";


    interface Props {
        title: string
        gamePieces: { [key: string]: DataNumericStatEntry[] }
    }
    let { title, gamePieces }: Props = $props();
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
