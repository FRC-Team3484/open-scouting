<!-- 
@component

The header component for the event page
-->
<script lang="ts">
    import * as Card from "$lib/components/ui/card/index.js";

	import Logo from "../generic/Logo.svelte";
</script>

<Card.Root>
    <Card.Content>
        <div class="flex flex-row gap-2 items-center">
            <Logo text={false} style="tiny" href="/" />

            <p class="text-lg font-bold">Event Details</p>
        </div>
    </Card.Content>
</Card.Root>

