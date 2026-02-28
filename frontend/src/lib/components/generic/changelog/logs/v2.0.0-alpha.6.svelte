<script lang="ts">
	import { Bug, Image, List, TextIndent, Wrench } from "phosphor-svelte";
	import MajorFeature from "../MajorFeature.svelte";
	import Generic from "./Generic.svelte";
</script>

{#snippet summary()}
    <p>This release improves the admin page, and fixes several bugs</p>
{/snippet}

{#snippet features()}
    <MajorFeature text="Bug Fixes">
        {#snippet icon()}
            <Bug weight="bold" />
        {/snippet}
    </MajorFeature>

    <MajorFeature text="Admin User and Event Management">
        {#snippet icon()}
            <Wrench weight="bold" />
        {/snippet}
    </MajorFeature>

    <MajorFeature text="Admin Scouting Data Management">
        {#snippet icon()}
            <List weight="bold" />
        {/snippet}
    </MajorFeature>

    <MajorFeature text="Pit Scouting Image Uploads">
        {#snippet icon()}
            <Image weight="bold" />
        {/snippet}
    </MajorFeature>

    <MajorFeature text="Field Descriptions">
        {#snippet icon()}
            <TextIndent weight="bold" />
        {/snippet}
    </MajorFeature>
{/snippet}

{#snippet details()}
    <p><span class="font-bold">Note:</span> <code>PUBLIC_VERSION</code> has been removed from the <code>.env</code> file to be replaced with a version included in each docker image. This key in the <code>.env</code> file can be safely removed.</p>
    <p><span class="font-bold">Note:</span> <code>UPLOAD_ROOT</code> needs added to your <code>.env</code> to make pit scouting image uploads work</p>
    
    <ul class="list-disc list-inside ml-4">
        <li>The changelog is now shown if the app has never been opened</li>
        <li>Improved pit scouting on smaller screens</li>
        <li>Internal routes are hidden from the Swagger docs in production</li>
        <li>Seasons can now be activated</li>
        <li>Fixed a few issues where match scouting boolean fields wouldn't reset properly</li>
        <li>Documentation improvements</li>
    </ul>
{/snippet}

<Generic summary={summary} features={features} details={details} />