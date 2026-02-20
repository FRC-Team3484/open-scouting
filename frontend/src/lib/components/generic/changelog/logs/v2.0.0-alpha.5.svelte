<script lang="ts">
	import { ArrowsOutLineVertical, Bug, ChartBar, Export, List } from "phosphor-svelte";
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

    <MajorFeature text="Reorder Match Scouting and Pit Questions">
        {#snippet icon()}
            <ArrowsOutLineVertical weight="bold" />
        {/snippet}
    </MajorFeature>

    <MajorFeature text="Bug Fixes">
        {#snippet icon()}
            <Bug weight="bold" />
        {/snippet}
    </MajorFeature>
{/snippet}

{#snippet details()}
    <ul class="list-disc list-inside ml-4">
        <li>Accessing a link from another user's start page will automatically fill in the event and year details</li>
        <li>Fixed an issue where pit scouting would create a duplicate pit on the client</li>
        <li>Enabled the button to go to the data page in the nav bar</li>
        <li>Team number autofilling is now disabled when an event has no valid match schedule data from TBA</li>
        <li>Fixed an issue where rapidly clicking increment buttons in match scouting would zoom the page</li>
    </ul>
{/snippet}

<Generic summary={summary} features={features} details={details} />