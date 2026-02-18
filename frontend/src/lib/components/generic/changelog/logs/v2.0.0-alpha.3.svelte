<script lang="ts">
	import { CalendarCheck, ChartBar, FilmScript } from "phosphor-svelte";
	import MajorFeature from "../MajorFeature.svelte";
	import Generic from "./Generic.svelte";
</script>

{#snippet summary()}
    <p>This release fixes several bugs, improves usability and some small features, and adds the ability to create custom events.</p>
{/snippet}

{#snippet features()}
    <MajorFeature text="Custom Events">
        {#snippet icon()}
            <CalendarCheck weight="bold" />
        {/snippet}
    </MajorFeature>
    
    <MajorFeature text="Unified Dialog Handler">
        {#snippet icon()}
            <FilmScript weight="bold" />
        {/snippet}
    </MajorFeature>

    <MajorFeature text="Direct Data View Links">
        {#snippet icon()}
            <ChartBar weight="bold" />
        {/snippet}
    </MajorFeature>
{/snippet}

{#snippet details()}

{/snippet}

<Generic summary={summary} features={features} details={details} />