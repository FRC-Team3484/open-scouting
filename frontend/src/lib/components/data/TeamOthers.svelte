<script lang="ts">
	import BaseTeamFolder from "./BaseTeamFolder.svelte";
    
    let { others } = $props();
</script>

<BaseTeamFolder title="Other">
    <div class="flex flex-col gap-2 text-left">
        <p class="font-bold text-lg">Other</p>
        {#each others as other}
            <p class="text-sm">{other.field_name}</p>
        {/each}
    </div>
</BaseTeamFolder>