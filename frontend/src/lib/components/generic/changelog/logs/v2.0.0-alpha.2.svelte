<script lang="ts">
	import { ArrowArcLeft, CalendarCheck, ChartBar, Confetti, Database, FilmScript, List, NumberCircleFour, NumberCircleOne, NumberCircleThree, NumberCircleTwo, Sidebar, Table, Textbox, Warning } from "phosphor-svelte";
	import MajorFeature from "../MajorFeature.svelte";
	import Generic from "./Generic.svelte";


</script>

{#snippet summary()}
    <p>Happy kickoff day! This release adds the ability to import and export match scouting fields and pit scouting questions, fixes many bugs, and improves the UI experience.</p>
{/snippet}

{#snippet features()}
    <MajorFeature text="2026 Rebuilt Support">
        {#snippet icon()}
            <Confetti weight="bold" />
        {/snippet}
    </MajorFeature>
    
    <MajorFeature text="Experimental Build Warning">
        {#snippet icon()}
            <Warning weight="bold" />
        {/snippet}
    </MajorFeature>

    <MajorFeature text="Import/Export Scouting Fields">
        {#snippet icon()}
            <Textbox weight="bold" />
        {/snippet}
    </MajorFeature>

    <MajorFeature text="Import/Export Pit Scouting Questions">
        {#snippet icon()}
            <List weight="bold" />
        {/snippet}
    </MajorFeature>

    <MajorFeature text="Better UI Usability">
        {#snippet icon()}
            <Sidebar weight="bold" />
        {/snippet}
    </MajorFeature>
{/snippet}

{#snippet details()}
    <ul class="list-disc list-inside ml-4">
        <li>Match scouting fields can also be imported from a preset on the server</li>
        <li>Pit scouting generation requests are now non-blocking on the server</li>
        <li>A temporary hack has been added to correctly repair the game piece UUIDs being different on a new server</li>
        <li>The ability to favorite events is correctly hidden when not signed in</li>
    </ul>
{/snippet}

<Generic summary={summary} features={features} details={details} />