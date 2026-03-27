<script lang="ts">
	import { ChartBar, Image, List, Pencil, Table } from "phosphor-svelte";
	import MajorFeature from "../MajorFeature.svelte";
	import Generic from "./Generic.svelte";
</script>

{#snippet summary()}
    <p>This is a beta release of <code>v2.1.0</code>, which adds a few small features and fixes many bugs.</p>
{/snippet}

{#snippet features()}
    <MajorFeature text="Optional Pit Scouting Questions">
        {#snippet icon()}
            <List weight="bold" />
        {/snippet}
    </MajorFeature>

    <MajorFeature text="Admin Pit Scouting Presets">
        {#snippet icon()}
            <Pencil weight="bold" />
        {/snippet}
    </MajorFeature>

    <MajorFeature text="Offline Pit Scouting Image Uploads">
        {#snippet icon()}
            <Image weight="bold" />
        {/snippet}
    </MajorFeature>
{/snippet}

{#snippet details()}    
    <ul class="list-disc list-inside ml-4">
        <li>Fixed an issue where the default value of number fields wasn't being fixed on submit</li>
        <li>Implemented optional pit scouting questions. Now only required questions must be filled out to mark a pit as completed</li>
        <li>Fixed an issue where the event selector on the data compare page wasn't fetching events when switching modes</li>
        <li>Improved the usablity of the data compare page on smaller screens</li>
        <li>Pit scouting questions can now be loaded from a preset, like match scouting fields</li>
        <li>Fixed an issue where empty string fields were being submitted when match scouting</li>
        <li>Fixed an issue where an event was marked as past on the last day of the event</li>
        <li>Pit scouting images are now stored in the local database until they are uploaded, allowing images to be saved and uploaded later if the user is offline</li>
    </ul>

    <p>This version is beta to get these fixes into prod, but more features will be coming to v2.1.0 before it leaves beta.</p>
{/snippet}

<Generic summary={summary} features={features} details={details} />