<script lang="ts">
	import Generic from "./Generic.svelte";
</script>

{#snippet summary()}
    <p>This release fixes a few issues with loading the correct .env values in auth components, and implements offline mode.</p>
{/snippet}

{#snippet features()}
    
{/snippet}

{#snippet details()}    
    <ul class="list-disc list-inside ml-4">
        <li><span class="font-mono">.env</span> values now load properly</li>
        <li>Database backups are now handled by a different docker image</li>
        <li>Offline mode is now supported. An oversight prevented the site from correctly serving cached pages. Open Scouting pages are now pre-rendered, and some modifications were made to user data to support offline mode.</li>
        <li>Further improvements to the offline experience will be added in <a class="underline" href="https://github.com/FRC-Team3484/open-scouting/issues/207">#207</a>.</li>
    </ul>
{/snippet}

<Generic summary={summary} features={features} details={details} />