<script lang="ts">
	import { ChartLineIcon, CloudSlashIcon, FloppyDiskIcon, ListIcon, LockIcon, PencilIcon, PhoneIcon, StarIcon, TextboxIcon } from "phosphor-svelte";
	import MajorFeature from "../MajorFeature.svelte";
	import Generic from "./Generic.svelte";
</script>

{#snippet summary()}
    <p>This is the first, highly experimental release, of Open Scouting <code>v2.0.0</code></p>
{/snippet}

{#snippet features()}
    <MajorFeature text="Complete Rebuild">
        {#snippet icon()}
            <StarIcon weight="bold" />
        {/snippet}
    </MajorFeature>
    
    <MajorFeature text="Match Scouting">
        {#snippet icon()}
            <TextboxIcon weight="bold" />
        {/snippet}
    </MajorFeature>

    <MajorFeature text="Pit Scouting">
        {#snippet icon()}
            <ListIcon weight="bold" />
        {/snippet}
    </MajorFeature>

    <MajorFeature text="Data View">
        {#snippet icon()}
            <ChartLineIcon weight="bold" />
        {/snippet}
    </MajorFeature>

    <MajorFeature text="Authentication">
        {#snippet icon()}
            <LockIcon weight="bold" />
        {/snippet}
    </MajorFeature>

    <MajorFeature text="Admin Interface">
        {#snippet icon()}
            <PencilIcon weight="bold" />
        {/snippet}
    </MajorFeature>

    <MajorFeature text="Local Data Storage">
        {#snippet icon()}
            <FloppyDiskIcon weight="bold" />
        {/snippet}
    </MajorFeature>

    <MajorFeature text="Offline Support">
        {#snippet icon()}
            <CloudSlashIcon weight="bold" />
        {/snippet}
    </MajorFeature>

    <MajorFeature text="Mobile Friendly">
        {#snippet icon()}
            <PhoneIcon weight="bold" />
        {/snippet}
    </MajorFeature>
{/snippet}

{#snippet details()}
    <p><code>v2.0.0</code> is a complete rebuild of Open Scouting, using SvelteKit and FastAPI. This version fixes several major issues with the original, most notably the database structure and how the frontend is organized.</p>
{/snippet}

<Generic summary={summary} features={features} details={details} />