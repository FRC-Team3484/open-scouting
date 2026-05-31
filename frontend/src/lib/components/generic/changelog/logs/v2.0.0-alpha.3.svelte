<script lang="ts">
	import { CalendarCheckIcon, ChartBarIcon, FilmScriptIcon } from "phosphor-svelte";
	import MajorFeature from "../MajorFeature.svelte";
	import Generic from "./Generic.svelte";
</script>

{#snippet summary()}
    <p>This release fixes several bugs, improves usability and some small features, and adds the ability to create custom events.</p>
{/snippet}

{#snippet features()}
    <MajorFeature text="Custom Events">
        {#snippet icon()}
            <CalendarCheckIcon weight="bold" />
        {/snippet}
    </MajorFeature>
    
    <MajorFeature text="Unified Dialog Handler">
        {#snippet icon()}
            <FilmScriptIcon weight="bold" />
        {/snippet}
    </MajorFeature>

    <MajorFeature text="Direct Data View Links">
        {#snippet icon()}
            <ChartBarIcon weight="bold" />
        {/snippet}
    </MajorFeature>
{/snippet}

<Generic summary={summary} features={features} />