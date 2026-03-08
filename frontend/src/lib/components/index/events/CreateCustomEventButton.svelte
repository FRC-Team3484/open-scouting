<script lang="ts">
	import Button from "$lib/components/ui/button/button.svelte";
    import * as Card from "$lib/components/ui/card/index.js";
	import { createCustomEventDialogOpen } from "$lib/stores/dialog";
</script>

<Card.Root class="mb-2">
    <Card.Content class="flex flex-col gap-2">
        <p>Is an event mising on The Blue Alliance?</p>
        <Button variant="default" class="w-full" onclick={() => {createCustomEventDialogOpen.set(true)}}>Create Custom Event</Button>
    </Card.Content>
</Card.Root>