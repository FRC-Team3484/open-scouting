<!-- 
@component
The capabilities section for each team on the default data view page

Props:
    - `capabilities` (`unknown`) - All capabilities for the team
-->
<script lang="ts">
	import BaseTeamFolder from "./BaseTeamFolder.svelte";
	import CapabilityDisplay from "./displays/CapabilityDisplay.svelte";


    // TODO: `data` from DataManager needs a proper response schema
    interface Props {
        capabilities: unknown
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