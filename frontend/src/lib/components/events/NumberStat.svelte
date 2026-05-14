<!-- 
@component
A number stat display for the event page

Shows scouting information for an event

Props:
    - `value` (`string | number`) - The value to display
    - `label` (`string`) - The label for the stat
    - `color` (`none | green | orange | red`) - The color of the number stat
-->
<script lang="ts">
    import * as Card from "$lib/components/ui/card/index.js";

    
    interface Props {
        value: string | number
        label: string
        color: "none" | "green" | "orange" | "red"
    }
    let { value, label, color = "none" }: Props = $props();
</script>

<Card.Root class="p-2">
    <Card.Content class="p-2">
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