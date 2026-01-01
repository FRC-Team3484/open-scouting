<script lang="ts">
	import BaseTeamFolder from "./BaseTeamFolder.svelte";

    let { capabilities } = $props();
</script>

<BaseTeamFolder title="Capabilities">
    <div class="flex flex-col gap-2 text-left">
        <p class="font-bold text-lg">Capabilities</p>
        {#each capabilities as capability}
            <p class="text-sm">{capability.field_name}</p>
        {/each}
    </div>
</BaseTeamFolder>