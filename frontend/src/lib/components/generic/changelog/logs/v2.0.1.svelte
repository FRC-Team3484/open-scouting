<script lang="ts">
	import Generic from "./Generic.svelte";
</script>

{#snippet summary()}
    <p>This release fixes issues with match scouting presets and game piece creation</p>
{/snippet}

{#snippet features()}

{/snippet}

{#snippet details()}    
    <ul class="list-disc list-inside ml-4">
        <li>Switched to use tortoise-orm's own migration system instead of aerich</li>
        <li>Fixed an issue where game pieces couldn't be created</li>
        <li>Fixed an issue where match scouting presets for 2024 and 2025 couldn't be imported due to the description field not being added</li>
    </ul>
{/snippet}

<Generic summary={summary} features={features} details={details} />