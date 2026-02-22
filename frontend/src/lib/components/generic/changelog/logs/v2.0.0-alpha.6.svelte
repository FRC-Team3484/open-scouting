<script lang="ts">
	import { ArrowsOutLineVertical, Bug, ChartBar, Export, List } from "phosphor-svelte";
	import MajorFeature from "../MajorFeature.svelte";
	import Generic from "./Generic.svelte";
</script>

{#snippet summary()}
    <p>This release improves the admin page, and fixes several bugs</p>
{/snippet}

{#snippet features()}

{/snippet}

{#snippet details()}
    <p><span class="font-bold">Note:</span> <code>PUBLIC_VERSION</code> has been removed from the <code>.env</code> file to be replaced with a version included in each docker image. This key in the <code>.env</code> file can be safely removed.</p>
    <ul class="list-disc list-inside ml-4">
        <li></li>
    </ul>
{/snippet}

<Generic summary={summary} features={features} details={details} />