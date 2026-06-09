<!-- 
@component
A section in the profile page

Props:
    - `title` (`string`) - The title of the section
    - `description` (`string`) - The description of the section
    - `children` (`children`) - The child components of the section
-->
<script lang="ts">
	import { fade, scale, slide } from "svelte/transition";
	import type { Snippet } from "svelte";
	import Separator from "../ui/separator/separator.svelte";
    

    interface Props {
        title: string
        description?: string
        children: Snippet
    }
    let { title, description = "", children }: Props = $props();
</script>

<div class="flex flex-col gap-2 w-full h-full" transition:slide>
    <p class="text-lg font-bold">{title}</p>
    <p class="text-sm text-muted-foreground">{description}</p>

    <Separator class="my-2" />

    <div class="flex flex-col gap-2">
        {@render children?.()}
    </div>
</div>