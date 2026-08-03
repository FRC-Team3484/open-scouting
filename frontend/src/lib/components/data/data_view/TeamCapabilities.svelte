<!-- 
@component
The capabilities section for each team on the default data view page

Props:
    - `capabilities` (`DataCapabilityStatEntry[]`) - All capabilities for the team
-->
<script lang="ts">
	import type { DataCapabilityStatEntry } from "$lib/api/model";
	import BaseTeamFolder from "./BaseTeamFolder.svelte";
	import CapabilityDisplay from "./displays/CapabilityDisplay.svelte";


    interface Props {
        capabilities: DataCapabilityStatEntry[]
    }
    let { capabilities }: Props = $props();
</script>

<BaseTeamFolder title="Capabilities">
    <div class="flex flex-col gap-2 text-left">
        {#each capabilities as capability}
            <CapabilityDisplay capability={capability} />
        {/each}
    </div>
</BaseTeamFolder>