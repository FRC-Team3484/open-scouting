<script lang="ts">
	import { ChartBar, Export, List } from "phosphor-svelte";
	import MajorFeature from "../MajorFeature.svelte";
	import Generic from "./Generic.svelte";
</script>

{#snippet summary()}
    <p>This release adds several new features to the data page, and adds a new match scouting field for scouting Fuel</p>
{/snippet}

{#snippet features()}
    <MajorFeature text="Changelog System">
        {#snippet icon()}
            <List weight="bold" />
        {/snippet}
    </MajorFeature>
    
    <MajorFeature text="Data Page Team Summaries">
        {#snippet icon()}
            <ChartBar weight="bold" />
        {/snippet}
    </MajorFeature>

    <MajorFeature text="Match Scouting Data Export">
        {#snippet icon()}
            <Export weight="bold" />
        {/snippet}
    </MajorFeature>

    <MajorFeature text="Copy Links to Events">
        {#snippet icon()}
            <ChartBar weight="bold" />
        {/snippet}
    </MajorFeature>

    <MajorFeature text="New Number Field for Fuel">
        {#snippet icon()}
            <ChartBar weight="bold" />
        {/snippet}
    </MajorFeature>
{/snippet}

{#snippet details()}

{/snippet}

<Generic summary={summary} features={features} details={details} />