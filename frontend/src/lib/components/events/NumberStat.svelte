<script lang="ts">
    import * as Card from "$lib/components/ui/card/index.js";

    let { value, label } = $props();
</script>

<Card.Root>
    <Card.Content>
        <div class="flex flex-col gap-2">
            <p class="text-xl">{value}</p>
            <p class="text-sm text-muted-foreground">{label}</p>
        </div>
    </Card.Content>
</Card.Root>