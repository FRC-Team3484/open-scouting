<script lang="ts">
	import { ChartBar, Table } from "phosphor-svelte";
	import MajorFeature from "../MajorFeature.svelte";
	import Generic from "./Generic.svelte";
</script>

{#snippet summary()}
    <p>This is a beta release of <code>v2.1.0</code>, which improves the data view page and fixes some bugs</p>
{/snippet}

{#snippet features()}
    <MajorFeature text="Data View Table View">
        {#snippet icon()}
            <Table weight="bold" />
        {/snippet}
    </MajorFeature>

    <MajorFeature text="Data View Chart View">
        {#snippet icon()}
            <ChartBar weight="bold" />
        {/snippet}
    </MajorFeature>
{/snippet}

{#snippet details()}    
    <ul class="list-disc list-inside ml-4">
        <li>Fixed an issue where unauthenticed users couldn't upload match scouting data. <span class="font-bold">Use the "Make all unsynced" button in the local data mangement drawer to fix local unsynced data.</span></li>
        <li>Added the ability to compare data between selected teams in both a table and chart view</li>
        <li>Fixed an issue where authenticated users couldn't favorite events</li>
    </ul>

    <p>This version is beta to get the new data view features into prod, but more features will be coming to v2.1.0 before it leaves beta.</p>
{/snippet}

<Generic summary={summary} features={features} details={details} />