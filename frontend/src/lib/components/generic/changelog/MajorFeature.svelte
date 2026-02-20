<script lang="ts">
    import * as Card from "$lib/components/ui/card/index.js";

    let { icon, text } = $props();
</script>

<div class="flex flex-col gap-2 justify-center rounded-sm shadow-sm bg-secondary border-card-foreground border p-2">
    <div class="flex flex-row gap-2 items-center">
        {@render icon?.()}
        <p class="text-sm">{text}</p>
    </div>
</div>