<script lang="ts">
    import * as Card from "$lib/components/ui/card/index.js";
	import Logo from "../generic/Logo.svelte";

    
</script>

<Card.Root class="mb-4">
    <div class="flex flex-row gap-4 items-center justify-between flex-wrap p-4">
        <Logo text={false} style="tiny" href="/" />
        <p class="text-2xl font-bold font-mono">Match Scouting</p>
    </div>
</Card.Root>