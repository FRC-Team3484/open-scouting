<script lang="ts">
	import { ArrowArcLeft, Database, NumberCircleFour, NumberCircleOne, NumberCircleThree, NumberCircleTwo, Table } from "phosphor-svelte";
	import MajorFeature from "../MajorFeature.svelte";
	import Generic from "./Generic.svelte";


</script>

{#snippet summary()}
    <p>This release adds many little fixes, adds backend data validation, and frontend client-side form validation.</p>
{/snippet}

{#snippet features()}
    <MajorFeature text="Backend Data Validation">
        {#snippet icon()}
            <Database weight="bold" />
        {/snippet}
    </MajorFeature>
    
    <MajorFeature text="Form Validation">
        {#snippet icon()}
            <Table weight="bold" />
        {/snippet}
    </MajorFeature>
{/snippet}

{#snippet details()}
    <ul class="list-disc list-inside ml-4">
        <li>Aerich migrations now run when the container starts</li>
        <li>Various issues and inconsistencies from the different locations that data has been submitted has been fixed as well</li>
    </ul>
{/snippet}

<Generic summary={summary} features={features} details={details} />