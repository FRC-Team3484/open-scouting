<script lang="ts">
    let { summary, features, details } = $props();
</script>

<div class="flex flex-col gap-4">
    {@render summary?.()}

    <div class="grid grid-cols-2 gap-2">
        {@render features?.()}
    </div>
    
    {@render details?.()}
</div>