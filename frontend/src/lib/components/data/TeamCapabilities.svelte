<script lang="ts">
    let { capabilities } = $props();
</script>

<div class="flex flex-col gap-2 text-left border-l-border border-l-2 pl-2">
    <p class="font-bold text-lg">Capabilities</p>
    {#each capabilities as capability}
        <p class="text-sm">{capability.field_name}</p>
    {/each}
</div>