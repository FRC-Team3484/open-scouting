<!-- 
@component
Header component for authentication modes

Props:
    - `title` (`string`) - The title of the header
    - `description` (`string`) - The description of the header
    - `children` (`Snippet`) - The icon to display
-->
<script lang="ts">
	import type { Snippet } from "svelte";

	import Separator from "$lib/components/ui/separator/separator.svelte";


    interface Props {
        title: string
        description: string
        children?: Snippet
    }
    let { title, description, children }: Props = $props();
</script>

<div class="flex flex-row gap-4 items-center text-left">
    {@render children?.()}

    <div class="flex flex-col gap-2">
        <p class="text-lg font-bold">{title}</p>
        <p class="text-sm text-muted-foreground">{description}</p>
    </div>
</div>

<Separator class="my-2" />