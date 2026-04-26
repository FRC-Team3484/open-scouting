<script lang="ts">
	import { BellIcon, CalendarBlankIcon, ChartBarIcon, ImageIcon, ListIcon, MapPinIcon, PencilIcon, TableIcon } from "phosphor-svelte";
	import MajorFeature from "../MajorFeature.svelte";
	import Generic from "./Generic.svelte";
</script>

{#snippet summary()}
    <p>This release adds many new features including data view improvements, a new event list, event details page, live events on the index page, and a info header during match scouting.</p>
{/snippet}

{#snippet features()}
    <MajorFeature text="Data View Table View">
        {#snippet icon()}
            <TableIcon weight="bold" />
        {/snippet}
    </MajorFeature>

    <MajorFeature text="Data View Chart View">
        {#snippet icon()}
            <ChartBarIcon weight="bold" />
        {/snippet}
    </MajorFeature>

    <MajorFeature text="Optional Pit Scouting Questions">
        {#snippet icon()}
            <ListIcon weight="bold" />
        {/snippet}
    </MajorFeature>

    <MajorFeature text="Offline Pit Scouting Image Uploads">
        {#snippet icon()}
            <ImageIcon weight="bold" />
        {/snippet}
    </MajorFeature>

    <MajorFeature text="Redesigned Event List">
        {#snippet icon()}
            <CalendarBlankIcon weight="bold" />
        {/snippet}
    </MajorFeature>

    <MajorFeature text="Event Page">
        {#snippet icon()}
            <MapPinIcon weight="bold" />
        {/snippet}
    </MajorFeature>
{/snippet}

{#snippet details()}    
    <ul class="list-disc list-inside ml-4">
        <li>Pit scouting questions can now also be imported from presets</li>
        <li>Action links allow copying a link to match or pit scouting for an event</li>
        <li>A live events widget has been added to the index page, to show events that are currently happening</li>
        <li>Match scouting info is now shown in the nav bar when scouting, to help scouts remember what robot they're watching</li>
    </ul>

    <p>Many bugs and issues have also been fixed.</p>
{/snippet}

<Generic summary={summary} features={features} details={details} />