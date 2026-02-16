<script lang="ts">
	import { ArrowArcLeft, CalendarCheck, ChartBar, ChartLine, CloudSlash, Confetti, Database, FilmScript, FloppyDisk, List, Lock, NumberCircleFour, NumberCircleOne, NumberCircleThree, NumberCircleTwo, Pencil, Phone, Sidebar, Star, Table, Textbox, Warning } from "phosphor-svelte";
	import MajorFeature from "../MajorFeature.svelte";
	import Generic from "./Generic.svelte";


</script>

{#snippet summary()}
    <p>This is the first, highly experimental release, of Open Scouting <code>v2.0.0</code></p>
{/snippet}

{#snippet features()}
    <MajorFeature text="Complete Rebuild">
        {#snippet icon()}
            <Star weight="bold" />
        {/snippet}
    </MajorFeature>
    
    <MajorFeature text="Match Scouting">
        {#snippet icon()}
            <Textbox weight="bold" />
        {/snippet}
    </MajorFeature>

    <MajorFeature text="Pit Scouting">
        {#snippet icon()}
            <List weight="bold" />
        {/snippet}
    </MajorFeature>

    <MajorFeature text="Data View">
        {#snippet icon()}
            <ChartLine weight="bold" />
        {/snippet}
    </MajorFeature>

    <MajorFeature text="Authentication">
        {#snippet icon()}
            <Lock weight="bold" />
        {/snippet}
    </MajorFeature>

    <MajorFeature text="Admin Interface">
        {#snippet icon()}
            <Pencil weight="bold" />
        {/snippet}
    </MajorFeature>

    <MajorFeature text="Local Data Storage">
        {#snippet icon()}
            <FloppyDisk weight="bold" />
        {/snippet}
    </MajorFeature>

    <MajorFeature text="Offline Support">
        {#snippet icon()}
            <CloudSlash weight="bold" />
        {/snippet}
    </MajorFeature>

    <MajorFeature text="Mobile Friendly">
        {#snippet icon()}
            <Phone weight="bold" />
        {/snippet}
    </MajorFeature>
{/snippet}

{#snippet details()}
    <p><code>v2.0.0</code> is a complete rebuild of Open Scouting, using SvelteKit and FastAPI. This version fixes several major issues with the original, most notably the database structure and how the frontend is organized.</p>
{/snippet}

<Generic summary={summary} features={features} details={details} />