<script lang="ts">
	import { Binoculars, ChartBar, CloudSlash, Garage, Lock, Pencil } from "phosphor-svelte";
	import MajorFeature from "../MajorFeature.svelte";
	import Generic from "./Generic.svelte";
</script>

{#snippet summary()}
    <p>A complete rebuild of Open Scouting, using SvelteKit and FastAPI</p>
{/snippet}

{#snippet features()}
    <MajorFeature text="Match Scouting">
        {#snippet icon()}
            <Binoculars weight="bold" />
        {/snippet}
    </MajorFeature>

    <MajorFeature text="Pit Scouting">
        {#snippet icon()}
            <Garage weight="bold" />
        {/snippet}
    </MajorFeature>

    <MajorFeature text="Data View">
        {#snippet icon()}
            <ChartBar weight="bold" />
        {/snippet}
    </MajorFeature>

    <MajorFeature text="Offline Support">
        {#snippet icon()}
            <CloudSlash weight="bold" />
        {/snippet}
    </MajorFeature>

    <MajorFeature text="Authentication">
        {#snippet icon()}
            <Lock weight="bold" />
        {/snippet}
    </MajorFeature>

    <MajorFeature text="Admin Management">
        {#snippet icon()}
            <Pencil weight="bold" />
        {/snippet}
    </MajorFeature>
{/snippet}

{#snippet details()}    
    <ul class="list-disc list-inside ml-4">
        <li>Easier frontend development</li>
        <li>More cohesive UI</li>
        <li>Better database organization</li>
        <li>Create match scouting fields and pit scouting questions from the admin page</li>
        <li>Frontend is offline-first, improving the offline experience</li>
    </ul>

    <p class="text-sm">Match scouting data from <code>v1</code> in 2025 will soon be migrated to this version. Until then, view that data <a class="underline" href="https://open-scouting-legacy.nfoert.dev">here</a>.</p>
{/snippet}

<Generic summary={summary} features={features} details={details} />