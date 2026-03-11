<script lang="ts">
	import Generic from "./Generic.svelte";
</script>

{#snippet summary()}
    <p>This release fixes various bugs and issues</p>
{/snippet}

{#snippet features()}

{/snippet}

{#snippet details()}    
    <ul class="list-disc list-inside ml-4">
        <li>Fixed an issue where the server would try to generate pits from TBA for custom events</li>
        <li>Made the menu smaller on larger screens</li>
        <li>Fixed an issue where multiple choice fields wouldn't reset</li>
        <li>Adjust the "unsynced pits" badge to use a liveQuery instead of checking when the data is synced</li>
        <li>Fixed an issue where pit scouting images were squished</li>
    </ul>
{/snippet}

<Generic summary={summary} features={features} details={details} />