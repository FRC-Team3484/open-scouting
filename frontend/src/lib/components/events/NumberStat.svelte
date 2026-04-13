<script lang="ts">
    import * as Card from "$lib/components/ui/card/index.js";

    // color can be none,green,orange,red
    let { value, label, color = "none" } = $props();
</script>

<Card.Root>
    <Card.Content>
        <div class="flex flex-col gap-2">                
            {#if color == "green"}
                <p class="text-lg text-green-300">{value}</p>
                <p class="text-sm text-green-300/70">{label}</p>
            {:else if color == "orange"}
                <p class="text-lg text-orange-400">{value}</p>
                <p class="text-sm text-orange-400/70">{label}</p>
            {:else if color == "red"}
                <p class="text-lg text-red-400">{value}</p>
                <p class="text-sm text-red-400/70">{label}</p>
            {:else}
                <p class="text-lg">{value}</p>
                <p class="text-sm text-muted-foreground">{label}</p>
            {/if}
        </div>
    </Card.Content>
</Card.Root>