<script lang="ts">
    let { others } = $props();
</script>

<div class="flex flex-col gap-2 text-left border-l-border border-l-2 pl-2">
    <p class="font-bold text-lg">Other</p>
    {#each others as other}
        <p class="text-sm">{other.field_name}</p>
    {/each}
</div>