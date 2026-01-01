<script lang="ts">
	import BaseTeamFolder from "./BaseTeamFolder.svelte";
	import CapabilityDisplay from "./CapabilityDisplay.svelte";

    let { capabilities } = $props();
</script>

<BaseTeamFolder title="Capabilities">
    <div class="flex flex-col gap-2 text-left">
        {#each capabilities as capability}
            <CapabilityDisplay capability={capability} />
        {/each}
    </div>
</BaseTeamFolder>