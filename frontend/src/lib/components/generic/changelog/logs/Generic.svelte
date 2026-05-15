<!-- 
@component

The container component for each changelog

Props:
    - `summary` (`Snippet`) - The small summary of the update
    - `features` (`Snippet`) - MajorFeature components
    - `details` (`Snippet`) - The details of the update
-->
<script lang="ts">
	import type { Snippet } from "svelte";


    interface Props {
        summary?: Snippet
        features?: Snippet
        details?: Snippet
    }
    let { summary, features, details }: Props = $props();
</script>

<div class="flex flex-col gap-4">
    {@render summary?.()}

    <div class="grid grid-cols-2 gap-2">
        {@render features?.()}
    </div>
    
    {@render details?.()}
</div>